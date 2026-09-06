# -*- coding: utf-8 -*-
"""TCPA MARKETING-PARTNER LISTS channel (layer L10-partners).

Insurance / solar / home-services quote sites must disclose the "marketing partners" that
may call a consumer. Those pages name hundreds of small lead and call sellers - exactly the
1-20 staff operators that never appear in search or databases. Measured 2026-09-06:
25 candidates -> 4 v6-qualified in one agent session, the best channel of five tried.

Per pass:
  1. discover new partner pages (a few TinyFish searches + probing standard paths on seed
     sites), keep pages that carry >= 20 company-like names
  2. fetch up to PAGES_PER_PASS partner pages (TinyFish Fetch renders JS; falls back to
     plain HTTP) and diff their names against everything already seen
  3. resolve up to NAMES_PER_PASS new names to domains: guess {compact}.com/.io/.net and
     verify by fetching (title/text must contain a distinctive token of the name); if no
     guess verifies, one TinyFish search on the exact name; unresolved names are recorded
     so they are never retried
  4. emit resolved, unknown domains as candidates

State (all under state/):
  partner_pages.json  url -> {first_seen, last_fetched, names_last, ok}
  partner_names.jsonl one line per name: {name, norm, domain|null, how, source_url, ts}
"""
import io, json, os, re, time, urllib.parse, urllib.request
import concurrent.futures as cf

ROOT = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(ROOT, 'state')
PAGES = os.path.join(STATE, 'partner_pages.json')
NAMES = os.path.join(STATE, 'partner_names.jsonl')
TF_KEY = os.environ.get('TINYFISH_API_KEY', '')

PAGES_PER_PASS = int(os.environ.get('PARTNER_PAGES_PER_PASS', '2'))
NAMES_PER_PASS = int(os.environ.get('PARTNER_NAMES_PER_PASS', '72'))
SEARCHES_PER_PASS = int(os.environ.get('PARTNER_SEARCHES_PER_PASS', '4'))
NAME_SEARCHES_PER_PASS = int(os.environ.get('PARTNER_NAME_SEARCHES_PER_PASS', '15'))

# seed sites whose disclosures the 2026-09-06 agent found productive
SEED_SITES = ['coveragebeacon.com', 'quotelab.com', 'ratequote.com', 'liheapassistance.org',
              'seniorinsuranceshopping.com', 'meetpolicies.com', 'viva-leads.com', 'everquote.com',
              'selectmypolicy.com', 'medicaresupplement.com', 'renuehome.com', 'windowquotefinder.com',
              'policyscout.com', 'adfluential.com', 'theswitchboardmarketing.com', 'smarthomequotes.com',
              'emberhomepros.com', 'smartfinancial.com', 'quotewizard.com', 'insurify.com', 'zebra.com',
              'healthplanone.com', 'medicareplan.com', 'solarreviews.com', 'modernize.com', 'homeadvisor.com',
              'assurance.com', 'lendingtree.com', 'nerdwallet.com', 'bankrate.com', 'quotelab.co',
              'ehealthinsurance.com', 'gohealth.com', 'selectquote.com', 'ratemarketplace.com']
PARTNER_PATHS = ['/partners', '/marketing-partners', '/partner-list', '/our-partners', '/partners/',
                 '/marketing-partners/', '/tcpa-partners', '/partner-companies', '/list-of-partners',
                 '/privacy/partners', '/partners.html', '/marketing-partner-list', '/partnerlist',
                 '/marketing_partners', '/privacy-policy/partners', '/companies-that-may-contact-you']
DISCOVERY_QUERIES = [
    '"marketing partners" "may contact you" insurance quotes',
    '"marketing partners" "may call" Medicare quotes list',
    '"list of marketing partners" auto insurance',
    '"marketing partners" solar quotes "may contact"',
    '"partner list" "TCPA" home improvement quotes',
    '"companies that may contact you" quotes',
    '"our marketing partners" final expense quotes',
    '"marketing partners" "home services" "may contact you"',
    '"partner companies" "may call" health insurance quotes',
    '"marketing partners" "debt relief" "may contact"',
    '"marketing partners" "auto warranty" quotes',
    '"marketing partners" roofing quotes "may contact"',
    '"marketing partners" "windows" quotes "may contact you"',
    '"marketing partners" "life insurance" "may contact you"',
    '"insurance partners" "may contact you at the number" list',
]

