# Run 3 coordinator notes

## Setup deviations from the brief
- **watchdog.py NOT used.** Its `spawn()` calls `kill_all()` on startup, which killed the
  pipeline/v6 workers launched per §2 and adopted its own Popen children; the watchdog was then
  reaped and took its children with it (the wrapper-reaping trap in §7). All four processes died
  within ~3 min of launch. State was clean at that point (0 accepted domains, no state files
  written), so nothing was corrupted. Workers relaunched directly as their own background
  commands. Coordinator performs the watchdog role off a 10-min `pulse.py`.
- `tasklist` cannot see the worker processes from the sandboxed shell. Liveness is judged by
  log growth / pulse advancement, not process listing.
- Added `pulse.py` (new, run-3 only): compact funnel + qualify-rate-per-source, for the 10-min
  monitor. Does not touch any run-2 file.

## Open issue to report at the end: prose-level Ringba mentions
Ringba is a HARD PERMANENT exclusion. `pipeline.py:131` drops tenants on an **infrastructure
fingerprint** (`ringba.com`, `js.ringba`, `_rgba_tags` etc. in page markup — `ppclib.py:169`).
It does NOT catch a company that only *names* Ringba in prose. The very first candidate of the
run, servicecallpros.org, said: "Ringba access is sent only after your identity and traffic
information are approved" — strong evidence it runs Ringba, but invisible to a tag fingerprint
if its corporate pages don't load the script (run-2 audit §4: only 2 of 90 homepages carried any
call infra at all, because the corporate site is a brochure and the tags live on landers).

Deliberately NOT changing the check mid-run: it is a tested script and verdicts must stay
comparable to the 12,780 already in the ledger. Instead: scan the crawl cache for prose Ringba
mentions among v6-qualified leads at export time and report them for the user to decide.

## Defect found mid-run: partial batches never classified
`pipeline.py` `emit_batches()` emits only `while len(rows) >= BATCH_SIZE` (50), and the final
flush at `pipeline.py:211` uses the same rule. So a tail of <50 crawled companies is never
written to `batches/` and never reaches v6 — on a saturated run that tail can be a large share
of total yield (44 were stranded when this was spotted).

Fix: added `flush_partial.py` (new, additive). `pipeline.py` deliberately NOT modified — it is
a tested script and run-2 comparability matters. Must be run ONLY after pipeline.py exits,
because it rewrites `pending_batch.jsonl` which the live pipeline appends to. Guards against
re-batching any domain that already has a verdict or already sits in an emitted batch.
ENDGAME ORDER: stop pipeline -> flush_partial.py -> let v6 drain -> export2 -> report2 -> ledger.

## CORRECTED finding: pagination depth is LAYER-SPECIFIC, not uniformly exhausted
An earlier note here claimed deep pagination was falsified outright. Agent 1's data contradicts
that, so the corrected position is:

- **MARKETPLACE layer — depth is exhausted.** Across ~18 phrases: "most net-new hits landed on
  pages 0-1; pages 2-4 increasingly returned the same saturated set" repeating verbatim
  (exclusivelivecalls subpages, brokercalls blog posts, buythecalls vertical pages). Several
  phrases returned zero new domains ("inbound call network" 0 results; "sell call traffic" 1
  result, already known).
- **COUNTERPARTY layer — depth is ALIVE and is the only thing producing.** All 35 net-new in
  agent 1's second pass came from pagination, concentrated on pages 1-2, with genuine finds as
  deep as **page 5** (worldlinkenterprises.com, turtleleads.com, advancegro.ca, zyvoracalls.com
  all at page 5 of "become a publisher"). This is also the highest-converting layer (76.9%).

Conclusion for run 4: buy pagination depth on counterparty phrases; do not buy it on
marketplace phrases. The audit's blanket "depth is untouched" hypothesis is half right.

## Path-shape hunting produced ZERO net-new - coordinator called this wrong
The brief and the run-2 audit both weighted path-shape hunting heavily (fetch /publishers,
/buyers, /advertisers etc. on every known operator), and I pushed all three agents toward it.
Measured result: **0 net-new companies** from agent 1 across 40 URLs in two batches, and
404-heavy for agent 3 on 9 marketplace domains. Mechanism, per agent 1: buyer/advertiser pages
that DO resolve don't name specific counterparties, for competitive reasons. The run-2 audit
already recorded this as "marketplace peer traversal -> 3 domains, a structural limit, not an
effort problem" (audit s4) - the tactic was re-tried this run and the structural limit held.
It remains useful as CONFIRMATION that a company trades calls; it is not a discovery channel.

