# Hiring agents run — 2026-09-12

Three parallel discovery agents (slices a/b/c), each run for 45+ minutes with 80+ TinyFish
searches minimum, per `agents/HIRING_AGENTS.md`.

## Per-slice tallies

| Slice | Source | Searches | Postings read | Employers evaluated | Already known | Emitted |
|---|---|---|---|---|---|---|
| a | OnlineJobs.ph / gig & freelance boards | 321 | ~40 | ~30 | 6 | 2 |
| b | bebee.com / LinkedIn / jobright / himalayas / ATS boards | ~336 | 70 | ~60+ | ~20+ | 0 |
| c | Offshore LinkedIn geos + social platforms | 150+ | ~120+ | ~45 | 15+ | 1 |
| **Total** | | **~807+** | **~230+** | **~135+** | **~40+** | **3** |

All three slices ran to at least 45 minutes wall-clock and cleared the 80-search minimum
(slice c cleared it comfortably at 150+; slices a and b ran far past it).

## Emitted — new employers (3, all confirmed NEW by `tools/tf.py known`)

1. **dial-xpress.com** — DialXpress. OnlineJobs.ph posting: "DialXpress is a fast-growing
   telemarketing company... deliver high-quality live transfers for home and auto insurance...
   Transfer interested customers to licensed insurance agents."
   (source: https://www.onlinejobs.ph/jobseekers/job/Home-and-Auto-Insurance-Telemarketer-600Month-Full-Time-Remote-1479857)

2. **insurancequotegenie.com** — Quote Genie. OnlineJobs.ph posting: "Quote Genie is a
   U.S.-based telemarketing company that connects interested consumers with licensed insurance
   professionals... transfers qualified prospects directly to the client"; $1/qualified transfer.
   (source: https://www.onlinejobs.ph/jobseekers/job/outbound-telemarketing-live-transfer-specialist-1687232)

3. **pennypermiles.com** — Linkinon Inc. Delaware-registered entity operating an auto-insurance
   quote/referral funnel; LinkedIn posting for a Delhi-based Advertising Media Buyer: "role
   focuses on CPL and Pay-Per-Call campaigns within the Insurance and Finance verticals."
   (source: https://in.linkedin.com/jobs/view/advertising-media-buyer-at-linkinon-inc-4360801780)

No cross-slice duplicates and no alias-of-known findings this run.

## What worked

- Slice a: the "[Company] is a [fast-growing/US-based] telemarketing company that
  connects/transfers..." phrasing directly names both employer and business model — highest
  yield pattern this run.
- Slice b: combining tool names (Ringba/TrackDrive/Retreaver/Phonexa) with roles and verticals
  on bebee.com/LinkedIn; checking the registered corporate entity behind India/Pakistan-posted
  roles (the "Linkinon Inc" pattern) is a technique worth reusing across slices.
- Slice c: tool-name/role combos on pk.linkedin.com and in.linkedin.com surfaced the most
  postings; Facebook group searches for "we buy calls"/"pay per call network" personas
  surfaced real US LLCs (mostly already known).

## What was blocked / limiting

- Nothing tool-level: TinyFish `search`/`fetch` worked throughout all three slices.
- Occasional `bot_blocked` on direct LinkedIn/company-page fetches; worked around via search
  snippets and cached mirrors (bebee.com, jooble.org, regional Indeed sites) where possible,
  otherwise those postings were skipped rather than guessed at.
- Several promising leads across all three slices were skipped for lack of a verifiable owned
  domain (no fabrication per the brief): We Grow Lead, Velocity Web Enterprises LLC, U.S. Data
  and Voice, LeadLedger (parked), Roofing Rocket, HomeServ Pro LLC, Blue Line Home Services,
  Tele Leads Communication, Casas Ad Co, and several anonymous "affiliate network" postings
  with no company name.
- The bulk of hiring signal in offshore-geo searches (slice c) traces to employers themselves
  headquartered outside US/UK/Canada (Pakistan, India, Bangladesh, Dubai) or to staffing
  agencies posting for unnamed clients — excluded per the brief's ICP/staffing-agency rules.
- The space continues to be heavily mined: the large majority of plausible ICP matches across
  all three slices were already in the exclusion index or the agent ledger from prior runs.

## Files

- `state/inbox/hiring_agents_2026-09-12.jsonl` — 3 new candidates for the next pipeline
  session to crawl and v6-score.
- `state/hiring_agent_seen.jsonl` — folded in 165 new entries (44 + 70 + 51) from the three
  per-slice seen files, which have been deleted.
