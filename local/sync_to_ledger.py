# -*- coding: utf-8 -*-
"""Append the daily job's verdicts to the Kaliper account ledger (file of record).

Run LOCALLY, on the machine that holds the ledger, after `git pull` of this repo:
    python local/sync_to_ledger.py                 # uses PPC_LEDGER or the archive path
    PPC_LEDGER="C:\\path\\to\\account_ledger.csv" python local/sync_to_ledger.py

Same contract as ppc-run2..5/append_to_ledger.py: back up first, APPEND ONLY, never edit
or drop an existing row, abort if the row count would not grow by exactly the number of
new rows. Deduped by domain against the ledger AND within its own input (the run-3 bug).
"""
import csv, io, json, os, shutil, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVAL = os.path.join(ROOT, 'state', 'evaluated.jsonl')
LEDGER = os.environ.get('PPC_LEDGER',
    r'D:\Archives Relevince\Relivence\relevince-outbound\clients\kaliper\account_ledger.csv')
TODAY = date.today().isoformat()
COLS = ['domain', 'company_name', 'qualified', 'disqualify_reason', 'fit_score',
        'contact_status', 'contact_name', 'title', 'phone', 'linkedin_url',
        'last_checked', 'source_run']

def rd(p):
    try: return list(csv.DictReader(io.open(p, encoding='utf-8-sig', errors='replace')))
    except Exception: return []

def main():
    if not os.path.exists(LEDGER): sys.exit('ledger not found: %s (set PPC_LEDGER)' % LEDGER)
    existing = rd(LEDGER)
    have = set((r.get('domain') or '').strip().lower() for r in existing)
    print('ledger before: %d rows, %d unique domains' % (len(existing), len(have)))

    best = {}
    for line in io.open(EVAL, encoding='utf-8', errors='replace'):
        try: r = json.loads(line)
        except Exception: continue
        d = (r.get('domain') or '').lower()
        if not d: continue
        v = r.get('v6') or {}; prev = best.get(d); pv = (prev or {}).get('v6') or {}
        if prev is None or (v.get('qualified') is True and pv.get('qualified') is not True) \
           or ((v.get('qualified') is True) == (pv.get('qualified') is True)
               and (v.get('fit_score') or 0) >= (pv.get('fit_score') or 0)):
            best[d] = r

    new_rows = []
    for d, r in sorted(best.items()):
        if d in have: continue
        v = r.get('v6') or {}
        st = r.get('status')
        if v:
            qualified = 'True' if v.get('qualified') is True else 'False'
            reason = '' if qualified == 'True' else (v.get('disqualify_reason') or 'no_clear_signal')
            fit = v.get('fit_score', '')
        else:
            qualified = ''; fit = ''
            reason = ('scrape blocked' if st == 'unreachable'
                      else 'tech/software vendor, not a seller' if st == 'ringba_banned'
                      else 'parked or unregistered domain' if st in ('parked', 'redirect_offdomain')
                      else 'no readable content')
        new_rows.append({
            'domain': d, 'company_name': (r.get('company_name') or '')[:120],
            'qualified': qualified, 'disqualify_reason': reason, 'fit_score': fit,
            'contact_status': 'no_contact_data', 'contact_name': '', 'title': '', 'phone': '',
            'linkedin_url': '', 'last_checked': r.get('run_date') or TODAY,
            'source_run': 'ppc-daily-%s' % (r.get('run_date') or TODAY)})
    print('to append: %d new domains (%d already in ledger)' % (len(new_rows), len(best) - len(new_rows)))
    if not new_rows: print('nothing to append'); return

    bak = LEDGER.replace('.csv', '.backup-%s-pre-dailysync.csv' % TODAY)
    shutil.copy2(LEDGER, bak); print('backup:', os.path.basename(bak))
    fieldnames = list(existing[0].keys()) if existing else COLS
    tmp = LEDGER + '.tmp'
    with io.open(tmp, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
        for r in existing: w.writerow({k: r.get(k, '') for k in fieldnames})
        for r in new_rows: w.writerow({k: r.get(k, '') for k in fieldnames})
    after = rd(tmp)
    if len(after) != len(existing) + len(new_rows):
        os.remove(tmp); sys.exit('ABORT: row count mismatch, ledger untouched')
    os.replace(tmp, LEDGER)
    import collections
    print('ledger after: %d rows (+%d)' % (len(after), len(new_rows)))
    print('by qualified:', dict(collections.Counter(r['qualified'] or '(unresolved)' for r in new_rows)))

if __name__ == '__main__':
    main()
