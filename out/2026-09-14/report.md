# Pay-per-call daily sourcing — 2026-09-14

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 0 -> 0 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 0 |
| raw finds (search) | 0 |
| constructed domains probed | 0 |
| net-new candidates after exclusion index | 0 |
|   of which from search | 0 |
|   of which from probing | 0 |
| crawled | 0 |
| probes that resolved to a real site | 0 |
| v6 classified | 0 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 0 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 20 |
| crawled ok | 15 |
| v6 classified | 15 |
| v6 qualified | 0 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 15 |
| redirect_offdomain | 3 |
| unreachable | 2 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L10-partners | 15 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 0** (ICP-clean: 0). Cumulative across all daily runs: 133.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 5 |
| lead_or_appointment_pricing | 4 |
| seo_or_ranking_agency | 3 |
| no_clear_signal | 2 |
| end_advertiser | 1 |

## Files

- `out/2026-09-14/qualified.csv` — every v6-qualified company found today
- `out/2026-09-14/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-14/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
