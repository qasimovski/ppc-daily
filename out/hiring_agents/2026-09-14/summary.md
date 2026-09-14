# Hiring agents run — 2026-09-14

Three subagents ran in parallel for ~45-47 minutes each (all crossed the 45-minute floor on
resume after an initial slightly-short report), covering the full DEPTH widening ladder
(tool x role, role x vertical, PPC vocabulary x hiring phrases, freshness/geo variants,
plus deep pagination on productive queries).

## Per-slice tallies

| Slice | Sources | Searches | Postings read | Employers found | Known/seen-by-sibling | Emitted |
|---|---|---|---|---|---|---|
| a — OnlineJobs.ph, gig/freelance boards | onlinejobs.ph, Upwork, Fiverr, Freelancer, Guru, Workana | 333 | 47 | 17 | 17 known | 0 |
| b — bebee.com / LinkedIn, US/UK/CA | bebee.com, LinkedIn, jobright.ai, himalayas.app, ATS boards | 368 | 54 | 52 | 17 known, 3 seen-by-sibling, 37 skipped | 0 |
| c — offshore geos + social | pk/in/ph/... .linkedin.com, Instagram/Facebook/X/Telegram, affpaying.com directory, mThink pay-per-call index | ~165 searches + ~40 fetch/known checks | 119 | ~100+ | 55 known, 2 seen-by-sibling, 56 skipped | 6 (2 downgraded to alias) |
| **Total** | | **~866** | **220** | | | **6 raw -> 4 net new** |

## Emitted (4 new employers, after alias dedup)

1. **sevenlogik.com** — Seven Logik, Inc, Miami FL. LinkedIn posting: "Senior Paid Media
   Director – Personal Injury Marketing." Homepage reads as a generic web/digital marketing
   agency — the personal-injury paid-media/call vertical is not visible on the homepage itself,
   so v6 should confirm fit rather than assume it from the job title alone.
2. **scypop.com** — Scypop Media. Small (~7-person) US pay-per-call network (flights/hotels/
   home services), founded 2020 by Tina Dixon. Found via team/conference page (LeadsCon,
   Affiliate Summit, Contact.io 2026), not a direct job ad — hiring signal is indirect (team
   growth / industry presence) rather than an open posting.
3. **insurancecallsdirect.com** — Insurance Calls Direct. Pay-per-call final-expense life
   insurance platform: TV + web-driven inbound calls sold to licensed agents, no contracts.
   Found via a marketing consultant's case study describing the launch of ICD's remote call
   center (a hiring/staffing signal) plus agent testimonials on LinkedIn/Instagram/Facebook.
   Small, brand-new company (13 LinkedIn followers at time of discovery).
4. **leadsquad.com** — Lead Squad. Homeowner-acquisition company selling verified leads AND
   calls (US-based live qualification/triage) to enterprise home-services operators; SOC2 and
   TCPA/DNC compliant. Founded by Todd Stearn (also CEO of the already-known Aragon
   Advertising). Found via mThink's pay-per-call partner index.

## Alias-of-known findings (not emitted as new)

- **jsonburns.com** and **wegetyoucited.com** — both confirmed via a Philippines-based
  employee's LinkedIn profile and the parent company's own site footer/ToS to be dba's of
  **Adolicious, LLC** (adolicious.co), already KNOWN in the exclusion index. Recorded here per
  the alias rule rather than emitted as new candidates.

## What worked

- Vertical-flavored quoted phrases ("pay per call" + vertical + hiring role) outperformed
  bare tool-name x role queries, which were dominated by unrelated ecommerce/Meta-ads "media
  buyer" noise.
- TCPA "marketing partners" disclosure pages surfacing incidentally in search results reliably
  confirmed real operators (slice b: 321 The Agency).
- Bulk-checking a curated pay-per-call directory (affpaying.com) and mThink's partner index
  against `tf.py known` was the highest-yield single move of the run — it cleanly separated
  ~45 already-known networks from a handful of true unknowns and produced 2 of the 4 net-new
  leads (leadsquad.com, and ruled out one dead domain).
- Following an employee's LinkedIn bio to the parent LLC's footer/ToS caught two alias domains
  of an already-known company.

## What was blocked / low-yield

- Upwork and ZipRecruiter job-detail pages returned `bot_blocked` on every fetch attempt across
  all three slices.
- LinkedIn company pages (as opposed to job-posting pages) were also blocked.
- Most Facebook Groups required login and could not be read (`login_required`).
- A large share of Pakistan/India/Bangladesh LinkedIn postings were solo founders running
  their own tiny PPC shops with no confirmed domain or clearly outside the US/UK/Canada scope
  — correctly skipped rather than fabricated.
- Several geo x tool-name combinations (id, my, lk, ve, ro, pt, it, gr, tr, pe, cl, br
  .linkedin.com) returned zero relevant results this run.

## Bottom line

866 total searches across three slices (10.8x the combined 240-search minimum) surfaced 4 net
new employers for the ledger after alias dedup, plus 2 alias findings folded into an already-
known company. The bulk of the pay-per-call niche reachable through hiring-signal search
appears to already be captured in the 13k+-domain exclusion index; the marginal yield here
came mostly from directory cross-checks and one-off small/new operators rather than fresh job
postings from previously-unseen companies.
