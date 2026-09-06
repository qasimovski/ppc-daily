# -*- coding: utf-8 -*-
"""Write today's deliverables from state/evaluated.jsonl:
    out/<date>/qualified.csv        every v6-qualified company found in this run
    out/<date>/qualified_icp_clean.csv  the US/UK/CA, no-flag subset (the list to work)
    out/<date>/rejected.csv         everything v6 rejected, with reason
    out/<date>/report.md            funnel + qualify-rate-per-channel, deduped by domain
    out/ALL_qualified.csv           cumulative across all daily runs (deduped by domain)
Column layout matches ppc-run2..5/export2.py so downstream scripts keep working.
"""
import collections, csv, io, json, os, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(ROOT, 'state')
OUT = os.path.join(ROOT, 'out')
EVAL = os.path.join(STATE, 'evaluated.jsonl')
IN_SCOPE_GEO = {'United States', 'United Kingdom', 'Canada'}

COLS = ['company_name', 'domain', 'v6_qualified', 'v6_fit_score', 'v6_business_model',
        'v6_marketplace_signal', 'v6_positive_evidence', 'v6_reasoning', 'v6_disqualify_reason',
        'discovery_layer', 'source_url', 'source_note', 'geography', 'tier1_phrases_on_site',
        'infrastructure_detected', 'pages_crawled', 'kaliper_flags', 'run_date']

def load_eval():
    best = {}
    if not os.path.exists(EVAL): return best
    for line in io.open(EVAL, encoding='utf-8', errors='replace'):
        try: r = json.loads(line)
        except Exception: continue
        d = r.get('domain')
        if not d: continue
        v = r.get('v6') or {}
        prev = best.get(d)
        if prev is None: best[d] = r; continue
        pv = prev.get('v6') or {}
        if (v.get('qualified') is True) and (pv.get('qualified') is not True): best[d] = r
        elif (v.get('qualified') is True) == (pv.get('qualified') is True):
            if (v.get('fit_score') or 0) >= (pv.get('fit_score') or 0): best[d] = r
    return best

def to_row(d, r):
    v = r.get('v6') or {}
    geo = r.get('geo') or []
    flags = []
    if geo and not any(g in IN_SCOPE_GEO for g in geo):
        flags.append('geo outside US/UK/CA: ' + ', '.join(geo[:2]))
    if not geo: flags.append('geo unknown')
    if 'Ringba' in (r.get('infra') or []): flags.append('EXCLUDE: Ringba tenant')
    if r.get('ringba_prose'): flags.append('REVIEW: names Ringba in prose (likely tenant)')
    if r.get('microsite_of'): flags.append('MICROSITE of known company: ' + ', '.join(r['microsite_of']))
    return {
        'company_name': r.get('company_name') or '',
        'domain': d,
        'v6_qualified': v.get('qualified'),
        'v6_fit_score': v.get('fit_score'),
        'v6_business_model': v.get('business_model', ''),
        'v6_marketplace_signal': v.get('marketplace_signal'),
        'v6_positive_evidence': (v.get('positive_evidence') or '').replace('\n', ' ')[:400],
        'v6_reasoning': (v.get('reasoning') or '').replace('\n', ' ')[:400],
        'v6_disqualify_reason': v.get('disqualify_reason', ''),
        'discovery_layer': r.get('layer', ''),
        'source_url': r.get('source_url', ''),
        'source_note': (r.get('source_note') or '').replace('\n', ' ')[:300],
        'geography': '; '.join(geo),
        'tier1_phrases_on_site': '; '.join(r.get('tier1') or []),
        'infrastructure_detected': '; '.join(r.get('infra') or []),
        'pages_crawled': r.get('pages', 0),
        'kaliper_flags': ' | '.join(flags),
        'run_date': r.get('run_date', ''),
    }

