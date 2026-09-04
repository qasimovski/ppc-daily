# Pay-Per-Call Sourcing — Audit of Runs 1 & 2

Written 2026-09-02. Every figure is deduped by registrable domain. Where a number is
small-n and therefore untrustworthy, it says so.

---

## 1. The funnel, end to end

| stage | run 1 | run 2 |
|---|---|---|
| Raw candidate lines from discovery agents | ~3,500 | 3,794 |
| **Killed by dedupe against the ledger** | n/a (reconciled after) | **2,825 (74%)** |
| Accepted as net-new | 856 | 969 |
| Crawled (free plain HTTP) | 856 | 969 |
| Judged | 856 (own gate) | 777 (Kaliper v6) |
| **Passed** | 173 (own gate, 20%) | **92 v6-qualified (11.8%)** |
| In Kaliper's US/UK/CA geography | 143 | 88 |
| Named contacts found | 10 | 23 |
| **Contacts with a verified phone** | 0 | **15** |
| Pushed to Attio | 2 company lines | **15 people + 2 lines** |

Ledger: **11,811 → 12,780 rows**. All 969 run-2 domains appended with verdict, reason,
fit score and contact status, so none can be re-sourced.

**The single biggest lever was the dedupe gate.** Moving the full 11,811-row ledger *into*
the pipeline as a pre-filter — rather than discovering first and reconciling afterwards —
is what fixed the original complaint that "very few survive v6". It killed 74% of finds
before they cost a crawl or a model call.

---

## 2. Which sources actually qualify — run 2, scored by Kaliper's own v6

| source | domains seen | v6 qualified | rate | verdict |
|---|---|---|---|---|
| L4-marketplace phrases | 4 | 4 | 100.0% | promising, **n too small to trust** |
| **L4-counterparty pages** | 11 | 9 | **81.8%** | **best real method — starved of volume** |
| **L4-vertical × phrase** | 173 | 53 | **30.6%** | **the workhorse: 58% of all wins** |
| L4-geo-granular (US metro) | 4 | 1 | 25.0% | untested at scale |
| L5-hiring signals | 17 | 2 | 11.8% | modest |
| L4-UK "hotkeys" jargon | 29 | 3 | 10.3% | real but thin |
| L2-directory profiles | 12 | 1 | 8.3% | exhausted |
| L4-geo-ops (UK/CA + ops vocab) | 185 | 13 | 7.0% | high volume, poor rate |
| L4-listicle mining | 62 | 2 | 3.2% | **exhausted — was run 1's best technique** |
| L1-platform tenants | 133 | 3 | 2.3% | **dead** |
| L4-GDPR disclosure lists | 146 | 1 | 0.7% | **worst idea of the run** |
| **TOTAL** | **777** | **92** | **11.8%** | |

### Where the 92 wins actually came from
- vertical × phrase — **53 (58%)**
- geo-ops — 13 (14%)
- counterparty pages — 9 (10%)
- marketplace phrases — 4; platform tenants — 3; UK jargon — 3
- hiring — 2; listicles — 2; everything else — 1 each

**Two sources produced 72% of all qualified leads.** Six sources produced 14 between them
across 604 domains.

---

## 3. What worked, and why

**Counterparty-page hunting (81.8%).** Search for the *page*, not the company: a live
"become a publisher" / "publisher payouts" / "publisher agreement" page means the company
transacts in calls almost by definition — which is exactly what v6 gates on. It only saw 11
domains because it launched late in the run. **This is the headline finding.**

**Vertical × exact phrase (30.6%).** Unglamorous and reliable. Crossing a Tier-1 phrase with
a specific vertical scales linearly with effort and never went dry.

**Putting the ledger in the pipeline.** See §1.

**Mining our own crawl cache (free).** Because the crawler kept every page, phone numbers,
emails, LinkedIn pages and owner names were extracted afterwards at zero cost — 27 phones and
51 emails across 79 companies, beating every paid vendor on that batch.

