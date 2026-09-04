# -*- coding: utf-8 -*-
"""Candidate discovery for the daily run. Two channels, both measured in runs 3-4 as the
only ones still producing net-new companies against a 13k-domain exclusion index:

  1. SEARCH  - TinyFish Search REST (free, 30 req/min). Long, specific counterparty and
     publisher-onboarding phrases, PAGINATED. Run 3 measured these phrases alive to page
     5-7 while short marketplace phrases die by page 1. State remembers the next page per
     query so every day advances the frontier instead of re-reading page 0.
  2. PROBE   - construct plausible domains ({vertical}calls.com, {vertical}leads.com and
     the hyphen / alt-TLD variants) and fetch them directly. Run 4: ~67% net-new vs ~4%
     for search. Only shapes that measured as productive are generated; the dead shapes
     (prefixed, suffixed, extended-suffix, generic call vocabulary) are deliberately absent.

Both channels write candidates through the same emit() so the orchestrator treats them
identically. Every candidate carries layer / source_url / source_note like the old inbox.
"""
import io, itertools, json, os, random, time, urllib.parse, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(ROOT, 'state')
SEARCH_PROGRESS = os.path.join(STATE, 'search_progress.json')
PROBED = os.path.join(STATE, 'probed_domains.txt')

TF_SEARCH = 'https://api.search.tinyfish.ai'
TF_KEY = os.environ.get('TINYFISH_API_KEY', '')

# ------------------------------------------------------------------ SEARCH CHANNEL
# Page-depth curve measured in run 3 (prompts/NOTES_run3.md): long specific counterparty
# phrases sustain to page 5-7. Each entry: (phrase, max_page, layer).
COUNTERPARTY = [
    ('"become a publisher" calls', 8, 'L4-counterparty'),
    ('"become a publisher" "pay per call"', 8, 'L4-counterparty'),
    ('"join our network" "pay per call"', 6, 'L4-counterparty'),
    ('"join our network" "inbound calls"', 6, 'L4-counterparty'),
    ('"weekly payouts" calls publishers', 4, 'L4-counterparty'),
    ('"apply to become a publisher" calls', 4, 'L4-counterparty'),
    ('"publisher application" "pay per call"', 3, 'L4-counterparty'),
    ('"apply as a publisher" calls', 3, 'L4-counterparty'),
    ('"top payouts" "pay per call"', 3, 'L4-counterparty'),
    ('"our verticals" "pay per call"', 3, 'L4-counterparty'),
    ('"become a buyer" calls publishers', 3, 'L4-counterparty'),
    ('"supply partners" calls', 3, 'L4-counterparty'),
    ('"publisher terms" calls', 3, 'L4-counterparty'),
    # untested carry-forwards from run 3 - each gets a fair page-0..2 trial, then is retired
    ('"publisher application form" calls', 3, 'L4-counterparty'),
    ('"join our publisher network" calls', 3, 'L4-counterparty'),
    ('"apply for publisher access"', 3, 'L4-counterparty'),
    ('"looking for traffic partners" calls', 3, 'L4-counterparty'),
    ('"accepting new publishers" calls', 3, 'L4-counterparty'),
    ('"publisher payout terms"', 3, 'L4-counterparty'),
    ('"payout terms" "per call"', 3, 'L4-counterparty'),
]
# Family A (transaction / payout vocabulary). "we buy calls" WITH the stock-option
# exclusions was the single best net-new source of run 3.
FAMILY_A = [
    ('"we buy calls" -options -stock -trading', 4, 'L4-vertical'),
    ('"we buy inbound calls"', 3, 'L4-vertical'),
    ('"paid per billable call"', 3, 'L4-vertical'),
    ('"call payouts" publishers', 3, 'L4-vertical'),
    ('"sell us your calls"', 3, 'L4-vertical'),
    ('"we buy calls for" -options -stock', 3, 'L4-vertical'),
]
# Family B (publisher-onboarding vocabulary) x the micro-operator vertical cluster where it
# actually produced. Run 3: does NOT scale with vertical breadth - keep this cluster tight.
FAMILY_B_PHRASES = ['"publisher portal"', '"publisher onboarding"', '"media buyer application"',
                    '"publisher signup"', '"publisher sign up"']
