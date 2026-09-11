# Hiring-signals agent run — 2026-09-11

Three subagents ran in parallel, one per slice, each for 43-45+ minutes with well over the
80-search minimum. Merged, deduped, and known-checked below.

## Per-slice tallies

| Slice | Source | Searches | Postings/employers logged | Emitted (NEW) | Already known |
|---|---|---|---|---|---|
| a | OnlineJobs.ph / gig boards | ~260 | 106 | 4 | ~100 |
| b | bebee.com / LinkedIn US/UK/CA | 401 | 49 | 0 | 16 resolved employers, all known |
| c | Offshore LinkedIn geos / social | 323 | 82 (102 lines incl. sub-checks) | 2 | 37 |
| **Total** | | **~984** | **257 seen-log lines** | **6** | — |

No cross-slice duplicate domains were found among the emitted candidates (dedupe kept all 6).
All 6 were re-verified as `NEW` via `python tools/tf.py known` at merge time.

## Emitted — 6 new employers

1. **wecall.llc** (WeCall LLC) — real estate/mortgage/debt-relief lead gen; sells a "Live
   Transfers" pricing tier; TCPA-compliant, US nationwide. Source: company site
   (`wecall.llc/about-us/`) — no literal job posting found despite dedicated searches.
2. **gopipelinedigital.com** (Pipeline Digital LLC) — "buyer-side media operation," MCA
   vertical explicitly priced Pay Per Call with a billable-duration threshold; 7+ years in
   regulated verticals. Source: company site — no job posting found.
3. **grovlabs.com** (GrovLabs) — pay-per-call network across ACA/Medicare/Final
   Expense/SSDI/MVA/Auto/Home/HVAC, "USA-based call center support," TCPA+TrustedForm.
   Source: company site — no job posting found.
4. **joinleadsbitmedia.com** (LeadsBitMedia LLC) — home-services pay-per-call network operator
   (HVAC/plumbing/roofing/etc.); US-registered LLC that recruits sub-affiliates in
   Pakistan/India. Source: affiliate/publisher recruitment page — no job posting found.
5. **tenxads.com** (TenX Ads) — ad-tech agency growing a "Paypercall" line (500k+/mo spend),
   selling leads/calls to aggregators; hiring a Media Buying Lead (CPL, Pay per call, CPA).
   Source: `me.linkedin.com/jobs/view/media-buying-lead-cpl-pay-per-call-cpa-at-tenx-ads-...`
6. **knovatiktechvision.com** (Knovatik Tech Vision LLC) — Riverview, FL lead-gen firm selling
   Live Transfers/qualified leads to US law firms and insurance agencies; India-based ops team
   hiring per LinkedIn posts. Source: `in.linkedin.com/company/knovatik`

**Caveat on candidates 1-4 (slice a):** none had a literal job-board posting as their
`source_url` despite targeted searches — the agent used the company's own site/partner-signup
page instead and flagged this plainly so a human can veto before these enter the crawl/v6
pipeline. Candidates 5-6 (slice c) each have an actual job-posting URL.

## Alias-of-known findings

- `porchgroup.com` (Porch Group Inc.) resolved as technically NEW but is the same public
  company as already-known `porch.com` and is a large enterprise, outside Kaliper's small-
  operator ICP — **not emitted**.
- "Whiterock Marketing" is a pay-per-call subsidiary brand of already-known Kimia Group; no
  separate domain found — not applicable as a new candidate.
- `zilliondatamarketing.com` was flagged `SEEN_BY_AGENT` (already handled by a sibling slice
  this session) — not re-emitted by slice c.
- `insuranceleads.us` was likewise already flagged by a sibling slice — not re-emitted by
  slice a.

## What worked

- bebee.com job-aggregator mirrors (slices a and b) were the highest-yield source — full,
  un-blocked Indeed/LinkedIn text with "About <Company>" employer attribution.
- Literal pay-per-call vocabulary phrases ("ping post," "buyer caps," "call transfers,"
  "live transfers") were consistently the highest-signal query shapes across all three slices.
- LinkedIn country-subdomain job pages (pk./in./ph./me.linkedin.com/jobs/view/...) worked
  reliably for slice c even though the main www.linkedin.com domain did not.

## What was blocked

- Upwork job-apply pages returned `bot_blocked` on every fetch attempt (slice a) — only
  search snippets were readable, never full postings.
- www.linkedin.com direct fetches (main domain, non-country-coded) returned `bot_blocked`
  (slice c); country subdomains worked instead.
- Facebook business pages and post fetches returned `login_required` (slices a and c).
- Telegram (`t.me/s/<channel>`) previews surfaced no relevant pay-per-call hiring content
  (slice c).
- No TinyFish/network-level failures; no missing-key preflight issues.

## Channel saturation note

Slice b (bebee/LinkedIn, the most mature US/UK/CA channel) returned **zero new employers**
across 401 searches — every pay-per-call-signal employer found was already in the 18,587+
domain exclusion index. This channel appears saturated; slices a (informal gig boards) and
c (offshore-geo job boards + widened to bebee) still produced fresh finds, consistent with
the 2026-09-06 measurement that this channel's main limiter is how few such employers exist
that Kaliper doesn't already know about.

## Ledger updates

- `state/inbox/hiring_agents_2026-09-11.jsonl` — 6 survivor candidates for the next
  pipeline session (01:00/13:00 UTC) to crawl and v6-score.
- `state/hiring_agent_seen.jsonl` — grown from 1195 to 1452 lines (a: 106, b: 49, c: 102
  appended); per-slice seen files deleted after folding in.
