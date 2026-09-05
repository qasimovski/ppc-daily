# Pay-per-call daily sourcing — 2026-09-05

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel

| stage | count |
|---|---|
| search requests | 32 |
| raw finds (search) | 252 |
| constructed domains probed | 300 |
| net-new candidates after exclusion index | 365 |
|   of which from search | 65 |
|   of which from probing | 300 |
| crawled | 362 |
|   crawl: ok | 53 |
|   crawl: thin | 4 |
|   crawl: unregistered | 286 |
|   crawl: unreachable | 13 |
|   crawl: parked | 2 |
|   crawl: redirect_offdomain | 4 |
| probes that resolved to a real site | 2 |
| v6 classified | 53 |
| carried to next run (unclassified) | 0 |
| V6 QUALIFIED | 1 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 229 |
| unreachable | 33 |
| thin | 23 |
| redirect_offdomain | 6 |
| unregistered | 1 |
| parked | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L7-probe | 34 | 4 | 11.8% |
| L4-counterparty | 66 | 5 | 7.6% |
| L4-familyB | 129 | 5 | 3.9% |

**V6 QUALIFIED TODAY: 14** (ICP-clean: 11). Cumulative across all daily runs: 16.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 95 |
| lead_or_appointment_pricing | 64 |
| seo_or_ranking_agency | 19 |
| no_clear_signal | 14 |
| end_advertiser | 6 |
| directory_or_content | 6 |
| software_or_crm | 4 |
| service_to_call_receiver | 4 |
| coach_or_consultant | 2 |
| recruiting | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | caraccidentcalls.com | 95 | sells live, exclusive phone calls to personal injury attorneys |  | United States |  |
|  | groei-media.com | 95 | pay-per-call marketing agency selling verified inbound calls to  | yes |  | geo unknown |
|  | damgomedia.com | 95 | pay-per-call marketing services to advertisers | yes | India | geo outside US/UK/CA: India |
|  | paypercallperformance.com | 95 | pay-per-call lead generation services for advertisers and publis | yes |  | geo unknown |
|  | join-our-network.com | 95 | affiliate network onboarding platform for pay-per-call publisher | yes |  | geo unknown | REVIEW: names Ringba in prose (likely tenant) |
|  | xvoramedia.com | 95 | Pay-per-call network for home services connecting publishers and | yes | United States | REVIEW: names Ringba in prose (likely tenant) |
|  | premierkeyassociates.com | 95 | performance marketing network selling pay-per-call and other per | yes | United States |  |
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
