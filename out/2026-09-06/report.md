# Pay-per-call daily sourcing — 2026-09-06

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 24 -> 18 |
| hiring postings read -> candidates | 6 -> 0 |
| linked-domain candidates | 0 |
| search requests | 10 |
| raw finds (search) | 24 |
| constructed domains probed | 0 |
| net-new candidates after exclusion index | 18 |
|   of which from search | 18 |
|   of which from probing | 0 |
| crawled | 18 |
|   crawl: ok | 13 |
|   crawl: unreachable | 1 |
|   crawl: redirect_offdomain | 4 |
| probes that resolved to a real site | 0 |
| v6 classified | 13 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 0 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 576 |
| crawled ok | 455 |
| v6 classified | 455 |
| v6 qualified | 17 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 455 |
| unreachable | 46 |
| redirect_offdomain | 37 |
| thin | 30 |
| unregistered | 8 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L9-hiring | 5 | 2 | 40.0% |
| L9-reviews | 3 | 1 | 33.3% |
| L9-podcast | 3 | 1 | 33.3% |
| L9-registry | 21 | 4 | 19.0% |
| L8-linked | 11 | 1 | 9.1% |
| L7-probe | 27 | 2 | 7.4% |
| L4-counterparty | 129 | 3 | 2.3% |
| L4-familyB | 50 | 1 | 2.0% |
| L10-partners | 143 | 2 | 1.4% |
| L4-vertical | 52 | 0 | 0.0% |
| L10-hiring | 11 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 17** (ICP-clean: 15). Cumulative across all daily runs: 35.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 150 |
| lead_or_appointment_pricing | 115 |
| no_clear_signal | 41 |
| seo_or_ranking_agency | 34 |
| end_advertiser | 33 |
| service_to_call_receiver | 31 |
| software_or_crm | 19 |
| directory_or_content | 8 |
| recruiting | 4 |
| diy_ads_or_setup | 2 |
| coach_or_consultant | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | callrealmedia.com | 95 | inbound pay-per-call network selling calls to advertisers | yes |  | geo unknown |
|  | gocallgo.com | 95 | pay-per-call lead generation network connecting consumers to ser | yes | United States |  |
| RingPerl | ringperl.com | 95 | pay-per-call network connecting affiliates with direct call buye | yes | United States | REVIEW: names Ringba in prose (likely tenant) |
| CallBound Media | callboundmedia.com | 95 | pay-per-call demand generation and live call transfers to buyers | yes |  | geo unknown |
| SmileNationUSA LLC | smilenationusa.com | 95 | pay-per-call marketing agency for service professionals |  | United States |  |
| Direct Web Advertising Inc. | directwebadvertising.com | 95 | pay-per-call lead generation and call selling to advertisers | yes |  | geo unknown |
|  | affiliature.com | 90 | affiliate marketing network selling various performance marketin | yes | United States; India |  |
|  | eliteremotes.com | 90 | pay-per-call campaign management and remote staffing services fo | yes | Pakistan; United States | REVIEW: names Ringba in prose (likely tenant) | MICROSITE of known company: t.me |
| LeadBaron | leadbaron.io | 90 | pay-per-call inbound call traffic broker | yes | United States |  |
| Harmony Leads, Inc | harmonyleads.com | 90 | lead generation and live call transfers to buyers |  |  | geo unknown |
| Instant Lead Source | instantleadsource.com | 90 | pay-per-call lead generation services for agents | yes |  | geo unknown |
| iFuze Marketing | ifuzemarketing.com | 90 | digital marketing services including lead generation and live ph |  | United States |  |
|  | treatmentlead.com | 90 | pay-per-call marketing services for treatment providers | yes |  | geo unknown |
|  | foreclosuredefenselead.com | 90 | foreclosure defense lead generation and live transfer calls to f |  | United States |  |
|  | melonlocal.com | 90 | digital marketing agency selling live transfer calls and interne |  |  | geo unknown |
| ICI Global Media | iciglobalmedia.com | 85 | pay-per-call advertising network connecting buyers and publisher | yes |  | geo unknown |
| Platinum Leads | platinumleads.com | 85 | pay-per-call lead generation network | yes |  | geo unknown |

## Files

- `out/2026-09-06/qualified.csv` — every v6-qualified company found today
- `out/2026-09-06/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-06/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