**Searching Clay by legal entity, not brand domain.** Clay held company records for only 22%
of these micro-brands, so domain-keyed people search found almost nothing. Extracting the
*operating entity* from the site's own footer/legal pages and searching that name returned
people immediately — 7 verified contacts, including all three Intelsio decision-makers.

---

## 4. What didn't work, and why

**Platform-tenant enumeration (2.3%).** Run 1's leading hypothesis. Finding TrackDrive /
Retreaver / Phonexa tenants surfaces software *users* — mostly agencies, end advertisers and
tool vendors — not call sellers. 133 domains, 3 wins.

**GDPR / RIDTPPA partner-list mining (0.7%).** Legally-mandated disclosure lists genuinely
exist and are long (one held 200+ names), but they enumerate *insurance carriers, adtech and
compliance vendors* — the demand side and the plumbing, not call sellers. 146 domains, 1 win.
Excellent volume, near-zero relevance.

**Listicle mining (3.2%).** Was the best technique in run 1 and is now exhausted: every
"best pay-per-call networks" article names the same ~30 operators, all long since in the ledger.

**Marketplace peer traversal.** Fetching `/publishers`, `/partners`, "trusted by" pages across
~25 confirmed marketplaces produced **3 domains**. Those pages name end advertisers and software
vendors, not peer networks. A structural limit, not an effort problem.

**Graph traversal past hop 1 (run 1).** Precision collapsed: hop 1 = 24%, hop 2 = 8%, hop 3 = 2.3%.
Run 1's contingency said to raise the hop cap to 4 if the frontier emptied; the data said the
opposite, so it wasn't done.

**Infrastructure fingerprinting (run 1, 0 wins).** A pay-per-call company's corporate site is a
brochure — Ringba and Retreaver tags live on landers the corporate site never links to. Only 2 of
90 seed homepages carried any call infrastructure. Dynamic-number-insertion testing agreed:
8 rotating numbers out of 412 domains.

**Buy-side hunting by vertical identity (run 1, 1.3%).** Looking for insurance agencies and law
firms with a buried affiliate page. An affiliate program is not a call desk, and v6 agrees.

---

## 5. Why v6 rejected 685 companies — and the 412-company opportunity

| reason | count |
|---|---|
| **lead_or_appointment_pricing** | **412** |
| seo_or_ranking_agency | 78 |
| unrelated | 64 |
| end_advertiser | 58 |
| service_to_call_receiver | 41 |
| no_clear_signal | 18 |
| software_or_crm | 6 |
| directory_or_content | 5 |
| recruiting | 3 |

**60% of all rejections are a single reason: they sell leads or appointments, not calls.**

Those 412 companies are already discovered, already crawled, already classified and already in
the ledger. If the pay-per-lead adjacent segment is ever reopened — the work-log shows Jake
reopened it once as `v8_tier3widen` — **that is 412 companies available for the cost of one
re-classification pass and zero new discovery.** It is by far the largest untapped asset here.

---

## 6. Contact acquisition — the part that nearly failed

Discovery was never the bottleneck. Contact data was.

| method | result |
|---|---|
| AI Ark, people by domain | 7 contacts at **6 of 88** companies (7%) |
| Clay people search **by domain** | 4 people at 3 of 82 — Clay held company records for only **18 of 82 (22%)** |
| Clay people search **by legal entity name** | 13 raw → **7 verified** |
| Apify company→employees ($0.19) | 15 profiles at 3 of 9; 6 leadership; **1** in geo |
| Deepline `quickenrich` (**free**) | 11 people at 3 of 25; **1** leadership |
| **Own crawl cache (free)** | **27 phones, 51 emails, 12 LinkedIn pages, 5 owner names** |

### The decisive finding: LeadMagic's hit rate is set by where the LinkedIn URL came from

| URL source | LeadMagic match rate |
|---|---|
| **Clay vanity URLs** | **11 / 15 (73%)** |
| Deepline vanity URL | 1 / 1 (100%, n=1) |
| AI Ark vanity URLs | 3 / 9 (33%) |
| Apify obfuscated URNs (`/in/ACwAA…`) | **0 / 1** |
| No URL at all | 0 / 13 — nothing to match on |

