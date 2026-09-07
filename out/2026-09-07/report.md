# Pay-per-call daily sourcing — 2026-09-07

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 13 -> 8 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 16 |
| raw finds (search) | 13 |
| constructed domains probed | 0 |
| net-new candidates after exclusion index | 8 |
|   of which from search | 8 |
|   of which from probing | 0 |
| crawled | 8 |
|   crawl: ok | 6 |
|   crawl: unreachable | 1 |
|   crawl: redirect_offdomain | 1 |
| probes that resolved to a real site | 0 |
| v6 classified | 6 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 0 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 235 |
| crawled ok | 185 |
| v6 classified | 185 |
| v6 qualified | 2 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 185 |
| redirect_offdomain | 25 |
| unreachable | 15 |
| thin | 5 |
| unregistered | 5 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L7-probe | 3 | 1 | 33.3% |
| L10-partners | 96 | 1 | 1.0% |
| L4-vertical | 44 | 0 | 0.0% |
| L4-counterparty | 42 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 2** (ICP-clean: 2). Cumulative across all daily runs: 42.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 63 |
| end_advertiser | 29 |
| lead_or_appointment_pricing | 27 |
| software_or_crm | 26 |
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
