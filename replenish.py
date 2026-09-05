# -*- coding: utf-8 -*-
"""Frontier replenishment: when every search query is retired and the constructed-domain
space is used up, generate NEW search phrase families and vertical tokens - constrained by
what runs 1-4 and the daily passes measured - and hand them to discovery.py.

    python replenish.py            # only if the frontier is exhausted
    python replenish.py --force    # generate a batch now (e.g. to seed more inventory)
    python replenish.py --dry-run  # show what would be added, write nothing

Why a script and not the routine agent: per-row judgment belongs in a script that calls a
model with the evidence in front of it, so it is reproducible, validated, and logged.
The agent only reports what was added (state/frontier_log.md).

Evidence given to the model, every time:
  - every query already run, with its net-new count and whether it qualified anything
  - every vertical token already probed, with resolve / qualify counts
  - the standing rules: long specific counterparty & publisher-onboarding vocabulary works
    (pages 0-7); short generic marketplace phrases die by page 1; banned terms; verticals
    must be call-brokerable (high RPC); no directories/listicles; no vendors.
Model: gpt-4.1 (one call per exhaustion event; not the v6 qualifier, so not frozen).
"""
import collections, io, json, os, re, sys, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
STATE = os.path.join(ROOT, 'state')
EXT = os.path.join(STATE, 'frontier_extensions.json')
LOGMD = os.path.join(STATE, 'frontier_log.md')
MODEL = os.environ.get('REPLENISH_MODEL', 'gpt-4.1')

BANNED = ['"ppc"', ' ppc ', 'lead generation"', '"lead generation', 'performance marketing', 'call center',
          'click to call', 'inbound marketing', 'affiliate program', 'partner program', 'marketing partner',
          'we buy calls"', 'best pay per call', 'top pay per call', 'pay per call networks list', 'review']
EXISTING_RULES = """
RULES MEASURED ACROSS RUNS 1-4 AND THE DAILY PASSES (do not violate):
1. Long, SPECIFIC counterparty / publisher-onboarding phrases work and sustain search depth to
   page 5-7: e.g. "become a publisher", "join our network", "weekly payouts", "publisher portal",
   "media buyer application", "apply to become a publisher". Short generic marketplace phrases
   ("call marketplace", "call exchange") die by page 1. Prefer the former shape.
2. Every query must contain at least one quoted phrase AND a call qualifier (calls, "pay per call",
   "inbound calls", "live transfers", "per call") unless the quoted phrase itself is call-specific.
3. BANNED (poisoned earlier runs): bare PPC, "lead generation", "performance marketing", "call center",
   "click to call", "inbound marketing", "affiliate program", "partner program", "marketing partner",
   anything that returns directories/listicles/reviews ("best", "top 10", "list of", "review").
4. "buy calls"/"sell calls" collide with stock options: always append -options -stock -trading.
5. Vertical tokens must be CALL-BROKERABLE (a phone call worth enough to sell per unit): insurance
   (Medicare, ACA, final expense, auto, home, commercial), legal (personal injury, mass tort, SSDI),
   finance (debt relief, tax relief, MCA, credit repair), home-service aggregation, auto glass,
   roadside/towing, junk cars, rehab/addiction, solar, restoration. Generic repair trades
   (gutters, garage doors, tree service, duct cleaning) measured DEAD - do not propose them.
6. Constructed-domain shapes that measured dead: prefixed (exclusive/direct/elite/national...),
   suffixed ({v}callsdirect/{v}leadsgroup), extended ({v}callnetwork/{v}transfers), generic call words
   (callexchange/ringflow). Productive: {vertical}calls.com, {vertical}leads.com, hyphenated, .io/.net.
7. Output must be net-new: do not repeat or trivially reword anything in the EXISTING lists.
"""

def _post(payload, key, timeout=120):
    req = urllib.request.Request('https://api.openai.com/v1/chat/completions', data=json.dumps(payload).encode('utf-8'),
                                 headers={'Content-Type': 'application/json', **({'Authorization': 'Bearer ' + key} if key else {})}, method='POST')
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8', 'replace'))

