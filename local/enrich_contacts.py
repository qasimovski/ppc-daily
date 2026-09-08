# -*- coding: utf-8 -*-
"""Contact enrichment for v6-qualified companies. Runs LOCALLY (needs the outbound repo's
.env and skill scripts), never in the routine.

    python local/enrich_contacts.py --dry-run          # free stage + credit estimates only
    python local/enrich_contacts.py                    # full run on every not-yet-enriched company
    python local/enrich_contacts.py --domains a.com,b.com
    python local/enrich_contacts.py --no-clay --no-aiark   # skip a vendor

Stages, in the order the run-2 audit found cheapest-first:
  A. MINE   free   re-fetch the company's own pages and extract phones, emails, LinkedIn
                   URLs, owner names, and "this is my cell" language. ppclib, plain HTTP.
  B. AI ARK  paid  decision-makers by domain (Find-decision-makers-ai-ark skill, Mode 2).
                   ~0.5 credit per record returned; misses are free.
  C. CLAY    free* people at the company via the clay CLI (Clay knew 22% of these companies
                   in run 2, but its LinkedIn URLs matched LeadMagic at 73% vs 33% for AI Ark).
  D. LEADMAGIC paid mobile numbers for people with a LinkedIn URL (LM-Enrich-mobile skill).
                   5 credits per successful match, misses free.
  E. TRESTLE  paid  validate every candidate number (validate-phone-trestle skill), ~1.5c each.
  F. ASSEMBLE       one row per person; switchboard rule (a number shared by >1 person or >1
                   company is never a personal line); persona filter; Attio-shaped CSV.

It does NOT push to Attio or write the ledger: it prints the exact commands. Both are
outward-facing writes that get a human look first (CLAUDE.md in the outbound repo).

Outputs -> out/contacts/<date>/ : contacts_for_attio.csv, people_all.csv,
company_lines.csv, companies_no_contact.csv, summary.md. State -> state/enriched.jsonl.
"""
import argparse, collections, csv, glob, io, json, os, re, subprocess, sys, time
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import ppclib as L
try:
    import phonenumbers
    from phonenumbers import geocoder, number_type, PhoneNumberType
except ImportError:
    sys.exit('pip install phonenumbers')

REL = os.environ.get('PPC_OUTBOUND', os.path.join(os.path.dirname(ROOT), 'relevince-outbound'))
SKILLS = os.path.join(REL, '.claude', 'skills')
AIARK = os.path.join(SKILLS, 'Find-decision-makers-ai-ark', 'find_decision_makers.py')
LEADMAGIC = os.path.join(SKILLS, 'LM-Enrich-mobile', 'enrich_mobile.py')
TRESTLE = os.path.join(SKILLS, 'validate-phone-trestle', 'validate_phones.py')
ATTIO = os.path.join(SKILLS, 'Upload-leads-to-attio', 'upload_to_attio.py')
LEDGER_APPEND = os.path.join(REL, 'scripts', 'ledger_append.py')
ENRICHED = os.path.join(ROOT, 'state', 'enriched.jsonl')
ALLQ = os.path.join(ROOT, 'out', 'ALL_qualified.csv')
PY = sys.executable

TITLES = ('CEO,Chief Executive Officer,Founder,Co-Founder,Owner,President,Managing Director,'
          'Managing Partner,Partner,Principal,VP,Vice President,Head of Partnerships,'
          'Director of Operations,Head of Publishers,Publisher Manager,Affiliate Manager')
COUNTRIES = 'United States,Canada,United Kingdom'
# persona: hands-on operators who can approve. Same regexes the run-2 Clay pass used.
KEEP = re.compile(r'\b(founder|co-?founder|owner|ceo|chief|president|partner|managing director|'
                  r'proprietor|principal|director|head of|vp|vice president|svp|evp|'
                  r'operations|partnerships|growth|media buy|publisher|affiliate|revenue)\b', re.I)
DROP = re.compile(r'\b(funeral|nursing|art director|creative director|director of finance|'
                  r'human resources|hr director|it director|technical director|medical director|'
                  r'clinical|dental|veterinar|school|academy|music|assistant|intern|student|'
                  r'volunteer|recruit|accountant|bookkeep|paralegal|nurse|teacher)\b', re.I)

# ------------------------------------------------------------------ helpers
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
def log(m): print(m, flush=True)

def load_env():
    p = os.path.join(REL, '.env')
    if not os.path.exists(p): sys.exit('outbound .env not found at %s (set PPC_OUTBOUND)' % p)
    for line in io.open(p, encoding='utf-8', errors='replace'):
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1); os.environ.setdefault(k.strip(), v.strip())

def run(cmd, cwd=REL, timeout=1800):
    log('  $ ' + ' '.join(('"%s"' % c if ' ' in c else c) for c in cmd[1:]))
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                       encoding='utf-8', errors='replace', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    out = (p.stdout or '') + (p.stderr or '')
    for ln in out.splitlines()[-25:]: log('    | ' + ln)
    return p.returncode, out

def rd(p):
    try: return list(csv.DictReader(io.open(p, encoding='utf-8-sig', errors='replace')))
    except Exception: return []

