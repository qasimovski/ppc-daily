# -*- coding: utf-8 -*-
"""Shared library: fetching, phrase detection, infra fingerprinting, classification."""
import html as htmllib, json, os, re, ssl, time, urllib.parse, urllib.request, urllib.error
from urllib.parse import urlparse, urljoin

ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ROOT, 'cache', 'pages')
os.makedirs(CACHE, exist_ok=True)
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

# ---------------------------------------------------------------- domain utils
MULTI_SLD = {'co.uk','org.uk','ac.uk','gov.uk','co.nz','co.za','com.au','net.au','org.au',
             'co.in','com.br','com.mx','co.jp','com.sg','com.ph','co.il','com.tr','com.ua'}

def reg_domain(h):
    h = (h or '').strip().lower()
    if '://' in h: h = urlparse(h).netloc
    h = h.split('/')[0].split(':')[0]
    if h.startswith('www.'): h = h[4:]
    p = h.split('.')
    if len(p) > 2 and '.'.join(p[-2:]) in MULTI_SLD: return '.'.join(p[-3:])
    return '.'.join(p[-2:]) if len(p) >= 2 else h

# ---------------------------------------------------------------- robots
_ROBOTS = {}

def robots_allows(url):
    """Conservative: block only when a Disallow rule for * clearly matches."""
    try:
        pr = urlparse(url); base = pr.scheme + '://' + pr.netloc
        if base not in _ROBOTS:
            try:
                req = urllib.request.Request(base + '/robots.txt', headers={'User-Agent': UA})
                with urllib.request.urlopen(req, timeout=12, context=CTX) as r:
                    txt = r.read(120000).decode('utf-8', 'replace')
            except Exception:
                txt = ''
            rules, cur = [], False
            for line in txt.splitlines():
                line = line.split('#')[0].strip()
                if not line or ':' not in line: continue
                k, v = line.split(':', 1); k = k.strip().lower(); v = v.strip()
                if k == 'user-agent': cur = (v == '*')
                elif k == 'disallow' and cur and v: rules.append(v)
            _ROBOTS[base] = rules
        path = pr.path or '/'
        for rule in _ROBOTS[base]:
            if rule == '/': return False
            if path.startswith(rule.replace('*', '')): return False
        return True
    except Exception:
        return True

# ---------------------------------------------------------------- fetch
def _cache_key(url):
    return re.sub(r'[^A-Za-z0-9._-]', '_', url)[:150] + '_' + str(abs(hash(url)) % 10**10)

def http_get(url, timeout=25, use_cache=True):
    """Plain-HTTP raw-source fetch, cached to disk. Returns (final_url, raw_html, err)."""
    cp = os.path.join(CACHE, _cache_key(url) + '.html')
    mp = cp + '.meta'
    if use_cache and os.path.exists(mp):
        try:
            meta = json.load(open(mp, encoding='utf-8'))
            body = open(cp, encoding='utf-8', errors='replace').read() if os.path.exists(cp) else ''
            return meta.get('final_url', url), body, meta.get('err')
        except Exception:
            pass
    if not robots_allows(url):
        json.dump({'final_url': url, 'err': 'robots_disallow'}, open(mp, 'w', encoding='utf-8'))
        return url, '', 'robots_disallow'
    err = None; body = ''; fu = url
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': UA,
                'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9'})
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                ct = (r.headers.get('Content-Type') or '').lower()
                raw = r.read(2500000)
                if ct and ('html' not in ct and 'xml' not in ct and 'text' not in ct):
                    err = 'non_html:' + ct[:40]; break
                body = raw.decode('utf-8', 'replace'); fu = r.geturl(); err = None; break
        except urllib.error.HTTPError as e:
            err = 'HTTP' + str(e.code)
            if e.code in (401, 402, 403, 407, 451):
                err = 'HTTP' + str(e.code) + '_blocked'; break
            if e.code in (404, 410): break
            time.sleep(1.5 * (2 ** attempt))
        except Exception as e:
            err = type(e).__name__
            time.sleep(1.5 * (2 ** attempt))
    if body:
        open(cp, 'w', encoding='utf-8').write(body)
    json.dump({'final_url': fu, 'err': err}, open(mp, 'w', encoding='utf-8'))
    return fu, body, err

