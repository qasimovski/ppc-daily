# Pay-per-call daily sourcing — 2026-09-05

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel

| stage | count |
|---|---|
| search requests | 8 |
| raw finds (search) | 72 |
| constructed domains probed | 150 |
| net-new candidates after exclusion index | 172 |
|   of which from search | 22 |
|   of which from probing | 150 |
| crawled | 172 |
|   crawl: ok | 20 |
|   crawl: thin | 3 |
|   crawl: unregistered | 128 |
|   crawl: unreachable | 20 |
|   crawl: redirect_offdomain | 1 |
| probes that resolved to a real site | 2 |
| v6 classified | 23 |
| carried to next run (unclassified) | 0 |
| V6 QUALIFIED | 2 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 23 |
| thin | 5 |
| unreachable | 2 |
| redirect_offdomain | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L7-probe | 4 | 1 | 25.0% |
| L4-familyB | 16 | 1 | 6.2% |
| L4-counterparty | 3 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 2** (ICP-clean: 2). Cumulative across all daily runs: 2.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 9 |
| lead_or_appointment_pricing | 5 |
| end_advertiser | 3 |
| no_clear_signal | 2 |
| software_or_crm | 1 |
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
