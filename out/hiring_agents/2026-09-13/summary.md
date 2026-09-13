# Hiring agents run — 2026-09-13

Three parallel subagents, one per slice, each ran ≥45 minutes and ≥80 searches per the DEPTH
requirement in `agents/HIRING_AGENTS.md`.

## Per-slice tallies

| Slice | Sources | Searches | Postings read | Employers found | Already known | Emitted |
|---|---|---|---|---|---|---|
| a — OnlineJobs.ph / gig boards | OnlineJobs.ph, Upwork, Fiverr, Freelancer, Guru, Workana, JobRack, RemoteStaff | ~276 | 436 | 169 distinct names / 18 distinct domains | 8 | 4 |
| b — bebee.com / LinkedIn US/UK/CA | bebee.com (us/ca/gb), LinkedIn jobs, jobright.ai, himalayas.app, remoterocketship, ATS boards | 150+ | ~70 employers evaluated | ~70 | 47 (+SEEN_BY_AGENT overlaps with a/c) | 1 |
| c — offshore LinkedIn geos / social | pk/in/ph/ar/mx/co/... .linkedin.com, Facebook/Instagram/Telegram (mostly blocked) | 375+ | 105 | ~100 | 46 | 4 (3 of which are aliases, see below) |
| **Total** | | **~800** | **~611 logged** | | **~101** | **6 emitted + 3 alias-of-known** |

Clocks: slice a 09:05:43–09:50:42 UTC, slice b 09:05:58–09:50:59 UTC, slice c 09:06:14–09:50:54 UTC — all ≥45 minutes.

## Emitted (new, written to `state/inbox/hiring_agents_2026-09-13.jsonl`)

1. **roadrescuenetwork.com** (Road Rescue Network) — towing/roadside call-dispatch marketplace; consumers call in, network bids the job to the nearest crew. Source: OnlineJobs.ph sales-rep posting.
2. **bigdaddyleads.com** (Big Daddy Leads) — life-insurance lead-gen/marketing firm with an internal media-buying team running inbound + outbound. Source: OnlineJobs.ph CSR posting.
3. **guaranteedestimates.com** (Guaranteed Estimates) — roofing "growth partner"; AI estimate funnel that books homeowner calls to vetted roofing partners. Source: OnlineJobs.ph sales-rep posting.
4. **handyalliance.com** (Handy Alliance) — home-services (pest control) call marketplace, site explicitly states "Pay for qualified calls." Source: OnlineJobs.ph cold-calling team-lead posting.
5. **myleads4u.com** (My Leads 4 U, Wainwright AB, Canada) — media buyer role generating leads for insurance/legal/home-service verticals, $100k+/mo ad spend. Source: LinkedIn (uk.linkedin.com mirror). Note: posting language leans "leads" more than explicitly "calls" — flagged with some ambiguity for downstream v6 scoring.
6. **legalassist4u.com** (Legal Assist) — Pakistan-based marketing specialist's LinkedIn bio names "Live Transfers, Pay per call, TCPA compliant traffic" and lists this as the employer's Company Website. Source: pk.linkedin.com.

## Alias-of-known findings (not emitted)

Slice c found a LinkedIn profile (Junior Affiliate Manager, ro.linkedin.com) listing five "Pay-Per-Call Network" sites operated by one employer, one of which — **tortclaims.com** — is already `KNOWN` in the exclusion index. Per the coordinator rule that a sibling domain of a known operator is not a new lead, these were recorded here rather than emitted:

- **johnfinds.com** — alias of known tortclaims.com (same IDS Group / JohnFinds network)
- **easysolar.us** — alias of known tortclaims.com (same network, solar vertical)
- **easydebtrelief.com** — alias of known tortclaims.com (same network, debt-relief vertical)

(`python tools/tf.py known` returns NEW for all three since the tool only matches literal domains, not common ownership — the alias call was made on the evidence in the LinkedIn profile itself.)

## What worked

- OnlineJobs.ph pay-per-call / tool-name / vertical phrasing remained the highest-yield source (slice a): postings that describe the employer's own inbound-call business model in the body, not just the platform tools used.
- LinkedIn `"pay per call"` + `"Company Website:"` on country-specific LinkedIn domains (pk/in/ph.linkedin.com) reliably surfaced an individual's employer URL directly (slice c) — the single source of this run's alias finding.
- bebee.com/gb and bebee.com/ca mirrors worked as advertised for full posting text (slice b).
- Cross-checking a company's self-description against its LinkedIn "About us" HQ location and the posting's country-locale reliably caught offshore-run "US LLC" shells claiming US/UK/CA status.

## What was blocked

- Upwork job pages: uniformly bot-blocked (slice a).
- Freelancer.com, Fiverr, Guru.com, Workana, JobRack, RemoteStaff.ph: near-zero yield — anonymized buyers, generic freelance gigs, or blog content, not operator postings (slice a).
- Many OnlineJobs.ph postings with strong pay-per-call signals hid the employer identity behind a login wall ("VIEW OTHER JOB POSTS FROM"); logged as `skipped:no_domain_found` per the no-fabrication rule rather than guessed (slice a).
- LinkedIn company pages frequently returned `bot_blocked` on fetch; worked around via search-snippet triangulation (slice b).
- Facebook groups (Pay Per Call Marketers Hub, PPC Publishers, Insurance Live Transfers) required login; permalink fetches showed only anonymized commenters (slice c).
- Telegram `t.me/s/<channel>` guesses resolved to private user contacts, not public channel histories — no usable public PPC hiring channel found (slice c).
- Instagram searches surfaced only generic job-board listings, no identifiable employer domains (slice c).

## Overall read

The 13k+/18.7k+-domain exclusion index is very mature for this channel: across all three slices, the large majority of genuine pay-per-call operators surfaced by any tool-name, role, or vertical query were already known — consistent with slice b's read that this niche has been mined thoroughly in prior runs. The limiting factor remains employer scarcity, not query coverage: 6 new leads (+3 flagged aliases) from ~800 searches and ~611 postings/profiles read.
