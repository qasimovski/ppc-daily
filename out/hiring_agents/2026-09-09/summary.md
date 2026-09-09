# Hiring agents run — 2026-09-09

Three parallel discovery agents, each working the full 45-minute depth floor (slice c was sent
back once for finishing at 40 minutes and completed a second pass to clear the floor). Merged
output: **11 new employers emitted**, no duplicate domains across the three slices.

## Per-slice tallies

| Slice | Source | Searches | Postings/profiles logged to seen | Employers evaluated | Already known | Skipped | Emitted |
|---|---|---|---|---|---|---|---|
| a | OnlineJobs.ph / gig boards | 282 | 111 | 81 | 37 | 69 | 4 (one employer, 4 domains) |
| b | bebee.com / LinkedIn US/UK/CA | 130+ | ~58 logged (300+ read/checked) | ~70 | ~38 | ~28 | 2 |
| c | Offshore LinkedIn geos / social | ~165 | 123 | ~55 | 36 | 82 | 5 |

Timing: all three agents ran ~09:08–09:53 UTC. Slice a: 44m49s. Slice b: ~45m. Slice c: first
report at 40m (sent back per instructions), final report at 45m13s. All three cleared the
80-search floor several times over.

## Emitted (11, after dedupe and re-verification against `tools/tf.py known`)

**Slice a — one employer, four domains (all NEW):**
1. **insurancehelpguru.com** — Magic Media Group LLC (Hollywood, FL). BeBee "Business
   Development Manager" posting: "Familiarity with CPL, CPA, rev share, pay-per-call, or other
   performance-based models"; owns this lead-gen/offer site.
2. **dmv.com** — sibling domain of Magic Media Group LLC, confirmed via the site's own Data
   Privacy Notice naming the same Hollywood, FL entity; free-guide funnel funded by marketing
   partners/ads.
3. **guidekiwi.com** — sibling domain of Magic Media Group LLC, confirmed via registrant lookup
   (owner Michael Spitaleri, 330 N Federal Hwy Ste 200, Hollywood FL) matching the same address.
4. **assistance-team.com** — sibling domain of Magic Media Group LLC; identical free-guide /
   marketing-partners funnel template to insurancehelpguru.com and dmv.com, same Hollywood FL
   entity.

**Slice b:**
5. **leadsrules.com** — LeadsRules. LinkedIn "Senior Talent Acquisition Partner – U.S. Insurance
   Sales": "LeadsRules is a performance marketing and lead-generation company...We deliver leads,
   inbound calls and clicks across Auto, Home, Life, Final Expense, Auto Warranty."
6. **calibercalls.com** — Caliber Calls. Own site: "inbound marketing and customer acquisition
   center...match inbound customers with top-tier products...ACA, Medicare, Home Energy...
   delivering qualified, ready-to-convert connections to our agency partners," founded 2016.

**Slice c:**
7. **starkhazemedia.com** — Starkhaze Media. LinkedIn company page: "100+ Exclusive
   Appointments, Inbound Calls & Live Transfers of pre-qualified, high-intent sellers every
   month" for US real-estate wholesalers.
8. **alrehmancommunicationllc.com** — Al Rehman Communication LLC. Founder/CEO LinkedIn covers
   Debt Relief & Tax Debt settlement, Final Expense; own site headlines "GENERATE CALLS - Pay Per
   Call (PPC) campaigns...attract engaged buyers" across Insurance/Home Improvement/Tort Claims.
9. **nextagmedia.com** — Nextag Media (Noida performance/affiliate agency). LinkedIn hiring post:
   "We're Hiring! Affiliate Partnerships Manager who can...scale CPL, Sweepstakes, iGaming, and
   Pay-Per-Call campaigns for the International market" #PayPerCall.
10. **restorationradius.com** — Restoration Radius. LinkedIn company page: "Marketing built
    exclusively for U.S. restoration companies" (water damage, mold, fire, storm, biohazard);
    specialties include "Pay-Per-Call Marketing" and "Call Tracking"; self-owned, founded 2024.
