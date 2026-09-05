# -*- coding: utf-8 -*-
"""Free plain-HTTP crawl of one candidate domain, producing the text the v6 qualifier
needs. Lifted from ppc-run2..5/pipeline.py (crawl_one + BLOCK + valid) so verdicts stay
comparable to the runs already in the ledger. Adds parking-page detection, which the
domain-probing channel needs and the search channel never did.
"""
import json, os, re, socket, urllib.error, urllib.request
from urllib.parse import urlparse
import ppclib as L

socket.setdefaulttimeout(10)

MAX_PAGES = 6

BLOCK = set('''google.com facebook.com linkedin.com twitter.com x.com instagram.com youtube.com
reddit.com quora.com wikipedia.org medium.com wordpress.com blogspot.com github.com apple.com
microsoft.com amazon.com indeed.com ziprecruiter.com glassdoor.com simplyhired.com monster.com
greenhouse.io lever.co workable.com ashbyhq.com bamboohr.com jazzhr.com breezy.hr recruitee.com
myworkdayjobs.com wellfound.com angel.co dice.com remoteok.com weworkremotely.com jooble.org
adzuna.com talent.com upwork.com freelancer.com fiverr.com g2.com capterra.com trustradius.com
getapp.com softwareadvice.com crunchbase.com owler.com zoominfo.com apollo.io clearbit.com
offervault.com affpaying.com affbank.com odigger.com businessofapps.com mthink.com
leadscon.com leadgenerationworld.com affiliatesummit.com affiliateworldconferences.com
mailcon.com contact.io eventbrite.com meetup.com hubspot.com salesforce.com wix.com
squarespace.com godaddy.com shopify.com cloudflare.com example.com bing.com yahoo.com
duckduckgo.com yelp.com bbb.org podcasts.apple.com spotify.com soundcloud.com vimeo.com
t.co bit.ly forbes.com techcrunch.com businesswire.com prnewswire.com globenewswire.com
einpresswire.com prweb.com entrepreneur.com inc.com trustpilot.com sitejabber.com
ringba.com retreaver.com trackdrive.com phonexa.com invoca.com callrail.com leadspedia.com
boberdoo.com everflow.io affise.com trackier.com voluum.com redtrack.io activeprospect.com
trustedform.com jornaya.com twilio.com convoso.com five9.com talkdesk.com
scribd.com slideshare.net issuu.com pinterest.com tiktok.com
researchandmarkets.com zippia.com affgate.com expertaff.com doppcall.com afftruster.com
blognife.com leadmaker.com callatlas.com paypercalldeals.com'''.split())

PARKED_NEEDLES = ['hugedomains', 'godaddy.com/domainsearch', 'this domain is for sale',
    'domain is for sale', 'buy this domain', 'domain may be for sale', 'sedoparking',
    'parkingcrew', 'afternic', 'dan.com', 'domainmarket', 'namegarage', 'undeveloped.com',
    'bodis.com', 'parked free', 'is parked', 'domain parking', 'make an offer on this domain',
    'sav.com/domain', 'spaceship.com', 'atom.com', 'brandbucket', 'squadhelp',
    'related searches', 'sponsored listings', 'www.namecheap.com/domains',
    'this domain has expired', 'domain expired', 'coming soon', 'under construction',
    'website coming soon', 'default web site page', 'apache2 ubuntu default',
    'welcome to nginx', 'index of /', 'plesk', 'cpanel', 'account suspended',
    'this site can’t be reached', 'future home of something quite cool']

COMMON_3P = set('''w3.org schema.org gstatic.com jquery.com bootstrapcdn.com fontawesome.com calendly.com
typeform.com jotform.com wufoo.com mailchimp.com zoom.us wistia.com wixsite.com framer.com webflow.com
googletagmanager.com google-analytics.com doubleclick.net gravatar.com wp.com w.org unsplash.com
amazonaws.com cloudfront.net jsdelivr.net unpkg.com cdnjs.com fonts.net adobe.com hotjar.com
intercom.com drift.com tawk.to zendesk.com freshdesk.com clarity.ms'''.split())

