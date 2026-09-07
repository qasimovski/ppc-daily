# Pay-per-call daily sourcing — 2026-09-07

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 2 |
| partner-list names resolved -> candidates | 14 -> 10 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 16 |
| raw finds (search) | 65 |
| constructed domains probed | 300 |
| net-new candidates after exclusion index | 325 |
|   of which from search | 25 |
|   of which from probing | 300 |
| crawled | 325 |
|   crawl: ok | 20 |
|   crawl: thin | 3 |
|   crawl: unregistered | 297 |
|   crawl: unreachable | 4 |
|   crawl: redirect_offdomain | 1 |
| probes that resolved to a real site | 2 |
| v6 classified | 20 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 2 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 361 |
| crawled ok | 289 |
| v6 classified | 289 |
| v6 qualified | 4 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 289 |
| redirect_offdomain | 32 |
| unreachable | 21 |
| thin | 11 |
| unregistered | 8 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L11-hiring-agent | 2 | 1 | 50.0% |
| L7-probe | 5 | 1 | 20.0% |
| L4-vertical | 96 | 1 | 1.0% |
| L10-partners | 139 | 1 | 0.7% |
| L4-counterparty | 47 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 4** (ICP-clean: 4). Cumulative across all daily runs: 44.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 96 |
| end_advertiser | 53 |
| software_or_crm | 40 |
| lead_or_appointment_pricing | 39 |
| service_to_call_receiver | 21 |
| seo_or_ranking_agency | 20 |
| no_clear_signal | 11 |
| directory_or_content | 3 |
| coach_or_consultant | 1 |
| recruiting | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
| CallSignal | callsignal.app | 95 | pay-per-call leads for pest control businesses | yes |  | geo unknown |
|  | insurances-calls.com | 95 | sells inbound insurance calls and live transfers to insurance pa | yes | United States |  |
|  | identityprotectionleads.com | 90 | sells identity protection leads and live transfer leads to buyer |  | United States |  |
| Bongoze | bongoze.com | 90 | warm lead live transfer service for sales teams |  | United States |  |

## Files

- `out/2026-09-07/qualified.csv` — every v6-qualified company found today
- `out/2026-09-07/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-07/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
