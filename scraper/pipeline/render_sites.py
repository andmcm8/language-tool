#!/usr/bin/env python3
"""Step 2b: re-load JavaScript-built sites (Wix, Square Online, Squarespace...) in headless
Chrome - the same as a normal visitor's browser - for sites whose plain HTML had little text.
Sites behind bot walls (HTTP 202/403/429, "Just a moment") and Toast are skipped, never
worked around.

usage: python3 scraper/pipeline/render_sites.py [--only slug,..] [--workers 6]
updates cache/<slug>/ and data/sites.json (pages get a "rendered": true flag)
"""
import json, os, re, subprocess, sys, threading, tempfile, shutil, urllib.parse
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_sites as F
import extract_menu as E

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WALL = re.compile(r"Just a moment|Attention Required|Verify you are human|Access denied|checking your browser", re.I)
def walled(h):
    return bool(WALL.search(E.html_text(h)[:1500]))
lock = threading.Lock()


def render(url, prof):
    try:
        r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-first-run", "--mute-audio",
                            f"--user-data-dir={prof}", "--virtual-time-budget=12000", "--dump-dom", url],
                           capture_output=True, timeout=60)
        return r.stdout.decode("utf-8", "ignore")
    except Exception:
        return ""


def thin(slug, site):
    tot = 0
    for p in site.get("pages", []):
        f = os.path.join(F.CACHE, slug, p["file"])
        if os.path.exists(f) and f.endswith(".html"):
            tot += len(E.html_text(open(f, errors="ignore").read()))
        elif f.endswith(".pdf"):
            tot += 3000
    return tot < 2500


def process(slug, site):
    prof = tempfile.mkdtemp(prefix="rprof")
    try:
        home = site.get("final") or site["site"]
        h = render(home, prof)
        if not h or walled(h):
            return None
        d = os.path.join(F.CACHE, slug)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "r_home.html"), "w").write(h)
        pages = [{"url": home, "file": "r_home.html", "type": "text/html", "rendered": True}]
        host = urllib.parse.urlparse(home).netloc.replace("www.", "")
        ls = F.links(h, home)
        cand = [u for u in ls if F.MENU_LINK.search(u) and urllib.parse.urlparse(u).netloc.replace("www.", "") == host and not u.lower().endswith(".pdf")]
        plats = set(site.get("platforms", [])) | set(F.detect(h))
        plinks = list(site.get("platform_links", [])) + [u for u in ls if F.detect(u) and not u.lower().endswith(".pdf")]
        for i, u in enumerate(list(dict.fromkeys(cand))[:6]):
            t = render(u, prof)
            if not t or walled(t):
                continue
            name = f"r{i}.html"
            open(os.path.join(d, name), "w").write(t)
            pages.append({"url": u, "file": name, "type": "text/html", "rendered": True})
            plats |= set(F.detect(t))
        # keep previously fetched PDFs
        pages += [p for p in site.get("pages", []) if p["file"].endswith(".pdf")]
        new = dict(site)
        new["pages"], new["platforms"], new["platform_links"], new["rendered"] = pages, sorted(plats), list(dict.fromkeys(plinks))[:20], True
        return new
    finally:
        shutil.rmtree(prof, ignore_errors=True)


def main():
    a = sys.argv[1:]
    only = set(a[a.index("--only") + 1].split(",")) if "--only" in a else None
    workers = int(a[a.index("--workers") + 1]) if "--workers" in a else 6
    path = os.path.join(F.DATA, "sites.json")
    sites = json.load(open(path))
    todo = [s for s, x in sites.items()
            if (only is None or s in only) and not x.get("rendered") and "toast" not in x.get("platforms", [])
            and x.get("status") not in (202, 403, 429) and (only or thin(s, x))]
    print("rendering", len(todo), flush=True)
    n = 0

    def run(s):
        nonlocal n
        r = process(s, sites[s])
        with lock:
            n += 1
            if r:
                sites[s] = r
            if n % 10 == 0:
                json.dump(sites, open(path, "w"), indent=0)
                print(n, flush=True)

    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(run, todo))
    json.dump(sites, open(path, "w"), indent=0)
    print("done", flush=True)


if __name__ == "__main__":
    main()
