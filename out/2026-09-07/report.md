# Pay-per-call daily sourcing — 2026-09-07

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 43 -> 34 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 16 |
| raw finds (search) | 151 |
| constructed domains probed | 300 |
| net-new candidates after exclusion index | 366 |
|   of which from search | 66 |
|   of which from probing | 300 |
| crawled | 366 |
|   crawl: ok | 55 |
|   crawl: thin | 2 |
|   crawl: unregistered | 301 |
|   crawl: unreachable | 5 |
|   crawl: redirect_offdomain | 3 |
| probes that resolved to a real site | 0 |
| v6 classified | 55 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 1 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 186 |
| crawled ok | 151 |
| v6 classified | 151 |
| v6 qualified | 2 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 151 |
| redirect_offdomain | 16 |
| unreachable | 11 |
| thin | 5 |
| unregistered | 3 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L7-probe | 3 | 1 | 33.3% |
| L10-partners | 77 | 1 | 1.3% |
| L4-vertical | 38 | 0 | 0.0% |
| L4-counterparty | 33 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 2** (ICP-clean: 2). Cumulative across all daily runs: 42.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 50 |
| end_advertiser | 25 |
| lead_or_appointment_pricing | 22 |
| software_or_crm | 21 |
| seo_or_ranking_agency | 12 |
| service_to_call_receiver | 10 |
| no_clear_signal | 6 |
| directory_or_content | 2 |
| coach_or_consultant | 1 |

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