def write_csv(path, rows):
    with io.open(path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader()
        for r in rows: w.writerow(r)

def main(run_date=None, stats=None):
    run_date = run_date or time.strftime('%Y-%m-%d')
    day_dir = os.path.join(OUT, run_date); os.makedirs(day_dir, exist_ok=True)
    best = load_eval()
    today = {d: r for d, r in best.items() if r.get('run_date') == run_date}
    q = sorted((to_row(d, r) for d, r in today.items() if (r.get('v6') or {}).get('qualified') is True),
               key=lambda r: -(r['v6_fit_score'] or 0))
    rej = sorted((to_row(d, r) for d, r in today.items()
                  if r.get('v6') and (r['v6'].get('qualified') is not True)),
                 key=lambda r: r['v6_disqualify_reason'] or '')
    clean = [r for r in q if not r['kaliper_flags'] or r['kaliper_flags'] == 'geo unknown']
    write_csv(os.path.join(day_dir, 'qualified.csv'), q)
    write_csv(os.path.join(day_dir, 'qualified_icp_clean.csv'), clean)
    write_csv(os.path.join(day_dir, 'rejected.csv'), rej)

    # cumulative
    allq = sorted((to_row(d, r) for d, r in best.items() if (r.get('v6') or {}).get('qualified') is True),
                  key=lambda r: (r['run_date'], -(r['v6_fit_score'] or 0)))
    write_csv(os.path.join(OUT, 'ALL_qualified.csv'), allq)

    # report
    st = collections.Counter(r.get('status') for r in today.values())
    lay = collections.defaultdict(collections.Counter)
    for r in today.values():
        if not r.get('v6'): continue
        k = (r.get('layer') or '?').split('+')[0]
        lay[k]['n'] += 1
        if r['v6'].get('qualified') is True: lay[k]['q'] += 1
    dq = collections.Counter((r.get('v6') or {}).get('disqualify_reason') or '?'
                             for r in today.values() if r.get('v6') and r['v6'].get('qualified') is False)
    L = []
    L.append('# Pay-per-call daily sourcing — %s\n' % run_date)
    L.append('All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper\'s v6 gate and '
             'was absent from the exclusion index at the start of the run.\n')
    if stats:
        L.append('## Funnel — LAST PASS ONLY (a day may have several passes)\n')
        L.append('| stage | count |\n|---|---|')
        for k, v in stats.items(): L.append('| %s | %s |' % (k, v))
        L.append('')
    L.append('## Day so far (all passes, unique domains)\n')
    L.append('| stage | count |\n|---|---|')
    L.append('| candidates crawled | %d |' % len(today))
    L.append('| crawled ok | %d |' % sum(1 for r in today.values() if r.get('status') == 'ok'))
    L.append('| v6 classified | %d |' % sum(1 for r in today.values() if r.get('v6')))
    L.append('| v6 qualified | %d |' % len(q))
    L.append('')
    L.append('## Crawl outcomes (net-new candidates only)\n')
    L.append('| status | count |\n|---|---|')
    for k, v in st.most_common(): L.append('| %s | %d |' % (k, v))
    L.append('')
    L.append('## v6 qualify rate per discovery channel\n')
    L.append('| channel | classified | qualified | rate |\n|---|---|---|---|')
    for k, c in sorted(lay.items(), key=lambda kv: -(kv[1]['q'] / max(1, kv[1]['n']))):
        L.append('| %s | %d | %d | %.1f%% |' % (k, c['n'], c['q'], 100 * c['q'] / max(1, c['n'])))
    L.append('')
    L.append('**V6 QUALIFIED TODAY: %d** (ICP-clean: %d). Cumulative across all daily runs: %d.\n'
             % (len(q), len(clean), len(allq)))
    if dq:
        L.append('## Why candidates failed v6\n')
        L.append('| reason | count |\n|---|---|')
        for k, v in dq.most_common(): L.append('| %s | %d |' % (k, v))
        L.append('')
    if q:
        L.append('## Qualified today\n')
        L.append('| company | domain | fit | business model | marketplace | geo | flags |\n|---|---|---|---|---|---|---|')
        for r in q:
            L.append('| %s | %s | %s | %s | %s | %s | %s |' % (
                (r['company_name'] or '')[:30], r['domain'], r['v6_fit_score'],
                (r['v6_business_model'] or '')[:64], 'yes' if r['v6_marketplace_signal'] else '',
                r['geography'], r['kaliper_flags']))
        L.append('')
    L.append('## Files\n')
    L.append('- `out/%s/qualified.csv` — every v6-qualified company found today' % run_date)
    L.append('- `out/%s/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**' % run_date)
    L.append('- `out/%s/rejected.csv` — v6 rejections with reason, for tuning' % run_date)
    L.append('- `out/ALL_qualified.csv` — cumulative, deduped by domain')
    L.append('- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`')
    io.open(os.path.join(day_dir, 'report.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L))
    return {'qualified': len(q), 'icp_clean': len(clean), 'rejected': len(rej), 'cumulative': len(allq)}

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
