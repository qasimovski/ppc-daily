# Pay-per-call daily sourcing — 2026-09-13

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 1 -> 0 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 0 |
| raw finds (search) | 1 |
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
| candidates crawled | 61 |
| crawled ok | 47 |
| v6 classified | 47 |
| v6 qualified | 1 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 47 |
| redirect_offdomain | 7 |
| unreachable | 5 |
| unregistered | 1 |
| thin | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L11-hiring-agent | 5 | 1 | 20.0% |
| L10-partners | 42 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 1** (ICP-clean: 1). Cumulative across all daily runs: 133.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 20 |
| lead_or_appointment_pricing | 10 |
| end_advertiser | 5 |
| seo_or_ranking_agency | 4 |
| directory_or_content | 3 |
| service_to_call_receiver | 2 |
| no_clear_signal | 2 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
| Handy Alliance | handyalliance.com | 95 | Qualified inbound home service calls sold to service businesses |  |  | geo unknown |

## Files

- `out/2026-09-13/qualified.csv` — every v6-qualified company found today
- `out/2026-09-13/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-13/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
