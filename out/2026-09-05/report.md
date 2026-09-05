# Pay-per-call daily sourcing — 2026-09-05

All figures are UNIQUE DOMAINS. A lead only counts if it passed Kaliper's v6 gate and was absent from the exclusion index at the start of the run.

## Funnel

| stage | count |
|---|---|
| search requests | 2 |
| raw finds (search) | 19 |
| constructed domains probed | 20 |
| net-new candidates after exclusion index | 22 |
|   of which from search | 2 |
|   of which from probing | 20 |
| crawled | 22 |
|   crawl: ok | 1 |
|   crawl: unregistered | 16 |
|   crawl: unreachable | 3 |
|   crawl: redirect_offdomain | 2 |
| probes that resolved to a real site | 0 |
| v6 classified | 1 |
| carried to next run (unclassified) | 0 |
| V6 QUALIFIED | 0 |

## Crawl outcomes (net-new candidates only)

| status | count |
|---|---|
| ok | 88 |
| thin | 13 |
| unreachable | 5 |
| redirect_offdomain | 2 |
| unregistered | 1 |
| parked | 1 |

## v6 qualify rate per discovery channel

| channel | classified | qualified | rate |
|---|---|---|---|
| L4-counterparty | 16 | 2 | 12.5% |
| L7-probe | 26 | 2 | 7.7% |
| L4-familyB | 46 | 2 | 4.3% |

**V6 QUALIFIED TODAY: 6** (ICP-clean: 5). Cumulative across all daily runs: 8.

## Why candidates failed v6

| reason | count |
|---|---|
| unrelated | 37 |
| lead_or_appointment_pricing | 30 |
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