I concluded too early that LeadMagic "couldn't work this population". It could. **The match key
was the bottleneck, not the data.** Clay returns clean vanity URLs; Apify returns unresolvable
URNs; AI Ark's coverage is simply thin.

**The chain that works: Clay (LinkedIn URL) → LeadMagic (mobile) → Trestle (validate).**

### Validation
14 of 14 US mobiles scored **100/100** on Trestle and were real carrier lines (Verizon /
T-Mobile / AT&T). By contrast 2 of 4 company lines scored 30 and were NonFixedVOIP. Mobiles pass;
VOIP company lines are where dead numbers cluster. That also supplies the control-group evidence
the Trestle skill flagged as missing — its precision holds, it isn't marking everything low.

---

## 7. Cost

| item | spend |
|---|---|
| v6 classification (777 companies, gpt-4.1-mini) | ~$0.50 |
| Own crawler (969 domains, ~9,500 pages) | **$0 — plain HTTP** |
| spider.cloud | 16.71 credits (one 4-domain job) |
| AI Ark find-people (88 companies) | 88 credits |
| AI Ark mobile finder | 0 (misses aren't billed) |
| LeadMagic (75 credits, 15 matches) | 75 credits |
| Apify LinkedIn employees | $0.185 |
| Trestle (14 numbers) | ~$0.21 |
| Deepline | $0 — free tool; paid tools blocked, workspace at 0 credits |

The expensive part of this pipeline is scraping, and it was avoided entirely by using our own
crawler and re-reading its cache.

---

## 8. What to do differently next time

1. **Lead with counterparty-page hunting, at scale.** 81.8% and it only got 11 domains. Give it
   two agents from minute one: counterparty phrases × 60 verticals × US/UK/CA, paginated deep.
2. **Keep vertical × phrase as the volume engine.** 58% of all wins. Never went dry.
3. **Drop four sources outright:** platform tenants (2.3%), GDPR disclosure lists (0.7%),
   listicle mining (3.2%), peer traversal (3 domains). Between them: 341 domains, 6 wins.
4. **Reopen the 412 `lead_or_appointment_pricing` companies** before doing any new discovery.
   Largest available pool, zero discovery cost.
5. **Make contact acquisition a first-class stage, not an afterthought.** Budget it as:
   parent-entity extraction → Clay by legal name → LeadMagic → Trestle. Roughly $0.02/contact.
6. **Never search Clay by brand domain for micro-companies.** 22% company coverage. Always
   extract the legal entity from the site's own footer/legal pages first.
7. **Always keep the crawl cache.** Every free contact win came from re-reading it.
8. **Expect saturation.** The exclusion index is now 12,780 domains. The last three agents of
   run 2 returned **0 net-new from 232 finds**. Roughly 90–100 v6-qualified per run is the
   ceiling on current sources; more searching will not move it.
9. **Fix two tooling gaps:** `validate-phone-trestle` silently drops non-NANP numbers (a valid UK
   mobile was skipped, not failed); and Deepline's paid tools need a credit top-up — its
   `enformion_contact_enrich` ($0.168) is explicitly built for "SMB owners with no LinkedIn or
   B2B presence", which is precisely the population that defeated every other vendor.

## 9. Things to be careful about

- **`clay.filter_to_companies` vs `experiences.any(company.domain…)`** — the docs prefer the
  former; tested, both return identical results. Not the cause of low yield.
- **Clay's people search returns no LinkedIn URL** — it comes from the enrichment/table layer, not
  the CLI search. That cost time to discover.
- **A company's own `/publishers` page can be a JS shell** — 25 verified companies had a real
  counterparty page whose text wasn't extractable; the URL alone was the evidence.
- **Same-name companies are a live risk.** "Apex Alliance" resolved to a hotel group in Bucharest;
  three separate firms share "Rapid Response Marketing". One contact (Kevin De Vincenzi) is still
  held back from Attio for this reason.
- **Phone junk classes worth filtering:** `555` reserved exchange, toll-free, shared switchboards,
  and template placeholders like `123456789` left in site markup.