# ---------------------------------------------------------------- text extraction
_SCRIPT_STRIP = re.compile(r'<(script|style|noscript|svg)\b[^>]*>.*?</\1>', re.I | re.S)
_TAG = re.compile(r'<[^>]+>')
_WS = re.compile(r'[ \t\r\f\v ]+')

def visible_text(raw):
    t = _SCRIPT_STRIP.sub(' ', raw or '')
    t = re.sub(r'<(br|/p|/div|/li|/h[1-6]|/tr|/td)\s*/?>', '\n', t, flags=re.I)
    t = _TAG.sub(' ', t)
    t = htmllib.unescape(t)
    t = _WS.sub(' ', t)
    t = re.sub(r'\n\s*\n+', '\n', t)
    return t.strip()

def headings(raw):
    out = []
    for m in re.finditer(r'<(h1|h2|h3|title)\b[^>]*>(.*?)</\1>', raw or '', re.I | re.S):
        s = _WS.sub(' ', htmllib.unescape(_TAG.sub(' ', m.group(2)))).strip()
        if s: out.append((m.group(1).lower(), s))
    return out

def page_links(raw, base):
    out = []
    for m in re.finditer(r'<a\b[^>]+href\s*=\s*["\']([^"\'#]+)', raw or '', re.I):
        try:
            u = urljoin(base, htmllib.unescape(m.group(1)).strip())
            if u.startswith('http'): out.append(u)
        except Exception:
            pass
    return out

# ---------------------------------------------------------------- TIER 1 phrases
TIER1 = ['pay per call', 'pay-per-call', 'sell calls', 'sell your calls', 'sell us your calls',
         'buy calls', 'buy inbound calls', 'we buy calls', 'live inbound calls',
         'live outbound calls', 'warm calls', 'warm transfers', 'live transfers']

_T1_RE = {}
for _p in TIER1:
    # Boundaries exclude '-', '/', '_' so a phrase buried in a URL slug
    # ('/pay-per-call-101/', '/aged-vs-pay-per-call/') is NOT counted as prose evidence.
    _T1_RE[_p] = re.compile(r'(?<![A-Za-z0-9/\-_])' + re.escape(_p).replace('\ ', '[  ]+') + r'(?![A-Za-z0-9/\-_])', re.I)

_URL_IN_TEXT = re.compile(r'(?:https?://|www\.)\S+|[A-Za-z0-9.\-]+\.(?:com|net|org|io|co|us|ca|uk|ai|agency|life|xyz|info|biz)/\S*', re.I)

def find_tier1(text):
    """Return {phrase: [verbatim sentence, ...]} for Tier-1 matches."""
    text = _URL_IN_TEXT.sub(' ', text or '')   # URLs shown as text are not prose
    hits = {}
    for p, rx in _T1_RE.items():
        for m in rx.finditer(text):
            s, e = m.start(), m.end()
            start = max(text.rfind('.', 0, s), text.rfind('\n', 0, s), text.rfind('!', 0, s)) + 1
            cands = [x for x in (text.find('.', e), text.find('\n', e)) if x != -1]
            ne = min(cands) if cands else len(text)
            sent = _WS.sub(' ', text[start:ne + 1]).strip()
            if len(sent) > 400 or len(sent) < 12:
                sent = _WS.sub(' ', text[max(0, s - 150):e + 150]).strip()
            if len(sent) < 10: continue
            hits.setdefault(p, [])
            if sent not in hits[p] and len(hits[p]) < 3:
                hits[p].append(sent)
    return hits

