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
  a few dev domains; the crawler fetches arbitrary company websites. Under Trusted, every
  HTTPS connection (including api.openai.com) is refused by the proxy with
  `CONNECT tunnel failed, response 403`, and `daily_run.py` aborts on its network preflight.
- **The two keys.** Either form works; the scripts detect which one is in use.
  - *Environment variables* (simplest): in the **Environment variables** box add
    ```
    OPENAI_API_KEY=sk-...
    TINYFISH_API_KEY=sk-tin-...
    ```
    `OPENAI_API_KEY` is the same key as `relevince-outbound/.env`; the TinyFish key is at
    https://agent.tinyfish.ai/api-keys (Search + Fetch are free).
  - *API credentials* (Pro/Max only; the key is attached by Anthropic's proxy and never
    visible to the session). Add two credentials on the existing environment:
    | Name | Allowed websites | Header name | Prefix | Value |
    |---|---|---|---|---|
    | OpenAI | `api.openai.com` | `Authorization` | `Bearer` | the OpenAI key |
    | TinyFish | `api.search.tinyfish.ai` | `X-API-Key` | *(clear it)* | the TinyFish key |
- **Click Save changes.** The first test run found neither the network change nor the keys
  applied — check the environment dialog shows **Full** and the two entries before re-running.
- **Setup script: leave it EMPTY.** The job has no dependencies (standard library only). A
  setup script runs before the repository is checked out, so `pip install -r requirements.txt`
  there fails with "No such file" and the session never starts.

**Verify from a cloud session**: ask it to run `curl -sS -o /dev/null -w '%{http_code}' https://example.com`
(expect `200`) and `python daily_run.py` prints `[net] outbound HTTP ok`,
`[search] preflight: ok (...)` and `[v6] preflight: ok (...)`.

## 3. The routine itself
Create it with `/schedule` (or paste the JSON below via `RemoteTrigger create`).

| field | value |
|---|---|
| name | `ppc-daily sourcing (Kaliper)` |
| schedule | daily. Suggested `0 1 * * *` = 01:00 UTC = **06:00 Asia/Karachi** |
| repo | `https://github.com/qasimovski/ppc-daily` |
| model | `claude-sonnet-5` (coordinator only; the judgment is in the scripts) |
| tools | `Bash`, `Read`, `Glob`, `Grep` (no `Write`/`Edit` — the agent must not modify scripts) |
| connectors | none |

**Prompt** (the repo's `CLAUDE.md` is loaded automatically and carries the rules):

```
Run today's pay-per-call sourcing for Kaliper exactly as CLAUDE.md describes: up to 4
passes. Each pass = `python daily_run.py` in the foreground (no dependencies to install),
then `cat state/last_pass.json`, then `git add -A state out`, commit as "daily run <today>
pass <k>: <qualified_this_pass> qualified (today <qualified_today>, cumulative
<cumulative_qualified>)" and push to origin main (pull --rebase and retry once if
rejected). Stop after a pass whose last_pass.json has "nothing_left_to_do": true. Never
run daily_run.py in the background and never skip the commit between passes. Do not edit
any script, prompt or state file by hand. If daily_run.py aborts (exclusion-index size
check, or 'outbound HTTP is blocked'), or a preflight reports the search or v6 API
unusable, stop, commit nothing further, and report the message verbatim. Finish with:
passes run and why you stopped, qualified today / ICP-clean / cumulative, the funnel
numbers from out/<today>/report.md, the qualify rate per channel, anything that failed,
and the last pushed commit hash.
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
        "sources": [{"git_repository": {"url": "https://github.com/qasimovski/ppc-daily"}}],
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
- TinyFish Search: free (45 requests, ~1.7 min at the 30/min ceiling).
- OpenAI gpt-4.1-mini: a fraction of a cent per classified company; typically < $0.10/day.
- Wall clock: `RUN_MINUTES=8` default, because a single Bash command in a cloud session is
  capped at 10 minutes. The run checkpoints per item and carries unfinished v6 work forward,
  so a cut-off never loses verdicts. Do not raise `RUN_MINUTES` above 9 for the routine.

## Weekly, locally
```
git pull
python local/sync_to_ledger.py
```
appends the week's verdicts to the account ledger (backup first, append-only, deduped).
