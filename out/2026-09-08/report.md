# Pay-per-call daily sourcing — 2026-09-08

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 20 -> 14 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 0 |
| raw finds (search) | 20 |
| constructed domains probed | 0 |
| net-new candidates after exclusion index | 14 |
|   of which from search | 14 |
|   of which from probing | 0 |
| crawled | 14 |
|   crawl: ok | 9 |
|   crawl: thin | 1 |
|   crawl: redirect_offdomain | 4 |
| probes that resolved to a real site | 0 |
| v6 classified | 9 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 0 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 61 |
| crawled ok | 51 |
| v6 classified | 51 |
| v6 qualified | 2 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 51 |
| redirect_offdomain | 6 |
| thin | 3 |
| unreachable | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L10-partners | 51 | 2 | 3.9% |

**V6 QUALIFIED TODAY: 2** (ICP-clean: 2). Cumulative across all daily runs: 47.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 17 |
| end_advertiser | 14 |
| lead_or_appointment_pricing | 12 |
| service_to_call_receiver | 2 |
| directory_or_content | 2 |
| no_clear_signal | 1 |
| seo_or_ranking_agency | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
| InstaCare | instacare.io | 90 | pay-per-call network connecting advertisers and publishers | yes |  | geo unknown |
| Taylored Legacy | tayloredlegacy.com | 90 | pay-per-call network for publishers and advertisers | yes |  | geo unknown |

## Files

- `out/2026-09-08/qualified.csv` — every v6-qualified company found today
- `out/2026-09-08/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-08/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