# ------------------------------------------------- INFRASTRUCTURE FINGERPRINTS
# Detection needles for call-routing / call-tracking / call-distribution platforms.
# STRONG = pay-per-call routing & distribution specific.
# MED    = call tracking / dynamic number insertion.
# LEADINFRA = lead compliance / affiliate distribution infra that co-occurs with call trading.
INFRA = {
    'Ringba':             (['ringba.com', 'js.ringba', 'rtb.ringba', 'ringba_tags', '_rgba_tags', 'ringba.js'], 'STRONG'),
    'Retreaver':          (['retreaver.com', 'retreaver.js', 'retreaver.campaign', 'use.retreaver'], 'STRONG'),
    'TrackDrive':         (['trackdrive.com', 'trackdrive.net', 'trackdrive.io'], 'STRONG'),
    'Phonexa':            (['phonexa.com', 'phonexa.io', 'phonexa.net'], 'STRONG'),
    'Invoca':             (['invoca.net', 'invocacdn.com', '_invoca', 'invoca.com/tag'], 'STRONG'),
    'LeadsPedia':         (['leadspedia.com', 'leadspedia.net'], 'STRONG'),
    'boberdoo':           (['boberdoo.com'], 'STRONG'),
    'LeadProsper':        (['leadprosper.io'], 'STRONG'),
    'ClickPoint':         (['clickpointsoftware.com'], 'STRONG'),
    'CallScaler':         (['callscaler.com'], 'STRONG'),
    'Marchex':            (['marchex.io', 'marchex.com', 'voicestar.com'], 'STRONG'),
    'DialogTech':         (['dialogtech.com', 'ifbyphone.com'], 'STRONG'),
    'Convirza':           (['convirza.com'], 'STRONG'),
    'RingPartner':        (['ringpartner.com'], 'STRONG'),
    'CallTools':          (['calltools.com'], 'STRONG'),
    'LeadExec':           (['leadexec.net'], 'STRONG'),
    'Databowl':           (['databowl.com'], 'STRONG'),
    'CallRail':           (['calltrk.com', 'callrail.com'], 'MED'),
    'CallTrackingMetrics': (['tctm.co', 'calltrackingmetrics.com'], 'MED'),
    'WhatConverts':       (['whatconverts.com'], 'MED'),
    'Nimbata':            (['nimbata.com'], 'MED'),
    'CallSource':         (['callsource.com'], 'MED'),
    'Infinity':           (['infinity-tracking.net', 'infinitycloud.com'], 'MED'),
    'ResponseTap':        (['responsetap.com'], 'MED'),
    'Delacon':            (['delacon.com'], 'MED'),
    'WildJar':            (['wildjar.com'], 'MED'),
    'Twilio':             (['twilio.com/js', 'taskrouter', 'twilio.js', 'sdk.twilio.com'], 'MED'),
    'TrustedForm':        (['trustedform.com', 'activeprospect.com', 'api.trustedform'], 'LEADINFRA'),
    'Jornaya/LeadiD':     (['jornaya.com', 'leadid.com', 'ldid.js'], 'LEADINFRA'),
    'BlacklistAlliance':  (['blacklistalliance.com', 'blacklistalliance.net'], 'LEADINFRA'),
    'Everflow':           (['everflow.io', 'everflowclient.io'], 'LEADINFRA'),
    'TUNE/HasOffers':     (['hasoffers.com', 'go2cloud.org'], 'LEADINFRA'),
    'Affise':             (['affise.com'], 'LEADINFRA'),
    'CAKE':               (['cakemarketing.com', 'getcake.com'], 'LEADINFRA'),
    'Trackier':           (['trackier.com'], 'LEADINFRA'),
    'Voluum':             (['voluum.com'], 'LEADINFRA'),
    'RedTrack':           (['redtrack.io'], 'LEADINFRA'),
    'ClickMagick':        (['clkmc.com', 'clickmagick.com'], 'LEADINFRA'),
    'Binom':              (['binom.org'], 'LEADINFRA'),
    'ThriveTracker':      (['thrivetracker.com'], 'LEADINFRA'),
}

def detect_infra(raw):
    low = (raw or '').lower(); found = []
    for name in INFRA:
        needles, tierk = INFRA[name]
        for n in needles:
            if n in low:
                found.append((name, tierk)); break
    return found

