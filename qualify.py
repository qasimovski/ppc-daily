# -*- coding: utf-8 -*-
"""Kaliper's own v6 hard-gate qualifier, run over crawled text. Config is the documented
runner config from clients/kaliper/PROMPTS.md and must not change - every verdict has to
stay comparable to the ~13k already in the account ledger:
    gpt-4.1-mini, max_tokens=600, temperature=0, content truncated to 5,000 chars.
Lifted from ppc-run2..5/v6_worker.py; only the I/O shape changed (in-process function
with a thread pool instead of a batch-file watcher).
"""
import concurrent.futures as cf, io, json, os, re, time

ROOT = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(ROOT, 'prompts', 'company_pass2_qualifier_v6_hardgate.txt')

MODEL = 'gpt-4.1-mini'
MAX_OUTPUT_TOKENS = 600
TEMPERATURE = 0
MAX_CONTENT_CHARS = 5000
WORKERS = int(os.environ.get('V6_WORKERS', '6'))

_PROMPT = io.open(PROMPT_PATH, encoding='utf-8').read()

def _client():
    from openai import OpenAI
    key = os.environ.get('OPENAI_API_KEY', '')
    if not key:
        raise RuntimeError('OPENAI_API_KEY not set - the v6 qualifier cannot run')
    return OpenAI(api_key=key)

def classify(client, name, content):
    user = 'Company: %s\n\nWebsite content:\n%s' % (name, (content or '')[:MAX_CONTENT_CHARS])
    for attempt in range(3):
        try:
            r = client.chat.completions.create(
                model=MODEL, max_tokens=MAX_OUTPUT_TOKENS, temperature=TEMPERATURE,
                messages=[{'role': 'system', 'content': _PROMPT},
                          {'role': 'user', 'content': user}])
            txt = (r.choices[0].message.content or '').strip()
            txt = re.sub(r'^```(?:json)?|```$', '', txt, flags=re.M).strip()
            try: return json.loads(txt), None
            except Exception:
                m = re.search(r'\{.*\}', txt, re.S)
                if m:
                    try: return json.loads(m.group(0)), None
                    except Exception: pass
                return None, 'parse_error'
        except Exception as e:
            if attempt == 2: return None, type(e).__name__ + ':' + str(e)[:120]
            time.sleep(2 * (attempt + 1))
    return None, 'unknown'

def qualify_many(rows, deadline, on_result, log=print):
    """rows: crawled records with status=='ok'. Calls on_result(record) per company as
    verdicts arrive so a cut-off run still leaves every finished verdict on disk."""
    if not rows: return 0
    client = _client()
    done = 0
    def work(r):
        res, err = classify(client, r.get('company_name') or r['domain'], r.get('text', ''))
        rec = {k: v for k, v in r.items() if k != 'text'}
        rec['ts'] = int(time.time()); rec['error'] = err
        if res: rec['v6'] = res
        return rec
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(work, r) for r in rows]
        for fut in cf.as_completed(futs):
            try: rec = fut.result()
            except Exception as e:
                log('[v6] worker error %s' % e); continue
            on_result(rec); done += 1
            if time.time() > deadline:
                log('[v6] time budget reached with %d/%d classified; rest carried to next run'
                    % (done, len(rows)))
                for f in futs: f.cancel()
                break
    return done
