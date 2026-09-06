#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TinyFish Search / Fetch from the shell (free at any balance). For agents running where the
TinyFish MCP server is not available (cloud routines). Needs TINYFISH_API_KEY in the env.

    python tools/tf.py search "\"Ringba\" site:onlinejobs.ph pay per call" [--page 1] [--location US]
    python tools/tf.py fetch https://a.com/job https://b.com/job ...     (up to 10 URLs)
    python tools/tf.py known example.com [other.com ...]                  (is it in the exclusion index?)

Output is JSON on stdout. Search results: [{title, url, snippet, site_name}]. Fetch: {url: text}.
Rate limit for search is ~30 requests/minute shared by everyone on the key: sleep ~2s between calls.
"""
import io, json, os, sys, time, urllib.parse, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get('TINYFISH_API_KEY', '')

def _req(url, data=None):
    hdr = {'Content-Type': 'application/json'}
    if KEY: hdr['X-API-Key'] = KEY
    req = urllib.request.Request(url, data=data, headers=hdr, method='POST' if data else 'GET')
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=110) as r: return json.loads(r.read().decode('utf-8', 'replace'))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(15); continue
            return {'error': 'HTTP %d' % e.code, 'body': e.read()[:300].decode('utf-8', 'replace')}
        except Exception as e:
            if attempt == 2: return {'error': type(e).__name__}
            time.sleep(3)
    return {'error': 'rate_limited'}

def search(q, page=0, location='US'):
    qs = urllib.parse.urlencode({'query': q, 'page': page, 'location': location})
    res = _req('https://api.search.tinyfish.ai?' + qs)
    if 'error' in res: return res
    return [{'title': r.get('title'), 'url': r.get('url'), 'snippet': r.get('snippet'), 'site_name': r.get('site_name')}
            for r in res.get('results') or []]

def fetch(urls):
    res = _req('https://api.fetch.tinyfish.ai', json.dumps({'urls': urls[:10], 'format': 'markdown'}).encode('utf-8'))
    if 'error' in res: return res
    out = {r.get('url'): (r.get('text') or '') for r in res.get('results') or []}
    for e in res.get('errors') or []: out[e.get('url')] = '__ERROR__ ' + str(e.get('error'))[:200]
    return out

def known(domains):
    p = os.path.join(ROOT, 'state', 'known_domains.txt')
    idx = set(x.strip() for x in io.open(p, encoding='utf-8')) if os.path.exists(p) else set()
    seen = set()
    sp = os.path.join(ROOT, 'state', 'hiring_agent_seen.jsonl')
    if os.path.exists(sp):
        for line in io.open(sp, encoding='utf-8', errors='replace'):
            try: seen.add(json.loads(line).get('domain'))
            except Exception: pass
    return {d: ('KNOWN' if d in idx else 'SEEN_BY_AGENT' if d in seen else 'NEW') for d in domains}

if __name__ == '__main__':
    try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass
    a = sys.argv[1:]
    if not a or a[0] not in ('search', 'fetch', 'known'): sys.exit(__doc__)
    if a[0] == 'search':
        page = int(a[a.index('--page') + 1]) if '--page' in a else 0
        loc = a[a.index('--location') + 1] if '--location' in a else 'US'
        q = ' '.join(x for i, x in enumerate(a[1:], 1) if x not in ('--page', '--location') and a[i - 1] not in ('--page', '--location'))
        print(json.dumps(search(q, page, loc), ensure_ascii=False, indent=1))
    elif a[0] == 'fetch':
        print(json.dumps(fetch(a[1:]), ensure_ascii=False, indent=1))
    else:
        print(json.dumps(known([x.lower().strip() for x in a[1:]]), indent=1))