def wr(p, rows, cols=None):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    cols = cols or (list(rows[0].keys()) if rows else ['domain'])
    with io.open(p, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader()
        for r in rows: w.writerow(r)
    return p

# ------------------------------------------------------------------ stage A: mine own pages
TOLL = {'800', '833', '844', '855', '866', '877', '888', '880', '881', '882', '889'}
LI_COMPANY = re.compile(r'https?://(?:[a-z]{2,3}\.)?linkedin\.com/company/[A-Za-z0-9._%\-]{2,80}', re.I)
LI_PERSON = re.compile(r'https?://(?:[a-z]{2,3}\.)?linkedin\.com/in/[A-Za-z0-9._%\-]{2,80}', re.I)
TEL = re.compile(r'href\s*=\s*["\'](?:tel|sms):\s*([+0-9().\-\s]{7,25})', re.I)
SMS = re.compile(r'href\s*=\s*["\']sms:\s*([+0-9().\-\s]{7,25})', re.I)
MAILTO = re.compile(r'href\s*=\s*["\']mailto:\s*([A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})', re.I)
EMAIL_TXT = re.compile(r'\b([A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})\b')
PHONE_TXT = re.compile(r'(?:\+?\d[\d().\-\s]{7,20}\d)')
ROLE_WORDS = (r'(?:Founders?|Co-?Founders?|Owners?|Co-?Owners?|CEO|Chief Executive(?: Officer)?|President|'
              r'Managing Director|Managing Partner|Partners?|Principal|Director|Chief Revenue Officer|'
              r'Chief Operating Officer|COO|CRO|CMO|Head of [A-Z][a-z]+)')
# a person name: 2-3 capitalised words, or "Peter & Tyler Day"
_NAME = r'([A-Z][a-z]{1,15}(?:[ \t]*&[ \t]*[A-Z][a-z]{1,15})?(?:[ \t]+[A-Z][a-z\'\-]{1,20}){1,2})'   # no line breaks inside a name
# name and role may sit in separate elements: visible_text keeps a newline between them
_SEP = r'[ \t]*(?:[,–—\-|:]|\n){1,3}[ \t\n]*'
NAME_BEFORE = re.compile(r'(?<![A-Za-z])' + _NAME + _SEP + ROLE_WORDS + r'\b')
NAME_AFTER = re.compile(r'\b' + ROLE_WORDS + _SEP + _NAME + r'(?![a-z])')
# prose: "its founder, Brian Fife, started" / "founded by Brian Fife" / "Founder Brian Fife"
NAME_PROSE = re.compile(r'(?i)\b(?:founder|co-?founder|owner|ceo|president)s?\b,?\s+(?:is\s+|are\s+|named\s+)?'
                        r'(?-i:([A-Z][a-z]{1,15}\s+[A-Z][a-z\'\-]{1,20}))')
NAME_FOUNDED_BY = re.compile(r'(?i)\b(?:founded|started|launched|owned|run)\s+by\s+(?-i:([A-Z][a-z]{1,15}\s+[A-Z][a-z\'\-]{1,20}))')
# words that mean a "name" match is actually navigation or a heading
NAME_STOP = re.compile(r'(?i)\b(pay|per|call|calls|lead|leads|media|group|inc|llc|login|logins|portal|publisher|'
                       r'publishers|intake|our|the|about|team|contact|meet|get|start|free|quote|home|privacy|'
                       r'terms|policy|us|we|you|your|why|how|what|apply|join|sign|learn|more|read|click|'
                       r'buyer|buyers|advertiser|affiliate|network|marketing|solutions|services|company|'
                       r'founders?|owners?|ceo|president|directors?|partners?|manager|verticals?|process|'
                       r'summit|mutual|insurance|final|expense|medicare|solar|roofing|legal|law|calls?|'
                       r'transfers?|live|inbound|exclusive|premium|quality|results|growth|revenue|digital|'
                       r'online|performance|agency|platform|program|programs|campaigns?|offers?|inc|'
                       r'data|lists?|site|map|sitemap|accounting|menu|search|blog|news|faq|pricing|careers)\b')

# Every field a Ringba mention can reach an ALL_qualified.csv row through: the crawl's own
# tag detection (infrastructure_detected), the REVIEW flag export.py writes off ringba_prose,
# the v6 evidence text, and the sourcing note (the hiring lane's only evidence). Ringba ONLY -
# TrackDrive / Retreaver / Phonexa tenants are fine for Kaliper.
RINGBA_RE = re.compile(r'\bringba\b', re.I)
RINGBA_FIELDS = ('kaliper_flags', 'infrastructure_detected', 'source_note', 'source_url',
                 'v6_positive_evidence', 'v6_reasoning', 'v6_business_model',
                 'tier1_phrases_on_site', 'company_name', 'domain')

def ringba_tainted(row):
    """Reason string if this row mentions Ringba anywhere, else '' (falsy)."""
    for f in RINGBA_FIELDS:
        v = row.get(f) or ''
        m = RINGBA_RE.search(v)
        if m:
            s = max(0, m.start() - 40); e = min(len(v), m.end() + 40)
            return '%s: ...%s...' % (f, v[s:e].replace('\n', ' '))
    return ''


def plausible_name(nm):
    nm = re.sub(r'\s+', ' ', nm).strip()
    if not (4 < len(nm) < 40): return None
    if NAME_STOP.search(nm): return None
    parts = nm.replace('&', ' ').split()
    if len(parts) < 2: return None
    return nm
CELL_RE = re.compile(r'\b(cell|mobile|text\s*me|txt\s*me|text\s*or\s*call|call\s*or\s*text|whatsapp|'
                     r'my\s+direct|direct\s+line|reach\s+me|contact\s+me\s+directly|message\s+me)\b', re.I)
ROLE_LOCALS = {'info', 'sales', 'support', 'contact', 'contactus', 'admin', 'hello', 'hi', 'team',
    'help', 'careers', 'jobs', 'hr', 'billing', 'accounts', 'noreply', 'no-reply', 'office',
    'enquiries', 'inquiries', 'mail', 'marketing', 'media', 'press', 'legal', 'privacy',
    'partners', 'partnerships', 'affiliates', 'publishers', 'buyers', 'leads', 'offers', 'general',
    'reception', 'service', 'services', 'compliance', 'ops', 'operations', 'success', 'accounting', 'partner',
    'affiliate', 'publisher', 'buyer', 'data', 'sales1', 'sales2', 'apply', 'payouts', 'payments', 'onboarding'}
SOCIAL = {'facebook.com', 'linkedin.com', 'twitter.com', 'x.com', 'instagram.com', 'youtube.com', 'tiktok.com',
          'google.com', 'apple.com', 'wixsite.com', 'wix.com', 'squarespace.com', 'godaddy.com', 'cloudflare.com',
          'w3.org', 'schema.org', 'gstatic.com', 'jquery.com', 'bootstrapcdn.com', 'fontawesome.com', 'calendly.com',
          'hubspot.com', 'typeform.com', 'jotform.com', 'mailchimp.com', 'zoom.us', 'vimeo.com', 'wistia.com'}
def _load_known():
    p = os.path.join(ROOT, 'state', 'known_domains.txt')
    try: return set(x.strip() for x in io.open(p, encoding='utf-8') if x.strip())
    except Exception: return set()
KNOWN_INDEX = _load_known()
PAGE_HINT = re.compile(r'(about|team|contact|leadership|our-story|who-we-are|founder|management|staff|meet|people)', re.I)
PROBE = ['/about', '/about-us', '/team', '/our-team', '/contact', '/contact-us', '/leadership',
         '/meet-the-team', '/publishers', '/partners']

def region_for(domain, geo):
    g = (geo or '').lower()
    if 'united kingdom' in g or domain.endswith('.uk'): return 'GB'
    if 'canada' in g or domain.endswith('.ca'): return 'CA'
    if 'australia' in g or domain.endswith('.au'): return 'AU'
    return 'US'

def classify_phone(raw, region):
    try: p = phonenumbers.parse(raw, region)
    except Exception: return None, 'unparseable', ''
    e164 = phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)
    nat = str(p.national_number)
    if region in ('US', 'CA'):
        if len(nat) != 10: return e164, 'invalid', 'not 10 NANP digits'
        if nat[3:6] == '555': return e164, 'invalid', '555 placeholder'
        if nat[:3] in TOLL: return e164, 'toll_free', 'toll-free switchboard'
    if not phonenumbers.is_valid_number(p): return e164, 'invalid', 'fails libphonenumber'
    nt = number_type(p)
    kind = ('mobile' if nt == PhoneNumberType.MOBILE else 'fixed_or_voip'
            if nt in (PhoneNumberType.FIXED_LINE, PhoneNumberType.VOIP, PhoneNumberType.FIXED_LINE_OR_MOBILE) else 'other')
    return e164, 'valid', '%s (%s)' % (geocoder.description_for_number(p, 'en') or region, kind)

