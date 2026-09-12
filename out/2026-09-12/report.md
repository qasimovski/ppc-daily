# Pay-per-call daily sourcing — 2026-09-12

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
| candidates crawled | 98 |
| crawled ok | 68 |
| v6 classified | 68 |
| v6 qualified | 2 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 68 |
| redirect_offdomain | 13 |
| unreachable | 11 |
| thin | 6 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L10-partners | 65 | 2 | 3.1% |
| L11-hiring-agent | 3 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 2** (ICP-clean: 2). Cumulative across all daily runs: 132.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 21 |
| lead_or_appointment_pricing | 17 |
| end_advertiser | 14 |
| service_to_call_receiver | 5 |
| directory_or_content | 3 |
| no_clear_signal | 3 |
| software_or_crm | 2 |
| seo_or_ranking_agency | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
| ExchangeFlo | exchangeflo.io | 90 | pay-per-call and lead marketplace for advertisers and publishers | yes |  | geo unknown |
| Affordable Auto | affordableautoinc.com | 90 | auto insurance lead generation and call sales | yes |  | geo unknown |

## Files

- `out/2026-09-12/qualified.csv` — every v6-qualified company found today
- `out/2026-09-12/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-12/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
