# Run 4 coordinator notes

Continuation run. Exclusion index rebuilt from the ledger AFTER run 3's 89 appends:
**13,179 domains** (12,697 from account_ledger.csv + 415 Clay - Leads + 60 qualified export +
7 consolidated candidates). Verified +89 exactly vs run 3's 13,090.

Prerequisite check before starting: 385 of the 387 unique domains run-3 agents emitted are now
in the ledger; the other 2 (digitalmastermedia.com, o2gmediagroup.com) were already owned via
Clay - Leads / the qualified export, which is why the pipeline dropped them. Nothing was lost.

Scripts copied from ppc-run3 (NOT run2) so they carry run-3's fixes: the append_to_ledger
dedupe fix and correct run labels. watchdog.py deliberately not copied. ONE pipeline instance
and ONE v6 worker this time - run 3's duplicate-process problem does not recur.

## CRITICAL METHODOLOGICAL FINDING: agents systematically overstate net-new
Agents cannot see the exclusion index, so every "net-new find" they report is really "a company
I found", most of which the client already owns. Measured this run:

| agent's claim | agent's count | ACTUAL net-new |
|---|---|---|
| a1: `"pay per call" [vertical] publisher network sell calls` = "single highest-yield tactic" | 15 | **0 of 15** |
| a2: Family B phrase search = "highest-yield channel, 14 of 22 (~64%)" | 14 | **1 of 14** |
| a2: domain-pattern probing = "low hit rate ~2.2%, plateaus" | 8 | **3 of 8** |

**Agent 2's conclusion was exactly inverted.** On net-new, domain probing beat phrase search
3 to 1, at a fraction of the cost (fetch_content batches 10 URLs and is barely throttled;
search is capped ~30 req/min shared). Phrase search is very good at re-finding the most
findable operators in the market - which is exactly the set already in the ledger.

**Process rule for future runs: never accept an agent's own yield ranking. Score every channel
against the exclusion index before drawing a conclusion.** All figures I report come from the
pipeline's dedupe, never from agent self-reports.

## Run-3 open question ANSWERED: niche vertical crosses have no multi-page tail
Run 3 left this as the highest-value unknown (potential 5x inventory). Agent 1 tested it:
solar x "become a publisher" productive pages 0-1, **recycled/dead by page 2**; and the great
majority of niche verticals (junk cars, cash for homes, basement waterproofing, tree service,
bail bonds, timeshare exit, generator/EV charger, moving, dental implants, assisted living,
home care, hearing tests, biohazard, structured settlement, invoice/equipment financing, SBA,
credit card processing, contractor/trucking insurance, janitorial) were **dead at page 0**.
The 5x-inventory hypothesis is falsified. Do not re-test.

## NEW CHANNEL VALIDATED: domain-pattern probing
Rationale: micro-operators too small to rank in search still have self-describing domain names,
so the domain can be CONSTRUCTED rather than discovered. Cost is near-zero (10 URLs per
fetch_content call, barely throttled).

Measured by agent 2 across ~370 probes over 78 vertical tokens:
- base-4 suffixes (`{v}calls`, `{v}leads`, `{v}leadspro`, `{v}livetransfers`): ~16% resolve,
  ~3.4% confirm as call sellers. **The productive channel.**
- extended suffixes (`{v}transfers`, `{v}callspro`, `{v}leadnetwork`, `buy{v}calls`,
  `sell{v}calls`, `{v}callnetwork`): ~2% resolve, effectively zero real content across ~250
  probes. **Dead - do not run again.**
- fresh obscure vertical tokens (car wreck, DUI, bankruptcy, fire/smoke damage, duct cleaning,
  pool repair, junk removal): **zero** confirmed. Token space is saturated.

Conclusion: the lever is NAME-SHAPE variation on the verticals already proven to host call
operators, not more vertical tokens. Agent 2 redirected to hyphenated/prefixed/suffixed/TLD
variants on proven tokens.

## Tooling added this run
- `peek_batch.py` - emits an early batch so v6 verdicts flow mid-run. pipeline.py only emits at
  50 crawled companies, and on a saturated run net-new can stay under 50 for hours, leaving the
  coordinator with no qualify-rate signal. Reads pending_batch.jsonl READ-ONLY and never
  rewrites it, so it cannot race the live pipeline or drop a row; the pipeline later re-emits
  those rows and v6_worker skips domains it has already judged.