# names that are carriers / brands / buyers / platforms, never a small call seller
BIG = re.compile(r'(?i)\b(state farm|allstate|progressive|geico|liberty mutual|nationwide|farmers|usaa|travelers|'
                 r'aetna|humana|cigna|anthem|unitedhealth|united health|kaiser|blue cross|blue shield|bcbs|mutual of omaha|'
                 r'aflac|metlife|prudential|transamerica|lincoln|john hancock|new york life|northwestern|mass ?mutual|'
                 r'colonial penn|globe life|american family|amfam|the general|elephant|esurance|root|lemonade|hippo|'
                 r'clearcover|safeco|hartford|chubb|amica|erie|auto-?owners|mercury|national general|dairyland|'
                 r'everquote|quotewizard|smartfinancial|lendingtree|nerdwallet|bankrate|zebra|insurify|policygenius|'
                 r'selectquote|ehealth|gohealth|assurance|healthmarkets|zillow|homeadvisor|angi|modernize|thumbtack|'
                 r'sunrun|sunpower|tesla|vivint|adt|renewal by andersen|leaffilter|leaf home|bath fitter|empire today|'
                 r'lowe|home depot|verizon|at&t|t-mobile|comcast|spectrum|dish|directv|google|meta|facebook|amazon|'
                 r'twilio|ringba|retreaver|trackdrive|phonexa|invoca|jornaya|trustedform|activeprospect|verisk|'
                 r'transunion|equifax|experian|lexisnexis|salesforce|hubspot)\b')
ORG_HINT = re.compile(r'(?i)\b(llc|l\.l\.c|inc|corp|co\b|ltd|group|media|leads?|marketing|direct|interactive|digital|'
                      r'partners|network|solutions|ventures|enterprises|holdings|agency|advertising|calls?|connect|'
                      r'quote|quotes|insurance|financial|health|home|solar|senior|benefits|advisors|services|'
                      r'consulting|labs|company|technologies|systems)\b')
NOISE_LINE = re.compile(r'(?i)(privacy|terms|cookie|copyright|©|all rights|click here|read more|contact us|'
                        r'phone number|email address|by submitting|consent|prerecorded|autodial|opt.?out|'
                        r'unsubscribe|do not (call|sell)|california|ccpa|gdpr|updated|effective date|page \d|^\d+$)')

def _load_pages():
    try: return json.load(io.open(PAGES, encoding='utf-8'))
    except Exception: return {}

def _save_pages(p):
    json.dump(p, io.open(PAGES + '.tmp', 'w', encoding='utf-8'), indent=1, sort_keys=True); os.replace(PAGES + '.tmp', PAGES)

def _load_names():
    seen = {}
    if os.path.exists(NAMES):
        for line in io.open(NAMES, encoding='utf-8', errors='replace'):
            try: r = json.loads(line); seen[r['norm']] = r
            except Exception: pass
    return seen

def _append_name(rec):
    with io.open(NAMES, 'a', encoding='utf-8') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')

def norm_name(s):
    s = re.sub(r'[^a-z0-9& ]+', ' ', s.lower())
    s = re.sub(r'\b(llc|l l c|inc|incorporated|corp|corporation|co|ltd|limited|the|dba|a|an|of)\b', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

# ------------------------------------------------------------------ fetching
def tf_fetch(urls, timeout=100):
    """TinyFish Fetch REST: up to 10 URLs, renders JS. Returns {url: text}. Free."""
    if not urls: return {}
    body = json.dumps({'urls': urls[:10], 'format': 'markdown', 'ttl': 86400 * 7}).encode('utf-8')
    hdr = {'Content-Type': 'application/json'}
    if TF_KEY: hdr['X-API-Key'] = TF_KEY
    req = urllib.request.Request('https://api.fetch.tinyfish.ai', data=body, headers=hdr, method='POST')
    out = {}
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode('utf-8', 'replace'))
        for res in data.get('results') or []:
            out[res.get('url')] = res.get('text') or ''
    except Exception as e:
        pass
    return out

