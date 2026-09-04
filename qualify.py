# -*- coding: utf-8 -*-
"""Kaliper's own v6 hard-gate qualifier, run over crawled text. Config is the documented
runner config from clients/kaliper/PROMPTS.md and must not change - every verdict has to
stay comparable to the ~13k already in the account ledger:
    gpt-4.1-mini, max_tokens=600, temperature=0, content truncated to 5,000 chars.
Lifted from ppc-run2..5/v6_worker.py; only the I/O shape changed (in-process function
with a thread pool instead of a batch-file watcher).

Transport is a raw HTTPS POST rather than the openai SDK so the request works under BOTH
ways a Claude Code cloud environment can hold the key:
  - OPENAI_API_KEY as an environment variable  -> we send Authorization: Bearer <key>
  - an "API credential" for host api.openai.com -> Anthropic's agent proxy attaches the
    header after the request leaves the VM; the key is never visible to this process, so
    we send NO Authorization header and let the proxy add it.
"""
import concurrent.futures as cf, io, json, os, re, ssl, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(ROOT, 'prompts', 'company_pass2_qualifier_v6_hardgate.txt')

MODEL = 'gpt-4.1-mini'
MAX_OUTPUT_TOKENS = 600
TEMPERATURE = 0
MAX_CONTENT_CHARS = 5000
WORKERS = int(os.environ.get('V6_WORKERS', '6'))
ENDPOINT = 'https://api.openai.com/v1/chat/completions'

_PROMPT = io.open(PROMPT_PATH, encoding='utf-8').read()
_CTX = ssl.create_default_context()

class QualifierUnavailable(RuntimeError):
    pass

def _headers():
    h = {'Content-Type': 'application/json'}
    key = os.environ.get('OPENAI_API_KEY', '').strip()
    if key: h['Authorization'] = 'Bearer ' + key
    return h

def _post(payload, timeout=90):
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode('utf-8'),
                                 headers=_headers(), method='POST')
    with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
        return json.loads(r.read().decode('utf-8', 'replace'))

def preflight():
    """One cheap call so a missing/invalid key fails the run loudly and early instead of
    producing 0 verdicts silently. Returns a short human-readable status string."""
    try:
        _post({'model': MODEL, 'max_tokens': 1, 'temperature': 0,
               'messages': [{'role': 'user', 'content': 'ping'}]}, timeout=30)
        return 'ok (auth via %s)' % ('OPENAI_API_KEY env var' if os.environ.get('OPENAI_API_KEY')
                                     else 'proxy-attached API credential')
    except urllib.error.HTTPError as e:
        body = e.read()[:300].decode('utf-8', 'replace')
        raise QualifierUnavailable('OpenAI HTTP %d: %s' % (e.code, body))
    except Exception as e:
        raise QualifierUnavailable('OpenAI unreachable: %s %s' % (type(e).__name__, str(e)[:200]))

def classify(name, content):
    user = 'Company: %s\n\nWebsite content:\n%s' % (name, (content or '')[:MAX_CONTENT_CHARS])
    payload = {'model': MODEL, 'max_tokens': MAX_OUTPUT_TOKENS, 'temperature': TEMPERATURE,
               'messages': [{'role': 'system', 'content': _PROMPT},
                            {'role': 'user', 'content': user}]}
    for attempt in range(3):
        try:
            r = _post(payload)
            txt = (r['choices'][0]['message'].get('content') or '').strip()
            txt = re.sub(r'^```(?:json)?|```$', '', txt, flags=re.M).strip()
            try: return json.loads(txt), None
            except Exception:
                m = re.search(r'\{.*\}', txt, re.S)
                if m:
                    try: return json.loads(m.group(0)), None
                    except Exception: pass
                return None, 'parse_error'
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                return None, 'auth:HTTP%d' % e.code
            if attempt == 2: return None, 'HTTP%d' % e.code
            time.sleep(3 * (attempt + 1) if e.code == 429 else 2 * (attempt + 1))
        except Exception as e:
            if attempt == 2: return None, type(e).__name__ + ':' + str(e)[:120]
            time.sleep(2 * (attempt + 1))
    return None, 'unknown'

def qualify_many(rows, deadline, on_result, log=print):
    """rows: crawled records with status=='ok'. Calls on_result(record) per company as
    verdicts arrive so a cut-off run still leaves every finished verdict on disk."""
    if not rows: return 0
    log('[v6] preflight: %s' % preflight())
    done = 0
    def work(r):
        res, err = classify(r.get('company_name') or r['domain'], r.get('text', ''))
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
            if (rec.get('error') or '').startswith('auth:'):
                log('[v6] authentication failed mid-run (%s); stopping' % rec['error'])
                for f in futs: f.cancel()
                break
            on_result(rec); done += 1
            if time.time() > deadline:
                log('[v6] time budget reached with %d/%d classified; rest carried to next run'
                    % (done, len(rows)))
                for f in futs: f.cancel()
                break
    return done