- `merge_qualified.py` - merges run-3 + run-4 qualified into one cumulative deliverable
  (out/ALL_qualified_leads.csv), per the client's request to append to the existing 44.

## DOMAIN PROBING VALIDATED HARD - the run-4 headline
Agent 1's corrected pass (phrase search -> domain probing) produced **5 of 6 net-new (83%)**,
against **0 of 15** from the phrase tactic it had self-rated as its "single highest-yield".

The right way to read the economics: probe-to-emit rate is only ~2.6%, but that is the wrong
denominator. Probes are nearly free (10 URLs per fetch_content call, barely throttled), and
**almost everything probing emits is net-new**, whereas phrase search emits plenty that is
already owned. Net-new per unit of cost, probing wins by an order of magnitude.

| channel | emits | net-new | net-new rate |
|---|---|---|---|
| a1 domain probing (corrected pass) | 6 | 5 | **83%** |
| a2 domain probing, base-4 suffixes | 8 | 3 | 38% |
| a3 standalone generic-brand probing | ~2 | 2 | ~100% (n tiny) |
| a1 phrase pattern "self-rated best" | 15 | 0 | **0%** |
| a2 Family B phrase search | 14 | 1 | 7% |
| a3 marketplace phrase search | ~19 | 1 | 5% |

### Sub-structure of the probing channel (measured)
WORKS:
- `{token}calls.com` and `{token}leads.com` - the two proven shapes
- standalone generic brand names (`callexchange.io`, `paypercallexchange.com`)
- **SHORT, natural tokens.** Every a1 winner was short: roadside, homeservice, injury, glass.
  Long compounds (windshieldrepair, structuredsettlements) mostly hit unregistered or parked
  domains. Real small businesses pick short brandable names.
DEAD:
- extended suffixes: `{v}transfers`, `{v}callspro`, `{v}leadnetwork`, `buy{v}calls`,
  `sell{v}calls`, `{v}callnetwork` (~2% resolve, zero content over ~250 probes)
- vertical-PREFIXED marketplace shapes (`sellmedicarecalls.com`, `finalexpensecallexchange.com`)
  - DNS failures, AWS placeholders, parking pages
- `{v}paypercall.com` - largely a single doorway farm (see below)
- fresh obscure vertical tokens (car wreck, DUI, bankruptcy, duct cleaning, pool repair) - zero

### Doorway-farm structure identified
The exclusivelivecalls family (one phone: 645-201-1868) has vertical-prefixed aliases -
`roofingpaypercall.com`, `finalexpensepaypercall.com`, `sellinboundcalls.com`,
`whitelabelpaypercall.com`, `paypercallmarketplace.org`, `paypercallsoftware.net`,
`bestpaypercallnetwork.com`, `buypaypercallleads.com`. Probing `{v}paypercall.com` mostly
rediscovers this one operator. All agents applied the one-emit-per-farm rule correctly.

### Discrimination worth preserving
Agents correctly rejected domains that resolve but sell the wrong thing: a direct-mail lead
vendor on movingleads.com, an email/CRM lead vendor on taxreliefleads.com, a single law firm on
personalinjurypartners.com, and an agency arguing against buying leads on autoglassleads.net.
A resolving domain is not a call seller.

## Generic-brand probing is DEAD - and it refines the probing rule
Agent 3 ran a clean controlled test: **71 standalone generic-brand names, 0 confirmed call
sellers.** 35 resolved (49%), of which 19 were parked/for-sale (HugeDomains, GoDaddy, Atom,
AWS placeholder) and 16 were real operating companies in the WRONG category.

| root family | probed | resolved | parked | confirmed |
|---|---|---|---|---|
| call- | 33 | 20 | 12 | 0 |
| paypercall- | 13 | 4 | 3 | 0 |
| ring-/dial- | 14 | 8 | 4 | 0 |
| transfer-/lead-hybrid | 11 | 3 | 2 | 0 |
| **total** | **71** | **35** | **19** | **0** |