# ---------------------------------------------------------------- structure signals
PROBE_PATHS = ['/publishers', '/publisher', '/affiliates', '/affiliate', '/partners',
    '/buyers', '/advertisers', '/media-partners', '/for-publishers', '/for-buyers',
    '/become-a-publisher', '/network', '/how-it-works', '/services', '/pricing',
    '/careers', '/jobs', '/about', '/contact', '/offers', '/verticals',
    '/sell-calls', '/buy-calls', '/publisher-agreement', '/terms', '/terms-of-service',
    '/terms-and-conditions', '/join', '/apply', '/solutions', '/what-we-do']

CP_URL_RE = re.compile(r'/(publisher|affiliate|media[-_]?partner|buyer|advertiser|become-a-publisher|sell-calls|buy-calls|for-publishers|for-buyers|for-advertisers|partners)', re.I)

CP_TEXT = ['become a publisher', 'become an affiliate', 'apply as a publisher', 'publisher application',
    'affiliate application', 'for publishers', 'for buyers', 'for advertisers', 'our publishers',
    'our buyers', 'publisher agreement', 'affiliate agreement', 'media partners', 'publisher portal',
    'affiliate portal', 'buyer portal', 'payout terms', 'top payouts', 'payout schedule',
    'sign up as a publisher', 'join our network', 'apply to our network', 'publisher support',
    'affiliate manager', 'publisher manager', 'call buyers', 'call sellers', 'send us your calls',
    'we have buyers', 'we have publishers', 'publishers and advertisers', 'buyers and publishers',
    'publisher login', 'affiliate login', 'advertiser login', 'buyer login', 'partner with us',
    'become a partner', 'media buyers', 'traffic partners', 'as a publisher', 'as a buyer']

PRICING_TEXT = ['cost per call', 'price per call', 'payout per call', 'per call basis', 'per-call basis',
    'pay per qualified call', 'billable call', 'billable calls', 'qualified call', 'call duration',
    'duration of the call', 'calls lasting', 'connected call', 'call length', 'minimum call duration',
    'billable duration', 'only pay for calls', 'pay only for calls', 'paid per call', 'revenue per call',
    'buyer bid', 'bid on calls', 'call auction', 'per inbound call', 'for every call', 'each qualified call',
    'per billable call', 'flat fee per call', 'fixed price per call', 'you only pay when']

PINGPOST_TEXT = ['ping post', 'ping/post', 'ping-post', 'ping tree', 'call routing', 'routing rules',
    'call concurrency', 'concurrency caps', 'ivr', 'duplicate policy', 'chargeback', 'call scrubbing',
    'call filtering', 'return policy', 'litigator scrub', 'dnc scrub', 'tcpa compliant', 'call caps',
    'geo routing', 'skill based routing', 'round robin', 'buyer caps', 'daily caps']

AGREEMENT_TEXT = ['publisher agreement', 'affiliate terms', 'insertion order', 'billable call',
    'call is billable', 'qualified call is defined', 'call shall be deemed', 'chargeback', 'clawback',
    'payout will be paid', 'net 15', 'net 30', 'net 7']

JOB_TEXT = ['pay per call manager', 'publisher manager', 'affiliate manager', 'media buyer',
    'call buyer', 'ringba', 'retreaver', 'trackdrive', 'phonexa', 'we are hiring', 'open positions',
    'join our team', 'current openings']

