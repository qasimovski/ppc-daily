# Pay-per-call daily sourcing — 2026-09-06

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel

| stage | count |
|---|---|
| linked-domain candidates | 0 |
| search requests | 28 |
| raw finds (search) | 97 |
| constructed domains probed | 300 |
| net-new candidates after exclusion index | 328 |
|   of which from search | 28 |
|   of which from probing | 300 |
| crawled | 326 |
|   crawl: ok | 23 |
|   crawl: thin | 1 |
|   crawl: unregistered | 292 |
|   crawl: unreachable | 10 |
| probes that resolved to a real site | 1 |
| v6 classified | 23 |
| carried to next run (unclassified) | 0 |
| V6 QUALIFIED | 1 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 76 |
| unreachable | 7 |
| thin | 5 |
| unregistered | 2 |
| redirect_offdomain | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L4-counterparty | 13 | 1 | 7.7% |
| L4-familyB | 15 | 1 | 6.7% |
| L7-probe | 5 | 0 | 0.0% |
| L4-vertical | 43 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 2** (ICP-clean: 2). Cumulative across all daily runs: 20.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 27 |
| service_to_call_receiver | 11 |
| lead_or_appointment_pricing | 8 |
| software_or_crm | 6 |
| end_advertiser | 6 |
| no_clear_signal | 5 |
| directory_or_content | 4 |
| seo_or_ranking_agency | 4 |
| diy_ads_or_setup | 2 |
| recruiting | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | callrealmedia.com | 95 | inbound pay-per-call network selling calls to advertisers | yes |  | geo unknown |
|  | affiliature.com | 90 | affiliate marketing network selling various performance marketin | yes | United States; India |  |

## Files

- `out/2026-09-06/qualified.csv` — every v6-qualified company found today
- `out/2026-09-06/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-06/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
