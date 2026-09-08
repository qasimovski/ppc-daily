# Pay-per-call daily sourcing — 2026-09-08

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel — LAST PASS ONLY (a day may have several passes)

| stage | count |
|---|---|
| inbox candidates | 0 |
| partner-list names resolved -> candidates | 1 -> 1 |
| hiring postings read -> candidates | 0 -> 0 |
| linked-domain candidates | 0 |
| search requests | 0 |
| raw finds (search) | 1 |
| constructed domains probed | 0 |
| net-new candidates after exclusion index | 1 |
|   of which from search | 1 |
|   of which from probing | 0 |
| crawled | 1 |
|   crawl: ok | 1 |
| probes that resolved to a real site | 0 |
| v6 classified | 1 |
| carried to next run (unclassified) | 0 |
| carried to next run (uncrawled) | 0 |
| V6 QUALIFIED | 0 |

## Day so far (all passes, unique domains)

| stage | count |
|---|---|
| candidates crawled | 708 |
| crawled ok | 547 |
| v6 classified | 547 |
| v6 qualified | 29 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 547 |
| redirect_offdomain | 58 |
| unreachable | 58 |
| thin | 24 |
| unregistered | 15 |
| parked | 5 |
| ringba_banned | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L12-exalookalike | 150 | 22 | 14.7% |
| L12-contactio | 179 | 4 | 2.2% |
| L10-partners | 138 | 3 | 2.2% |
| L12-affsummit | 65 | 0 | 0.0% |
| L11-hiring-agent | 1 | 0 | 0.0% |
| L12-trackdrive | 1 | 0 | 0.0% |
| L8-linked | 13 | 0 | 0.0% |

**V6 QUALIFIED TODAY: 29** (ICP-clean: 26). Cumulative across all daily runs: 74.

## Why candidates failed v6

| reason | count |
|---|---|
| lead_or_appointment_pricing | 151 |
| unrelated | 136 |
| service_to_call_receiver | 58 |
| end_advertiser | 52 |
| seo_or_ranking_agency | 36 |
| no_clear_signal | 29 |
| software_or_crm | 29 |
| directory_or_content | 22 |
| recruiting | 3 |
| coach_or_consultant | 1 |
| diy_ads_or_setup | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | leadwhich.com | 95 | pay-per-call lead generation for inbound calls | yes |  | geo unknown | REVIEW: names Ringba in prose (likely tenant) |
|  | quotedleads.com | 95 | sells live transfer insurance leads to insurance agents and agen |  | United States | MICROSITE of known company: pages.dev |
|  | elegalcalls.com | 95 | pay-per-call marketing for law firms |  |  | geo unknown |
|  | leadlync.site | 95 | pay-per-call lead generation for advertisers |  |  | geo unknown |
|  | cre8tiveleadmedia.com | 95 | pay-per-call advertising network connecting advertisers and publ | yes | Romania | geo outside US/UK/CA: Romania |
|  | adluxmedia.com | 95 | pay-per-call inbound call generation and delivery to businesses |  | United States |  |
|  | callmediagroup.com | 95 | sells exclusive inbound insurance calls to agents |  |  | geo unknown |
|  | healthcallgroup.com | 95 | pay-per-call marketing agency selling inbound health and Medicar | yes |  | geo unknown |
|  | 1zl2.com | 95 | pay-per-call marketing services to businesses |  |  | geo unknown |
|  | agencybounce.com | 95 | pay-per-call live transfer dialing service for insurance agencie |  | United States |  |
| InstaCare | instacare.io | 90 | pay-per-call network connecting advertisers and publishers | yes |  | geo unknown |
| Taylored Legacy | tayloredlegacy.com | 90 | pay-per-call network for publishers and advertisers | yes |  | geo unknown |
| Direct Response Leads | forbesmarketinggroup.com | 90 | sells live transfer calls and direct response leads to buyers |  | United States |  |
| Structurely | structurely.com | 90 | Conversational AI platform selling AI-handled live phone transfe |  | United States |  |
| TELEGENCE COMMUNICATION | telegencecommunication.com | 90 | performance marketing with live transfer calls and callbacks sol |  | United States |  |
|  | realmcaleads.com | 90 | pay-per-call and pay-per-lead MCA lead generation and call trans |  |  | geo unknown |
|  | firemcaleads.com | 90 | MCA lead and live transfer provider to lenders and brokers |  |  | geo unknown |
|  | eze-media.com | 90 | media buying agency selling pay-per-call campaigns to advertiser |  | United States |  |
|  | teamrex.net | 90 | pay-per-call lead generation and live transfer services |  |  | geo unknown |
|  | revring.com | 90 | call center software and lead marketplace platform for pay-per-c | yes | United States |  |
|  | actionmcaleads.com | 90 | lead generation and exclusive live transfer sales to funders and |  | United States |  |
|  | rpm-leads.com | 90 | sells live, exclusive inbound Medicare insurance calls to licens |  |  | geo unknown |
|  | core-comlinx.com | 90 | Medicare live transfer call lead generation for licensed agents |  |  | geo unknown |
|  | mrleadsllc.com | 90 | telemarketing and lead generation services with inbound live tra |  | Pakistan; United States |  |
|  | medialey.com | 90 | pay-per-call advertising and lead generation services |  |  | geo unknown |
|  | livelegalcalls.com | 90 | exclusive live phone calls sold to law firms |  | United States |  |
|  | amplifyleadmedia.com | 90 | performance-based digital marketing services to businesses |  | India; United States |  |
| 2ND CHANCE CREDIT FUNDING | 2ndchancecreditfunding.com | 85 | pay-per-call lead generation for credit funding | yes |  | geo unknown |
| SURETY AUTO GROUP | suretyautogroup.com | 85 | insurance agency selling car insurance quotes and live transfers |  |  | geo unknown |

## Files

- `out/2026-09-08/qualified.csv` — every v6-qualified company found today
- `out/2026-09-08/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-08/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
