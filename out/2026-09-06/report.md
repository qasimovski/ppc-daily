# Pay-per-call daily sourcing — 2026-09-06

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 14 -> 13 |
| hiring postings read -> candidates | 8 -> 4 |
| linked-domain candidates | 0 |
| search requests | 3 |
| raw finds (search) | 27 |
| constructed domains probed | 0 |
| net-new candidates after exclusion index | 22 |
|   of which from search | 22 |
|   of which from probing | 0 |
| crawled | 22 |
|   crawl: ok | 16 |
|   crawl: thin | 1 |
|   crawl: unreachable | 1 |
|   crawl: parked | 1 |
|   crawl: redirect_offdomain | 3 |
| probes that resolved to a real site | 0 |
| v6 classified | 16 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 2 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 683 |
| crawled ok | 542 |
| v6 classified | 542 |
| v6 qualified | 20 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 542 |
| unreachable | 49 |
| redirect_offdomain | 49 |
| thin | 32 |
| unregistered | 10 |
| parked | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L9-hiring | 5 | 2 | 40.0% |
| L9-reviews | 3 | 1 | 33.3% |
| L9-podcast | 3 | 1 | 33.3% |
| L9-registry | 21 | 4 | 19.0% |
| L8-linked | 11 | 1 | 9.1% |
| L7-probe | 31 | 2 | 6.5% |
| L10-partners | 184 | 5 | 2.7% |
| L4-counterparty | 136 | 3 | 2.2% |
| L4-familyB | 50 | 1 | 2.0% |
| L4-vertical | 78 | 0 | 0.0% |
| L10-hiring | 18 | 0 | 0.0% |
| L11-hiring-agent | 2 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 20** (ICP-clean: 18). Cumulative across all daily runs: 38.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 180 |
| lead_or_appointment_pricing | 131 |
| no_clear_signal | 45 |
| seo_or_ranking_agency | 42 |
| end_advertiser | 40 |
| service_to_call_receiver | 37 |
| software_or_crm | 28 |
| directory_or_content | 10 |
| recruiting | 5 |
| diy_ads_or_setup | 2 |
| coach_or_consultant | 2 |

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
| New Jersey | newjersey.com | 90 | pay-per-call advertising network | yes |  | geo unknown |
| ICI Global Media | iciglobalmedia.com | 85 | pay-per-call advertising network connecting buyers and publisher | yes |  | geo unknown |
| Platinum Leads | platinumleads.com | 85 | pay-per-call lead generation network | yes |  | geo unknown |
| Procedures | procedures.com | 85 | pay-per-call marketplace connecting buyers and publishers | yes |  | geo unknown |
| Tennessee | tennessee.net | 85 | pay-per-call network connecting buyers and affiliates | yes | United States |  |

## Files

- `out/2026-09-06/qualified.csv` — every v6-qualified company found today
- `out/2026-09-06/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-06/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