def tf_search(query, page=0):
    import discovery as D
    try: return D.tf_search(query, page).get('results') or []
    except Exception: return []

def page_text(url, log=print):
    txt = tf_fetch([url]).get(url, '')
    if len(txt) < 500:
        import ppclib as L
        fu, raw, e = L.http_get(url, timeout=15)
        if raw: txt = L.visible_text(raw)
    return txt

# ------------------------------------------------------------------ name extraction
GENERIC = set('''address information phone email website method system systems forms form training controls control
providers provider partners partner agencies agency calls call marketing media leads lead group direct services service
solutions company companies data privacy policy notice terms contact about home page site online web digital national
american america usa united states insurance health senior seniors benefits financial quote quotes plan plans coverage
care life auto home solar energy roofing windows mortgage debt relief tax credit medicare medicaid final expense
who we are what how why when where your our their this that these those and the for with from
mailing service property preferred operating referral employee website ip access'''.split())

def _distinct(norm):
    return [t for t in norm.replace('&', ' ').split() if len(t) >= 4 and t not in GENERIC]

def _list_blocks(text):
    """Lines that sit inside a dense run (>= 12 consecutive short lines) - a partner list looks
    like that; privacy-policy prose and article headings do not."""
    lines = [re.sub(r'^\s*(?:[-*•·]|\d+[.)])\s*', '', l).strip() for l in (text or '').splitlines()]
    out, run = [], []
    def flush():
        if len(run) >= 12: out.extend(run)
    for l in lines:
        if 2 <= len(l) <= 70 and len(l.split()) <= 7 and not re.search(r'[.!?:]\s', l + ' ') and not l.endswith(':'):
            run.append(l)
        else:
            if l == '' and run: continue          # blank lines inside a list are fine
            flush(); run = []
    flush()
    # comma-separated lists on one line also count
    for l in lines:
        if l.count(',') >= 10 and len(l) > 200: out.extend(p.strip() for p in l.split(','))
    return out

def extract_names(text, host=''):
    names, seen = [], set()
    for raw in _list_blocks(text):
        s = re.sub(r'^\W+|\W+$', '', raw.strip()); s = re.sub(r'\s+', ' ', s)
        if not (3 <= len(s) <= 60) or NOISE_LINE.search(s): continue
        words = s.split()
        if not (1 <= len(words) <= 7): continue
        caps = sum(1 for w in words if w[:1].isupper() or w.isupper())
        if caps < max(1, len(words) - 1): continue
        if BIG.search(s): continue
        n = norm_name(s)
        if len(n) < 4 or n in seen: continue
        if not _distinct(n) and not ORG_HINT.search(s): continue       # "Mailing address"
        if not _distinct(n) and len(words) < 2: continue
        if host and host.split('.')[0] in n.replace(' ', ''): continue  # the page's own company
        seen.add(n); names.append((s, n))
    return names

PARTNER_CONTEXT = re.compile(r'(?i)(marketing partners?|partner list|may (?:contact|call) you|companies that may|'
                             r'our partners|partner companies|third[- ]party partners|tcpa)')
BAD_HOST = re.compile(r'(arxiv\.org|\.edu$|\.gov$|hospital|clinic|university|wikipedia|\.pdf$|sec\.gov|law\.cornell)', re.I)

def looks_like_partner_page(text, url=''):
    if url and BAD_HOST.search(urllib.parse.urlparse(url).netloc + urllib.parse.urlparse(url).path): return False
    if not PARTNER_CONTEXT.search(text or ''): return False
    return len(extract_names(text)) >= 20

def canon(u):
    return u.split('#')[0].split('?')[0].rstrip('/')

# ------------------------------------------------------------------ domain resolution
def _tokens(norm):
    return _distinct(norm)

