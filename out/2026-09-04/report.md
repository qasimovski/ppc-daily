# Pay-per-call daily sourcing — 2026-09-04

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel

| stage | count |
|---|---|
| search requests | 0 |
| raw finds (search) | 0 |
| constructed domains probed | 500 |
| net-new candidates after exclusion index | 500 |
|   of which from search | 0 |
|   of which from probing | 500 |
| crawled | 500 |
|   crawl: unregistered | 429 |
|   crawl: unreachable | 71 |
| probes that resolved to a real site | 0 |
| v6 classified | 0 |
| carried to next run (unclassified) | 0 |
| V6 QUALIFIED | 0 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|

**V6 QUALIFIED TODAY: 0** (ICP-clean: 0). Cumulative across all daily runs: 2.

## Files

- `out/2026-09-04/qualified.csv` — every v6-qualified company found today
- `out/2026-09-04/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-04/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