def microsite_of(ext_links, domain, known):
    """Parent company candidate: a linked domain already in the exclusion index that either shares
    the site's name token (joinoptimizetoconvert.com -> optimizetoconvert.com) or is linked >= 5x."""
    core = re.sub(r'^(join|get|my|the|go|try|use|hello|team|hey|buy|sell)', '', domain.split('.')[0].replace('-', ''))
    out = []
    for ed, n in ext_links or []:
        if ed not in known or n < 2: continue
        if n >= 5 or (len(core) >= 6 and core in ed.replace('-', '')) or ed.split('.')[0].replace('-', '') in domain.replace('-', ''):
            out.append(ed)
    return out

PROBE = ['/publishers', '/affiliates', '/partners', '/buyers', '/advertisers',
         '/pricing', '/how-it-works', '/services', '/offers', '/contact', '/about']

def valid(d):
    d = L.reg_domain(d)
    if not d or '.' not in d: return None
    if d in BLOCK: return None
    if len(d) < 5 or len(d) > 63: return None
    if not re.match(r'^[a-z0-9][a-z0-9.\-]*\.[a-z]{2,24}$', d): return None
    if d.endswith(('.gov', '.edu', '.mil')): return None
    return d

def looks_parked(raw, text):
    low = (raw or '').lower()
    hits = [n for n in PARKED_NEEDLES if n in low]
    # a real site can mention one of these in passing; parking pages are tiny and hit several
    if len(hits) >= 2: return True
    if hits and len((text or '').strip()) < 600: return True
    return False

def _dns_available():
    """Claude Code cloud VMs route all traffic through an HTTP proxy and may have no working
    resolver of their own; there, a local DNS pre-check would mark every domain
    'unregistered' (this happened: 429 of 500 on the first cloud run). Only trust DNS when
    it can resolve a host that certainly exists."""
    if os.environ.get('PPC_SKIP_DNS_CHECK'): return False
    for h in ('example.com', 'github.com'):
        try:
            socket.getaddrinfo(h, 443); return True
        except Exception:
            continue
    return False

DNS_OK = _dns_available()

# error classes a proxy or resolver hands back for a name that does not exist
_NXDOMAIN_MARKERS = ('name or service not known', 'nodename nor servname', 'getaddrinfo failed',
                     'no address associated', 'http502', 'http503', 'http504',
                     'name_not_resolved', 'could not resolve', 'temporary failure in name resolution')

def resolves(d):
    if not DNS_OK: return True          # cannot tell locally; let the fetch decide
    try:
        socket.getaddrinfo(d, 443); return True
    except Exception:
        try: socket.getaddrinfo('www.' + d, 443); return True
        except Exception: return False

def _classify_dead(errs):
    """Map the fetch errors of an unreachable domain to 'unregistered' when they look like
    name-resolution failures (proxy 502/503, gaierror), else 'unreachable'."""
    low = ' '.join(str(e or '') for e in errs).lower()
    if any(m in low for m in _NXDOMAIN_MARKERS): return 'unregistered'
    return 'unreachable'

def fast_get(url, timeout=8):
    """Single attempt, no retry/backoff: for constructed-domain probes, where most targets
    are parked or unregistered and the 3x exponential retry in ppclib.http_get turned 40
    probes into a 9-minute crawl. Falls back to the cache like http_get does."""
    cp = os.path.join(L.CACHE, L._cache_key(url) + '.html'); mp = cp + '.meta'
    if os.path.exists(mp):
        try:
            meta = json.load(open(mp, encoding='utf-8'))
            body = open(cp, encoding='utf-8', errors='replace').read() if os.path.exists(cp) else ''
            return meta.get('final_url', url), body, meta.get('err')
        except Exception: pass
    try:
        req = urllib.request.Request(url, headers={'User-Agent': L.UA,
            'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.9'})
        with urllib.request.urlopen(req, timeout=timeout, context=L.CTX) as r:
            ct = (r.headers.get('Content-Type') or '').lower()
            raw = r.read(2500000)
            if ct and ('html' not in ct and 'xml' not in ct and 'text' not in ct):
                return r.geturl(), '', 'non_html'
            body = raw.decode('utf-8', 'replace'); fu = r.geturl()
    except urllib.error.HTTPError as e:
        json.dump({'final_url': url, 'err': 'HTTP%d' % e.code}, open(mp, 'w', encoding='utf-8'))
        return url, '', 'HTTP%d' % e.code
    except Exception as e:
        # keep the reason: a proxy's "name not resolved" is how we detect unregistered
        # domains when the VM has no resolver of its own
        return url, '', '%s:%s' % (type(e).__name__, str(getattr(e, 'reason', e))[:120])
    open(cp, 'w', encoding='utf-8').write(body)
    json.dump({'final_url': fu, 'err': None}, open(mp, 'w', encoding='utf-8'))
    return fu, body, None