FAMILY_B_VERTICALS = ['auto glass', 'towing', 'moving', 'foundation repair', 'final expense',
                      'personal injury', 'medicare', 'restoration', 'ACA', 'debt relief',
                      'roadside', 'junk cars', 'solar', 'mass tort', 'tax relief']

def _family_b():
    for p, v in itertools.product(FAMILY_B_PHRASES, FAMILY_B_VERTICALS):
        yield ('%s %s calls' % (p, v), 2, 'L4-familyB')

def all_queries():
    return COUNTERPARTY + FAMILY_A + list(_family_b())

def _load_progress():
    try: return json.load(io.open(SEARCH_PROGRESS, encoding='utf-8'))
    except Exception: return {}

def _save_progress(p):
    tmp = SEARCH_PROGRESS + '.tmp'
    json.dump(p, io.open(tmp, 'w', encoding='utf-8'), indent=1, sort_keys=True)
    os.replace(tmp, SEARCH_PROGRESS)

def tf_search(query, page):
    if not TF_KEY: raise RuntimeError('TINYFISH_API_KEY not set')
    qs = urllib.parse.urlencode({'query': query, 'page': page, 'location': 'US',
                                 'purpose': 'find small pay-per-call publishers, networks and '
                                            'call brokers - company websites, not articles'})
    req = urllib.request.Request(TF_SEARCH + '?' + qs, headers={'X-API-Key': TF_KEY})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode('utf-8', 'replace'))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(20 + 10 * attempt); continue
            if 500 <= e.code < 600: time.sleep(5); continue
            raise
        except Exception:
            time.sleep(5)
    return {'results': []}

def run_search(emit, is_known, budget, deadline, log=print):
    """Advance the search frontier: `budget` requests, round-robin over queries that are
    not yet exhausted. A query is retired when its page yields nothing new twice in a
    row, or it passes its measured max page. Returns number of requests used."""
    if not TF_KEY:
        log('[search] TINYFISH_API_KEY missing - search channel skipped'); return 0
    prog = _load_progress()
    queries = all_queries()
    random.shuffle(queries)              # spread budget; state keeps it fair over days
    used = 0
    # queries with the most remaining runway first, but everyone gets a turn per day
    for q, maxp, layer in sorted(queries, key=lambda x: prog.get(x[0], {}).get('next_page', 0)):
        if used >= budget or time.time() > deadline: break
        st = prog.setdefault(q, {'next_page': 0, 'dry_streak': 0, 'new_total': 0, 'retired': False})
        if st['retired'] or st['next_page'] > maxp: st['retired'] = True; continue
        page = st['next_page']
        try:
            res = tf_search(q, page)
        except Exception as e:
            log('[search] %s p%d error %s' % (q[:50], page, type(e).__name__)); used += 1
            time.sleep(2.2); continue
        used += 1
        new = 0
        for r in (res.get('results') or []):
            url = r.get('url') or ''
            d = emit(url, layer=layer, source_url=url,
                     source_note=((r.get('title') or '') + ' | ' + (r.get('snippet') or ''))[:300],
                     query=q, page=page)
            if d: new += 1
        st['next_page'] = page + 1
        st['new_total'] += new
        st['dry_streak'] = 0 if new else st['dry_streak'] + 1
        if st['dry_streak'] >= 2 or (page == 0 and not res.get('results')):
            st['retired'] = True
        st['last_run'] = time.strftime('%Y-%m-%d')
        log('[search] %-58s p%d -> %d results, %d net-new%s' % (
            q[:58], page, len(res.get('results') or []), new, '  (retired)' if st['retired'] else ''))
        _save_progress(prog)
        time.sleep(2.2)                  # 30 req/min shared ceiling
    active = sum(1 for v in prog.values() if not v.get('retired'))
    log('[search] used %d requests; %d queries still active, %d retired'
        % (used, active, len(prog) - active))
    return used

