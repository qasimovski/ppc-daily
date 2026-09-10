# Pay-per-call daily sourcing — 2026-09-10

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 9 -> 7 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 0 |
| raw finds (search) | 9 |
| constructed domains probed | 0 |
| net-new candidates after exclusion index | 7 |
|   of which from search | 7 |
|   of which from probing | 0 |
| crawled | 7 |
|   crawl: ok | 7 |
| probes that resolved to a real site | 0 |
| v6 classified | 7 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 0 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 940 |
| crawled ok | 567 |
| v6 classified | 567 |
| v6 qualified | 21 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 567 |
| unreachable | 226 |
| unregistered | 79 |
| thin | 28 |
| redirect_offdomain | 22 |
| parked | 13 |
| ringba_banned | 5 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L12-exalike-gen2 | 503 | 21 | 4.2% |
| L10-partners | 60 | 0 | 0.0% |
| L11-hiring-agent | 1 | 0 | 0.0% |
| L8-linked | 3 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 21** (ICP-clean: 20). Cumulative across all daily runs: 125.

## Why candidates failed v6

| reason | count |
|---|---|
| lead_or_appointment_pricing | 189 |
| seo_or_ranking_agency | 85 |
| unrelated | 75 |
| service_to_call_receiver | 74 |
| no_clear_signal | 44 |
| end_advertiser | 28 |
| directory_or_content | 26 |
| software_or_crm | 18 |
| coach_or_consultant | 3 |
| recruiting | 2 |
| diy_ads_or_setup | 2 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | magimedialeads.com | 95 | pay-per-call marketing service for moving businesses |  |  | geo unknown |
|  | fireleadz.com | 95 | pay-per-call live transfer leads for MCA funders |  |  | geo unknown |
|  | leadchampionmarketing.com | 95 | pay-per-call lead generation agency selling qualified calls to b |  | United States |  |
|  | luxmediamix.com | 95 | pay-per-call lead generation for advertisers | yes | United States; Philippines |  |
|  | thedirectquotes.net | 95 | pay-per-call advertising network connecting advertisers with inb | yes |  | geo unknown |
|  | agentautodialer.com | 90 | pay-per-call live transfer call selling platform | yes |  | geo unknown |
|  | arcleadai.com | 90 | pay-per-call inbound call generation and appointment booking for |  |  | geo unknown |
|  | quotedynamics.com | 90 | sells live transfer calls and leads to insurance agencies |  | United States |  |
|  | callingcare.com | 90 | automated telephone reassurance call service to individuals and  |  | United States |  |
|  | leadbreeze.com | 90 | bilingual call center providing live call transfers and lead man |  |  | geo unknown |
|  | leadhelix.ai | 90 | performance marketing and lead generation for pay-per-call progr |  |  | geo unknown |
|  | leadjar.io | 90 | pay-per-call marketing agency selling qualified inbound calls to |  |  | geo unknown |
|  | liveduicalls.com | 90 | sells exclusive live phone calls to DUI attorneys |  | United States |  |
|  | legaleagle.ai | 90 | legal marketing services selling pay-per-call and pay-per-lead t |  | United States |  |
|  | medication-reminder-calls.com | 90 | automated medication reminder calls to subscribers |  | United States |  |
|  | nicomediagroup.com | 90 | sells inbound insurance calls to insurance partners |  | United States |  |
|  | primeconnectnetwork.com | 90 | pay-per-call network for TV and internet service leads | yes |  | geo unknown |
|  | revring.ai | 90 | AI sales agents platform with live call transfers to buyers |  | United States |  |
|  | theleadsmedia.com | 90 | pay-per-call live transfer leads for MCA and credit repair |  | United States; Canada |  |
|  | leadgon.com | 85 | affiliate network selling pay-per-call traffic | yes | United States; India | MICROSITE of known company: postaffiliatepro.com, ladesk.com |
|  | pixelproaimarketing.com | 85 | pay-per-call marketing network connecting buyers and publishers | yes |  | geo unknown |

## Files

- `out/2026-09-10/qualified.csv` — every v6-qualified company found today
- `out/2026-09-10/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-10/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