# ---------------------------------------------------------------- exclusions
EXCL = {
    'ppc_seo_agency': (['pay per click', 'pay-per-click', 'google ads management', 'adwords management',
        'seo services', 'search engine optimization services', 'link building', 'social media management',
        'web design services', 'ppc management', 'paid search management', 'google ads agency',
        'meta ads agency', 'seo agency', 'content marketing services', 'email marketing services',
        'branding services', 'graphic design services', 'website development'], 4),
    'call_center_bpo': (['bpo', 'business process outsourcing', 'outsourced call center', 'call center services',
        'answering service', 'virtual assistant', 'per agent', 'per seat', 'agent seats', 'dedicated agents',
        'offshore agents', 'staffing solutions', 'customer support outsourcing', 'inbound call center services',
        'telemarketing services', 'cold calling services', 'appointment setting services', 'our agents',
        'trained agents', 'seat pricing', 'hourly rate'], 4),
    'voip_pbx': (['cloud pbx', 'hosted pbx', 'sip trunk', 'sip trunking', 'voip provider',
        'unified communications', 'ucaas', 'business phone system', 'pbx system', 'wholesale voip',
        'a-z termination', 'sip termination', 'softswitch', 'did numbers', 'voip minutes'], 3),
    'widget_vendor': (['click to call widget', 'callback widget', 'chat widget', 'live chat software',
        'chatbot platform', 'website chat', 'call back button', 'chat plugin'], 3),
    'calltracking_saas': (['call tracking software', 'call tracking platform', 'start your free trial',
        'free 14-day trial', 'free trial no credit card', 'per month billed annually',
        'call analytics platform', 'conversation intelligence platform', 'our platform', 'api documentation',
        'developer docs', 'integrations directory', 'no credit card required'], 4),
    # AI voice-agent / virtual-receptionist SaaS: uses counterparty vocabulary but sells software
    'ai_voice_agent': (['ai voice agent', 'voice ai', 'ai receptionist', 'ai phone agent',
        'conversational ai', 'ai answering', 'ai sdr', 'ai dialer', 'voice agents', 'ai agents',
        'never miss a call', 'answer calls 24/7', 'ai-powered phone', 'ai employee',
        'books appointments automatically', 'speech recognition', 'text to speech',
        'natural language understanding', 'ai call center', 'ai phone calls'], 3),
    # answering service / virtual receptionist: sells staffed or automated agent time, not calls
    'answering_service': (['virtual receptionist', 'answering service', 'our receptionists',
        'we answer your calls', 'appointment scheduling service', 'live receptionist',
        'call answering', '24/7 receptionist', 'message taking'], 2),
    'form_leadgen_only': (['form fills', 'form-fill leads', 'exclusive form leads', 'web form leads'], 3),
    'directory_blog': (['category archives', 'tag archives', 'read more posts', 'recent posts',
        'posted on', 'leave a comment', 'submit your listing', 'add your business',
        'browse categories', 'sponsored listing'], 5),
}

def count_hits(text_low, needles):
    return [n for n in needles if n in text_low]

# ---------------------------------------------------------------- misc extraction
LINKEDIN_RE = re.compile(r'https?://(?:[a-z]{2,3}\.)?linkedin\.com/company/[A-Za-z0-9._%\-]+', re.I)
TEL_RE = re.compile(r'href\s*=\s*["\']tel:([+0-9().\-\s]{7,25})', re.I)

GEO_HINT = {
    'United States': ['united states', ' usa', 'u.s.a', 'us-based', 'nationwide', 'all 50 states',
        'florida', 'texas', 'california', 'new york', 'nevada', 'arizona', 'georgia', 'illinois',
        'north carolina', 'utah', 'colorado', 'tennessee', 'ohio', 'michigan', 'new jersey',
        'pennsylvania', 'washington', 'oregon', 'massachusetts', 'minnesota', 'missouri', 'virginia',
        'maryland', 'wisconsin', 'indiana', 'alabama', 'oklahoma', 'kansas', 'iowa', 'kentucky',
        'louisiana', 'south carolina', 'connecticut', 'arkansas', 'delaware', 'idaho', 'new mexico'],
    'Canada': ['canada', 'ontario', 'toronto', 'vancouver', 'british columbia', 'alberta', 'quebec',
        'montreal', 'calgary'],
    'United Kingdom': ['united kingdom', 'london', 'england', 'manchester', 'scotland', 'wales'],
    'India': ['india', 'mumbai', 'new delhi', 'bangalore', 'bengaluru', 'noida', 'gurgaon', 'gurugram',
        'pune', 'hyderabad', 'ahmedabad', 'chennai', 'kolkata', 'jaipur', 'indore', 'mohali', 'chandigarh'],
    'Pakistan': ['pakistan', 'karachi', 'lahore', 'islamabad', 'rawalpindi', 'faisalabad'],
    'Philippines': ['philippines', 'manila', 'cebu', 'makati', 'quezon city'],
    'Australia': ['australia', 'sydney', 'melbourne', 'brisbane', 'perth'],
    'UAE': ['united arab emirates', 'dubai', 'abu dhabi'],
    'Bangladesh': ['bangladesh', 'dhaka'],
    'Israel': ['israel', 'tel aviv'],
    'Ukraine': ['ukraine', 'kyiv'],
    'Poland': ['poland', 'warsaw', 'krakow'],
    'Mexico': ['guadalajara', 'mexico city'],
    'Ireland': ['ireland', 'dublin'],
    'Singapore': ['singapore'],
    'Nigeria': ['nigeria', 'lagos'],
    'Cyprus': ['cyprus', 'limassol'],
    'Romania': ['romania', 'bucharest'],
}

