# -*- coding: utf-8 -*-
"""One bounded daily pass of the pay-per-call sourcing pipeline for Kaliper.

    python daily_run.py                 # full run, default budgets
    RUN_MINUTES=60 python daily_run.py  # tighter wall-clock budget

Phases (each checkpoints to state/ as it goes, so a killed run loses nothing):
  0. load the exclusion index (state/known_domains.txt) + everything already evaluated
  1. carry-over: candidates crawled-but-unclassified from a cut-off previous run
  2. discovery  - search frontier (TinyFish REST) + constructed-domain probes
  3. crawl      - free plain HTTP, drops Ringba tenants, detects parked/unresolved probes
  4. v6 qualify - gpt-4.1-mini, Kaliper's hard-gate prompt, unchanged config
  5. export     - out/<date>/… + out/ALL_qualified.csv + report.md
  6. grow the exclusion index with every domain judged today

Every domain that was crawled is appended to state/known_domains.txt at the end, whether
it qualified or not, so tomorrow never re-sources it. That mirrors what append_to_ledger.py
did for the account ledger in runs 2-5; the ledger itself is synced from this repo by
local/sync_to_ledger.py on the machine that holds it.

Environment:
  OPENAI_API_KEY     required (v6 qualifier)
  TINYFISH_API_KEY   optional; without it the search channel is skipped, probing still runs
  RUN_MINUTES        wall-clock budget, default 8 (a cloud Bash call is capped at 10 min)
  SEARCH_BUDGET      TinyFish requests per run, default 45 (~1.7 min at the 30/min ceiling)
  PROBE_BUDGET       constructed domains to fetch per run, default 300
  CRAWL_WORKERS      default 16
"""
import collections, concurrent.futures as cf, io, json, os, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import ppclib as L
import crawl as C
import discovery as D
import export as E
import qualify as Q

STATE = os.path.join(ROOT, 'state')
KNOWN = os.path.join(STATE, 'known_domains.txt')
EVAL = os.path.join(STATE, 'evaluated.jsonl')
PENDING = os.path.join(STATE, 'pending_v6.jsonl')      # crawled ok, not yet classified
CANDS = os.path.join(STATE, 'candidates_seen.jsonl')   # every emit, for auditing sources
LOG = os.path.join(ROOT, 'out', 'run.log')

# Defaults are sized to finish inside ONE cloud Bash call, which is capped at 10 minutes:
# ~2 min search (25%), crawl done by ~5 min (65%), v6 gets the rest, export in seconds.
# Measured locally: 150 probes + 8 searches + 23 v6 calls = 2.5 min. Raise via env vars
# only when running somewhere without that cap.
RUN_MINUTES = float(os.environ.get('RUN_MINUTES', '8'))
SEARCH_BUDGET = int(os.environ.get('SEARCH_BUDGET', '45'))
PROBE_BUDGET = int(os.environ.get('PROBE_BUDGET', '300'))
CRAWL_WORKERS = int(os.environ.get('CRAWL_WORKERS', '16'))
RUN_DATE = os.environ.get('RUN_DATE') or time.strftime('%Y-%m-%d')

os.makedirs(STATE, exist_ok=True); os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True)
_logf = io.open(LOG, 'a', encoding='utf-8')
def log(msg):
    line = '%s %s' % (time.strftime('%H:%M:%S'), msg)
    print(line, flush=True); _logf.write(line + '\n'); _logf.flush()

def read_lines(p):
    if not os.path.exists(p): return []
    return [x.strip() for x in io.open(p, encoding='utf-8', errors='replace') if x.strip()]

def read_jsonl(p):
    out = []
    for line in read_lines(p):
        try: out.append(json.loads(line))
        except Exception: pass
    return out

