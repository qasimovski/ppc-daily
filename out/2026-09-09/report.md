# Pay-per-call daily sourcing — 2026-09-09

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 20 -> 14 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 5 |
| search requests | 0 |
| raw finds (search) | 25 |
| constructed domains probed | 0 |
| net-new candidates after exclusion index | 19 |
|   of which from search | 19 |
|   of which from probing | 0 |
| crawled | 19 |
|   crawl: ok | 13 |
|   crawl: unregistered | 2 |
|   crawl: parked | 1 |
|   crawl: redirect_offdomain | 3 |
| probes that resolved to a real site | 0 |
| v6 classified | 13 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 0 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 95 |
| crawled ok | 66 |
| v6 classified | 66 |
| v6 qualified | 1 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 66 |
| redirect_offdomain | 14 |
| unreachable | 5 |
| thin | 5 |
| unregistered | 4 |
| parked | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L10-partners | 63 | 1 | 1.6% |
| L8-linked | 3 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 1** (ICP-clean: 1). Cumulative across all daily runs: 103.

## Why candidates failed v6

| reason | count |
|---|---|
| lead_or_appointment_pricing | 23 |
| end_advertiser | 17 |
| unrelated | 14 |
| service_to_call_receiver | 4 |
| no_clear_signal | 3 |
| seo_or_ranking_agency | 2 |
| recruiting | 1 |
| coach_or_consultant | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
| Quoting Fast | quotingfast.com | 95 | lead generation with live transfer calls and internet leads sold | yes | United States |  |

## Files

- `out/2026-09-09/qualified.csv` — every v6-qualified company found today
- `out/2026-09-09/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-09/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
