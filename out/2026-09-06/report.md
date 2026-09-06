# Pay-per-call daily sourcing — 2026-09-06

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel

| stage | count |
|---|---|
| linked-domain candidates | 0 |
| search requests | 26 |
| raw finds (search) | 140 |
| constructed domains probed | 300 |
| net-new candidates after exclusion index | 357 |
|   of which from search | 57 |
|   of which from probing | 300 |
| crawled | 357 |
|   crawl: ok | 53 |
|   crawl: thin | 4 |
|   crawl: unregistered | 291 |
|   crawl: unreachable | 6 |
|   crawl: parked | 1 |
|   crawl: redirect_offdomain | 2 |
| probes that resolved to a real site | 4 |
| v6 classified | 53 |
| carried to next run (unclassified) | 0 |
| V6 QUALIFIED | 1 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 53 |
| thin | 4 |
| unreachable | 4 |
| unregistered | 2 |
| redirect_offdomain | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L4-familyB | 6 | 1 | 16.7% |
| L7-probe | 4 | 0 | 0.0% |
| L4-vertical | 42 | 0 | 0.0% |
| L4-counterparty | 1 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 1** (ICP-clean: 1). Cumulative across all daily runs: 19.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 20 |
| service_to_call_receiver | 9 |
| end_advertiser | 6 |
| software_or_crm | 5 |
| no_clear_signal | 4 |
| lead_or_appointment_pricing | 4 |
| directory_or_content | 2 |
| diy_ads_or_setup | 1 |
| recruiting | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | affiliature.com | 90 | affiliate marketing network selling various performance marketin | yes | United States; India |  |

## Files

- `out/2026-09-06/qualified.csv` — every v6-qualified company found today
- `out/2026-09-06/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-06/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
