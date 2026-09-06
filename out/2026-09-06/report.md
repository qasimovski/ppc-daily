# Pay-per-call daily sourcing — 2026-09-06

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel

| stage | count |
|---|---|
| linked-domain candidates | 0 |
| search requests | 30 |
| raw finds (search) | 260 |
| constructed domains probed | 300 |
| net-new candidates after exclusion index | 372 |
|   of which from search | 72 |
|   of which from probing | 300 |
| crawled | 369 |
|   crawl: ok | 60 |
|   crawl: thin | 2 |
|   crawl: unregistered | 292 |
|   crawl: unreachable | 13 |
|   crawl: redirect_offdomain | 2 |
| probes that resolved to a real site | 3 |
| v6 classified | 60 |
| carried to next run (unclassified) | 0 |
| V6 QUALIFIED | 0 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 177 |
| unreachable | 23 |
| thin | 9 |
| unregistered | 6 |
| redirect_offdomain | 5 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L4-familyB | 50 | 1 | 2.0% |
| L4-counterparty | 74 | 1 | 1.4% |
| L7-probe | 8 | 0 | 0.0% |
| L4-vertical | 43 | 0 | 0.0% |
| L8-linked | 2 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 2** (ICP-clean: 2). Cumulative across all daily runs: 20.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 69 |
| lead_or_appointment_pricing | 36 |
| no_clear_signal | 16 |
| service_to_call_receiver | 14 |
| seo_or_ranking_agency | 13 |
| software_or_crm | 9 |
| end_advertiser | 7 |
| directory_or_content | 7 |
| diy_ads_or_setup | 2 |
| recruiting | 2 |

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
