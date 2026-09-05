# -*- coding: utf-8 -*-
"""Build state/known_domains.txt — the exclusion index — from every local source of
already-seen Kaliper domains. DOMAIN-ONLY output: no names, phones or people, so the
file is safe to commit and ship to the cloud runner.

Run on the machine that holds the ledger and the archived runs (this one):
    python local/build_known_index.py

Sources (edit the lists below if the archive moves):
  - the Kaliper account ledger (file of record)
  - the Clay / qualified / consolidated seed CSVs
  - every crawled / frontier / seen / results file in the archived ppc-* runs
  - the daily job's own state/evaluated.jsonl (so rebuilding never loses ground)
"""
import csv, glob, io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import ppclib as L

ARCHIVE = os.environ.get('PPC_ARCHIVE', r'D:\Archives Relevince\Relivence')
LEDGER = os.environ.get('PPC_LEDGER',
    os.path.join(ARCHIVE, 'relevince-outbound', 'clients', 'kaliper', 'account_ledger.csv'))

CSV_SOURCES = [
    (LEDGER, ['domain']),
    (os.path.join(ARCHIVE, 'KALIPER_ALL_QUALIFIED_COMPANIES_2026-09-01.csv'), ['company_domain']),
    (os.path.join(ARCHIVE, 'Clay - Leads.csv'), ['Domain']),
    (os.path.join(ARCHIVE, 'kaliper_ICP_candidates_consolidated.csv'), ['domain']),
    (os.path.join(ARCHIVE, 'kaliper_qualified_master.csv'), ['domain', 'company_domain']),
    (os.path.join(ARCHIVE, 'Pay Per Call - Directors and above.csv'), ['company_domain']),
]
RUN_GLOBS = [
    os.path.join(ARCHIVE, 'ppc-*', 'state', '*.jsonl'),
    os.path.join(ARCHIVE, 'ppc-*', 'state', 'seen_domains.txt'),
    os.path.join(ARCHIVE, 'ppc-*', 'inbox', '*.jsonl'),
    os.path.join(ARCHIVE, 'ppc-*', 'out', '*.csv'),
    os.path.join(ROOT, 'state', 'evaluated.jsonl'),
]
DOMAIN_KEYS = ('domain', 'company_domain', 'Domain', 'website', 'url', 'source_domain')

def norm(v):
    d = L.reg_domain((v or '').strip())
    return d if d and '.' in d and len(d) > 3 else None

def main():
    known = {}
    def add(d, src):
        if d: known.setdefault(d, src)
    for path, cols in CSV_SOURCES:
        if not os.path.exists(path):
            print('  (missing) %s' % path); continue
        n = 0
        for r in csv.DictReader(io.open(path, encoding='utf-8-sig', errors='replace')):
            for c in cols:
                d = norm(r.get(c))
                if d: add(d, os.path.basename(path)); n += 1
        print('  %-55s %6d' % (os.path.basename(path)[:55], n))
    for g in RUN_GLOBS:
        for path in glob.glob(g):
            n = 0
            try:
                if path.endswith('.txt'):
                    for line in io.open(path, encoding='utf-8', errors='replace'):
                        d = norm(line)
                        if d: add(d, path); n += 1
                elif path.endswith('.jsonl'):
                    for line in io.open(path, encoding='utf-8', errors='replace'):
                        line = line.strip()
                        if not line.startswith('{'): continue
                        try: r = json.loads(line)
                        except Exception: continue
                        for k in DOMAIN_KEYS:
                            d = norm(r.get(k)) if isinstance(r.get(k), str) else None
                            if d: add(d, path); n += 1
                elif path.endswith('.csv'):
                    for r in csv.DictReader(io.open(path, encoding='utf-8-sig', errors='replace')):
                        for k in DOMAIN_KEYS:
                            d = norm(r.get(k))
                            if d: add(d, path); n += 1
            except Exception as e:
                print('  skip %s: %s' % (path, e))
            if n:
                try: label = os.path.relpath(path, ARCHIVE)
                except ValueError: label = path          # different drive on Windows
                print('  %-55s %6d' % (label[-55:], n))
    out = os.path.join(ROOT, 'state', 'known_domains.txt')
    with io.open(out, 'w', encoding='utf-8', newline='\n') as f:
        for d in sorted(known): f.write(d + '\n')
    print('\nexclusion index: %d domains -> %s' % (len(known), out))
    if len(known) < 13000:
        sys.exit('ABORT-LEVEL WARNING: index is smaller than the ledger alone should make it. '
                 'Check PPC_ARCHIVE / PPC_LEDGER paths before shipping this file.')

if __name__ == '__main__':
    main()