# ------------------------------------------------------------------ PROBE CHANNEL
# Run 4: a per-call market only forms where a call is worth enough to broker. Generic
# service-repair morphemes resolved to nothing (0 of 40+). Tokens below are the verticals
# that actually hosted operators, plus their common spellings.
VERTICAL_TOKENS = [
    # insurance / health (highest RPC)
    'finalexpense', 'final-expense', 'medicare', 'medicareadvantage', 'medsupp', 'aca',
    'obamacare', 'healthinsurance', 'lifeinsurance', 'autoinsurance', 'carinsurance',
    'homeinsurance', 'homeownersinsurance', 'commercialinsurance', 'truckinginsurance',
    'workerscomp', 'insurance', 'u65', 'burialinsurance',
    # legal
    'personalinjury', 'injury', 'accident', 'caraccident', 'masstort', 'tort', 'attorney',
    'lawyer', 'legal', 'ssdi', 'disability', 'workerscompensation', 'camplejeune',
    # finance
    'debtrelief', 'debt', 'debtsettlement', 'taxrelief', 'taxdebt', 'creditrepair',
    'studentloan', 'mca', 'merchantcashadvance', 'businessloan', 'businessfunding', 'erc',
    'mortgage', 'refinance', 'reversemortgage', 'heloc',
    # home services that trade per call
    'homeservice', 'homeservices', 'homeimprovement', 'solar', 'roofing', 'hvac', 'plumbing',
    'restoration', 'waterdamage', 'mold', 'pestcontrol', 'windows', 'siding', 'foundation',
    'homewarranty', 'homesecurity', 'garage',
    # auto / roadside
    'autoglass', 'windshield', 'glass', 'roadside', 'towing', 'tow', 'junkcar', 'junkcars',
    'cashforcars', 'autowarranty', 'autotransport', 'carshipping', 'moving', 'movers',
    # other proven per-call verticals
    'rehab', 'addiction', 'treatment', 'detox', 'medicalalert', 'homecare', 'seniorcare',
    'locksmith', 'bailbonds', 'timeshare', 'timeshareexit', 'dental', 'hearing',
    'travel', 'flights', 'cruise', 'education', 'petinsurance', 'lifealert',
]
# Only shapes that measured productive. Order = priority.
SHAPES = ['{v}calls', '{v}leads', '{v}-calls', '{v}-leads', '{v}livetransfers',
          '{v}leadspro', '{v}transfers', '{v}call', '{v}lead']
TLDS = ['.com', '.io', '.net', '.co', '.us', '.agency']

def _load_probed():
    s = set()
    if os.path.exists(PROBED):
        s = set(x.strip() for x in io.open(PROBED, encoding='utf-8') if x.strip())
    return s

def generate_probes(is_known, limit):
    """Yield never-probed, never-known constructed domains, best shapes first."""
    probed = _load_probed()
    out = []
    for shape in SHAPES:
        for tld in TLDS:
            for v in VERTICAL_TOKENS:
                if '-' in v and shape.startswith('{v}-'): continue    # avoid double hyphen
                d = shape.format(v=v) + tld
                if d in probed or is_known(d): continue
                out.append(d)
                if len(out) >= limit: return out
    return out

def mark_probed(domains):
    with io.open(PROBED, 'a', encoding='utf-8', newline='\n') as f:
        for d in domains: f.write(d + '\n')

def run_probe(emit, is_known, limit, log=print):
    """Emit constructed domains as candidates. The orchestrator's crawl decides which ones
    resolve to a real site; unresolved / parked ones are recorded so they are never
    probed again (see daily_run.py, which appends every probe to probed_domains.txt)."""
    cands = generate_probes(is_known, limit)
    n = 0
    for d in cands:
        if emit(d, layer='L7-probe', source_url='https://' + d,
                source_note='constructed domain: vertical x shape probe'):
            n += 1
    log('[probe] generated %d constructed domains (%d emitted as candidates)' % (len(cands), n))
    return cands
