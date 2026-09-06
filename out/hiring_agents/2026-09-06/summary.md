# Hiring-signals agent run — 2026-09-06

Three subagents, ~45 minutes each, run in parallel. TinyFish search preflight passed
(`python tools/tf.py search test` returned results). No script or prompt files were
modified.

## Per-slice totals

| Slice | Source | Searches | Postings read | Employers found | Emitted (new) |
|---|---|---|---|---|---|
| a | OnlineJobs.ph, Upwork, Fiverr, freelancer.com, guru.com | ~25 | 25 | 10 | 0 |
| b | bebee.com, LinkedIn, jobright.ai, himalayas.app | ~30 | 35 | ~30 | 2 |
| c | Offshore LinkedIn geos, Instagram/Facebook/Telegram | ~35 | 47 | ~20 | 1 |
| **Total** | | **~90** | **107** | **~60** | **3 raw → 2 net-new** |

## Emitted (2, after merge/dedupe/known-check)

1. **3littlebirdsinteractive.com** — 3 Little Birds Interactive (Los Angeles). Bebee posting
   for "Performance Media Buyer": *"fast growing startup in the pay per call marketing
   space... deliver thousands of hot inbound call leads daily... United States and Canada."*
2. **adolicious.com** — Adolicious, LLC (Camarillo, CA; 2-10 employees). PH-based "Affiliate
   Operations & Campaign Management" posting titled "Pay Per Call - Admin Operations";
   company's own LinkedIn page confirms it as a pay-per-call/lead-gen broker.

## Dropped as a judgment call (not counted, flagged for review)

- **leadbank.homealliance.com** (slice b) — "LeadBank," described as a "global paper call
  platform... sell calls to major partners like HomeAdvisor." Its parent domain
  `homealliance.com` is already in `state/known_domains.txt`. Treated as the same company
  already in the exclusion index rather than a new discovery, so it was not emitted. A human
  may want to verify LeadBank is genuinely the same legal entity as HomeAlliance before
  ruling this out for good.

## What worked

- bebee.com job postings reliably name the employer and often quote full "About Us" copy
  that reveals the pay-per-call business model directly — the highest-signal source across
  all three slices.
- Combining a tool name (Ringba/TrackDrive/Retreaver/etc.) with a board-specific search
  operator (e.g. site:onlinejobs.ph) surfaced the cleanest self-identifying postings.
- LinkedIn country-site "About" company pages, when not bot-blocked, gave fast HQ/size/
  website confirmation for judging US/UK/Canada basis on offshore-posted roles.
- Cross-referencing an offshore employee's LinkedIn profile against the employer's own
  company page resolved Adolicious, whose own site had thin content.

## What was blocked

- Upwork job pages returned `bot_blocked` on fetch in slice a (4 occurrences) — title/snippet
  only, several leads (Retreaver Expert, Meta Ads Expert for Pay-Per-Call) could not be
  resolved to an employer and were skipped per the "never fabricate a domain" rule.
- himalayas.app company/market pages returned `bot_blocked` in slice b (search snippets still
  usable).
- `www.linkedin.com/company/...` pages frequently `bot_blocked` in slice c; regional
  `xx.linkedin.com` company pages usually worked as a substitute.
- Telegram and Instagram/Facebook search coverage (slice c) was thin for this vertical — mostly
  unrelated cold-calling gigs and generic "we're hiring" posts with no identifiable employer.
- Freelancer.com project postings (slice a) are posted by anonymous individual clients with no
  resolvable company — skipped per the fabrication rule.

## Why most candidates didn't convert

The large majority of employers found across all three slices (~55 of ~60) were already
present in `state/known_domains.txt` or `state/hiring_agent_seen.jsonl` from prior runs —
consistent with the 2026-09-06 measurement note in `agents/HIRING_AGENTS.md` that the limiting
factor for this channel is that most pay-per-call employers hiring on these boards are already
known. A meaningful secondary bucket was wrong-geography employers (Pakistan, India, Philippines,
Mexico, Spain HQ) posting offshore roles, correctly excluded per the brief.

## Next step

The inbox `state/inbox/hiring_agents_2026-09-06.jsonl` (2 candidates) will be crawled and
v6-scored by the next pipeline session (01:00 / 13:00 UTC daily_run.py).