def append_jsonl(p, rec):
    with io.open(p, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')

def main():
    t0 = time.time(); deadline = t0 + RUN_MINUTES * 60
    known = set(read_lines(KNOWN))
    if len(known) < 13000:
        sys.exit('ABORT: exclusion index has %d domains; expected >= 13,000. A broken index '
                 're-sources companies the client already owns. Run local/build_known_index.py.'
                 % len(known))
    evaluated = set(r.get('domain') for r in read_jsonl(EVAL))
    probed = D._load_probed()
    log('=== daily run %s | known=%d evaluated=%d probed=%d budget=%dmin'
        % (RUN_DATE, len(known), len(evaluated), len(probed), RUN_MINUTES))

    # ---- 0. network preflight ------------------------------------------------------------
    # In a Claude Code cloud environment whose network access is still "Trusted", every
    # outbound HTTPS CONNECT is refused with 403 by the proxy. Without this check the run
    # would mark hundreds of live domains 'unreachable' and never probe them again.
    net_errs = []
    for probe_url in ('https://example.com', 'https://www.iana.org'):
        fu, raw, err = C.fast_get(probe_url, timeout=15)
        if raw and len(raw) > 200: break
        net_errs.append('%s -> %s' % (probe_url, err))
    else:
        sys.exit('ABORT: outbound HTTP is blocked from this machine (%s). In a cloud '
                 'environment this means Network access is not set to Full. Nothing was '
                 'crawled or recorded.' % '; '.join(net_errs))
    log('[net] outbound HTTP ok')
    stats = collections.OrderedDict()

    def is_known(d): return d in known or d in evaluated

    # ---- 2. discovery ---------------------------------------------------------------
    cands, seen_today = [], set()
    raw_emits = collections.Counter()
    def emit(url_or_domain, layer, source_url, source_note, **extra):
        raw_emits[layer] += 1
        d = C.valid(url_or_domain)
        if not d: return None
        if is_known(d) or d in seen_today: return None
        seen_today.add(d)
        rec = {'domain': d, 'company_name': extra.pop('company_name', ''), 'layer': layer, 'source_url': source_url,
               'source_note': source_note, 'run_date': RUN_DATE, **extra}
        cands.append(rec); append_jsonl(CANDS, rec)
        return d

    carry = [r for r in read_jsonl(PENDING) if r.get('domain') not in evaluated]
    if carry: log('[carry] %d crawled-but-unclassified candidates from a previous run' % len(carry))

    inbox_n = D.run_inbox(emit, log)
    stats['inbox candidates'] = inbox_n
    search_deadline = min(deadline, t0 + 0.25 * RUN_MINUTES * 60)
    used = D.run_search(emit, is_known, SEARCH_BUDGET, search_deadline, log)
    linked = D.run_linked(emit, is_known, int(os.environ.get('LINKED_BUDGET', '60')), log)
    probes = D.run_probe(emit, is_known, PROBE_BUDGET, log)
    stats['linked-domain candidates'] = linked
    stats['search requests'] = used
    stats['raw finds (search)'] = sum(v for k, v in raw_emits.items() if not k.startswith('L7'))
    stats['constructed domains probed'] = len(probes)
    stats['net-new candidates after exclusion index'] = len(cands)
    stats['  of which from search'] = sum(1 for c in cands if not c['layer'].startswith('L7'))
    stats['  of which from probing'] = sum(1 for c in cands if c['layer'].startswith('L7'))
    log('[discovery] %d net-new candidates (search %d, probe %d); %d raw finds killed by index'
        % (len(cands), stats['  of which from search'], stats['  of which from probing'],
           stats['raw finds (search)'] - stats['  of which from search']))

    # ---- 3. crawl -------------------------------------------------------------------
    # Budget split: crawl must end by 65% of the wall clock so v6 always gets its turn.
    crawl_deadline = min(deadline, t0 + 0.65 * RUN_MINUTES * 60)
    DEAD_PROBE = {'unregistered', 'unreachable', 'parked', 'redirect_offdomain'}
    crawled, to_v6 = {}, list(carry)
    def on_crawled(res):
        d = res['domain']; crawled[d] = res
        if res.get('ext_links'):
            ms = C.microsite_of(res['ext_links'], d, known)
            if ms: res['microsite_of'] = ms; log('[crawl] %s links to KNOWN %s -> flagged as microsite' % (d, ', '.join(ms)))
        if res['status'] == 'ok':
            to_v6.append(res); append_jsonl(PENDING, res)
        elif res['layer'].startswith('L7') and res['status'] in DEAD_PROBE:
            # a constructed domain that is not a live site is not a company: it goes in
            # probed_domains.txt only (never re-probed), NOT in evaluated/known/ledger
            pass
        else:
            # a real domain with nothing to classify: record it so it is never re-sourced
            rec = {k: v for k, v in res.items() if k != 'text'}
            append_jsonl(EVAL, rec); evaluated.add(d)
    if cands and time.time() < crawl_deadline:
        # probes first: they are the cheap, high-yield channel and mostly fail fast
        order = sorted(cands, key=lambda r: 0 if r['layer'].startswith('L7') else 1)
        with cf.ThreadPoolExecutor(max_workers=CRAWL_WORKERS) as ex:
            futs = {ex.submit(C.crawl_one, r): r for r in order}
            n = 0
            try:
                for fut in cf.as_completed(futs, timeout=max(30, crawl_deadline - time.time())):
                    n += 1
                    try: on_crawled(fut.result())
                    except Exception as e: log('[crawl] error %s' % e)
                    if n % 50 == 0: log('[crawl] %d/%d' % (n, len(cands)))
            except cf.TimeoutError:
                log('[crawl] time budget hit at %d/%d; remainder is dropped (not marked known)' % (n, len(cands)))
                for f in futs: f.cancel()
    # every probe that was crawled is recorded as probed, live or not
    D.mark_probed([d for d in probes if d in crawled])
    # outbound links of live sites -> candidates for the next pass
    D.queue_linked(list(crawled.values()), is_known, log)
    cs = collections.Counter(r['status'] for r in crawled.values())
    stats['crawled'] = len(crawled)
    for k in ('ok', 'thin', 'unregistered', 'unreachable', 'parked', 'redirect_offdomain', 'ringba_banned'):
        if cs.get(k): stats['  crawl: %s' % k] = cs[k]
    probe_live = sum(1 for d in probes if crawled.get(d, {}).get('status') == 'ok')
    stats['probes that resolved to a real site'] = probe_live
    log('[crawl] %s' % dict(cs))

    # ---- 4. v6 ----------------------------------------------------------------------
    # dedupe to_v6 by domain (carry-over + today)
    uniq = {}
    for r in to_v6: uniq.setdefault(r['domain'], r)
    to_v6 = [r for d, r in uniq.items() if d not in evaluated]
    qualified = []
    def on_result(rec):
        rec['run_date'] = RUN_DATE
        append_jsonl(EVAL, rec); evaluated.add(rec['domain'])
        if (rec.get('v6') or {}).get('qualified') is True:
            qualified.append(rec)
            log('[v6] QUALIFIED %-34s fit=%-3s %s' % (rec['domain'][:34], rec['v6'].get('fit_score'),
                                                     (rec['v6'].get('business_model') or '')[:60]))
    if to_v6 and time.time() < deadline:
        log('[v6] classifying %d companies' % len(to_v6))
        try:
            Q.qualify_many(to_v6, deadline, on_result, log)
        except RuntimeError as e:
            log('[v6] %s' % e)
    # rewrite pending with whatever is still unclassified
    left = [r for r in to_v6 if r['domain'] not in evaluated]
    with io.open(PENDING, 'w', encoding='utf-8') as f:
        for r in left: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    stats['v6 classified'] = len(to_v6) - len(left)
    stats['carried to next run (unclassified)'] = len(left)
    stats['V6 QUALIFIED'] = len(qualified)

    # ---- 5. export ------------------------------------------------------------------
    res = E.main(RUN_DATE, stats)

    # ---- 6. grow the exclusion index --------------------------------------------------
    add = sorted(d for d in evaluated if d not in known)
    if add:
        with io.open(KNOWN, 'a', encoding='utf-8', newline='\n') as f:
            for d in add: f.write(d + '\n')
    log('[index] +%d domains -> known_domains.txt now %d' % (len(add), len(known) + len(add)))
    # machine-readable pass summary, so a session running several passes knows when to stop:
    # nothing left to discover = every search query retired AND no constructed domain left to probe
    frontier_left = (sum(1 for v in D._load_progress().values() if not v.get('retired'))
                     if used or D.TF_KEY else -1)
    probes_left = len(D.generate_probes(is_known, 1))
    linked_left = sum(1 for _ in read_lines(D.LINKQ)) if os.path.exists(D.LINKQ) else 0
    # ---- 7. replenish the frontier when it is exhausted ---------------------------------
    replenished = (0, 0)
    # Replenish when the SEARCH frontier is (nearly) dry, even if constructed-domain probes remain:
    # the probe space is mostly dead alt-TLD combinations and would otherwise block new phrases
    # for days (2026-09-06: 2 live queries left, probes yielding 0 live sites, no replenishment).
    search_dry = (0 <= frontier_left <= 2)
    if (search_dry or (not probes_left and not linked_left)) and not os.environ.get('PPC_NO_REPLENISH'):
        import replenish as R
        log('[replenish] %s - generating new phrase families and vertical tokens'
            % ('search frontier down to %d live queries' % frontier_left if search_dry else 'frontier exhausted'))
        replenished = R.generate(force=search_dry, dry_run=False, log=log)
        frontier_left = sum(1 for v in D._load_progress().values() if not v.get('retired')) + replenished[0]
        probes_left = len(D.generate_probes(is_known, 1))
    pass_info = {'run_date': RUN_DATE, 'finished_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                 'replenished_queries': replenished[0], 'replenished_tokens': replenished[1],
                 'linked_candidates_queued': linked_left,
                 'minutes': round((time.time() - t0) / 60, 1),
                 'net_new_candidates': len(cands), 'crawled_ok': cs.get('ok', 0),
                 'v6_classified': stats['v6 classified'], 'qualified_this_pass': len(qualified),
                 'qualified_today': res['qualified'], 'cumulative_qualified': res['cumulative'],
                 'search_queries_still_active': frontier_left, 'probe_space_remaining': bool(probes_left),
                 'carried_to_next_pass': len(left),
                 'nothing_left_to_do': (len(cands) == 0 and len(left) == 0 and linked_left == 0
                                        and not probes_left and frontier_left == 0)}
    json.dump(pass_info, io.open(os.path.join(STATE, 'last_pass.json'), 'w', encoding='utf-8'), indent=1)
    log('PASS_RESULT ' + json.dumps(pass_info))
    log('=== done in %.1f min | qualified today %d | cumulative %d'
        % ((time.time() - t0) / 60, res['qualified'], res['cumulative']))

if __name__ == '__main__':
    main()