def fetch_company_pages(d):
    home_url, home_raw = None, ''
    for cand in ('https://' + d, 'https://www.' + d, 'http://' + d):
        fu, raw, e = L.http_get(cand, timeout=12)
        if raw and len(raw) > 300: home_url, home_raw = fu, raw; break
    if not home_raw: return []
    pages = [(home_url, home_raw)]
    picked = []
    for u in L.page_links(home_raw, home_url):
        try:
            if L.reg_domain(urlparse(u).netloc) != d: continue
        except Exception: continue
        if PAGE_HINT.search(urlparse(u).path or '') and u not in picked: picked.append(u)
    base = home_url.rstrip('/')
    for p in PROBE:
        if base + p not in picked: picked.append(base + p)
    for u in picked[:12]:
        fu, raw, e = L.http_get(u, timeout=10)
        if raw and len(raw) > 300 and all(fu != x[0] for x in pages): pages.append((fu, raw))
    return pages

def mine_company(row):
    d = row['domain']; region = region_for(d, row.get('geography', ''))
    pages = fetch_company_pages(d)
    phones, emails, licos, lipers, names, cells = {}, set(), set(), set(), [], set()
    person_phone = {}          # e164 -> (name/email, evidence)
    for fu, raw in pages:
        txt = L.visible_text(raw)
        for m in LI_COMPANY.findall(raw): licos.add(m.split('?')[0].rstrip('/'))
        for m in LI_PERSON.findall(raw): lipers.add(m.split('?')[0].rstrip('/'))
        for m in MAILTO.findall(raw): emails.add(m.lower())
        for m in EMAIL_TXT.findall(txt):
            if not m.lower().endswith(('.png', '.jpg', '.svg', '.gif', '.webp')): emails.add(m.lower())
        sms_nums = set(x.strip() for x in SMS.findall(raw))
        cands = [(x.strip(), 'tel: href') for x in TEL.findall(raw)]
        cands += [(x.strip(), 'page text') for x in PHONE_TXT.findall(txt) if len(re.sub(r'\D', '', x)) >= 9]
        for rawnum, src in cands:
            e164, status, detail = classify_phone(rawnum, region)
            if not e164: continue
            rank = {'valid': 0, 'toll_free': 1, 'invalid': 2}.get(status, 3)
            if e164 not in phones or rank < phones[e164][0]:
                phones[e164] = (rank, status, detail, src)
            if status != 'valid': continue
            # personal-line evidence: sms: link, or "cell/text me" language within 160 chars,
            # or a person email / capitalised name within 320 chars
            i = txt.find(rawnum)
            window = txt[max(0, i - 160): i + 160] if i >= 0 else ''
            wide = txt[max(0, i - 320): i + 320] if i >= 0 else ''
            if rawnum in sms_nums or CELL_RE.search(window): cells.add(e164)
            pe = [m for m in EMAIL_TXT.findall(wide) if m.split('@')[0].lower() not in ROLE_LOCALS]
            nm = NAME_BEFORE.findall(wide) + NAME_AFTER.findall(wide)
            if pe or nm:
                person_phone.setdefault(e164, ((nm[0] if nm else pe[0]), 'name/email within 320 chars'))
        for rx in (NAME_BEFORE, NAME_AFTER, NAME_PROSE, NAME_FOUNDED_BY):
            for m in rx.findall(txt):
                nm = plausible_name(m if isinstance(m, str) else m[0])
                if nm and nm not in names: names.append(nm)
        # "Our Founder / Tim believes..." -> first name only, kept as a weak lead
        for m in re.finditer(r'(?i)\bour\s+(?:founder|owner|ceo)\b[\s,:\-–—]*\n?\s*([A-Z][a-z]{2,15})\b(?![a-z])', txt):
            fn = m.group(1)
            if not NAME_STOP.search(fn) and not any(n.startswith(fn) for n in names): names.append(fn + ' (first name only)')
    # microsite detection: a discovered domain whose pages link to a domain that is already in
    # the exclusion index is very likely a landing page / recruiting site of a KNOWN company
    # (joinoptimizetoconvert.com -> optimizetoconvert.com, 2026-09-05). Report it, don't enrich it.
    ext = collections.Counter()
    for fu, raw in pages:
        for u in L.page_links(raw, fu):
            try: ed = L.reg_domain(urlparse(u).netloc)
            except Exception: continue
            if ed and ed != d and ed not in SOCIAL and not ed.endswith(('.google.com', 'googleapis.com')): ext[ed] += 1
    core = re.sub(r'^(join|get|my|the|go|try|use|hello|team|hey|buy|sell)', '', d.split('.')[0].replace('-', ''))
    parent = [ed for ed, n in ext.most_common(15) if ed in KNOWN_INDEX and n >= 2 and
              (n >= 5 or (len(core) >= 6 and core in ed.replace('-', '')) or ed.split('.')[0].replace('-', '') in d.replace('-', ''))]
    person_emails = sorted(e for e in emails if e.split('@')[0] not in ROLE_LOCALS
                           and (e.split('@')[1] == d or e.split('@')[1].endswith('.' + d)))
    role_emails = sorted(e for e in emails if e not in person_emails)
    # the site's own name, for search queries: <title> up to the first separator
    site_title = ''
    if pages:
        for tag, s in L.headings(pages[0][1]):
            if tag == 'title' and s.strip():
                site_title = re.split(r'\s+[|\-–—:]\s+', s.strip())[0][:60]; break
    return {'domain': d, 'pages': len(pages), 'region': region, 'phones': phones, 'cells': sorted(cells),
            'site_title': site_title, 'parent_candidates': parent, 'external_links': ext.most_common(5),
            'person_phone': person_phone, 'li_company': sorted(licos), 'li_person': sorted(lipers),
            'person_emails': person_emails, 'role_emails': role_emails[:5], 'names': names[:5]}