def load_ext():
    try: return json.load(io.open(EXT, encoding='utf-8'))
    except Exception: return {'batches': []}

def evidence():
    import discovery as D
    prog = D._load_progress()
    # qualified per query / per layer / per probe token, from evaluated.jsonl
    q_by_query, q_by_token, res_by_token = collections.Counter(), collections.Counter(), collections.Counter()
    tried_tokens = set()
    p = os.path.join(STATE, 'evaluated.jsonl')
    if os.path.exists(p):
        for line in io.open(p, encoding='utf-8', errors='replace'):
            try: r = json.loads(line)
            except Exception: continue
            ok = (r.get('v6') or {}).get('qualified') is True
            if r.get('query') and ok: q_by_query[r['query']] += 1
            if (r.get('layer') or '').startswith('L7'):
                tok = re.sub(r'(calls|leads|livetransfers|leadspro|transfers|call|lead)$', '', r['domain'].split('.')[0].replace('-', ''))
                tried_tokens.add(tok); res_by_token[tok] += 1
                if ok: q_by_token[tok] += 1
    probed = D._load_probed()
    for d in probed:
        tried_tokens.add(re.sub(r'(calls|leads|livetransfers|leadspro|transfers|call|lead)$', '', d.split('.')[0].replace('-', '')))
    queries = [{'query': q, 'pages_run': st.get('next_page', 0), 'net_new': st.get('new_total', 0),
                'qualified': q_by_query.get(q, 0), 'retired': st.get('retired', False)} for q, st in prog.items()]
    queries.sort(key=lambda x: (-x['qualified'], -x['net_new']))
    tokens = sorted(set(D.VERTICAL_TOKENS) | tried_tokens)
    token_stats = {t: {'live_sites': res_by_token.get(t, 0), 'qualified': q_by_token.get(t, 0)} for t in tokens if res_by_token.get(t) or q_by_token.get(t)}
    return queries, tokens, token_stats

def validate(batch, existing_q, existing_t):
    normq = lambda s: re.sub(r'\s+', ' ', s.lower()).strip()
    have_q = set(normq(q) for q in existing_q)
    out_q = []
    for item in batch.get('queries') or []:
        q = (item.get('q') or item.get('query') or '').strip()
        if not q or normq(q) in have_q or len(q) > 110 or '"' not in q: continue
        if any(b in q.lower() for b in BANNED): continue
        if ('buy calls' in q.lower() or 'sell calls' in q.lower()) and '-options' not in q: q += ' -options -stock -trading'
        layer = item.get('layer') if item.get('layer') in ('L4-counterparty', 'L4-vertical', 'L4-familyB') else 'L4-counterparty'
        m = re.search(r'\d+', str(item.get('max_page') or '3')); maxp = max(1, min(int(m.group()) if m else 3, 7))
        out_q.append([q, maxp, layer]); have_q.add(normq(q))
    have_t = set(existing_t)
    out_t = []
    # run-4 measured these morphemes dead for constructed domains (no per-call market forms there)
    dead = re.compile(r'(repair|install|cleaning|removal|gutter|garage|tree|duct|pool|lawn|landscap|handyman|'
                      r'paint|fence|concrete|floor|window|siding|maid|janitor|ivf|petmed|vision|estate|'
                      r'wedding|photograph|tutor|fitness|yoga|salon|spa)')
    for t in batch.get('vertical_tokens') or []:
        t = re.sub(r'[^a-z0-9\-]', '', str(t).lower().replace(' ', ''))
        if 3 <= len(t) <= 24 and t not in have_t and not dead.search(t): out_t.append(t); have_t.add(t)
    return out_q, out_t

