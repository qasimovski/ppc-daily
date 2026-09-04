# Pay-per-call daily sourcing — 2026-09-04

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel

| stage | count |
|---|---|
| search requests | 35 |
| raw finds (search) | 296 |
| constructed domains probed | 300 |
| net-new candidates after exclusion index | 363 |
|   of which from search | 63 |
|   of which from probing | 300 |
| crawled | 361 |
|   crawl: ok | 46 |
|   crawl: thin | 3 |
|   crawl: unregistered | 300 |
|   crawl: unreachable | 8 |
|   crawl: redirect_offdomain | 4 |
| probes that resolved to a real site | 0 |
| v6 classified | 46 |
| carried to next run (unclassified) | 0 |
| V6 QUALIFIED | 2 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 46 |
| unreachable | 8 |
| redirect_offdomain | 4 |
| thin | 3 |
| unregistered | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L4-familyB | 32 | 2 | 6.2% |
| L4-counterparty | 13 | 0 | 0.0% |
| L4-vertical | 1 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 2** (ICP-clean: 2). Cumulative across all daily runs: 4.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 22 |
| lead_or_appointment_pricing | 12 |
| seo_or_ranking_agency | 8 |
| service_to_call_receiver | 1 |
| no_clear_signal | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | ampbusinesslimited.com | 95 | pay-per-call and lead generation network | yes |  | geo unknown |
|  | joinoptimizetoconvert.com | 90 | pay-per-call lead generation for media buyers | yes |  | geo unknown |

## Files

- `out/2026-09-04/qualified.csv` — every v6-qualified company found today
- `out/2026-09-04/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-04/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
