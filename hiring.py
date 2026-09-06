# -*- coding: utf-8 -*-
"""HIRING SIGNALS channel (layer L10-hiring).

Only a call-selling business hires "pay-per-call media buyers" or asks for Ringba /
TrackDrive / Retreaver / Phonexa experience. Measured 2026-09-06: tool-name phrasing on
OnlineJobs.ph and bebee (which mirror full posting text and are not bot-blocked) gave
5 candidates -> 2 v6-qualified; generic phrasing on Indeed/ZipRecruiter gave nothing and
those boards block fetches anyway. US operators often post offshore (LatAm / Asia
LinkedIn geos, OnlineJobs.ph), so the employer's country is NOT the poster's.

Per pass: a handful of searches (rotating through QUERIES with page state), fetch the new
postings (TinyFish Fetch renders JS), extract the employer's domain from the posting text
(explicit domains first; else the company name resolved like a partner name), emit.

State: state/hiring_state.json  {queries: {q: next_page/retired}, seen_urls: [...]}
"""
import io, json, os, re, time, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(ROOT, 'state')
HS = os.path.join(STATE, 'hiring_state.json')
TF_KEY = os.environ.get('TINYFISH_API_KEY', '')
SEARCHES_PER_PASS = int(os.environ.get('HIRING_SEARCHES_PER_PASS', '4'))
POSTINGS_PER_PASS = int(os.environ.get('HIRING_POSTINGS_PER_PASS', '10'))

TOOLS = ['Ringba', 'TrackDrive', 'Retreaver', 'Phonexa', 'CallerReady', 'Dialics', 'LeadsPedia', 'boberdoo']
ROLES = ['media buyer', 'affiliate manager', 'publisher manager', 'call buyer', 'campaign manager',
         'call QA', 'call routing', 'operations assistant', 'virtual assistant']
BOARDS = ['site:onlinejobs.ph', 'site:bebee.com', 'site:linkedin.com/jobs', 'site:jobright.ai',
          'site:himalayas.app', 'site:remoterocketship.com', 'site:workable.com', 'site:indeed.com']

def all_queries():
    qs = []
    for tool in TOOLS:
        for board in BOARDS[:3]:
            qs.append('"%s" %s pay per call' % (tool, board))
    for role in ROLES[:6]:
        for board in BOARDS[:2]:
            qs.append('"pay per call" "%s" %s' % (role, board))
    for board in BOARDS[3:]:
        qs.append('"pay per call" media buyer %s Ringba OR TrackDrive OR Retreaver' % board)
    qs += ['"pay-per-call" "we are hiring" media buyer inbound calls',
           '"live transfers" "affiliate manager" hiring insurance calls',
           '"ping post" "call" campaign manager job', '"buyer caps" calls job posting']
    return qs

JOB_HOST = re.compile(r'(onlinejobs\.ph|bebee\.com|linkedin\.com|indeed\.com|jobright\.ai|himalayas\.app|remoterocketship\.com|'
                      r'workable\.com|glassdoor\.com|ziprecruiter\.com|simplyhired\.com|lever\.co|greenhouse\.io|breezy\.hr|'
                      r'jazzhr\.com|recruitee\.com|upwork\.com|fiverr\.com|facebook\.com|instagram\.com|google\.com|youtube\.com|'
                      r'twitter\.com|x\.com|tiktok\.com|wellfound\.com|monster\.com|talent\.com|jooble\.org|adzuna\.com)', re.I)
DOMAIN_IN_TEXT = re.compile(r'\b((?:[a-z0-9-]+\.)+(?:com|io|net|co|us|ca|uk|co\.uk|agency|media|marketing|ai))\b', re.I)
EMAIL_DOMAIN = re.compile(r'[A-Za-z0-9._%+-]+@((?:[a-z0-9-]+\.)+[a-z]{2,})', re.I)
COMPANY_LINE = re.compile(r'(?im)^(?:company|employer|about (?:us|the company)|hiring company)\s*[:\-]\s*(.{3,80})$')
PPC_EVIDENCE = re.compile(r'(?i)(pay[ -]?per[ -]?call|ringba|trackdrive|retreaver|phonexa|callerready|dialics|inbound calls?|'
                          r'live transfers?|call buyers?|publishers?|payout|buyer caps?|ping ?post|call routing)')
FREEMAIL = {'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com', 'icloud.com', 'protonmail.com', 'live.com'}

def _load():
    try: return json.load(io.open(HS, encoding='utf-8'))
    except Exception: return {'queries': {}, 'seen_urls': []}

def _save(s):
    json.dump(s, io.open(HS + '.tmp', 'w', encoding='utf-8'), indent=1); os.replace(HS + '.tmp', HS)

STAFFING = re.compile(r'(?i)\b(paired|talent hackers|a hiring group|huzzle|expandiq|3 little birds|hype hr|kajae|fostr|'
                      r'staffing|recruit(?:ing|ment)|talent|outsourc|somewhere|jobrack|remote ?staff|virtual ?staff)\b')