def generate(force=False, dry_run=False, log=print):
    import discovery as D
    queries, tokens, token_stats = evidence()
    active = [q for q in queries if not q['retired']]
    probes_left = bool(D.generate_probes(lambda d: False, 1))
    if not force and (active or probes_left):
        log('[replenish] frontier not exhausted (%d active queries, probe space %s) - nothing to do'
            % (len(active), 'remaining' if probes_left else 'empty')); return 0, 0
    key = os.environ.get('OPENAI_API_KEY', '')
    ext = load_ext()
    all_q = [q['query'] for q in queries] + [x[0] for x in D.all_queries()]
    user = {
        'task': 'Propose NEW search queries and NEW vertical tokens for discovering small pay-per-call '
                'publishers, networks and call brokers (1-20 staff) that are NOT already known. Kaliper sells '
                'software to them. We need net-new companies, so prefer vocabulary that only such operators use.',
        'existing_queries_with_results': queries[:150],
        'existing_vertical_tokens': tokens,
        'token_stats_live_sites_and_qualified': token_stats,
        'previous_extension_batches': [{'generated_at': b['generated_at'], 'queries': [q[0] for q in b['queries']],
                                        'tokens': b['tokens']} for b in ext['batches'][-3:]],
        'want': {'queries': 25, 'vertical_tokens': 15},
        'output_format': {'queries': [{'q': 'quoted phrase + call qualifier', 'max_page': '1-7', 'layer': 'L4-counterparty|L4-vertical|L4-familyB',
                                       'why': 'one sentence grounded in the evidence'}],
                          'vertical_tokens': ['lowercase, no spaces, e.g. finalexpense'],
                          'rationale': '3-5 sentences on what the evidence says and what this batch tries'}}
    payload = {'model': MODEL, 'temperature': 0.4, 'response_format': {'type': 'json_object'},
               'messages': [{'role': 'system', 'content': 'You are a GTM data engineer extending a measured web-discovery frontier. '
                             'Answer with valid JSON only.' + EXISTING_RULES},
                            {'role': 'user', 'content': json.dumps(user, ensure_ascii=False)}]}
    try:
        r = _post(payload, key)
        txt = r['choices'][0]['message']['content']
        batch = json.loads(txt)
    except urllib.error.HTTPError as e:
        log('[replenish] OpenAI HTTP %d: %s' % (e.code, e.read()[:200].decode('utf-8', 'replace'))); return 0, 0
    except Exception as e:
        log('[replenish] failed: %s %s' % (type(e).__name__, str(e)[:200])); return 0, 0
    new_q, new_t = validate(batch, all_q, tokens)
    log('[replenish] model proposed %d queries / %d tokens; %d / %d survived validation'
        % (len(batch.get('queries') or []), len(batch.get('vertical_tokens') or []), len(new_q), len(new_t)))
    for q in new_q: log('   + %-70s p<=%d %s' % (q[0][:70], q[1], q[2]))
    for t in new_t: log('   + token %s' % t)
    if dry_run or not (new_q or new_t): return len(new_q), len(new_t)
    entry = {'generated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'model': MODEL,
             'trigger': 'forced' if force else 'frontier exhausted', 'queries': new_q, 'tokens': new_t,
             'rationale': (batch.get('rationale') or '')[:1200],
             'why': {(i.get('q') or i.get('query') or ''): (i.get('why') or '')[:200] for i in (batch.get('queries') or [])}}
    ext['batches'].append(entry)
    json.dump(ext, io.open(EXT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    with io.open(LOGMD, 'a', encoding='utf-8') as f:
        f.write('\n## %s — %s (%s)\n\n%s\n\n' % (entry['generated_at'], entry['trigger'], MODEL, entry['rationale']))
        f.write('| query | max page | layer | why |\n|---|---|---|---|\n')
        for q in new_q: f.write('| %s | %d | %s | %s |\n' % (q[0].replace('|', '/'), q[1], q[2], entry['why'].get(q[0], '').replace('|', '/')))
        if new_t: f.write('\nNew vertical tokens: %s\n' % ', '.join(new_t))
    return len(new_q), len(new_t)

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('--force', action='store_true'); ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    if not os.environ.get('OPENAI_API_KEY'):
        try:
            for line in io.open(os.path.join(os.path.dirname(ROOT), 'relevince-outbound', '.env'), encoding='utf-8'):
                if line.startswith('OPENAI_API_KEY='): os.environ['OPENAI_API_KEY'] = line.split('=', 1)[1].strip()
        except Exception: pass
    generate(force=a.force, dry_run=a.dry_run)
