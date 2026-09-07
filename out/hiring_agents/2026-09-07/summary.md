# Hiring agents run — 2026-09-07

Three parallel subagents (slices a/b/c) ran the depth-required hunt for pay-per-call
employers via hiring signals, per `agents/HIRING_AGENTS.md`. All three exceeded the
45-minute / 80-search floor.

## Per-slice tallies

| Slice | Source | Duration | Searches | Postings/profiles read | Employers evaluated | Already known | Emitted (raw) |
|---|---|---|---|---|---|---|---|
| a | OnlineJobs.ph / gig & freelance boards | ~44 min | ~400+ | ~35 fetched (46 seen-log lines) | 8 | 6 | 2 |
| b | bebee.com + LinkedIn (US/UK/CA) | 45.35 min | 261 | 92 | ~70 | 20 | 2 |
| c | Offshore LinkedIn geos + social (FB/IG/Telegram) | ~43.5 min | ~353 | 126 | many | 39 | 2 |
| **Total** | | | **~1014+** | **~253 logged in seen ledger** | | **65+** | **6 raw → 4 after alias dedupe** |

## Merge/dedupe result

6 candidates were emitted by the three agents. `python tools/tf.py known` marked all 6
domains themselves `NEW`, but 2 were aliases of already-**KNOWN** companies and were
dropped from the inbox per the alias rule:

- **legalrepp.com** — alias of known **mvaresolve.com**. Same founder/CEO (Brian
  Muthuyia) runs both; LegalRepp is a second personal-injury/auto-accident intake site
  under the same operation.
- **clientbridgeservices.com** — alias of known **truecaremarketing.com**. Explicitly
  "operated by TrueCare Marketing LLC" per the posting; a second-brand personal-injury
  lead/call marketplace for the same known company.

## Emitted — 4 new employers → `state/inbox/hiring_agents_2026-09-07.jsonl`

1. **callsignal.app** — CallSignal. Pay-per-call marketplace connecting Nashville
   homeowners with local pest control companies ("pay only when the call is real").
   Source: US-based cold-caller ad on freelancer.com.
2. **clickrush.com** — Clickrush Marketing. Runs Call-Only Google Ads campaigns
   delivering exclusive inbound pay-per-call leads to insurance agents nationwide;
   tracked via Ringba, per-call pricing. Source: Media Buyer ad on OnlineJobs.ph.
3. **pipeproof.com** — Proof Response Group (PipeProof / The FVG), Winnipeg MB Canada.
   "Finding call sellers and call buyers... coordinating DID, Ringba, and GHL setup"
   across restoration/plumbing/HVAC. Source: LinkedIn (rw.linkedin.com) posting.
4. **upon.media** — Upon Media, LLC, New York City. Founder previously Sr. Director of
   Pay Per Call at Madrivo and Digital Media Solutions, now building his own pay-per-call
   network. Source: LinkedIn founder profile.

## What worked

- Unrestricted (no `site:`) phrase searches like `"we are hiring" "call buyers"` and
  `"pay per call" "we're growing"` (slice b) surfaced real named companies that
  site-restricted bebee/LinkedIn queries missed.
- Facebook groups (Pay Per Call Marketers Hub, leadszee, cbpaypercallglobal) and
  Instagram were the highest-yield channels in slice c — anonymous "publisher wanted"
  posts often named a real LLC once fetched in full.
- Direct-quote patterns (`"we run pay-per-call"`, `"call marketplace"`, `"pay per call
  network"`) plus vertical+role combos were slice a's only genuine hits; generic
  tool-name x board queries mostly returned freelancer self-promotion.
- Founder/CEO LinkedIn profiles were a reliable way to surface a person's *other*
  domains (both alias findings came this way).

## What was blocked

- Upwork `/freelance-jobs/apply/...` detail pages consistently `bot_blocked` on fetch
  (slice a) — several promising leads (a Retreaver insurance-routing job, an
  affiliate/publisher ops role) could not be resolved to a company and were skipped
  rather than fabricated.
- `linkedin.com/company/...` pages `bot_blocked` on fetch (slice b); company HQ had to
  be triangulated via secondary search snippets instead.
- ~18 bebee URLs returned a generic render error on repeated fetch (slice b, mostly
  MCA postings — low value anyway).
- Several LinkedIn profile fetches `bot_blocked` in slice c; a few vendor domains were
  unreachable/invalid and skipped rather than fabricated (agentcalls.com — wrong domain,
  actual is .io; caseacq.com; leadsyncro.com; profyads.com).

## Notable pattern flagged (not emitted, watch list)

Slice c found a recurring cluster of Pakistan/Bangladesh-founder-operated "pay-per-call
LLCs" claiming to serve the US market but HQ'd offshore (P1 Lead Network, Tele Leads
Communication/Aero Healthcare, Zero-X Advertising, The Pay Per Calls Company, Lead
Syncro, Nextstar Insurance LLC, Teleza Marketing, HomeServ Pro LLC) — skipped per the
US/UK/Canada rule, logged in the seen ledger for visibility.

One strong ICP match, "Customers Direct" (national home-services live-transfer
network), was skipped only because its domain (customersdirect.com) is parked/for sale
— worth a human look if the real site can be found.

## Ledger

- `state/inbox/hiring_agents_2026-09-07.jsonl` — 4 new candidates for the next
  pipeline session to crawl and v6-score.
- `state/hiring_agent_seen.jsonl` — folded, now 405 lines total (was 141 before this
  run; +264 postings/profiles logged across the three slices, deduped per-slice files
  deleted).
