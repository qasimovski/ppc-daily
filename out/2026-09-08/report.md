# Pay-per-call daily sourcing — 2026-09-08

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 519 |
| partner-list names resolved -> candidates | 16 -> 12 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 0 |
| raw finds (search) | 563 |
| constructed domains probed | 0 |
| net-new candidates after exclusion index | 531 |
|   of which from search | 531 |
|   of which from probing | 0 |
| crawled | 343 |
|   crawl: ok | 262 |
|   crawl: thin | 11 |
|   crawl: unregistered | 6 |
|   crawl: unreachable | 27 |
|   crawl: parked | 2 |
|   crawl: redirect_offdomain | 34 |
|   crawl: ringba_banned | 1 |
| probes that resolved to a real site | 0 |
| v6 classified | 170 |
| carried to next run (unclassified) | 92 |
| carried to next run (uncrawled) | 188 |
| V6 QUALIFIED | 1 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 380 |
| crawled ok | 277 |
| v6 classified | 277 |
| v6 qualified | 4 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 277 |
| redirect_offdomain | 50 |
| unreachable | 30 |
| thin | 14 |
| unregistered | 6 |
| parked | 2 |
| ringba_banned | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L10-partners | 107 | 3 | 2.8% |
| L12-contactio | 105 | 1 | 1.0% |
| L12-affsummit | 65 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 4** (ICP-clean: 4). Cumulative across all daily runs: 49.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 83 |
| lead_or_appointment_pricing | 67 |
| end_advertiser | 36 |
| service_to_call_receiver | 31 |
| seo_or_ranking_agency | 18 |
| software_or_crm | 17 |
| no_clear_signal | 14 |
| directory_or_content | 4 |
| recruiting | 2 |
| coach_or_consultant | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
| InstaCare | instacare.io | 90 | pay-per-call network connecting advertisers and publishers | yes |  | geo unknown |
| Taylored Legacy | tayloredlegacy.com | 90 | pay-per-call network for publishers and advertisers | yes |  | geo unknown |
| Direct Response Leads | forbesmarketinggroup.com | 90 | sells live transfer calls and direct response leads to buyers |  | United States |  |
| 2ND CHANCE CREDIT FUNDING | 2ndchancecreditfunding.com | 85 | pay-per-call lead generation for credit funding | yes |  | geo unknown |

## Files

- `out/2026-09-08/qualified.csv` — every v6-qualified company found today
- `out/2026-09-08/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-08/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
