# Pay-per-call daily sourcing — 2026-09-05

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel

| stage | count |
|---|---|
| search requests | 33 |
| raw finds (search) | 264 |
| constructed domains probed | 300 |
| net-new candidates after exclusion index | 350 |
|   of which from search | 50 |
|   of which from probing | 300 |
| crawled | 349 |
|   crawl: ok | 37 |
|   crawl: unregistered | 297 |
|   crawl: unreachable | 14 |
|   crawl: redirect_offdomain | 1 |
| probes that resolved to a real site | 1 |
| v6 classified | 37 |
| carried to next run (unclassified) | 0 |
| V6 QUALIFIED | 3 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 176 |
| unreachable | 28 |
| thin | 19 |
| redirect_offdomain | 3 |
| unregistered | 1 |
| parked | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L7-probe | 32 | 4 | 12.5% |
| L4-counterparty | 44 | 5 | 11.4% |
| L4-familyB | 100 | 4 | 4.0% |

**V6 QUALIFIED TODAY: 13** (ICP-clean: 10). Cumulative across all daily runs: 15.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 68 |
| lead_or_appointment_pricing | 52 |
| seo_or_ranking_agency | 12 |
| no_clear_signal | 11 |
| directory_or_content | 6 |
| end_advertiser | 5 |
| software_or_crm | 4 |
| service_to_call_receiver | 3 |
| recruiting | 1 |
| coach_or_consultant | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | caraccidentcalls.com | 95 | sells live, exclusive phone calls to personal injury attorneys |  | United States |  |
|  | groei-media.com | 95 | pay-per-call marketing agency selling verified inbound calls to  | yes |  | geo unknown |
|  | damgomedia.com | 95 | pay-per-call marketing services to advertisers | yes | India | geo outside US/UK/CA: India |
|  | paypercallperformance.com | 95 | pay-per-call lead generation services for advertisers and publis | yes |  | geo unknown |
|  | join-our-network.com | 95 | affiliate network onboarding platform for pay-per-call publisher | yes |  | geo unknown | REVIEW: names Ringba in prose (likely tenant) |
|  | xvoramedia.com | 95 | Pay-per-call network for home services connecting publishers and | yes | United States | REVIEW: names Ringba in prose (likely tenant) |
|  | seagullsmediasolutions.com | 90 | performance marketing network selling pay-per-call and other per | yes | United States |  |
|  | injuryleads.io | 90 | pay-per-lead legal leads with optional live call transfers |  | United States |  |
|  | trudova.com | 90 | pay-per-call lead generation and call transfer services for insu | yes |  | geo unknown |
|  | mcaleads.us | 90 | MCA lead and live transfer seller to MCA brokers |  |  | geo unknown |
|  | towleads.co | 90 | pay-per-call live tow truck customer calls to towing businesses |  | United States |  |
|  | funneltrafficpros.com | 90 | pay-per-call lead generation network | yes |  | geo unknown |
|  | connectivanetwork.com | 85 | pay-per-call network connecting buyers and publishers | yes |  | geo unknown |

## Files

- `out/2026-09-05/qualified.csv` — every v6-qualified company found today
- `out/2026-09-05/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-05/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
