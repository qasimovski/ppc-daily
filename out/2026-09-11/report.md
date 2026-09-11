# Pay-per-call daily sourcing — 2026-09-11

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 7 -> 7 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 0 |
| raw finds (search) | 7 |
| constructed domains probed | 0 |
| net-new candidates after exclusion index | 7 |
|   of which from search | 7 |
|   of which from probing | 0 |
| crawled | 7 |
|   crawl: ok | 4 |
|   crawl: unreachable | 2 |
|   crawl: redirect_offdomain | 1 |
| probes that resolved to a real site | 0 |
| v6 classified | 4 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 0 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 26 |
| crawled ok | 18 |
| v6 classified | 18 |
| v6 qualified | 0 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 18 |
| unreachable | 4 |
| redirect_offdomain | 2 |
| thin | 2 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L10-partners | 18 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 0** (ICP-clean: 0). Cumulative across all daily runs: 125.

## Why candidates failed v6

| reason | count |
|---|---|
| end_advertiser | 6 |
| unrelated | 4 |
| lead_or_appointment_pricing | 3 |
| service_to_call_receiver | 2 |
| seo_or_ranking_agency | 2 |
| software_or_crm | 1 |

## Files

- `out/2026-09-11/qualified.csv` — every v6-qualified company found today
- `out/2026-09-11/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-11/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