VERTICALS = {
    'Medicare/Health Ins': ['medicare', 'medicare advantage', 'aca ', 'affordable care act', 'obamacare',
        'health insurance', 'u65', 'under 65', 'supplemental health', 'dental insurance'],
    'Auto Insurance': ['auto insurance', 'car insurance', 'vehicle insurance', 'sr22'],
    'Home Insurance': ['home insurance', 'homeowners insurance', 'property insurance'],
    'Life/Final Expense': ['life insurance', 'final expense', 'term life', 'burial insurance'],
    'Legal/Mass Tort': ['mass tort', 'personal injury', 'camp lejeune', 'roundup', 'talcum',
        'mesothelioma', 'accident lawyer', 'workers compensation', 'ssdi', 'social security disability',
        'bankruptcy attorney', 'criminal defense', 'immigration lawyer', 'divorce lawyer', 'class action'],
    'Home Services': ['hvac', 'roofing', 'plumbing', 'plumber', 'pest control', 'garage door',
        'siding', 'remodeling', 'flooring', 'landscaping', 'tree service', 'junk removal',
        'appliance repair', 'electrician', 'concrete', 'fencing', 'gutters', 'bathroom remodel',
        'kitchen remodel', 'windows replacement'],
    'Solar': ['solar panels', 'solar installation', 'solar leads', 'solar calls'],
    'Home Warranty': ['home warranty', 'appliance warranty'],
    'Water/Restoration': ['water damage', 'restoration', 'mold remediation', 'fire damage'],
    'Debt/Tax/Credit': ['debt relief', 'debt consolidation', 'debt settlement', 'tax relief',
        'tax debt', 'credit repair', 'student loan', 'loan forgiveness'],
    'Addiction/Rehab': ['addiction treatment', 'rehab', 'substance abuse', 'detox', 'drug rehab',
        'alcohol rehab', 'mental health treatment'],
    'Mortgage/RealEstate': ['mortgage', 'refinance', 'reverse mortgage', 'heloc', 'home equity',
        'real estate leads', 'sell my house', 'motivated seller'],
    'AutoTransport/Moving': ['auto transport', 'car shipping', 'moving company', 'movers',
        'long distance moving'],
    'Travel': ['flight booking', 'airline reservations', 'travel booking', 'cruise'],
    'Senior/MedDevice': ['medical alert', 'hearing aid', 'mobility scooter', 'stair lift',
        'walk-in tub', 'diabetic supplies', 'back brace'],
    'Education': ['online degree', 'university enrollment', 'trade school', 'vocational'],
    'Locksmith/Towing': ['locksmith', 'towing', 'roadside assistance'],
    'Auto Warranty': ['auto warranty', 'extended warranty', 'vehicle service contract'],
    'Utilities/Internet': ['internet service', 'cable tv', 'satellite tv', 'energy supplier'],
    'Timeshare': ['timeshare exit', 'timeshare cancellation'],
    'Bail Bonds': ['bail bonds'],
    'Insurance (general)': ['insurance leads', 'insurance calls'],
}

def guess_from_map(text_low, mapping, cap=4):
    scored = []
    for label in mapping:
        c = sum(text_low.count(n) for n in mapping[label])
        if c: scored.append((c, label))
    scored.sort(reverse=True)
    return [l for _, l in scored[:cap]]
