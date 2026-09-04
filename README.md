# ppc-daily — daily pay-per-call lead sourcing for Kaliper

A bounded, self-contained daily pass of the pipeline that ran as `ppc-run2` (the 5-hour
run) through `ppc-run5` on 2026-09-02, restructured so a **Claude Code routine** in
Anthropic's cloud can run it every day with no access to the local machine.

What changed versus the archived runs, and why:

| archived runs | ppc-daily | why |
|---|---|---|
| 3–15 Claude subagents doing discovery via TinyFish MCP | `discovery.py` calls TinyFish's free **REST** search API and constructs domains directly | routines cannot use Claude Code MCP servers; scripts are also deterministic and resumable |
| `pipeline.py` + `v6_worker.py` + `watchdog.py` as long-running background processes | one `daily_run.py` with a wall-clock budget and per-item checkpoints | a cloud session is short-lived; the watchdog's kill/respawn logic killed run 3 |
| exclusion index rebuilt from `account_ledger.csv` (PII, gitignored in the outbound repo) | `state/known_domains.txt` — domain-only, committed, grows every run | the cloud cannot see the ledger; a domain list carries no PII |
| `append_to_ledger.py` at the end of each run | `local/sync_to_ledger.py`, run locally after `git pull` | only the local machine has the ledger |
| batches of 50, partial tail never classified (run-3 bug) | in-process qualifier, `state/pending_v6.jsonl` carries a cut-off tail to the next run | fixes the stranded-tail defect without a second script |

Unchanged on purpose: `ppclib.py` (verbatim from run 5), the crawl logic and Ringba drop,
and the v6 qualifier prompt + model config. Verdicts stay comparable to the ~13k in the ledger.

## Discovery channels (only the ones that measured alive)

- **Search** (`L4-counterparty`, `L4-vertical`, `L4-familyB`): long counterparty phrases
  paginated to the depth run 3 measured, Family A payout vocabulary, Family B onboarding
  vocabulary × the micro-operator vertical cluster. `state/search_progress.json` remembers
  the next page per query; a query retires after two dry pages. ~90 requests/day.
- **Probe** (`L7-probe`): `{vertical}calls.com`, `{vertical}leads.com`, hyphenated and
  alt-TLD variants over the call-brokerable vertical list. Run 4 measured ~67% net-new for
  this channel vs ~4% for search. `state/probed_domains.txt` guarantees no domain is ever
  fetched twice. Dead shapes from run 4 are deliberately not generated.

Expect the numbers to be small and honest: the market is largely enumerated. The value of a
daily cadence is catching new operators as they register and finishing the long tails.

## Layout
```
daily_run.py        orchestrator (run this)
discovery.py        search frontier + constructed-domain probes
crawl.py            free HTTP crawl, Ringba drop, parking detection
qualify.py          Kaliper v6 hard gate, gpt-4.1-mini (config frozen)
export.py           out/<date>/{qualified,qualified_icp_clean,rejected}.csv + report.md, out/ALL_qualified.csv
ppclib.py           shared library (verbatim from ppc-run5)
prompts/            v6 prompt + the audits/notes from runs 1–4
state/              known_domains.txt (exclusion index), probed_domains.txt,
                    search_progress.json, evaluated.jsonl, pending_v6.jsonl
local/              build_known_index.py, sync_to_ledger.py — run on the machine with the ledger
ROUTINE.md          how to wire this up as a daily routine
```

## Run locally
No dependencies (standard library only).
```
set OPENAI_API_KEY=...      # from relevince-outbound/.env
set TINYFISH_API_KEY=...    # optional; probing runs without it
python daily_run.py
```
Knobs: `RUN_MINUTES` (8, sized for the 10-minute cloud Bash cap), `SEARCH_BUDGET` (45),
`PROBE_BUDGET` (300), `CRAWL_WORKERS` (16). Locally you can raise all of them.

## After each cloud run, locally
```
git pull
python local/sync_to_ledger.py       # appends new verdicts to account_ledger.csv, backup first
```
