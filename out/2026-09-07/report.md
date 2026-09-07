# Pay-per-call daily sourcing — 2026-09-07

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 6 -> 3 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 18 |
| raw finds (search) | 57 |
| constructed domains probed | 186 |
| net-new candidates after exclusion index | 202 |
|   of which from search | 16 |
|   of which from probing | 186 |
| crawled | 202 |
|   crawl: ok | 14 |
|   crawl: thin | 2 |
|   crawl: unregistered | 183 |
|   crawl: unreachable | 2 |
|   crawl: redirect_offdomain | 1 |
| probes that resolved to a real site | 0 |
| v6 classified | 14 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 0 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 378 |
| crawled ok | 303 |
| v6 classified | 303 |
| v6 qualified | 4 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 303 |
| redirect_offdomain | 33 |
| unreachable | 21 |
| thin | 13 |
| unregistered | 8 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L11-hiring-agent | 2 | 1 | 50.0% |
| L7-probe | 5 | 1 | 20.0% |
| L4-vertical | 108 | 1 | 0.9% |
| L10-partners | 141 | 1 | 0.7% |
| L4-counterparty | 47 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 4** (ICP-clean: 4). Cumulative across all daily runs: 44.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 100 |
| end_advertiser | 56 |
| software_or_crm | 42 |
| lead_or_appointment_pricing | 41 |
| service_to_call_receiver | 22 |
| seo_or_ranking_agency | 21 |
| no_clear_signal | 12 |
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
