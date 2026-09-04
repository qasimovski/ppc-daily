# Wiring ppc-daily up as a daily Claude Code routine

Routines run in Anthropic's cloud: a fresh VM, a fresh clone of a GitHub repo, no access to
this machine, no Claude Code MCP servers. Three things have to be true before the first run.

## 1. This folder is a GitHub repo the routine can clone AND push to
Persistence between days is `git push`. Every run appends to `state/` and writes `out/<date>/`,
then commits and pushes to `main`. If the push cannot land, tomorrow's run starts from
yesterday's state and re-sources the same companies.

- Create a **private** repo (suggested name `ppc-daily`) under your GitHub account and push
  this folder to it. Do **not** put it inside `relevince-outbound` — that repo's rules forbid
  lead data and unrequested commits, and its `.gitignore` would swallow `state/*.jsonl`.
- No branch protection on `main`, or the routine's push is rejected.
- The Claude GitHub app must have **write** access to the repo (it is granted when you connect
  the repo in the routine form).

## 2. The cloud environment can reach the open web and holds the two keys
Environment: **Default** (`env_01SGYcgc4ieBHEuBJwXEJxAH`) — created for you today; edit it
at https://claude.ai/code → environment settings.

- **Network access → Full.** The Default "Trusted" policy allows only package registries and
  a few dev domains; the crawler fetches arbitrary company websites and would fail every
  request with `403 host_not_allowed`.
- **Environment variables / API credentials:**
  - `OPENAI_API_KEY` — the same key as `relevince-outbound/.env` (v6 qualifier, gpt-4.1-mini)
  - `TINYFISH_API_KEY` — from https://agent.tinyfish.ai/api-keys (Search + Fetch are free)
  On Pro/Max, store them under *API credentials* rather than plain variables.
- **Setup script** (optional, cached): `pip install -r requirements.txt`

## 3. The routine itself
Create it with `/schedule` (or paste the JSON below via `RemoteTrigger create`).

| field | value |
|---|---|
| name | `ppc-daily sourcing (Kaliper)` |
| schedule | daily. Suggested `0 1 * * *` = 01:00 UTC = **06:00 Asia/Karachi** |
| repo | `https://github.com/<you>/ppc-daily` |
| model | `claude-sonnet-5` (coordinator only; the judgment is in the scripts) |
| tools | `Bash`, `Read`, `Glob`, `Grep` (no `Write`/`Edit` — the agent must not modify scripts) |
| connectors | none |

**Prompt** (the repo's `CLAUDE.md` is loaded automatically and carries the rules):

```
Run today's pay-per-call sourcing pass for Kaliper exactly as CLAUDE.md describes:
`pip install -q -r requirements.txt`, then `python daily_run.py`, then read
out/<today>/report.md, then `git add -A state out`, commit as
"daily run <today>: <N> qualified (<M> icp-clean)" and push to origin main
(pull --rebase and retry once if rejected). Do not edit any script, prompt or state
file by hand. If daily_run.py aborts on the exclusion-index size check, or every crawl
fails with 403 host_not_allowed, or a key is missing, stop and report that verbatim.
Finish with: qualified today / ICP-clean / cumulative, the funnel numbers, the qualify
rate per channel, anything that failed, and the pushed commit hash.
```

**Create body** (fill in `<you>` and a fresh lowercase v4 UUID):

```json
{
  "name": "ppc-daily sourcing (Kaliper)",
  "cron_expression": "0 1 * * *",
  "enabled": true,
  "job_config": {
    "ccr": {
      "environment_id": "env_01SGYcgc4ieBHEuBJwXEJxAH",
      "session_context": {
        "model": "claude-sonnet-5",
        "sources": [{"git_repository": {"url": "https://github.com/<you>/ppc-daily"}}],
        "allowed_tools": ["Bash", "Read", "Glob", "Grep"]
      },
      "events": [{"data": {
        "uuid": "<uuid>",
        "session_id": "",
        "type": "user",
        "parent_tool_use_id": null,
        "message": {"role": "user", "content": "<the prompt above>"}
      }}]
    }
  }
}
```

## Budget per run
- TinyFish Search: free (90 requests, 3.5 min at the 30/min ceiling).
- OpenAI gpt-4.1-mini: a fraction of a cent per classified company; typically < $0.10/day.
- Wall clock: `RUN_MINUTES=75` default. Lower it via an environment variable if cloud
  sessions are capped shorter; the run checkpoints and carries unfinished work forward.

## Weekly, locally
```
git pull
python local/sync_to_ledger.py
```
appends the week's verdicts to the account ledger (backup first, append-only, deduped).
