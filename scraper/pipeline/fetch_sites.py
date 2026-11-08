#!/usr/bin/env python3
"""Step 2 of the menu pipeline: fetch each place's official website and its menu/ordering
pages, and record which menu platform(s) it uses.

usage: python3 scraper/pipeline/fetch_sites.py [--limit N] [--only slug,slug]
reads  scraper/pipeline/data/worklist.json  (entries with a website)
writes scraper/pipeline/cache/<slug>/*.html and scraper/pipeline/data/sites.json
"""
import json, os, re, sys, hashlib, gzip, threading
import urllib.request, urllib.parse, ssl
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CACHE = os.path.join(HERE, "cache")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
CTX = ssl.create_default_context()
CTX_LAX = ssl._create_unverified_context()

PLATFORMS = [
    ("toast", r"toasttab\.com|order\.toasttab|toast\.app/"),
    ("chownow", r"chownow\.com"),
    ("square", r"square\.site|squareup\.com/store|\.square\.site|order\.online-?square"),
    ("clover", r"clover\.com/online-ordering|clover\.com/order"),
    ("spoton", r"order\.spoton\.com|spotonordering"),
    ("popmenu", r"popmenu\.com|popmenucloud|data-popmenu"),
    ("bentobox", r"getbento\.com|bentobox"),
    ("owner", r"owner\.com|data-menu-item-id"),
    ("dineonline", r"\.dine\.online"),
    ("menufy", r"menufy\.com"),
    ("beyondmenu", r"beyondmenu\.com"),
    ("singleplatform", r"singleplatform\.com|places\.singleplatform"),
    ("olo", r"olo\.com|\.olo\."),
    ("slice", r"slicelife\.com"),
    ("doordash_storefront", r"order\.online/store"),
    ("wix_restaurants", r"wix-restaurants|restaurants\.wix"),
    ("menu_pdf", r"\.pdf(\?|\"|')"),
    ("jsonld_menu", r"\"@type\"\s*:\s*\"(Menu|MenuSection|MenuItem)\""),
]
MENU_LINK = re.compile(r"/eat\b|/drinks?\b|menu|order|food|drink|dinner|lunch|brunch|breakfast|dessert|wine|cocktail|catering|toasttab|chownow|square\.site|clover\.com|spoton|\.pdf", re.I)
SKIP_LINK = re.compile(r"facebook|instagram|twitter|tiktok|yelp|tripadvisor|google\.|ubereats|doordash\.com|grubhub|postmates|seamless|opentable|resy\.com|mailto:|tel:|javascript:|\.(jpg|jpeg|png|gif|webp|svg|css|js)(\?|$)", re.I)

lock = threading.Lock()


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/pdf,*/*", "Accept-Encoding": "gzip", "Accept-Language": "en-US,en;q=0.9"})
    for ctx in (CTX, CTX_LAX):
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                body = r.read(8_000_000)
                if r.headers.get("Content-Encoding") == "gzip":
                    body = gzip.decompress(body)
                return r.status, r.geturl(), r.headers.get("Content-Type", ""), body
        except ssl.SSLError:
            continue
        except urllib.error.HTTPError as e:
            return e.code, url, "", b""
        except Exception as e:
            return 0, url, str(e)[:100], b""
    return 0, url, "ssl", b""


def links(html, base):
    out = []
    for m in re.finditer(r"href\s*=\s*[\"']([^\"'#]+)[\"']", html, re.I):
        u = urllib.parse.urljoin(base, m.group(1).strip())
        if u.startswith("http") and not SKIP_LINK.search(u):
            out.append(u)
    return list(dict.fromkeys(out))


def detect(text):
    return [name for name, rx in PLATFORMS if re.search(rx, text, re.I)]


def process(w):
    slug = w["slug"]
    site = (w.get("osm") or {}).get("website") or (w.get("osm") or {}).get("contact:website") or w.get("website")
    if not site:
        return None
    if not site.startswith("http"):
        site = "http://" + site
    d = os.path.join(CACHE, slug)
    os.makedirs(d, exist_ok=True)
    rec = {"slug": slug, "name": w["name"], "site": site, "pages": [], "platforms": [], "platform_links": []}
    st, final, ct, body = fetch(site)
    rec["status"], rec["final"] = st, final
    if not body:
        rec["error"] = ct
        return rec
    html = body.decode("utf-8", "ignore")
    open(os.path.join(d, "home.html"), "w").write(html)
    rec["pages"].append({"url": final, "file": "home.html", "type": ct})
    rec["title"] = (re.findall(r"<title[^>]*>(.*?)</title>", html, re.S | re.I) or [""])[0].strip()[:150]
    host = urllib.parse.urlparse(final).netloc.replace("www.", "")
    cand = [u for u in links(html, final) if MENU_LINK.search(u)]
    plats = set(detect(html))
    plinks = [u for u in links(html, final) if detect(u) and not u.lower().endswith(".pdf")]
    # same-site menu pages and PDFs (limit), external platform links recorded
    same = [u for u in cand if urllib.parse.urlparse(u).netloc.replace("www.", "") == host]
    pdfs = [u for u in cand if ".pdf" in u.lower()]
    for i, u in enumerate((same + [p for p in pdfs if p not in same])[:16]):
        st2, f2, ct2, b2 = fetch(u)
        if not b2:
            continue
        name = "p%d.%s" % (i, "pdf" if ("pdf" in ct2 or b2[:4] == b"%PDF") else "html")
        if name.endswith("pdf"):
            open(os.path.join(d, name), "wb").write(b2)
        else:
            t2 = b2.decode("utf-8", "ignore")
            open(os.path.join(d, name), "w").write(t2)
            plats |= set(detect(t2))
            plinks += [x for x in links(t2, f2) if detect(x) and not x.lower().endswith(".pdf")]
        rec["pages"].append({"url": f2, "file": name, "type": ct2})
    rec["platforms"] = sorted(plats)
    rec["platform_links"] = list(dict.fromkeys(plinks))[:20]
    return rec


def main():
    args = sys.argv[1:]
    limit = int(args[args.index("--limit") + 1]) if "--limit" in args else None
    only = set(args[args.index("--only") + 1].split(",")) if "--only" in args else None
    work = json.load(open(os.path.join(DATA, "worklist.json")))
    work = [w for w in work if (w.get("osm") or {}).get("website") or (w.get("osm") or {}).get("contact:website") or w.get("website")]
    if only:
        work = [w for w in work if w["slug"] in only]
    if limit:
        work = work[:limit]
    out_path = os.path.join(DATA, "sites.json")
    res = json.load(open(out_path)) if os.path.exists(out_path) else {}
    todo = [w for w in work if w["slug"] not in res or only]
    print("fetching", len(todo), flush=True)
    n = 0
    with ThreadPoolExecutor(16) as ex:
        for r in ex.map(process, todo):
            if not r:
                continue
            with lock:
                res[r["slug"]] = r
                n += 1
                if n % 25 == 0:
                    json.dump(res, open(out_path, "w"), indent=0)
                    print(n, flush=True)
    json.dump(res, open(out_path, "w"), indent=0)
    from collections import Counter
    c = Counter(p for r in res.values() for p in r.get("platforms", []))
    print("done", len(res), c.most_common())


if __name__ == "__main__":
    main()
