# Pay-per-call daily sourcing — 2026-09-06

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 283 |
| crawled ok | 224 |
| v6 classified | 224 |
| v6 qualified | 4 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 224 |
| unreachable | 32 |
| thin | 12 |
| unregistered | 8 |
| redirect_offdomain | 7 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L8-linked | 11 | 1 | 9.1% |
| L4-familyB | 50 | 1 | 2.0% |
| L4-counterparty | 108 | 2 | 1.9% |
| L7-probe | 12 | 0 | 0.0% |
| L4-vertical | 43 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 4** (ICP-clean: 3). Cumulative across all daily runs: 22.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 86 |
| lead_or_appointment_pricing | 48 |
| no_clear_signal | 21 |
| seo_or_ranking_agency | 18 |
| service_to_call_receiver | 14 |
| software_or_crm | 11 |
| end_advertiser | 9 |
| directory_or_content | 8 |
| recruiting | 3 |
| diy_ads_or_setup | 2 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | callrealmedia.com | 95 | inbound pay-per-call network selling calls to advertisers | yes |  | geo unknown |
|  | gocallgo.com | 95 | pay-per-call lead generation network connecting consumers to ser | yes | United States |  |
|  | affiliature.com | 90 | affiliate marketing network selling various performance marketin | yes | United States; India |  |
|  | eliteremotes.com | 90 | pay-per-call campaign management and remote staffing services fo | yes | Pakistan; United States | REVIEW: names Ringba in prose (likely tenant) | MICROSITE of known company: t.me |

## Files

- `out/2026-09-06/qualified.csv` — every v6-qualified company found today
- `out/2026-09-06/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-06/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