Mechanism (agent 3's own reading, and it is convincing): short generic 2-morpheme
call/ring/dial compounds are overwhelmingly either **squatted by domainers for resale** or
**already claimed by unrelated SaaS/telecom brands**. The generic namespace is saturated by
everyone EXCEPT pay-per-call operators.

**THE REFINED RULE — this is the durable finding of run 4:**
- `{vertical-token}calls.com` / `{vertical-token}leads.com` **WORKS** (glasscalls, injurycalls,
  roadsidecalls, homeservicecalls, autoglasscalls, debtreliefleads, personalinjurycalls) —
  because that IS how a small vertical call operator names itself.
- `{generic-call-vocabulary}.com` **FAILS** (callexchange, callmarket, ringflow, dialsource) —
  domainer and SaaS territory.
The vertical word is what carries the signal, not the call word.

New blocklist entries (real companies, wrong category, surfaced by generic probing):
CallSource, Billable Calls, Ringflow, RingYield, Callroute, Callstream, Callbridge, Callflow
(Israeli queue-management), ExclusiveCalls (B2B outbound appointment-setting agency), CallFlow
Media (perf-marketing agency, no call-sale product), RingSource, RingRoute (Sur-Tec,
law-enforcement tech), RingTrade, TransferMarket.

## Doorway farm final size: 5+ confirmed domains, one phone (645-201-1868)
paypercallexchange.com, sellinboundcalls.com, whitelabelpaypercall.com,
paypercallmarketplace.org, paypercallpartners.com, plus the earlier-identified
exclusivelivecalls.com, paypercallsoftware.net, bestpaypercallnetwork.com,
buypaypercallleads.com, roofingpaypercall.com, finalexpensepaypercall.com. Probing
`{v}paypercall.com` or `paypercall{v}.com` mostly rediscovers this single operator.
One emit per farm was applied throughout.

## Agent 3 (marketplace) CLOSED at 21 finds / 3 net-new
Phrase channel spent (1 net-new from ~19 emits) and its new channel returned 0 from 71 probes.
Its own assessment agrees. Not resumed further.

## TOKEN-SPECIFICITY SWEET SPOT - corrects the "short tokens win" rule
I drew "short natural tokens win" from agent 1's first probing pass. Its next pass tested that
directly and **the rule is wrong on net-new**: short-token sweep produced only **1 of 5
net-new** (accidentleads.com), versus 5 of 6 the pass before.

Mechanism: short OBVIOUS single-word tokens are the most findable domains in the market, so
prior runs' phrase searches already surfaced them and the ledger already owns them. `legalcalls`,
`attorneyleads`, `homecalls`, `thelegalleads`, `hvac-leads`, `towingleads`, `medicareleads`,
`junkcarleads`, `roadsideleads`, `windshieldrepairleads` - all already owned.

**The real rule is MEDIUM specificity - two-morpheme compound VERTICAL tokens:**

| token shape | example | outcome |
|---|---|---|
| single generic word | legal, attorney, home | registered but ALREADY OWNED (too findable) |
| **two-morpheme vertical compound** | **autoglass, finalexpense, personalinjury, homeservice, debtrelief, roadside** | **NET-NEW - the sweet spot** |
| long compound / obscure | windshieldrepair, structuredsettlements, ductcleaning | unregistered or parked |

Net-new winners this run, nearly all two-morpheme vertical compounds: roadsidecalls,
homeservicecalls, injurycalls, glasscalls, autoglasscalls, debtreliefleads, personalinjurycalls,
finalexpense-calls, locksmith-leads, acaleads.io, finalexpenseleads.net, accidentleads.

Specific enough that search never surfaced it; common enough that a real operator registered it.

### Parking absorbs the short-token advantage
Agent 1's measurement: short tokens resolve ~29% vs much sparser for long compounds - but ~20
of those ~32 resolutions were domain-parking/resale pages (GoDaddy, HugeDomains, Atom,
Spaceship, DomainMarket, NameGarage). Squatters bought the short obviously-valuable names
first. So emittable rate only rose from ~2.6% to ~4.5%, not proportionally to resolve rate.
Actionable: prefer `.io`/`.co`/`.net` on tokens whose `.com` is squatted - that is where live
small-operator sites actually sit (confirmed by acaleads.io and finalexpenseleads.net).

### More excellent agent discrimination (a resolving domain is not a call seller)
Rejected: acaleads.com (self-described "high-volume bulk ACA web form provider" = data broker -
note agent 2 correctly EMITTED acaleads.io as a genuine live-transfer company; different firms),
settlementleads.com (email/SMS/CRM delivery, no calls), attorneycalls.com (PPC agency for single
firms, not a multi-buyer broker), septicleads/lawnleads/plumbcalls (single-client agencies, one
states "we don't sell leads"), roofcalls.com (call-tracking login portal), autotransportleads.net
(spun AI content farm, no business identity), directmovingleads.com (domain-flip disclaimer page).
Farm discipline held: mortgageleads.com identified as an Astoria Company alias and not
double-counted.

## I OVER-GENERALIZED THE TOKEN RULE - agent 1's pushback is correct
Agent 1's final pass (two-morpheme compounds on `.io` then `.net`) returned **1 net-new from
~70 probes (1.4%)**, worse than both its prior passes, and it argued - correctly - that the
"two-morpheme compound sweet spot" did not reproduce and that my 6-winner sample may be
survivorship bias rather than a generator. Taking that at face value.

**Where I went wrong:** I bundled two variables into one rule. The compound winners
(autoglasscalls.com, debtreliefleads.com, personalinjurycalls.com, homeservicecalls.com,
roadsidecalls.com, accidentleads.com) were all on **`.com`**. I then told agents to try
compounds on `.io`/`.net` first, generalizing from just two alt-TLD hits (acaleads.io,
finalexpenseleads.net). Agent 1's data shows compound verticals are largely UNREGISTERED on
`.io`/`.net` - they return `invalid_url`, not parking pages, because squatters bought up the
short `.com`s but never touched alt-TLD compounds.

**Honest state of the rule (small sample, ~16 net-new emits total across the run):**
- The ONE reproducible productive cell: `{compound-vertical}calls.com` / `{compound-vertical}leads.com`
  (hit by agent 2's first pass AND agent 1's second pass - two independent confirmations).
- Hyphenated `{v}-calls.com` / `{v}-leads.com`: productive, 3/102 (agent 2).
- Alt-TLD `.io`/`.net`: 2 hits total (acaleads.io, finalexpenseleads.net, + cashforcars.io) -
  real but NOT a reliable channel; registration density is sparse.
- Single generic words: high resolve, high already-owned. Long/obscure compounds: unregistered.
- Everything else measured dead: prefixed, suffixed, extended suffixes, generic call-vocabulary,
  vertical-prefixed marketplace shapes, `{v}paypercall`.

**Do not present the token-specificity rule as settled.** The defensible claim is narrower and
still valuable: *domain probing beats phrase search by roughly an order of magnitude on net-new
per unit cost, and the productive shape is a vertical word plus "calls"/"leads" on .com.*
Everything finer than that needs a larger sample.

## Agent 1 (counterparty) CLOSED at 80 finds
Pass-by-pass net-new: 7 (phrase, from 68 finds) -> 5 of 6 (probing) -> 1 of 5 (short tokens)
-> 1 of 70 (compounds on alt-TLD). Exhausted.

## Agent 2's closing refinement - the most useful version of the token rule
Final pass: 336 compound probes -> 1 net-new (0.30%); partial single-word pass 90 probes ->
1 net-new (1.1%). So **compounds did NOT outperform single words** - both are low, and both are
far below its earlier hyphenated/alt-TLD pass (5 from 448). This independently corroborates
agent 1's pushback. The token-specificity rule is NOT supported.

**What IS supported, and it is a better rule:** the productive zone is compounds naming a
vertical that genuinely sustains a per-call market - the high-RPC insurance/legal/aggregator
verticals Kaliper's client base already targets: **final expense, ACA, Medicare, personal
injury, attorney/legal, debt relief, home-service aggregation, auto glass, roadside, junk cars**.
Compounds built from generic service-repair morphemes produced NOTHING: **none of 40+**
(roofrepair, acrepair, furnacerepair, ductcleaning, sewerrepair, gutterinstall, sidinginstall,
windowreplacement, treeremoval, poolrepair, etc.) resolved to anything at all.

Mechanism: a per-call market only forms where the call is worth enough to broker. A roofing or
gutter lead isn't traded per-call by micro-networks; a Medicare, ACA, final-expense, mass-tort
or personal-injury call is. **So the vertical must be economically call-brokerable - that, not
token morphology, is the real selector.** This also explains why run 3's "long-tail home
services" verticals looked productive in phrase search but yielded so little net-new.

Also found: `autoinsuranceleads.net` shares a phone/template with the already-emitted
`finalexpenseleads.net`, and `homeservice-calls.com` is BunnyLeads - same operator as
`finalexpense-calls.com`, different vertical microsite. Multi-microsite operators are common in
this population; agents correctly emitted distinct registrable domains while noting the link.

## Agent 2 (vertical) CLOSED at 29 finds
Pass-by-pass net-new: 4 (from 22) -> 4 of 5 (name shapes) -> 2 (compounds + partial single word).

## ALL THREE AGENTS CLOSED. Run-4 discovery complete.
