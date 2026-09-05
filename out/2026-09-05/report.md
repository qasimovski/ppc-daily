# Pay-per-call daily sourcing — 2026-09-05

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel

| stage | count |
|---|---|
| search requests | 32 |
| raw finds (search) | 277 |
| constructed domains probed | 300 |
| net-new candidates after exclusion index | 338 |
|   of which from search | 38 |
|   of which from probing | 300 |
| crawled | 335 |
|   crawl: ok | 50 |
|   crawl: thin | 8 |
|   crawl: unregistered | 200 |
|   crawl: unreachable | 54 |
|   crawl: parked | 5 |
|   crawl: redirect_offdomain | 18 |
| probes that resolved to a real site | 20 |
| v6 classified | 50 |
| carried to next run (unclassified) | 0 |
| V6 QUALIFIED | 4 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 87 |
| thin | 13 |
| unreachable | 4 |
| redirect_offdomain | 2 |
| unregistered | 1 |
| parked | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L4-counterparty | 16 | 2 | 12.5% |
| L7-probe | 26 | 2 | 7.7% |
| L4-familyB | 45 | 2 | 4.4% |

**V6 QUALIFIED TODAY: 6** (ICP-clean: 5). Cumulative across all daily runs: 8.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 37 |
| lead_or_appointment_pricing | 29 |
| no_clear_signal | 6 |
| end_advertiser | 3 |
| seo_or_ranking_agency | 3 |
| software_or_crm | 2 |
| service_to_call_receiver | 1 |

## Qualified today

| company | domain | fit | business model | marketplace | geo | flags |
|---|---|---|---|---|---|---|
|  | caraccidentcalls.com | 95 | sells live, exclusive phone calls to personal injury attorneys |  | United States |  |
|  | groei-media.com | 95 | pay-per-call marketing agency selling verified inbound calls to  | yes |  | geo unknown |
|  | damgomedia.com | 95 | pay-per-call marketing services to advertisers | yes | India | geo outside US/UK/CA: India |
|  | seagullsmediasolutions.com | 90 | performance marketing network selling pay-per-call and other per | yes | United States |  |
|  | injuryleads.io | 90 | pay-per-lead legal leads with optional live call transfers |  | United States |  |
|  | trudova.com | 90 | pay-per-call lead generation and call transfer services for insu | yes |  | geo unknown |

## Files

- `out/2026-09-05/qualified.csv` — every v6-qualified company found today
- `out/2026-09-05/qualified_icp_clean.csv` — US/UK/CA subset with no exclusion flag. **This is the list to work.**
- `out/2026-09-05/rejected.csv` — v6 rejections with reason, for tuning
- `out/ALL_qualified.csv` — cumulative, deduped by domain
- `state/evaluated.jsonl` — every domain judged, for `local/sync_to_ledger.py`
