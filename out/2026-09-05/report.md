# Pay-per-call daily sourcing — 2026-09-05

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel

| stage | count |
|---|---|
| search requests | 0 |
| raw finds (search) | 0 |
| constructed domains probed | 0 |
| net-new candidates after exclusion index | 0 |
|   of which from search | 0 |
|   of which from probing | 0 |
| crawled | 0 |
| probes that resolved to a real site | 0 |
| v6 classified | 14 |
| carried to next run (unclassified) | 0 |
| V6 QUALIFIED | 0 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 37 |
| thin | 5 |
| unreachable | 2 |
| redirect_offdomain | 1 |
| unregistered | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L7-probe | 6 | 1 | 16.7% |
| L4-familyB | 22 | 1 | 4.5% |
| L4-counterparty | 9 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 2** (ICP-clean: 2). Cumulative across all daily runs: 2.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 12 |
| lead_or_appointment_pricing | 10 |
| no_clear_signal | 4 |
| end_advertiser | 3 |
| seo_or_ranking_agency | 3 |
| software_or_crm | 2 |
| service_to_call_receiver | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | caraccidentcalls.com | 95 | sells live, exclusive phone calls to personal injury attorneys |  | United States |  |
|  | seagullsmediasolutions.com | 90 | performance marketing network selling pay-per-call and other per | yes | United States |  |

## Files

- `out/2026-09-05/qualified.csv` — every v6-qualified company found today
- `out/2026-09-05/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-05/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
