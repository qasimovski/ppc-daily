# Hiring agents run — 2026-09-08

Three parallel discovery agents, each working the full 45-minute depth floor. Merged output:
**2 new employers emitted** (interestmedia.com, leadroll.io); leadroll.io was found independently
by both slice b and slice c and deduped, keeping the first (slice b) source.

## Per-slice tallies

| Slice | Source | Searches | Postings read | Employers evaluated | Already known | Skipped | Emitted |
|---|---|---|---|---|---|---|---|
| a | OnlineJobs.ph / gig boards | 358+ (400+ tool calls) | 98 | ~45 | 13 | 83 | 1 |
| b | bebee.com / LinkedIn US/UK/CA | 300+ | ~110 surfaced, ~35 read in full | ~55 | ~35 | ~35 | 1 |
| c | Offshore LinkedIn geos / social | ~180 | ~55 | ~50 | 14 | ~37 | 1 (dup of b, dropped) |

Timing: all three agents ran ~09:07–09:52 UTC (45+ minutes each), well past the 80-search floor.

## Emitted (2, after dedupe)

1. **interestmedia.com** — Interest Media, Inc. (Kansas City, MO). Slice a, via bebee.com
   "Senior Account Executive – Performance Marketing & Call Transfers": *"performance marketing
   publisher that owns and operates a portfolio of proprietary digital media properties...100% of
   our traffic, leads, and call transfers are generated through internally owned and operated
   assets and call center operations...monetize inbound and outbound call transfers on both CPL
   and CPA models"* across ACA, Medicare, Final Expense, SSDI, Auto Warranty.
2. **leadroll.io** — LeadRoll (Tampa, FL). Found independently by slice b and slice c via the same
   LinkedIn "Operations Manager for Affiliate Marketing Firm" posting: site touts "Exclusive &
   Verified Leads...reducing wasted calls", TCPA-compliant lead/call delivery via API/CRM, and
   explicit "familiarity with call-tracking platforms like Ringba, Retreaver, and Redtrack — or
   experience setting up ping-post campaigns."

Both confirmed `NEW` via `tools/tf.py known` at merge time.

## Alias-of-known findings

None identified this run — no agent found an employer already known under one domain operating a
second, previously-unknown domain.

## What worked

- **bebee.com** (mirrors Indeed/Lensa/Jobted, not bot-blocked) was the highest-yield source across
  both slice a and slice b — full posting text, employer names in "About <Company>" blocks.
- Pay-per-call vocabulary queries ("ping post", "buyer caps", "call flow", "DNI", "billable call",
  "duplicate policy") outperformed plain tool-name/role queries once the obvious tool-name hits
  were exhausted — the highest-signal widening step across all three slices.
- **pk.linkedin.com / bd.linkedin.com** (slice c) had real yield — Ray Advertising and DOPPCALL
  each had dozens of postings there, though both were already known.
- LinkedIn `/jobs/view/` pages were readable via fetch roughly half the time.

## What was blocked / unproductive

- Upwork anonymizes client identity behind a bot-blocked apply page.
- Fiverr, Freelancer.com, Guru, Workana, JobRack, RemoteStaff.ph: generic ecommerce/BPO gigs,
  essentially zero pay-per-call vocabulary.
- OnlineJobs.ph's own `/jobseekers/jobsearch` pages render as JS with no titles/links via fetch —
  had to route everything through the TinyFish search index instead.
- himalayas.app frequently `bot_blocked`; ziprecruiter.com blocked fetch entirely; several
  jobs.workable.com postings returned `empty_content`.
- Most non-South-Asian offshore geos (do, gt, hn, sv, pe, cl, ve, br, pt, es, it, gr, tr, ge, am)
  returned zero relevant results for this niche.
- Instagram/X company search surfaced almost entirely individual profiles, not identifiable
  employers with domains.
- Several LinkedIn company pages returned `bot_blocked`.

## Same established space is well covered

Across all three slices, the majority of employers with real pay-per-call hiring signals were
already known: Ray Advertising, DOPPCALL, Elevarus, The Aragon Company/Vibrant Performance,
Crossblade Media, OnCore Leads, Lead Smart Inc, Cash Network LLC, WhaleMaven, and others recurred
across multiple slices independently — consistent with the 2026-09-06 observation that the
limiting factor in this channel is that most qualifying employers are already indexed.

## Flagged for other channels / a human look (not emitted — no confirmable hiring posting or domain)

- **leadbrothersinc.com** (Lead Brothers Inc) — confirmed NEW domain, 30-year Medicare/Final
  Expense live-transfer leads business, but every mention found was marketing/sales content, not
  a hiring posting — outside this task's hiring-signal mandate.
- **Guidestar Marketing Group LLC** — explicit "U.S.-based...routes thousands of live calls daily
  through our in-house call center", appears on multiple insurance-quote-site TCPA marketing-
  partner disclosure pages (the exact pattern `partners.py` targets) — no official domain found.
- **Scypop Media** (scypop.com, NEW in ledger) — homepage explicitly "Your Premier Pay Per Call
  Network" (travel/home-services, AI call routing) — found via general web search, not a hiring
  posting; no confirmed US/UK/CA HQ.
- **Clear Choice Marketing Group** (Oxnard, CA) — "lead marketplace and pay-per-call operation"
  for financial distress — name collides with an unrelated Raleigh, NC SEO/PPC agency of the
  identical name; domain not confirmed.
- **Trakvion Solutions** — "US-based performance marketing and lead generation company
  specializing in insurance call transfers" — no domain found.
- Several anonymous OnlineJobs.ph / Facebook postings with strong call-routing/pay-per-call
  language but company names hidden behind logins or Telegram-DM-only contact — could not resolve
  to a domain, so nothing emitted.

## Next steps

`state/inbox/hiring_agents_2026-09-08.jsonl` (2 candidates) will be crawled and v6-scored by the
next pipeline session (01:00 / 13:00 UTC daily_run.py).