def crawl_one(rec):
    d = rec['domain']
    is_probe = (rec.get('layer') or '').startswith('L7')
    if not resolves(d):
        return {**rec, 'status': 'unregistered', 'text': '', 'pages': 0}
    getter = (lambda u, timeout: fast_get(u, timeout)) if is_probe else L.http_get
    home_url, home_raw, errs = None, '', []
    for cand in ('https://' + d, 'https://www.' + d, 'http://' + d):
        fu, raw, e = getter(cand, timeout=8 if is_probe else 12)
        errs.append(e)
        if raw and len(raw) > 300:
            home_url, home_raw = fu, raw; break
    if not home_raw:
        return {**rec, 'status': _classify_dead(errs), 'text': '', 'pages': 0,
                'fetch_errors': [str(e) for e in errs if e]}
    # a probe that redirects off-domain is someone else's site (or a registrar landing)
    try:
        if L.reg_domain(urlparse(home_url).netloc) != d:
            return {**rec, 'status': 'redirect_offdomain', 'text': '', 'pages': 1,
                    'final_url': home_url}
    except Exception:
        pass
    home_text = L.visible_text(home_raw)
    if looks_parked(home_raw, home_text):
        return {**rec, 'status': 'parked', 'text': '', 'pages': 1}
    pages = [(home_url, home_raw)]
    links = L.page_links(home_raw, home_url)
    picked = []
    for u in links:
        try:
            if L.reg_domain(urlparse(u).netloc) != d: continue
        except Exception: continue
        p = (urlparse(u).path or '').lower()
        if re.search(r'/(publisher|affiliate|partner|buyer|advertiser|pricing|how-it-works|'
                     r'service|offer|vertical|network|about|contact)', p):
            if u not in picked: picked.append(u)
    for u in picked[:MAX_PAGES - 1]:
        fu, raw, e = L.http_get(u, timeout=10)
        if raw and len(raw) > 300: pages.append((fu, raw))
    if len(pages) < MAX_PAGES:
        base = home_url.rstrip('/')
        have = set((urlparse(p[0]).path or '/').rstrip('/').lower() for p in pages)
        for p in PROBE:
            if len(pages) >= MAX_PAGES: break
            if p in have: continue
            fu, raw, e = L.http_get(base + p, timeout=8)
            if raw and len(raw) > 300: pages.append((fu, raw))
    all_raw = '\n'.join(r for _, r in pages)
    infra = [n for n, t in L.detect_infra(all_raw)]
    # external domains this site links to, for microsite-of-a-known-company detection
    ext = {}
    for u, raw in pages:
        for lk in L.page_links(raw, u):
            try: ed = L.reg_domain(urlparse(lk).netloc)
            except Exception: continue
            if ed and ed != d and ed not in BLOCK and ed not in COMMON_3P: ext[ed] = ext.get(ed, 0) + 1
    ext_top = sorted(ext.items(), key=lambda kv: -kv[1])[:15]
    # Kaliper is permanently banned from Ringba - drop before spending anything on it
    if 'Ringba' in infra:
        return {**rec, 'status': 'ringba_banned', 'text': '', 'pages': len(pages), 'infra': infra}
    parts = []
    def rank(u):
        p = (urlparse(u).path or '/').rstrip('/')
        if p in ('', '/'): return 0
        if re.search(r'(publisher|affiliate|buyer|advertiser|partner)', p, re.I): return 1
        if re.search(r'(pricing|how-it-works|service|offer)', p, re.I): return 2
        return 3
    for u, raw in sorted(pages, key=lambda x: rank(x[0])):
        t = L.visible_text(raw)
        if t.strip(): parts.append('--- %s ---\n%s' % (u, t))
    text = '\n\n'.join(parts)
    low = text.lower()
    return {**rec, 'status': 'ok' if len(text) > 400 else 'thin',
            'text': text[:12000], 'pages': len(pages), 'infra': infra,
            'geo': L.guess_from_map(low, L.GEO_HINT, 2),
            'tier1': sorted(L.find_tier1(text).keys()),
            'ext_links': ext_top,
            # run-3 finding: a tenant can NAME Ringba in prose without loading its tag
            'ringba_prose': bool(re.search(r'\bringba\b', low))}