# ------------------------------------------------------------------ stage C: Clay
# Per the clay plugin's search skill + `clay search query-mode reference`: current-employer
# lookups by domain use clay.filter_to_companies((...)); results carry name, title, company
# NAME (not domain), location — no LinkedIn URL. Managed routine "Enrich Person" (0 credits)
# resolves an email to a profile when Clay knows the person.
CLAY_ENRICH_PERSON = 'function:t_0thxfkkMDtcTV434ewG'

def clay(args, inp=None, timeout=400):
    try:
        p = subprocess.run(['wsl', '--', 'clay'] + args, input=inp, capture_output=True, text=True,
                           timeout=timeout, encoding='utf-8', errors='replace')
        return json.loads((p.stdout or '').strip())
    except Exception as e:
        return {'_err': str(e)[:200]}

def _norm_co(s):
    s = re.sub(r'[^a-z0-9]+', ' ', (s or '').lower())
    return re.sub(r'\b(llc|inc|ltd|limited|corp|co|the|group|media|marketing|solutions)\b', ' ', s).strip()

def clay_people(targets):
    """People whose CURRENT employer is one of the target domains. Company is matched back to
    a target by name similarity (Clay returns the company name, not the domain)."""
    doms = [t['domain'] for t in targets]
    by_norm = {}
    for t in targets:
        by_norm[_norm_co(t['company_name'])] = t['domain']
        by_norm[_norm_co(t['domain'].split('.')[0])] = t['domain']
    out = []
    for i in range(0, len(doms), 50):
        q = 'select from people where clay.filter_to_companies((%s))' % ', '.join('"%s"' % d for d in doms[i:i + 50])
        created = clay(['search', 'query-mode', 'create', '--query', q])
        sid = created.get('searchId') if isinstance(created, dict) else None
        if not sid:
            log('  [clay] search unavailable: %s' % json.dumps(created)[:200]); return None
        for page in range(4):
            res = clay(['search', 'query-mode', 'run', sid, '--limit', '50'])
            data = res.get('data') if isinstance(res, dict) else None
            if data is None:
                if isinstance(res, dict) and res.get('error'): log('  [clay] %s' % json.dumps(res.get('error'))[:200])
                break
            for p in data:
                me = (p.get('matched_experiences') or [{}])[0]
                co = me.get('company') if isinstance(me.get('company'), str) else (me.get('company') or {}).get('name', '')
                nco = _norm_co(co)
                dom = by_norm.get(nco) or next((d for k, d in by_norm.items() if k and (k in nco or nco in k)), '')
                loc = p.get('location') or {}
                out.append({'contact_name': p.get('name') or '', 'title': me.get('title') or '', 'domain': dom,
                            'company_name': co or '', 'linkedin_url': '', 'email': '', 'source': 'clay',
                            'clay_profile_id': p.get('clay_profile_id'), 'location': loc.get('name', '')})
            if not res.get('hasMore'): break
    return out

def clay_enrich_by_email(emails):
    """Managed 'Enrich Person' routine, 0 credits: email -> profile (LinkedIn URL, name, title)
    when Clay holds the person. Returns {email: result dict}."""
    if not emails: return {}
    body = {'items': [{'id': str(i), 'inputs': {'Email': e}} for i, e in enumerate(emails)]}
    s = clay(['routines', 'runs', 'start', CLAY_ENRICH_PERSON, '--input', '-'], json.dumps(body))
    rid = s.get('routineRunId') if isinstance(s, dict) else None
    if not rid: log('  [clay] enrich-person start failed: %s' % json.dumps(s)[:200]); return {}
    r = clay(['routines', 'runs', 'get', rid, '--wait', '180', '--limit', '100'])
    out = {}
    for it in (r.get('data') or []) if isinstance(r, dict) else []:
        res = it.get('result') or {}
        if res: out[emails[int(it['id'])]] = res
    return out

# ------------------------------------------------------------------ stage C2: LinkedIn URL via TinyFish search (free)
LI_IN = re.compile(r'https?://(?:[a-z]{2,3}\.)?linkedin\.com/in/[A-Za-z0-9._%\-]+', re.I)

def tf_search(query):
    key = os.environ.get('TINYFISH_API_KEY', '')
    import urllib.parse, urllib.request
    qs = urllib.parse.urlencode({'query': query, 'location': 'US'})
    req = urllib.request.Request('https://api.search.tinyfish.ai?' + qs, headers={'X-API-Key': key} if key else {})
    try:
        with urllib.request.urlopen(req, timeout=40) as r: return json.loads(r.read().decode('utf-8', 'replace')).get('results') or []
    except Exception as e:
        log('  [linkedin-lookup] search error %s' % type(e).__name__); return []

def find_linkedin(name, company_name, domain):
    """Accept a profile ONLY when the result title names the company (or its domain token):
    'Peter Day - Chief Executive Officer at Optimize to Convert' passes; a bare 'Brian Fife -
    Greater Boston' does not, however well the name matches."""
    name = name.replace(' (first name only)', '')
    core = re.sub(r'^(join|get|my|the|go|try|use|hello|team|hey|we|buy|sell)', '', domain.split('.')[0].replace('-', ''))
    words = [t for t in _norm_co(company_name).split() if len(t) > 3]
    last = name.split()[-1].lower()
    queries = ['"%s" "%s" linkedin' % (name, company_name)] if company_name and company_name.lower() != domain else []
    queries.append('"%s" %s linkedin' % (name, domain))
    for q in queries:
        for r in tf_search(q)[:10]:
            url = r.get('url') or ''
            if not LI_IN.match(url): continue
            title = (r.get('title') or ''); snippet = r.get('snippet') or ''
            # the person's surname must be a whole word in the result TITLE
            if not re.search(r'(?<![a-z])%s(?![a-z])' % re.escape(last), title.lower()): continue
            # and the company must be named in the title or snippet (whole words, or the
            # domain core as a compact match) - never matched against the URL
            hay = _norm_co(title + ' ' + snippet); compact = hay.replace(' ', '')
            company_named = (len(core) >= 6 and core in compact) or \
                            any(re.search(r'\b%s\b' % re.escape(w), hay) for w in words)
            if not company_named: continue
            m = re.match(r'^(.*?)\s+[-–|]\s+(.*?)(?:\s+[-–|]\s+LinkedIn)?$', title)
            title_guess = (m.group(2) if m else '').replace(' - LinkedIn', '').strip()
            return url.split('?')[0].rstrip('/'), title_guess
        time.sleep(2.2)
    return '', ''

