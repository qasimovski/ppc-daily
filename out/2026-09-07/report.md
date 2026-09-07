# Pay-per-call daily sourcing — 2026-09-07

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 8 -> 3 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 18 |
| raw finds (search) | 8 |
| constructed domains probed | 102 |
| net-new candidates after exclusion index | 105 |
|   of which from search | 3 |
|   of which from probing | 102 |
| crawled | 105 |
|   crawl: ok | 2 |
|   crawl: unregistered | 101 |
|   crawl: unreachable | 1 |
|   crawl: redirect_offdomain | 1 |
| probes that resolved to a real site | 0 |
| v6 classified | 2 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 0 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 324 |
| crawled ok | 262 |
| v6 classified | 262 |
| v6 qualified | 2 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 262 |
| redirect_offdomain | 29 |
| unreachable | 19 |
| thin | 8 |
| unregistered | 6 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L7-probe | 3 | 1 | 33.3% |
| L10-partners | 125 | 1 | 0.8% |
| L4-vertical | 90 | 0 | 0.0% |
| L4-counterparty | 44 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 2** (ICP-clean: 2). Cumulative across all daily runs: 42.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 85 |
| end_advertiser | 51 |
| software_or_crm | 39 |
| lead_or_appointment_pricing | 33 |
| service_to_call_receiver | 21 |
| seo_or_ranking_agency | 17 |
| no_clear_signal | 10 |
| directory_or_content | 2 |
| coach_or_consultant | 1 |
| recruiting | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | identityprotectionleads.com | 90 | sells identity protection leads and live transfer leads to buyer |  | United States |  |
| Bongoze | bongoze.com | 90 | warm lead live transfer service for sales teams |  | United States |  |

## Files

- `out/2026-09-07/qualified.csv` — every v6-qualified company found today
- `out/2026-09-07/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-07/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