def guess_company(text, url):
    """Employer name from the posting's title line / URL, board by board."""
    head = '\n'.join((text or '').splitlines()[:6])
    m = COMPANY_LINE.search(text or '')
    if m: return m.group(1).strip()
    # "About Creative Clicks" heading - the most reliable employer marker across boards
    m = re.search(r'(?m)^#{0,4}\s*About\s+(?!us\b|the\b|this\b|you\b)([A-Z][A-Za-z0-9&\'\.\- ]{2,50}?)\s*:?\s*$', text or '')
    if m: return m.group(1).strip()
    m = re.search(r'(?m)^#{0,4}\s*([A-Z][A-Za-z0-9&\'\.\- ]{2,50}?) is (?:a|an|the) (?:global |leading |growing |fast-growing )?'
                  r'(?:performance|pay[- ]per[- ]call|lead|marketing|affiliate|digital|media|call)', text or '')
    if m: return m.group(1).strip()
    host = urllib.parse.urlparse(url).netloc.lower()
    if 'bebee.com' in host:
        # "Senior Media Buyer - Creative Clicks - Toronto, Ontario" (first heading)
        for line in head.splitlines():
            parts = [p.strip(' #*') for p in re.split(r'\s+[-–|]\s+', line) if p.strip(' #*')]
            if len(parts) >= 2 and len(parts[1]) < 60: return parts[1]
    if 'linkedin.com' in host:
        m = re.search(r'^#*\s*(.{2,80}?) hiring .{2,80}? in ', head, re.M)
        if m: return m.group(1).strip()
    if 'onlinejobs.ph' in host:
        m = re.search(r'(?im)^(?:company|employer|about (?:us|the company))\s*[:\-]?\s*(.{3,80})$', text or '')
        if m: return m.group(1).strip()
        m = re.search(r'(?i)\b(?:we are|we\'re|join)\s+([A-Z][A-Za-z0-9&\'\- ]{2,40}?)(?:,|\.| is | a )', text or '')
        if m: return m.group(1).strip()
    for line in head.splitlines():
        m = re.search(r'(?i)\bat\s+([A-Z][A-Za-z0-9&\'\- ]{2,40})\s*(?:[-–|]|$)', line)
        if m: return m.group(1).strip()
    return ''

def extract_employer(text, posting_url):
    """Returns (domain|None, company_name, evidence_snippet)."""
    import crawl as C
    ev = PPC_EVIDENCE.search(text or '')
    if not ev: return None, '', ''
    snippet = text[max(0, ev.start() - 80): ev.end() + 120].replace('\n', ' ')
    import collections
    company = guess_company(text, posting_url)
    if company and (len(company.split()) < 2 and not re.search(r'(?i)(llc|inc|media|leads|group|calls?)', company)):
        company = ''                                   # "building", "hiring": not a company
    emails = collections.Counter()
    for m in EMAIL_DOMAIN.finditer(text):
        d = C.valid(m.group(1).lower())
        if d and d not in FREEMAIL and not JOB_HOST.search(d): emails[d] += 1
    mentions = collections.Counter()
    for m in DOMAIN_IN_TEXT.finditer(text):
        d = C.valid(m.group(1).lower())
        if d and d not in FREEMAIL and not JOB_HOST.search(d) and d not in C.COMMON_3P: mentions[d] += 1
    # an email domain is authoritative; a bare mention only counts if it recurs or matches the name
    if emails: return emails.most_common(1)[0][0], company, snippet
    for d, n in mentions.most_common():
        if n >= 2 or (company and re.sub(r'[^a-z0-9]', '', company.lower())[:8] in d.replace('-', '')):
            return d, company, snippet
    return None, company, snippet

def run(emit, is_known, deadline, log=print):
    st = _load(); stats = {'searches': 0, 'postings': 0, 'emitted': 0}
    if not TF_KEY:
        log('[hiring] TINYFISH_API_KEY missing - skipped'); return stats
    import discovery as D, partners as P
    seen = set(st.get('seen_urls') or [])
    qs = st.setdefault('queries', {})
    order = sorted(all_queries(), key=lambda q: (qs.get(q, {}).get('retired', False), qs.get(q, {}).get('next_page', 0)))
    new_urls = []
    for q in order:
        if stats['searches'] >= SEARCHES_PER_PASS or time.time() > deadline: break
        s = qs.setdefault(q, {'next_page': 0, 'retired': False, 'new_total': 0})
        if s['retired']: continue
        try: res = D.tf_search(q, s['next_page']).get('results') or []
        except Exception: res = []
        stats['searches'] += 1
        urls = [r.get('url') for r in res if r.get('url') and r['url'] not in seen]
        s['next_page'] += 1; s['new_total'] += len(urls)
        if not urls or s['next_page'] > 3: s['retired'] = True
        new_urls += urls
        time.sleep(2.2)
    new_urls = new_urls[:POSTINGS_PER_PASS]
    name_searches = int(os.environ.get('HIRING_NAME_SEARCHES_PER_PASS', '8'))
    for i in range(0, len(new_urls), 10):
        if time.time() > deadline: break
        got = P.tf_fetch(new_urls[i:i + 10])
        for u, txt in got.items():
            seen.add(u); stats['postings'] += 1
            d, company, snippet = extract_employer(txt, u)
            if company and STAFFING.search(company): continue          # intermediaries, not operators
            if not d and company:
                d, how, used = P.resolve_name(company, P.norm_name(company), 1 if name_searches > 0 else 0)
                name_searches -= used
                if used: time.sleep(2.2)
            if d and emit(d, layer='L10-hiring', source_url=u,
                          source_note=('%s | ' % company if company else '') + snippet[:220], company_name=company):
                stats['emitted'] += 1
    st['seen_urls'] = sorted(seen)[-5000:]
    _save(st)
    log('[hiring] searches %d | postings read %d | employers emitted %d' % (stats['searches'], stats['postings'], stats['emitted']))
    return stats
