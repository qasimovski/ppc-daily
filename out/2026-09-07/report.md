# Pay-per-call daily sourcing — 2026-09-07

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 30 -> 22 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 19 |
| raw finds (search) | 73 |
| constructed domains probed | 293 |
| net-new candidates after exclusion index | 334 |
|   of which from search | 41 |
|   of which from probing | 293 |
| crawled | 334 |
|   crawl: ok | 28 |
|   crawl: unregistered | 295 |
|   crawl: unreachable | 3 |
|   crawl: redirect_offdomain | 8 |
| probes that resolved to a real site | 0 |
| v6 classified | 28 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 0 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 227 |
| crawled ok | 179 |
| v6 classified | 179 |
| v6 qualified | 2 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 179 |
| redirect_offdomain | 24 |
| unreachable | 14 |
| thin | 5 |
| unregistered | 5 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L7-probe | 3 | 1 | 33.3% |
| L10-partners | 90 | 1 | 1.1% |
| L4-vertical | 44 | 0 | 0.0% |
| L4-counterparty | 42 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 2** (ICP-clean: 2). Cumulative across all daily runs: 42.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 60 |
| end_advertiser | 28 |
| software_or_crm | 26 |
| lead_or_appointment_pricing | 25 |
| service_to_call_receiver | 14 |
| seo_or_ranking_agency | 13 |
| no_clear_signal | 7 |
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
