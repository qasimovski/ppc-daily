# Pay-per-call daily sourcing — 2026-09-11

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 0 -> 0 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 0 |
| raw finds (search) | 0 |
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
| candidates crawled | 86 |
| crawled ok | 61 |
| v6 classified | 61 |
| v6 qualified | 5 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 61 |
| redirect_offdomain | 12 |
| unreachable | 6 |
| thin | 6 |
| unregistered | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L11-hiring-agent | 6 | 5 | 83.3% |
| L10-partners | 55 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 5** (ICP-clean: 3). Cumulative across all daily runs: 130.

## Why candidates failed v6

| reason | count |
|---|---|
| end_advertiser | 15 |
| unrelated | 15 |
| lead_or_appointment_pricing | 11 |
| service_to_call_receiver | 5 |
| no_clear_signal | 4 |
| software_or_crm | 3 |
| seo_or_ranking_agency | 2 |
| directory_or_content | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
| GrovLabs | grovlabs.com | 95 | pay-per-call network selling live transferred inbound calls to b | yes | United States | MICROSITE of known company: app.google |
| LeadsBitMedia LLC | joinleadsbitmedia.com | 95 | pay-per-call affiliate network for home-services calls | yes | Pakistan; India | geo outside US/UK/CA: Pakistan, India |
| Knovatik Tech Vision LLC | knovatiktechvision.com | 90 | pay-per-call lead generation and call center services for US cam |  | United States; India |  |
| WeCall LLC | wecall.llc | 90 | lead generation agency selling exclusive leads and live transfer |  | United States |  |
| TenX Ads | tenxads.com | 85 | pay-per-call advertising network | yes |  | geo unknown |

## Files

- `out/2026-09-11/qualified.csv` — every v6-qualified company found today
- `out/2026-09-11/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-11/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
