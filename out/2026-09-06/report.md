# Pay-per-call daily sourcing — 2026-09-06

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel

| stage | count |
|---|---|
| linked-domain candidates | 3 |
| search requests | 30 |
| raw finds (search) | 257 |
| constructed domains probed | 300 |
| net-new candidates after exclusion index | 357 |
|   of which from search | 57 |
|   of which from probing | 300 |
| crawled | 357 |
|   crawl: ok | 41 |
|   crawl: thin | 2 |
|   crawl: unregistered | 301 |
|   crawl: unreachable | 10 |
|   crawl: redirect_offdomain | 3 |
| probes that resolved to a real site | 0 |
| v6 classified | 41 |
| carried to next run (unclassified) | 0 |
| V6 QUALIFIED | 0 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 117 |
| unreachable | 16 |
| thin | 7 |
| unregistered | 4 |
| redirect_offdomain | 4 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L4-familyB | 29 | 1 | 3.4% |
| L4-counterparty | 38 | 1 | 2.6% |
| L7-probe | 5 | 0 | 0.0% |
| L4-vertical | 43 | 0 | 0.0% |
| L8-linked | 2 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 2** (ICP-clean: 2). Cumulative across all daily runs: 20.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 47 |
| lead_or_appointment_pricing | 18 |
| service_to_call_receiver | 12 |
| no_clear_signal | 11 |
| end_advertiser | 7 |
| software_or_crm | 6 |
| directory_or_content | 5 |
| seo_or_ranking_agency | 5 |
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