def guess_domains(norm):
    if not _distinct(norm): return []                    # nothing distinctive to verify against
    compact = re.sub(r'[^a-z0-9]', '', norm.replace('&', 'and'))
    hyph = re.sub(r'[^a-z0-9-]', '', norm.replace(' ', '-').replace('&', 'and'))
    if not compact or len(compact) > 40: return []
    out = [compact + '.com']
    if hyph != compact: out.append(hyph + '.com')
    out += [compact + '.io', compact + '.net', compact + 'llc.com', compact + 'inc.com']
    return out

def verify_domain(domain, norm):
    """Fetch the homepage; accept if reachable, not parked, and it names the company."""
    import ppclib as L, crawl as C
    if not C.valid(domain): return None
    fu, raw, e = C.fast_get('https://' + domain, timeout=8)
    if not raw or len(raw) < 300:
        fu, raw, e = C.fast_get('https://www.' + domain, timeout=8)
    if not raw or len(raw) < 300: return None
    txt = L.visible_text(raw)
    if C.looks_parked(raw, txt): return None
    hay = (txt[:6000] + ' ' + ' '.join(s for _, s in L.headings(raw))).lower()
    toks = _tokens(norm)
    if not toks: return None
    hits = sum(1 for t in toks if t in hay)
    if hits >= max(1, min(2, len(toks))): return domain
    return None

def resolve_name(display, norm, search_budget):
    """Returns (domain|None, how, searches_used)."""
    import crawl as C
    m = re.fullmatch(r'(?:https?://)?(?:www\.)?([a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,})/?', display.strip().lower())
    if m and C.valid(m.group(1)):                        # the list named the domain itself
        return m.group(1), 'literal', 0
    for d in guess_domains(norm):
        if verify_domain(d, norm): return d, 'guess:' + d, 0
    if search_budget <= 0: return None, 'unresolved:no-search-budget', 0
    import crawl as C
    toks = _tokens(norm)
    if not toks: return None, 'unresolved:generic-name', 0
    res = tf_search('"%s"' % display)
    for r in res[:8]:
        url = r.get('url') or ''
        try: d = C.valid(url)
        except Exception: d = None
        if not d or d in C.BLOCK or d in C.COMMON_3P: continue
        title = (r.get('title') or '').lower()
        if sum(1 for t in toks if t in title) >= max(1, min(2, len(toks))):
            return d, 'search', 1
    return None, 'unresolved:search-miss', 1