## (superseded) original pagination note
The run-2 audit hypothesised that because prior runs "mostly stayed on page 0", search pages
1-5 were untouched inventory. The marketplace agent tested this directly across ~18 phrases
and reported: **"Most net-new hits landed on pages 0-1; pages 2-4 increasingly returned the
same saturated set"** — repeating verbatim results (exclusivelivecalls subpages, brokercalls
blog posts, buythecalls vertical pages). Several phrases returned literally zero new domains
("inbound call network" 0 results; "sell call traffic" 1 result, already known).

So the depth hypothesis is falsified for this layer: search engines converge on the same
result set regardless of page depth for these narrow commercial phrases. Pagination is not the
lever run 4 should buy.

## Second structural finding: path-shape hunting is population-specific
`/publishers`-style paths 404 on most MARKETPLACE domains (9 confirmed misses: paypercallprogram,
calldrive, cortexleads, ridgerisemedia, firstbuzzmedia, livetransferexchange, ringlabmedia,
omnicallnetwork, servicedirect) while the same tactic is the top performer on the COUNTERPARTY
population (76.9%). Marketplaces don't expose guessable publisher paths the way networks do.

## All three agents defaulted to the exhausted directory/listicle shape
Unprompted, and each had to be corrected individually: agent 1 mined affpaying + offervault +
roundups ("highest-yield tactic"), agent 2 mined leadmaker/callatlas/mThink/paypercalldeals
("highest density per fetch"), agent 3 mined doppcall blog/AffTruster/Blognife ("very high
yield"). All three judged it productive because it returns 5-15 companies per fetch. It is
measured at 3.2-8.3% and is the direct cause of the ~87% dedupe kill. Any future run brief
should ban it in the strongest possible terms up front, per-agent.

## THE run-4 lever: phrase novelty beats page depth
Agent 2's second pass (131 -> 243) found the `"buy calls"` / `"sell calls"` / `"we buy calls for"`
/ publisher-signup phrase family at **page 0** outproduced deep pagination of familiar phrases:
~45 net-new domains in one angle, described as "an entire population of small dedicated
pay-per-call networks that never appear in roundup articles". Its own words: "page 0 was
actually the highest-yield once the phrase changed - not page depth alone."

Triangulating all three agents:
- new phrase family, page 0        -> best net-new yield (agent 2, ~45 domains)
- old phrase, deep pages           -> works on counterparty phrases to page 5 (agent 1, 35),
                                      dead on marketplace phrases past page 1 (agent 3)
- directories / listicles          -> near-zero net-new (all three agents, corrected)
- path-shape traversal             -> ZERO net-new (agent 1, 40 URLs)

So the binding constraint is PHRASE COVERAGE, not search depth and not effort. Run 4 should
spend its budget generating new phrase families (transaction/payout vocabulary, call-desk
operations vocabulary) rather than paginating known phrases or re-mining directories.

Note: the brief called `"we buy calls"` "100% noise as a query, a perfect on-site filter".
Used as a phrase family WITH the -options -stock -trading exclusions it was in fact the single
best net-new source of the run. Worth revising that guidance.

## append_to_ledger.py label fix (logic untouched)
The copied script hardcoded `SOURCE_RUN = 'ppc-run2-structural-sweep'`, the backup filename
suffix `pre-run2append`, and a "run2 accepted" progress line. Left as-is, every run-3 domain
would have been written into the shared file of record labelled as run 2's work, making it
impossible for a later run to attribute a domain to the run that sourced it. Changed the three
labels only: SOURCE_RUN -> 'ppc-run3-top3-methods'. The append/backup/abort logic is byte-
identical and was verified safe: backs up first, rewrites every existing row unchanged, aborts
on row-count mismatch and refuses to write if the ledger would not grow.

Note: it reads out/FINAL_people_contacts.csv and out/cache_mined_contacts_79.csv, which do not
exist in run 3 (this run has no contact-acquisition stage per the brief). rd() returns [] on
failure so it degrades gracefully - every appended row will be contact_status=no_contact_data,
which is correct for this run's scope.

## Phrase-family comparison (agent 2, controlled test) - the run-4 blueprint
All three families run from page 0 against the same micro-operator verticals:

| family | net-new | signal quality |
|---|---|---|
| **B - publisher-onboarding vocabulary** ("publisher portal", "publisher login", "publisher onboarding", "get approved", "media buyer application") | **8 - best** | Cleanest signal of the run. These pages exist purely to onboard traffic partners, so they are never in a roundup and search surfaces them on the vocabulary alone. |
| A - transaction/payout ("we buy calls", "we buy inbound calls", "paid per billable call", "call payouts") | 7 | Strong but noisy - "call buyers", "earn per call", "send us your calls" pull real-estate cold-calling and roadside-consumer noise. |
| C - call-desk operations ("billable duration", "scrub rate", "ping post", "concurrency", "call disposition") | 2 - weakest | Real operator language, but equally native to call-tracking VENDORS' content marketing (Ringba, Retreaver, CallMatrix) and generic call-centre KPI blogs. Use as a confirmatory on-site filter, NOT a mining source. |

Run-4 recommendation: lead with Family B crossed against the full vertical list. Family A
second with tighter negative keywords. Do not mine Family C standalone.

Also newly confirmed saturated: bail bonds and Medicare/final expense crossed with
"we buy calls" / "publisher sign up" returned ZERO results.

## Marginal-yield curve per agent pass (evidence of true exhaustion)
- agent 1 counterparty : 112 -> 147 (+35, pagination) -> pass 3 running
- agent 2 vertical     : 131 -> 243 (+112, new phrase family) -> 243 -> 260 (+17)
- agent 3 marketplace  : 35 -> 62 (+27) -> 62 -> 74 (+12), then STOPPED as exhausted
The +112 spike came from switching phrase family, not from more effort. Effort alone yields
+12 to +17 per pass. This is the clearest signal in the run: new vocabulary buys inventory,
more searching does not.

## Page-depth curve for counterparty phrases (agent 1, measured) - most reusable artifact
Last page with a genuine net-new find -> first dead page:

| phrase | died at page | note |
|---|---|---|
| `"become a publisher"` | 9 | genuine finds through page **7** (homeservprollc.site) |
| `"join our network"` | 6 | new finds through page **5** (directcallmedia.com, paypercall.agency, paypercall.net.au) |
| `"weekly payouts"` | **STILL ALIVE at 3** | page 3 still producing (callmint.net, fastmediaads.com, leadswitchmedia.com, nexegonllc.com) - NOT pushed to 4. Unexploited seam. |
| `"weekly payouts"`, `"apply as a publisher"`, `"publisher application"`, `"top payouts"`, `"our verticals"`, `"become a buyer"`, `"supply partners"`, `"publisher terms"` | 2-3 | die quickly |
| `"publishers wanted"`, `"live campaigns"`, `"call quality standards"` | 2 | dead |
| `"publisher FAQ"`, `"chargeback policy"`, `"request calls"` | 1 | 0 results, never worth pushing |

Rule extracted: **long, specific counterparty phrases sustain depth to page 5-7; short/generic
ones die by page 1-2.** Prior runs stopped at page 0 and left 5-7 pages of inventory on exactly
two phrases ("become a publisher", "join our network"). This is the concrete, reusable number
the audit's blanket "depth is untouched" claim was reaching for.

Reconciles the apparent contradiction with agent 3's marketplace result: depth is a function of
PHRASE SPECIFICITY, not of layer. Marketplace phrases ("call marketplace", "call exchange") are
short and generic -> die by page 1. Counterparty phrases are long and specific -> survive to 7.

## Family B does NOT scale with vertical breadth (agent 2, final pass: +5)
Tested directly. The original 8 net-new came from the micro-operator vertical cluster (auto
glass, towing, moving, foundation repair, final expense, personal injury, Medicare,
restoration). Sweeping the SAME vocabulary across ~25 further verticals (solar, HVAC, windows,
mold, biohazard, pest control, tree service, concrete, fencing, commercial insurance subtypes,
credit card processing, timeshare, alarm monitoring, janitorial, structured settlements, SBA/
equipment financing, GLP-1, dental implants, hearing tests, assisted living, medical alert)
returned almost nothing new.

Mechanism: Family B works only where a vertical has genuine micro-operator density - home
services long-tail and high-RPC insurance/legal. Verticals far from "a phone call is the
sellable unit" economics (GLP-1, dental, medical alert, janitorial, structured settlements)
never spawned dedicated small call networks, so there is nothing there to find.

Run-4 correction: Family B's lever is **phrase breadth within the proven vertical cluster**,
not vertical breadth. More onboarding-vocabulary variants against auto glass / towing / moving /
restoration / final expense / personal injury / Medicare. Do not sweep it across 60 verticals.

### New false-positive class worth adding to any future blocklist
`researchandmarkets.com` carries a generic "Publisher Sign Up / Publisher Portal" footer on
EVERY market-report page, so publisher-onboarding vocabulary matches it thousands of times.
Also polluting that vocabulary: government job listings with "become a publisher" ToS
boilerplate, academic pest-management papers, GLP-1 medical literature, and book-publishing
forums.

## Final marginal-yield curves (both agents ran to genuine exhaustion)
- agent 2 vertical     : +112 (new phrase family) -> +17 -> +5   STOPPED, exhausted
- agent 3 marketplace  : +27 -> +12                              STOPPED, exhausted
- agent 1 counterparty : +35 -> +31 -> final pass running        still producing steadily
Only the counterparty layer never showed a collapsing marginal curve.

## Do phrase x vertical crosses have independent page depth? (agent 1, final pass: +7)
Partial answer, honestly caveated by the agent as SAMPLED not exhausted.

**Yes, but it is vertical-dependent, not uniform:**
- Crosses on **under-served niche verticals** surface net-new operators the bare phrase never
  would, and they appear at **page 0** without needing depth: solar (trafficclan.com,
  instal-us.com), junk cars / cash for homes (towingleads.com, youcallwehaul.com), auto glass.
  Mechanism: these operators only rank once the search engine sees the vertical term.
- Crosses on **heavily-served verticals** return the same saturated set as the bare phrase and
  add nothing: mass tort, debt relief, roofing, towing all 100% already-known. Mechanism: pages
  that dominate the generic phrase also dominate the cross.
- medical alert: 0 results, dead on arrival.

**Still unanswered:** whether the PRODUCTIVE crosses (solar, auto glass, junk cars) have their
own multi-page tail. The agent ran page 0 only across ~10 representative verticals per phrase
rather than the full 48 x 2 x 5 = 480 searches, and did not have budget to paginate the
productive ones to page 5. This is the single highest-value open question for run 4: if
productive niche crosses DO have a 5-page tail, the addressable inventory is roughly 5x what
this run sampled.

Also this pass:
- `"weekly payouts"` floor confirmed: productive through page 3, **dies at page 4** (page 4 was
  100% job-board noise - Jooble, Glassdoor, Zippia).
- New phrase `"apply to become a publisher"` **productive** (popularmarketing.com,
  americanipmarketinginc.com). `"we are looking for publishers"` and `"now accepting
  publishers"` both dead (directory/forum noise; unrelated content-publishing platforms).
- Untested for lack of budget, carry to run 4: `"publisher application form"`, `"join our
  publisher network"`, `"apply for publisher access"`, `"looking for traffic partners"`,
  `"accepting new publishers"`, `"publisher payout terms"`, `"payout terms"` + calls.
- Quality: excluded baselinenetwork.com (fetched full terms, zero call/phone language, pure
  banner-ad network) and peddle.com (large single-business junk-car buyer, not a broker).

## LATENT BUG FOUND AND FIXED: append_to_ledger.py duplicated the file of record
First append run wrote **266 rows for 89 unique domains** into account_ledger.csv.

Cause: `accepted` was read from `state/seen_domains.txt` line-by-line with no dedupe, and that
file is append-only - a domain gets written once per pipeline instance that ingests it. With
concurrent/restarted pipelines it held 266 lines for 89 domains. The script's `skipped` guard
only tests membership in the PRE-EXISTING ledger (`have`), which is never updated as rows are
appended, so duplicates within its own input sail through. It also inflated the reported
qualified count to 131 (vs the true deduped 44).

Run 2 never hit this because it presumably ran a single pipeline instance, leaving
seen_domains.txt dupe-free. Latent, not new.

Recovery: the script backs up before writing, so `account_ledger.backup-2026-09-02-pre-
run3append.csv` held the clean 12,780 rows. Restored from it (verified 0 ppc-run3 rows present),
applied an order-preserving dedupe to `accepted`, re-ran.

Verified after fix: 12,780 -> 12,869 (+89); 12,869 rows / 12,869 unique domains; 0 duplicate
domains anywhere in the ledger; original 12,780 rows preserved in order; 89 ppc-run3 rows
(True=44, False=27, unresolved=18) matching the deduped funnel exactly.

**Carry to run 4:** every script that reads seen_domains.txt, crawled.jsonl or v6_results.jsonl
must dedupe by domain first. status.py, export2.py and pulse.py already did; append_to_ledger.py
did not. Also fixed this run: report2.py wrote out/run2_report.md (label only).
