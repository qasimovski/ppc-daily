# Pay-per-call daily sourcing — 2026-09-07

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 32 -> 32 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 16 |
| raw finds (search) | 77 |
| constructed domains probed | 300 |
| net-new candidates after exclusion index | 347 |
|   of which from search | 47 |
|   of which from probing | 300 |
| crawled | 347 |
|   crawl: ok | 35 |
|   crawl: thin | 1 |
|   crawl: unregistered | 301 |
|   crawl: unreachable | 2 |
|   crawl: redirect_offdomain | 8 |
| probes that resolved to a real site | 0 |
| v6 classified | 35 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 0 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 91 |
| crawled ok | 75 |
| v6 classified | 75 |
| v6 qualified | 1 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 75 |
| redirect_offdomain | 9 |
| unreachable | 5 |
| thin | 1 |
| unregistered | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L7-probe | 3 | 1 | 33.3% |
| L10-partners | 33 | 0 | 0.0% |
| L4-vertical | 25 | 0 | 0.0% |
| L4-counterparty | 14 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 1** (ICP-clean: 1). Cumulative across all daily runs: 41.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 26 |
| end_advertiser | 13 |
| lead_or_appointment_pricing | 9 |
| software_or_crm | 8 |
| service_to_call_receiver | 7 |
| seo_or_ranking_agency | 5 |
| no_clear_signal | 3 |
| directory_or_content | 2 |
| coach_or_consultant | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | identityprotectionleads.com | 90 | sells identity protection leads and live transfer leads to buyer |  | United States |  |

## Files

- `out/2026-09-07/qualified.csv` — every v6-qualified company found today
- `out/2026-09-07/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-07/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
