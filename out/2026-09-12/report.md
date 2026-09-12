# Pay-per-call daily sourcing — 2026-09-12

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 11 -> 6 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 0 |
| raw finds (search) | 11 |
| constructed domains probed | 0 |
| net-new candidates after exclusion index | 6 |
|   of which from search | 6 |
|   of which from probing | 0 |
| crawled | 6 |
|   crawl: ok | 6 |
| probes that resolved to a real site | 0 |
| v6 classified | 6 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 1 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 54 |
| crawled ok | 36 |
| v6 classified | 36 |
| v6 qualified | 1 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 36 |
| unreachable | 7 |
| redirect_offdomain | 7 |
| thin | 4 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L10-partners | 36 | 1 | 2.8% |

**V6 QUALIFIED TODAY: 1** (ICP-clean: 1). Cumulative across all daily runs: 131.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 14 |
| lead_or_appointment_pricing | 11 |
| end_advertiser | 5 |
| directory_or_content | 2 |
| service_to_call_receiver | 2 |
| no_clear_signal | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
| ExchangeFlo | exchangeflo.io | 90 | pay-per-call and lead marketplace for advertisers and publishers | yes |  | geo unknown |

## Files

- `out/2026-09-12/qualified.csv` — every v6-qualified company found today
- `out/2026-09-12/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-12/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