11. **dymarkmedia.systeme.io** — Dymark Media (Gurgaon). Hiring post (Senior Brand Executive):
    "performance-focused marketing company that helps mortgage professionals...deliver exclusive
    appointments, inbound calls, and live transfers from pre-qualified, high-intent mortgage
    borrowers every month."

All 11 confirmed `NEW` (not KNOWN, not SEEN_BY_AGENT) via `tools/tf.py known` at merge time; no
domain appeared in more than one slice's inbox.

## Alias-of-known findings

None reported by any slice this run — no agent found an employer already known under one domain
operating a second, previously-unknown domain (distinct from the Magic Media Group LLC case
above, which is a single NEW employer operating four NEW sibling domains, not an alias of a
KNOWN one).

## What worked

- **bebee.com** was again the highest-yield source (slice a, slice b) — full posting text and
  "About <Company>" blocks give employer name, business model, and often verticals directly.
- LinkedIn company pages' "Website:" field (slice c) let agents verify a real domain instead of
  guessing from a search snippet — essential once past the first page of results.
- The recurring template phrase "Exclusive Appointments / Inbound Calls / Live Transfers" (slice
  c) and pay-per-call vocabulary combos ("ping post", "call flow", "buyer caps") outperformed
  plain tool-name x role queries once obvious tool-name hits were exhausted.
- `site:<geo>.linkedin.com "pay per call" hiring` across bd/in/pk/ph/ar/za geos (slice c) was the
  richest offshore-geo query shape; most LatAm/SEA/African geos were unproductive (see below).

## What was blocked / unproductive

- Upwork job-detail pages: `bot_blocked` on every fetch attempt (slice a).
- guru.com, workana.com, jobrack.io: essentially zero relevant results across all attempts
  (slice a).
- LinkedIn job pages and ZipRecruiter: intermittently/fully blocked (slice a).
- Most Latin American, SEA, and African geos (mx, rs, eg, ng, ke, ro, do, gt, hn, sv, pe, cl, ve,
  br, pt, es, it, gr, tr, vn, id, my, ge, am) returned zero or irrelevant results even with
  translated vocabulary (slice c).
- Facebook group posts were almost entirely peer-to-peer classified ads between existing
  publishers/buyers, not named-employer job postings; the "Pay Per Call Marketers Hub" group
  returned no results. Telegram (`t.me/s`, `site:t.me`) never surfaced anything (slice c).
- A cluster of solo Indian freelancers/very-small shops uses an identical pitch template ("50+
  Exclusive Appointments, Inbound Calls & Live Transfers...every Month") targeting US mortgage
  brokers, PI lawyers, roofers, credit-repair consultants — clearly a shared script. Almost all
  had no company domain (LinkedIn personal profile only) and were correctly skipped per the
  no-fabrication rule; only the two with confirmed real websites were emitted (Dymark Media,
  Starkhaze Media).

## Same established space is well covered

Across all three slices, most employers with real pay-per-call hiring signals were already
known: Voax Media, CallBound Media, SmileNationUSA, Aragon Company/Vibrant Performance,
Crossblade Media, Interest Media, LeadLedger, Marketcall, BrokerCalls, Call Trader, Soleo/
CallThread, OnCore Leads, Bid On Calls, PX Media, Exclusive Live Calls, ResultCalls, CallSignal,
Boomsourcing, LeadBank/Home Alliance, Standard Conversions, Kimia Group, Launch Potato,
Centerfield, and others recurred across multiple slices independently — consistent with prior
runs' observation that the limiting factor in this channel is that most qualifying employers are
already indexed.

## Flagged for a human look (not emitted — no confirmable domain or outside hiring-signal mandate)

- **Customers Direct** (slice b) — strong fit (US national network of home-service installers
  buying "inbound customer opportunities and live transfers" across HVAC/roofing/solar/pest
  control) but its apparent domain (customersdirect.com) is a parked for-sale page; could not
  confirm the real site.
- **BestEdgeSolutions** (slice b) — CA-based call center for Medicare/ACA/Auto/Home Services;
  plausible match to bestleadsnetwork.com but unverified — not emitted.

## Next steps

`state/inbox/hiring_agents_2026-09-09.jsonl` (11 candidates) will be crawled and v6-scored by the
next pipeline session (01:00 / 13:00 UTC daily_run.py).
