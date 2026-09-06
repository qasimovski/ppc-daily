# Pay-per-call daily sourcing — 2026-09-06

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel

| stage | count |
|---|---|
| linked-domain candidates | 9 |
| search requests | 10 |
| raw finds (search) | 83 |
| constructed domains probed | 300 |
| net-new candidates after exclusion index | 325 |
|   of which from search | 25 |
|   of which from probing | 300 |
| crawled | 325 |
|   crawl: ok | 20 |
|   crawl: thin | 2 |
|   crawl: unregistered | 298 |
|   crawl: unreachable | 4 |
|   crawl: redirect_offdomain | 1 |
| probes that resolved to a real site | 1 |
| v6 classified | 20 |
| carried to next run (unclassified) | 0 |
| V6 QUALIFIED | 1 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 197 |
| unreachable | 26 |
| thin | 11 |
| unregistered | 8 |
| redirect_offdomain | 6 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L8-linked | 8 | 1 | 12.5% |
| L4-familyB | 50 | 1 | 2.0% |
| L4-counterparty | 87 | 1 | 1.1% |
| L7-probe | 9 | 0 | 0.0% |
| L4-vertical | 43 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 3** (ICP-clean: 2). Cumulative across all daily runs: 21.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 76 |
| lead_or_appointment_pricing | 43 |
| no_clear_signal | 17 |
| seo_or_ranking_agency | 16 |
| service_to_call_receiver | 14 |
| software_or_crm | 9 |
| end_advertiser | 8 |
| directory_or_content | 7 |
| diy_ads_or_setup | 2 |
| recruiting | 2 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | callrealmedia.com | 95 | inbound pay-per-call network selling calls to advertisers | yes |  | geo unknown |
|  | affiliature.com | 90 | affiliate marketing network selling various performance marketin | yes | United States; India |  |
|  | eliteremotes.com | 90 | pay-per-call campaign management and remote staffing services fo | yes | Pakistan; United States | REVIEW: names Ringba in prose (likely tenant) | MICROSITE of known company: t.me |

## Files

- `out/2026-09-06/qualified.csv` — every v6-qualified company found today
- `out/2026-09-06/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-06/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