# ------------------------------------------------------------------ Attio pre-check (read-only)
def attio_known_linkedin():
    """Every LinkedIn URL on an Attio Person record. Paginated read, no writes. Lets us skip
    LeadMagic for people the CRM already holds (2026-09-05: two founders re-bought for 10 credits)."""
    import urllib.request
    key = os.environ.get('ATTIO_API_KEY', '')
    if not key: log('   [attio] ATTIO_API_KEY missing - pre-check skipped'); return set()
    out, offset = set(), 0
    while True:
        req = urllib.request.Request('https://api.attio.com/v2/objects/people/records/query',
                                     data=json.dumps({'limit': 500, 'offset': offset}).encode(),
                                     headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=90) as r: data = json.loads(r.read()).get('data', [])
        except Exception as e:
            log('   [attio] pre-check failed: %s' % type(e).__name__); return out
        for rec in data:
            for x in rec.get('values', {}).get('linkedin') or []:
                v = (x.get('value') or '').lower().rstrip('/').replace('https://www.', 'https://')
                if v: out.add(v)
        if len(data) < 500: break
        offset += 500
    return out

# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--domains', help='comma-separated domains (default: every qualified, not yet enriched)')
    ap.add_argument('--limit', type=int, default=50)
    ap.add_argument('--include-flagged', action='store_true', help='also enrich rows with a kaliper_flags value other than geo unknown')
    ap.add_argument('--dry-run', action='store_true', help='stage A + credit estimates only; spend nothing')
    ap.add_argument('--no-aiark', action='store_true'); ap.add_argument('--no-clay', action='store_true')
    ap.add_argument('--no-leadmagic', action='store_true'); ap.add_argument('--no-trestle', action='store_true')
    a = ap.parse_args()
    load_env()
    date = time.strftime('%Y-%m-%d')
    OUT = os.path.join(ROOT, 'out', 'contacts', date); os.makedirs(OUT, exist_ok=True)

    done = set()
    if os.path.exists(ENRICHED):
        for line in io.open(ENRICHED, encoding='utf-8'):
            try: done.add(json.loads(line)['domain'])
            except Exception: pass
    allq = rd(ALLQ)
    if a.domains:
        want = set(x.strip().lower() for x in a.domains.split(','))
        targets = [r for r in allq if r['domain'] in want]
    else:
        targets = [r for r in allq if r['domain'] not in done
                   and (a.include_flagged or r.get('kaliper_flags', '') in ('', 'geo unknown'))]

    # Kaliper is PERMANENTLY banned from Ringba, so a Ringba company can never be worked -
    # no sourcing, no enrichment, no dial list. The kaliper_flags gate above happens to catch
    # "REVIEW: names Ringba in prose" rows, but BOTH --include-flagged and --domains walk
    # straight past it, and neither ever looked at infrastructure_detected. This screen runs
    # after both branches, reads every field the evidence can land in, and is deliberately
    # not overridable - it sits immediately before the first paid call (AI Ark, Clay,
    # LeadMagic, Trestle) and before the Attio push.
    banned = [r for r in targets if ringba_tainted(r)]
    if banned:
        log('\n!! RINGBA GATE: dropping %d company(ies) - Kaliper is banned from Ringba' % len(banned))
        for r in banned:
            log('   DROP %-32s %s' % (r['domain'], ringba_tainted(r)))
        targets = [r for r in targets if not ringba_tainted(r)]

    targets = targets[:a.limit]
    if not targets: log('nothing to enrich (all qualified companies already processed)'); return
    log('=== contact enrichment %s | %d companies%s' % (date, len(targets), ' | DRY RUN' if a.dry_run else ''))
    for r in targets: log('   %-30s fit=%s %s' % (r['domain'], r['v6_fit_score'], (r['v6_business_model'] or '')[:50]))

    # ---- A. mine own pages (free)
    log('\n--- A. mining company pages (free)')
    mined = {}
    microsites = []
    for r in list(targets):
        m = mine_company(r); mined[r['domain']] = m
        valid = [e for e, v in m['phones'].items() if v[1] == 'valid']
        log('   %-30s pages=%-2d phones=%d(valid %d) cells=%d person-emails=%d li-people=%d names=%s%s' % (
            r['domain'], m['pages'], len(m['phones']), len(valid), len(m['cells']),
            len(m['person_emails']), len(m['li_person']), '; '.join(m['names'][:2]) or '-',
            ('  ** links to KNOWN company %s -> microsite, not enriched' % ', '.join(m['parent_candidates'])) if m['parent_candidates'] else ''))
        if m['parent_candidates']:
            microsites.append({**r, 'parent_domain': '; '.join(m['parent_candidates'])}); targets.remove(r)
    if microsites:
        wr(os.path.join(OUT, 'microsites_of_known_companies.csv'), microsites)
    if not targets: log('every company was a microsite of a known company; nothing to enrich'); return

    people = []          # candidate persons across sources
    for r in targets:
        m = mined[r['domain']]
        # a usable display name: the qualified list's name, else the site's own <title>
        if not r['company_name'] or len(r['company_name']) < 4 or r['company_name'].lower() == r['domain']:
            r['company_name'] = m['site_title'] or r['company_name'] or ''
        cname = r['company_name'] or r['domain']
        for nm in m['names']:
            people.append({'contact_name': nm, 'title': 'owner/leader (site)', 'company_name': cname,
                           'domain': r['domain'], 'linkedin_url': '', 'email': '', 'source': 'site:name'})
        for li in m['li_person'][:3]:
            people.append({'contact_name': '', 'title': '', 'company_name': cname, 'domain': r['domain'],
                           'linkedin_url': li, 'email': '', 'source': 'site:linkedin'})
        for em in m['person_emails'][:3]:
            local = em.split('@')[0]
            guess = local.replace('.', ' ').replace('_', ' ').title()
            # brian@ + "Brian Fife" on the same site -> one person, not two
            full = next((n for n in m['names'] if n.split()[0].lower() == local.split('.')[0].lower()), None)
            if full:
                for p in people:
                    if p['domain'] == r['domain'] and p['contact_name'] == full and not p['email']:
                        p['email'] = em; p['source'] += '+email'; break
                continue
            people.append({'contact_name': guess, 'title': '', 'company_name': cname,
                           'domain': r['domain'], 'linkedin_url': '', 'email': em, 'source': 'site:email'})

    # ---- B. AI Ark decision makers (paid)
    accounts = wr(os.path.join(OUT, 'accounts.csv'), [{'company_name': r['company_name'] or r['domain'], 'domain': r['domain']} for r in targets],
                  ['company_name', 'domain'])
    if not a.no_aiark:
        log('\n--- B. AI Ark decision makers%s' % (' (dry run: cost estimate only)' if a.dry_run else ''))
        cmd = [PY, AIARK, '--input', accounts, '--titles', TITLES, '--country', COUNTRIES,
               '--max-per-company', '3', '--output', os.path.join(OUT, 'aiark.csv')]
        cmd += ['--dry-run'] if a.dry_run else ['--yes']
        rc, out = run(cmd)
        if not a.dry_run:
            for p in rd(os.path.join(OUT, 'aiark.csv')):
                if (p.get('contact_name') or '').strip():
                    people.append({'contact_name': p['contact_name'], 'title': p.get('title', ''), 'company_name': p.get('company_name', ''),
                                   'domain': (p.get('domain') or '').lower(), 'linkedin_url': p.get('linkedin_url', ''),
                                   'email': '', 'source': 'ai_ark', 'qa_country': p.get('qa_actual_country', ''),
                                   'qa_size': p.get('qa_actual_company_size_total', '')})
            log('   AI Ark returned %d people' % sum(1 for p in people if p['source'] == 'ai_ark'))

    # ---- C. Clay (search is free; Enrich Person by email is 0 credits)
    if not a.no_clay and not a.dry_run:
        log('\n--- C. Clay: people whose current employer is one of these domains')
        cp = clay_people(targets)
        if cp is not None:
            wr(os.path.join(OUT, 'clay_raw.csv'), cp) if cp else None
            # Kaliper's ICP is 1-20 staff. If Clay shows a big current headcount, the company is
            # probably over-size (Melon Local: 40+ staff, 2026-09-06): flag it and keep only the
            # founder / C-level rather than every Director.
            headcount = collections.Counter(p['domain'] for p in cp if p['domain'])
            oversize = {d for d, n in headcount.items() if n > 20}
            for d in oversize:
                log('   ** %s: Clay lists %d current employees - over Kaliper\'s 1-20 ICP; keeping founders/C-level only' % (d, headcount[d]))
            EXEC = re.compile(r'\b(founder|co-?founder|owner|ceo|chief|president|managing director|managing partner)\b', re.I)
            n = 0
            for p in cp:
                ok = p['domain'] and KEEP.search(p['title'] or '') and not DROP.search(p['title'] or '')
                if ok and p['domain'] in oversize and not EXEC.search(p['title'] or ''): ok = False
                if p['domain'] in oversize: p['oversize'] = headcount[p['domain']]
                log('   %-22s %-32s @ %-26s %-22s %s' % ((p['contact_name'] or '')[:22], (p['title'] or '')[:32],
                    (p['company_name'] or '')[:26], (p['location'] or '')[:22], 'KEEP' if ok else 'drop'))
                if ok: people.append(p); n += 1
            log('   Clay: %d raw, %d kept after persona filter (raw saved to clay_raw.csv)' % (len(cp), n))
        emails = sorted(set(p['email'] for p in people if p.get('email')))
        if emails:
            hits = clay_enrich_by_email(emails)
            log('   Clay Enrich Person by email: %d of %d emails known' % (len(hits), len(emails)))
            for p in people:
                h = hits.get(p.get('email'))
                if h:
                    p['linkedin_url'] = p['linkedin_url'] or h.get('LinkedIn URL') or h.get('linkedin_url') or ''
                    p['title'] = p['title'] or h.get('Job Title') or h.get('title') or ''
                    p['contact_name'] = h.get('Full Name') or h.get('name') or p['contact_name']

    # ---- C2. LinkedIn URL lookup (free, TinyFish search) for named people without one
    if not a.dry_run:
        need = [p for p in people if p.get('contact_name') and len(p['contact_name'].split()) >= 2
                and not p.get('linkedin_url') and '(first name only)' not in p['contact_name']]
        if need:
            log('\n--- C2. LinkedIn URL lookup via search for %d named people (company must appear in the result)' % len(need))
            for p in need:
                if '&' in p['contact_name']:            # "Peter & Tyler Day" -> two people
                    first_parts, last = p['contact_name'].rsplit(' ', 1)
                    firsts = [x.strip() for x in first_parts.split('&')]
                    p['contact_name'] = '%s %s' % (firsts[0], last)
                    for f in firsts[1:]:
                        people.append(dict(p, contact_name='%s %s' % (f, last), linkedin_url=''))
                        need.append(people[-1])
                url, tguess = find_linkedin(p['contact_name'], p['company_name'], p['domain'])
                if url:
                    p['linkedin_url'] = url; p['title'] = p['title'] if p['title'] and 'site' not in p['title'] else (tguess or p['title'])
                    p['source'] += '+linkedin-search'
                log('   %-26s %-28s -> %s %s' % (p['contact_name'][:26], p['domain'][:28], url or 'no confident match', ('(%s)' % tguess) if tguess else ''))

    # ---- persona filter + dedupe people (by linkedin, else name+domain)
    keep = []
    seen = set()
    for p in people:
        t = p.get('title') or ''
        if t and p['source'] != 'site:name' and (DROP.search(t) or not KEEP.search(t)): continue
        key = (p['linkedin_url'].lower().rstrip('/') if p.get('linkedin_url') else '') or (p['contact_name'].lower(), p['domain'])
        if key in seen: continue
        seen.add(key); keep.append(p)
    people = keep
    log('\n   %d candidate people across sources (after persona filter + dedupe)' % len(people))

    # ---- D. LeadMagic mobiles (paid) on people with a LinkedIn URL or personal email
    attio_li = attio_known_linkedin() if not a.dry_run else set()
    for p in people:
        li = (p.get('linkedin_url') or '').lower().rstrip('/').replace('https://www.', 'https://')
        if li and li in attio_li: p['already_in_attio'] = True
    n_known = sum(1 for p in people if p.get('already_in_attio'))
    if n_known: log('   %d of these people are ALREADY in Attio (matched on LinkedIn URL) - not sent to LeadMagic' % n_known)
    lm_in = [p for p in people if (p.get('linkedin_url') or p.get('email')) and not p.get('already_in_attio')]
    if lm_in and not a.no_leadmagic:
        log('\n--- D. LeadMagic mobile enrichment: %d people with a match key (worst case %d credits)' % (len(lm_in), 5 * len(lm_in)))
        if not a.dry_run:
            src = wr(os.path.join(OUT, 'leadmagic_in.csv'), lm_in,
                     ['contact_name', 'title', 'company_name', 'domain', 'linkedin_url', 'email', 'source'])
            rc, out = run([PY, LEADMAGIC, '--input', src, '--output', os.path.join(OUT, 'leadmagic_out.csv'), '--yes'])
            byk = {}
            for r in rd(os.path.join(OUT, 'leadmagic_out.csv')):
                k = (r.get('linkedin_url') or '').lower().rstrip('/') or ((r.get('contact_name') or '').lower(), r.get('domain'))
                byk[k] = r
            for p in people:
                k = (p.get('linkedin_url') or '').lower().rstrip('/') or (p['contact_name'].lower(), p['domain'])
                r = byk.get(k)
                if r:
                    p['mobile_phone'] = r.get('mobile_phone', ''); p['mobile_status'] = r.get('phone_status', '')
                    p['mobile_detail'] = r.get('phone_detail', ''); p['data_provider'] = r.get('data_provider', '')
            log('   LeadMagic valid mobiles: %d' % sum(1 for p in people if p.get('mobile_status') == 'valid'))

    # ---- attach site-mined phones to people / companies
    phone_owner = collections.defaultdict(set)
    for d, m in mined.items():
        for e, v in m['phones'].items():
            if v[1] == 'valid': phone_owner[e].add(d)
    for p in people:
        if p.get('mobile_phone'): phone_owner[p['mobile_phone']].add(p['domain'])
    company_lines = []
    for r in targets:
        m = mined[r['domain']]
        for e, v in m['phones'].items():
            if v[1] != 'valid': continue
            shared = len(phone_owner[e]) > 1
            personal = e in m['cells'] or e in m['person_phone']
            company_lines.append({'company_name': r['company_name'], 'domain': r['domain'], 'e164': e,
                                  'detail': v[2], 'found_via': v[3],
                                  'personal_evidence': ('sms/cell language' if e in m['cells'] else '') +
                                                       ((' ' + m['person_phone'][e][1] + ': ' + str(m['person_phone'][e][0])) if e in m['person_phone'] else ''),
                                  'shared_across_companies': 'YES - switchboard/farm' if shared else '',
                                  'classification': 'shared_switchboard' if shared else ('likely_personal' if personal else 'company_line')})

    # ---- E. Trestle validation (paid) on every candidate number
    nums = []
    for p in people:
        if p.get('mobile_status') == 'valid': nums.append({'e164': p['mobile_phone'], 'kind': 'mobile', 'domain': p['domain'], 'who': p['contact_name']})
    for c in company_lines:
        if c['classification'] != 'shared_switchboard': nums.append({'e164': c['e164'], 'kind': c['classification'], 'domain': c['domain'], 'who': ''})
    uniq = {}
    for n in nums: uniq.setdefault(n['e164'], n)
    nums = list(uniq.values())
    trestle = {}
    if nums and not a.no_trestle:
        log('\n--- E. Trestle validation: %d numbers (~$%.2f)' % (len(nums), 0.015 * len(nums)))
        if not a.dry_run:
            src = wr(os.path.join(OUT, 'trestle_in.csv'), nums, ['e164', 'kind', 'domain', 'who'])
            rc, out = run([PY, TRESTLE, 'run', '--input', src, '--output', os.path.join(OUT, 'trestle_out.csv'),
                           '--run-dir', OUT, '--phone-column', 'e164', '--yes'])
            for r in rd(os.path.join(OUT, 'trestle_out.csv')):
                trestle[r['e164']] = r
            log('   Trestle: %d of %d numbers dialable (well-formed AND not flagged skip/disconnected)' % (
                sum(1 for r in trestle.values() if str(r.get('trestle_is_valid', '')).lower() in ('true', '1', 'yes')
                    and not str(r.get('trestle_recommendation', '')).lower().startswith('skip')), len(trestle)))

    # ---- F. assemble
    def tres(e):
        r = trestle.get(e, {})
        return (str(r.get('trestle_is_valid', '')), r.get('trestle_recommendation', ''), r.get('trestle_line_type', ''))
    def tres_extra(e):
        r = trestle.get(e, {})
        return {k: r.get(k, '') for k in ('trestle_activity_score', 'trestle_carrier', 'trestle_validated_at')}
    def phone_ok(e):
        """Trestle 'is_valid' only says the number is well-formed; the recommendation carries
        the activity score. A 'skip' recommendation = disconnected/low activity -> not dialable."""
        if not e: return False
        if not trestle: return True
        r = trestle.get(e)
        if not r: return True
        return str(r.get('trestle_is_valid', '')).lower() in ('true', '1', 'yes') and not str(r.get('trestle_recommendation', '')).lower().startswith('skip')
    attio, all_people = [], []
    by_domain = collections.defaultdict(list)
    for p in people:
        mob = p.get('mobile_phone') if p.get('mobile_status') == 'valid' else ''
        if mob and len(phone_owner[mob]) > 1: mob = ''             # shared across companies -> not personal
        tv, trec, tlt = tres(mob) if mob else ('', '', '')
        row = {'company_name': p['company_name'], 'domain': p['domain'], 'contact_name': p['contact_name'],
               'title': p.get('title', ''), 'linkedin_url': p.get('linkedin_url', ''), 'phone': mob,
               'email': p.get('email', ''), 'company_notes': '', 'source': p['source'],
               'mobile_status': p.get('mobile_status', ''), 'data_provider': p.get('data_provider', ''),
               'trestle_is_valid': tv, 'trestle_recommendation': trec, 'trestle_line_type': tlt,
               'qa_country': p.get('qa_country', ''), 'qa_company_size': p.get('qa_size', '')}
        all_people.append(row); by_domain[p['domain']].append(row)
    # a company-level personal line with no named person still beats nothing: attach as note
    for r in targets:
        d = r['domain']; lines = [c for c in company_lines if c['domain'] == d]
        note = '; '.join('%s %s [%s]' % (c['e164'], c['classification'], c['detail']) for c in lines)
        for row in by_domain[d]: row['company_notes'] = note
        if not by_domain[d] and lines:
            best = sorted(lines, key=lambda c: {'likely_personal': 0, 'company_line': 1, 'shared_switchboard': 2}[c['classification']])[0]
            m = mined[d]
            who = str(m['person_phone'].get(best['e164'], ('', ''))[0]) if best['e164'] in m['person_phone'] else ''
            tv, trec, tlt = tres(best['e164'])
            all_people.append({'company_name': r['company_name'], 'domain': d, 'contact_name': who, 'title': 'owner/operator (unnamed)' if not who else '',
                               'linkedin_url': (m['li_person'][:1] or [''])[0], 'phone': best['e164'] if best['classification'] != 'shared_switchboard' else '',
                               'email': (m['person_emails'][:1] or m['role_emails'][:1] or [''])[0], 'company_notes': note,
                               'source': 'site:' + best['classification'], 'mobile_status': '', 'data_provider': 'site',
                               'trestle_is_valid': tv, 'trestle_recommendation': trec, 'trestle_line_type': tlt, 'qa_country': '', 'qa_company_size': ''})
    known_li = set(p.get('linkedin_url', '').lower().rstrip('/') for p in people if p.get('already_in_attio'))
    for row in all_people:
        if known_li and row.get('linkedin_url', '').lower().rstrip('/') in known_li:
            row['source'] += ' (ALREADY IN ATTIO - not pushed)'; row['phone'] = ''; row['linkedin_url'] = ''
        if not phone_ok(row['phone']): row['phone'] = ''          # keep the row, drop the dead number
        if row['phone'] or (row['contact_name'] and row['linkedin_url'] and '(first name only)' not in row['contact_name']):
            attio.append(row)
    no_contact = [r for r in targets if not any(x['domain'] == r['domain'] for x in all_people)]

    cols = ['company_name', 'domain', 'contact_name', 'title', 'linkedin_url', 'phone', 'email', 'company_notes',
            'source', 'mobile_status', 'data_provider', 'trestle_is_valid', 'trestle_recommendation', 'trestle_line_type',
            'trestle_activity_score', 'trestle_carrier', 'trestle_validated_at', 'qa_country', 'qa_company_size']
    for row in all_people: row.update(tres_extra(row['phone']))
    # Upload-leads-to-attio refuses unknown columns; this is exactly the set it maps
    ATTIO_COLS = ['company_name', 'domain', 'contact_name', 'title', 'linkedin_url', 'phone', 'email', 'company_notes',
                  'data_provider', 'trestle_is_valid', 'trestle_line_type', 'trestle_activity_score', 'trestle_carrier', 'trestle_validated_at']
    wr(os.path.join(OUT, 'contacts_for_attio.csv'), attio, ATTIO_COLS)
    wr(os.path.join(OUT, 'people_all.csv'), all_people, cols)
    wr(os.path.join(OUT, 'company_lines.csv'), company_lines)
    wr(os.path.join(OUT, 'companies_no_contact.csv'), no_contact, list(targets[0].keys()))

    dialable = sum(1 for r in attio if r['phone'])
    named = sum(1 for r in attio if r['contact_name'] and not r['phone'])
    S = ['# Contact enrichment — %s%s' % (date, ' (DRY RUN)' if a.dry_run else ''), '',
         '| stage | result |', '|---|---|',
         '| companies in | %d |' % len(targets),
         '| site mining: companies with a valid phone on their own pages | %d |' % sum(1 for d, m in mined.items() if any(v[1] == 'valid' for v in m['phones'].values())),
         '| site mining: companies with a personal-line signal | %d |' % sum(1 for m in mined.values() if m['cells'] or m['person_phone']),
         '| candidate people (all sources, persona-filtered) | %d |' % len(people),
         '|   from AI Ark | %d |' % sum(1 for p in people if p['source'] == 'ai_ark'),
         '|   from Clay | %d |' % sum(1 for p in people if p['source'] == 'clay'),
         '|   from the company site | %d |' % sum(1 for p in people if p['source'].startswith('site')),
         '| LeadMagic valid mobiles | %d |' % sum(1 for p in people if p.get('mobile_status') == 'valid'),
         '| Trestle-checked numbers | %d |' % len(trestle),
         '| **rows for Attio** | **%d** (%d with a phone, %d named without) |' % (len(attio), dialable, named),
         '| companies with nothing at all | %d |' % len(no_contact), '',
         '## Rows for Attio', '', '| company | contact | title | phone | trestle | source |', '|---|---|---|---|---|---|']
    for r in attio: S.append('| %s | %s | %s | %s | %s | %s |' % (r['domain'], r['contact_name'], (r['title'] or '')[:30], r['phone'], r['trestle_recommendation'] or r['trestle_is_valid'], r['source']))
    S += ['', '## Next (manual, outward-facing — not run by this script)', '', '```',
          'cd "%s"' % REL,
          'python .claude/skills/Upload-leads-to-attio/upload_to_attio.py --client Kaliper --file "%s" --no-archive --dry-run --yes' % os.path.join(OUT, 'contacts_for_attio.csv'),
          'python .claude/skills/Upload-leads-to-attio/upload_to_attio.py --client Kaliper --file "%s" --no-archive --check-existing' % os.path.join(OUT, 'contacts_for_attio.csv'),
          'python scripts/ledger_append.py contacts --input "%s" --date %s --run ppc-daily-contacts-%s --ledger "<path to account_ledger.csv>"' % (os.path.join(OUT, 'contacts_for_attio.csv'), date, date),
          '```']
    io.open(os.path.join(OUT, 'summary.md'), 'w', encoding='utf-8').write('\n'.join(S) + '\n')
    log('\n' + '\n'.join(S))

    if not a.dry_run:
        with io.open(ENRICHED, 'a', encoding='utf-8') as f:
            for r in targets:
                rows = [x for x in all_people if x['domain'] == r['domain']]
                status = ('dialable' if any(x['phone'] for x in rows) else 'named_no_phone' if any(x['contact_name'] for x in rows) else 'no_contact_data')
                f.write(json.dumps({'domain': r['domain'], 'date': date, 'status': status, 'people': len(rows)}) + '\n')
        log('\nrecorded %d companies in state/enriched.jsonl; outputs in %s' % (len(targets), OUT))

if __name__ == '__main__':
    main()