# ------------------------------------------------------------------ main entry
def run(emit, is_known, deadline, log=print):
    pages = _load_pages(); names = _load_names()
    stats = {'pages_discovered': 0, 'pages_fetched': 0, 'names_new': 0, 'resolved': 0, 'emitted': 0, 'searches': 0}
    if not TF_KEY:
        log('[partners] TINYFISH_API_KEY missing - channel needs search+fetch; skipped'); return stats

    t_start = time.time(); span = max(60, deadline - t_start)
    def add_page(u, t):
        u = canon(u)
        if u in pages or not looks_like_partner_page(t, u): return False
        pages[u] = {'first_seen': time.strftime('%Y-%m-%d'), 'last_fetched': '', 'names_last': 0, 'ok': True}
        stats['pages_discovered'] += 1; return True

    # 1. discovery gets at most the first 30% of the channel's time; the productive work
    #    (reading known partner pages and resolving names) always gets the rest
    disc_deadline = t_start + 0.30 * span
    unprobed = [s for s in SEED_SITES if 'seed:' + s not in pages]
    for site in unprobed[:2]:
        if time.time() > disc_deadline: break
        got = tf_fetch(['https://' + site + p for p in PARTNER_PATHS[:10]])
        found = any(add_page(u, t) for u, t in got.items())
        pages['seed:' + site] = {'probed': time.strftime('%Y-%m-%d'), 'found': found}
    qdone = pages.setdefault('_queries_done', [])
    for q in DISCOVERY_QUERIES:
        if stats['searches'] >= SEARCHES_PER_PASS or time.time() > disc_deadline: break
        if q in qdone: continue
        res = tf_search(q); stats['searches'] += 1; qdone.append(q)
        cand = [r.get('url') for r in res if r.get('url') and canon(r['url']) not in pages][:10]
        for u, t in tf_fetch(cand).items(): add_page(u, t)
        time.sleep(2.2)
    _save_pages(pages)
    if stats['pages_discovered']: log('[partners] discovered %d new partner-list pages' % stats['pages_discovered'])

    # 2. fetch a few partner pages (never-fetched first, then oldest), diff names
    todo = sorted([u for u, v in pages.items() if u.startswith('http') and v.get('ok')],
                  key=lambda u: pages[u].get('last_fetched') or '')[:PAGES_PER_PASS]
    fresh = []
    for u in todo:
        if time.time() > deadline: break
        txt = page_text(u, log); stats['pages_fetched'] += 1
        ex = extract_names(txt, urllib.parse.urlparse(u).netloc.replace('www.', ''))
        pages[u]['last_fetched'] = time.strftime('%Y-%m-%d'); pages[u]['names_last'] = len(ex)
        if len(ex) < 20: pages[u]['ok'] = False            # page changed / blocked; stop re-reading it
        for disp, n in ex:
            if n not in names:
                names[n] = {'name': disp, 'norm': n, 'domain': None, 'how': 'pending', 'source_url': u, 'ts': ''}
                fresh.append(n)
        log('[partners] %s -> %d names, %d never seen' % (u[:70], len(ex), sum(1 for d, n in ex if n in fresh)))
    _save_pages(pages)
    stats['names_new'] = len(fresh)

    # 3. resolve pending names (this pass's new ones first, then older pendings), bounded
    pending = fresh + [n for n, r in names.items() if r.get('how') == 'pending' and n not in fresh]
    # call-sellers first: the 4 qualified from this channel on 2026-09-06 were all "Direct",
    # "Leads", "Media", "Marketing" names; carriers/agencies/"Health" names are buyers
    def score(n):
        s = 0
        if re.search(r'\b(calls?|transfers?|inbound|ring|dial|phone)\b', n): s += 4
        if re.search(r'\b(media|leads?|direct|marketing|digital|interactive|network|advertising|traffic|performance|ventures)\b', n): s += 2
        if re.search(r'\b(insurance|agency|agencies|health|benefits|advisors|financial|brokerage|life|senior|solutions)\b', n): s -= 2
        if re.search(r'\b(llc|inc)\b', n): s += 1
        return -s
    pending = sorted(pending, key=score)[:NAMES_PER_PASS]
    sb = NAME_SEARCHES_PER_PASS
    # guess+verify in parallel, in chunks, stopping at the channel deadline; searches for the
    # misses are serialised afterwards (30/min shared ceiling) while time remains
    results = {}
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        for i in range(0, len(pending), 24):
            if time.time() > deadline: break
            chunk = pending[i:i + 24]
            for n, (d, how, used) in zip(chunk, ex.map(lambda n: resolve_name(names[n]['name'], n, 0), chunk)):
                results[n] = (d, how)
    for n in pending:
        if n not in results: continue                    # ran out of time: stays pending
        if time.time() > deadline + 60: break            # hard stop: leave the rest pending
        d, how = results[n]
        if not d and sb > 0 and time.time() < deadline and not how.startswith('unresolved:generic'):
            d, how, used = resolve_name(names[n]['name'], n, 1); sb -= used; stats['searches'] += used
            time.sleep(2.2)
        rec = names[n]; rec.update(domain=d, how=how, ts=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
        if how.startswith('unresolved:no-search'): rec['how'] = 'pending'       # retry next pass
        else: _append_name(rec)
        if d:
            stats['resolved'] += 1
            if emit(d, layer='L10-partners', source_url=rec['source_url'],
                    source_note='named as marketing partner on %s; resolved via %s' % (urllib.parse.urlparse(rec['source_url']).netloc, how),
                    company_name=rec['name']):
                stats['emitted'] += 1
    log('[partners] pages fetched %d | new names %d | resolved %d | emitted %d | searches %d | pending %d'
        % (stats['pages_fetched'], stats['names_new'], stats['resolved'], stats['emitted'], stats['searches'],
           sum(1 for r in names.values() if r.get('how') == 'pending')))
    return stats
