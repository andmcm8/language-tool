#!/usr/bin/env python3
"""Step 2c: menus posted as images or scanned PDFs. Runs macOS Vision OCR (tools/ocr, built from
tools/ocr.swift) on PDFs that have no text layer and on large images from menu pages, and keeps
the OCR text only when it looks like a menu (5+ prices or menu words). The OCR text then becomes
the "source text" that every extracted item is checked against, exactly like web text.

usage: python3 scraper/pipeline/ocr_menus.py [--only slug,..]
adds pages of type "ocr" (cache/<slug>/ocr_N.txt) to data/sites.json
"""
import json, os, re, subprocess, sys, urllib.parse, threading
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_sites as F
import extract_menu as E

OCR = os.path.join(HERE, "tools", "ocr")
IMG = re.compile(r"""(?:src|data-src|href|srcset|data-image|url\()\s*=?\s*["'(]?([^"' )]+?\.(?:jpe?g|png|webp|gif)(?:\?[^"' )]*)?)""", re.I)
SKIP_IMG = re.compile(r"(?i)logo|icon|favicon|sprite|avatar|badge|social|facebook|instagram|yelp|google|button|arrow|bg[-_]|background|banner|header|footer|map")
lock = threading.Lock()


def ocr(path):
    try:
        r = subprocess.run([OCR, path], capture_output=True, timeout=180)
        return r.stdout.decode("utf-8", "ignore")
    except Exception:
        return ""


def menuish(t):
    return len(E.PRICE_STRICT.findall(t)) >= 5 or len(E.MENU_WORDS.findall(t)) >= 4


def process(slug, site):
    d = os.path.join(F.CACHE, slug)
    new_pages, k = [], 0
    # 1) PDFs with no text layer
    for p in site.get("pages", []):
        f = os.path.join(d, p["file"])
        if f.endswith(".pdf") and os.path.exists(f) and len(E.pdf_text(f).strip()) < 200:
            t = ocr(f)
            if menuish(t):
                name = f"ocr_{k}.txt"; k += 1
                open(os.path.join(d, name), "w").write(t)
                new_pages.append({"url": p["url"], "file": name, "type": "ocr"})
    # 2) images on menu pages (not the home page) that have little text
    home = site.get("final") or ""
    seen = set()
    imgs = []
    for p in site.get("pages", []):
        f = os.path.join(d, p["file"])
        if not f.endswith(".html") or not os.path.exists(f) or p["url"] == home or not E.MENU_URL.search(p["url"]):
            continue
        h = open(f, errors="ignore").read()
        if len(E.PRICE_STRICT.findall(E.html_text(h))) >= 10:
            continue
        for m in IMG.finditer(h):
            u = urllib.parse.urljoin(p["url"], m.group(1).replace("&amp;", "&"))
            base = re.sub(r"\?.*", "", u)
            if base in seen or SKIP_IMG.search(base) or not u.startswith("http"):
                continue
            seen.add(base)
            # prefer a large rendition on common CDNs
            u2 = re.sub(r"([?&])width=\d+", r"\1width=2400", u) if "editmysite" in u else re.sub(r"/v1/fill/[^/]+/", "/", u) if "wixstatic" in u else u
            imgs.append((p["url"], u2))
    for page_url, u in imgs[:12]:
        st, fu, ct, b = F.fetch(u)
        if not b or len(b) < 30000:
            continue
        ext = ".png" if b[:4] == b"\x89PNG" else ".jpg"
        fp = os.path.join(d, f"img_{k}{ext}")
        open(fp, "wb").write(b)
        t = ocr(fp)
        if menuish(t):
            name = f"ocr_{k}.txt"
            open(os.path.join(d, name), "w").write(t)
            new_pages.append({"url": u, "file": name, "type": "ocr", "page": page_url})
        k += 1
    return new_pages


def main():
    a = sys.argv[1:]
    only = set(a[a.index("--only") + 1].split(",")) if "--only" in a else None
    path = os.path.join(F.DATA, "sites.json")
    sites = json.load(open(path))
    ext = json.load(open(os.path.join(F.DATA, "extract.json")))
    todo = [s for s in sites if (only and s in only) or (not only and ext.get(s, {}).get("status") in ("no-menu-text", "no-menu"))]
    todo = [s for s in todo if not sites[s].get("ocr_done")]
    print("ocr", len(todo), flush=True)
    found = []

    def run(s):
        try:
            pages = process(s, sites[s])
        except Exception as e:
            pages = []
            print(s, "error", e, flush=True)
        with lock:
            sites[s]["pages"] = [p for p in sites[s]["pages"] if p.get("type") != "ocr"] + pages
            sites[s]["ocr_done"] = True
            if pages:
                found.append(s)
                print(s, len(pages), flush=True)
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(run, todo))
    json.dump(sites, open(path, "w"), indent=0)
    print("FOUND", ",".join(found), flush=True)


if __name__ == "__main__":
    main()
