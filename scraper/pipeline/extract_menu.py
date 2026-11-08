#!/usr/bin/env python3
"""Step 3: turn each fetched official website (cache/<slug>/) into a draft source menu
(scraper/real_menus/<slug>.json format) - with strict anti-hallucination checks.

Gemini only *reads* the restaurant's own pages and copies items out. Then every item is
checked deterministically against the page text:
  - the item name must appear verbatim (case/whitespace/quote-insensitive) in the source text
  - the description is kept only if it appears verbatim, otherwise blanked
  - the price is kept only if that exact price appears within 400 chars after the name
Items failing the name check are DROPPED. Coverage (how many of the page's prices ended up on
items) and identity (restaurant name + phone/town found on the site) are scored. Results with
any doubt are marked "review"; only clean ones are marked "ok".

usage: python3 scraper/pipeline/extract_menu.py [--only slug,..] [--limit N] [--workers N]
writes scraper/pipeline/drafts/<slug>.json and scraper/pipeline/data/extract.json
"""
import json, os, re, sys, html as H, threading, time, difflib
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(ROOT, "scraper"))
import build_real_menu as B  # reuse gemini_json + api key loading

CACHE, DATA, DRAFTS = (os.path.join(HERE, x) for x in ("cache", "data", "drafts"))
os.makedirs(DRAFTS, exist_ok=True)
PRICE = re.compile(r"(?<![\d.])\$?\s?(\d{1,3}(?:[.,]\d{2})|\d{1,3})(?![\d])")
PRICE_STRICT = re.compile(r"\$\s?\d{1,3}(?:\.\d{2})?|(?<![\d.$])\d{1,3}\.\d{2}(?![\d])|[\u2013\u2014-]\s?\d{1,3}(?:/\d{1,3})?[ \t]*$|^[ \t]*\d{1,3}(?:\.\d{2})?(?:/\d{1,3})?[ \t]*$", re.M)
MENU_URL = re.compile(r"(?i)menu|/eat\b|/drinks?\b|food|dinner|lunch|brunch|breakfast|dessert|wine|cocktail|beer|\.pdf")
MENU_WORDS = re.compile(r"(?i)appetizer|entree|entr\u00e9e|salad|sandwich|dessert|starters|pasta|burger|pizza|coffee|espresso|soup|wings|tacos")


def html_text(s):
    s = re.sub(r"(?is)<(script|style|noscript|svg|head)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h\d|tr|td|th|section|article|span|a|dt|dd)>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = H.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


def pdf_text(path):
    try:
        import pypdf
        r = pypdf.PdfReader(path)
        return "\n".join((p.extract_text() or "") for p in r.pages[:12])
    except Exception:
        return ""


def norm(s):
    s = H.unescape(s or "").lower()
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-").replace("&amp;", "&")
    s = re.sub(r"[^a-z0-9$.&'\"%/+-]+", " ", s)
    return " ".join(s.split())


_TOWNS = None
def ct_towns():
    global _TOWNS
    if _TOWNS is None:
        osm = json.load(open(os.path.join(DATA, "osm_ct.json")))["elements"]
        _TOWNS = {(e["tags"].get("addr:city") or "").lower().strip() for e in osm} - {""}
    return _TOWNS


def other_location(url, town):
    """True if the URL names a different CT town (e.g. /greenwich-menu for the Westport place)."""
    u = url.lower().replace("_", "-")
    for t in ct_towns():
        if len(t) > 4 and t != town and re.search(r"(?<![a-z])" + re.escape(t.replace(" ", "-")) + r"(?![a-z])", u):
            return True
    return False


def page_texts(slug, site, town=""):
    d = os.path.join(CACHE, slug)
    out = []
    for p in site.get("pages", []):
        f = os.path.join(d, p["file"])
        if not os.path.exists(f) or (town and other_location(p["url"], town)):
            continue
        if f.endswith(".pdf"):
            t = pdf_text(f)
        elif f.endswith(".txt"):
            t = open(f, errors="ignore").read()
        else:
            t = html_text(open(f, errors="ignore").read())
        if t.strip():
            out.append((p["url"], t))
    return out


PROMPT = """You are copying a restaurant's menu EXACTLY as published on its own website, for a bilingual menu site.
Below is text scraped from the restaurant's official web pages (each page starts with ### URL).

Rules - accuracy is critical:
- Copy every food and drink item that is on the menu text. Do not skip sections. Do not summarise.
- Copy item names, descriptions and prices EXACTLY as written (you may fix ALL-CAPS to Title Case). Never invent, guess, or "improve" anything. Never add an item that is not in the text.
- price: the item's price as written, formatted like "$12.00". If several sizes/prices, use the first/smallest as price and put the size list in desc exactly as written (e.g. "Small $12 / Large $18"). If no price is written, use "".
- desc: the description as written, or "" if none. Do not write your own descriptions.
- Section names: as on the menu.
- If a section lists several dishes in one comma-separated line (e.g. "Sides: potato salad, cole slaw, cannoli"), make each dish its own item.
- Include every menu the pages show (lunch, dinner, brunch, drinks, wine, desserts, kids, catering). If the same dish appears on two menus (e.g. lunch and dinner) with different prices, keep both and add the menu name in parentheses to the second one, e.g. "Cobb Salad (Lunch)".
- Skip daily specials and limited-time holiday menus (Thanksgiving, Valentine's, etc.).
- Ignore navigation, reviews, events, gift cards, job postings, and marketing copy.
- If the pages contain NO actual menu items (e.g. only "view our menu" links or images), return "has_menu": false.
- Also copy, only if written on the pages: the restaurant's name, street address, phone, and opening hours. Use "" if not present.
- hours: map what is written into three strings (monday_friday, saturday, sunday) using only the times written; "" if unknown.

Return JSON:
{"has_menu": true/false, "name_on_site": "", "address": "", "phone": "", "hours": {"monday_friday": "", "saturday": "", "sunday": ""},
 "cuisine": "short cuisine/type in English, e.g. 'Italian restaurant'", "cuisine_es": "the same in Spanish, e.g. 'Restaurante italiano'",
 "sections": [{"name": "", "items": [["name", "desc", "$0.00"]]}]}

PAGES:
"""


XMODELS = ["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-flash-latest", "gemini-3.8-flash"]


def gemini(prompt):
    import urllib.request, urllib.error
    body = json.dumps({"contents": [{"role": "user", "parts": [{"text": prompt}]}],
                       "generationConfig": {"responseMimeType": "application/json", "temperature": 0, "maxOutputTokens": 65536}}).encode()
    last = None
    if B.daily_quota_hit():
        raise SystemExit("Gemini daily quota reached")
    for rnd in range(6):
        if rnd:
            time.sleep(20 * rnd)
        per_day = 0
        for m in XMODELS:
            req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                                         data=body, headers={"Content-Type": "application/json", "x-goog-api-key": B.api_key()})
            try:
                with urllib.request.urlopen(req, timeout=300) as r:
                    data = json.load(r)
                return json.loads("".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"]))
            except urllib.error.HTTPError as e:
                last = e
                if e.code == 429:
                    if B.note_429(e):
                        per_day += 1
                    continue
            except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError, OSError) as e:
                last = e
        if per_day == len(XMODELS):
            open(B.QUOTA_FLAG, "w").write(time.strftime("%Y-%m-%d"))
            raise SystemExit("Gemini daily quota reached")
    raise SystemExit(f"Gemini failed: {last}")


def find_after(hay, needle, start=0):
    return hay.find(needle, start)


def tidy(name):
    name = name.strip(" \t-–—:|•·*")
    if name.isupper() and len(name) > 3:
        name = " ".join(w if (len(w) <= 3 and w.isalpha() and w in ("BBQ", "BLT", "NY", "IPA", "XL", "GF", "DF", "VG")) else w.capitalize() for w in name.split())
    return name


def name_candidates(texts):
    """(normalized, original) name-like fragments from the source text: each line, and the part
    of the line before a price / dash / colon."""
    out = {}
    for _, t in texts:
        for line in t.split("\n"):
            line = line.strip()
            if not line or len(line) > 160:
                continue
            for frag in {line, re.split(r"\s[-–—|:]\s|\s?\$\s?\d|\.{3,}|\s\d{1,3}(?:\.\d{2})?\s*$", line)[0]}:
                f = frag.strip()
                if 2 < len(f) <= 90:
                    out.setdefault(norm(f), f)
    return out


def verify(sections, texts):
    full = "\n".join(t for _, t in texts)
    N = norm(full)
    cands = None
    import bisect

    def locate(name):
        """Return (name_as_published, position) or (None, -1). Exact match first; otherwise the
        closest fragment of the page (>= 0.9 similar) and use the PAGE's wording, never the model's."""
        nonlocal cands
        nn = norm(name)
        if not nn:
            return None, -1
        k = N.find(nn)
        if k >= 0:
            return name, k
        alt = nn.strip(" .-:")
        if alt and N.find(alt) >= 0:
            return name, N.find(alt)
        if cands is None:
            cands = name_candidates(texts)
        keys = [c for c in cands if abs(len(c) - len(nn)) <= max(4, 0.3 * len(nn))]
        m = difflib.get_close_matches(nn, keys, n=1, cutoff=0.9)
        if m and N.find(m[0]) >= 0:
            return tidy(cands[m[0]]), N.find(m[0])
        return None, -1

    # pass 1: resolve names and positions in menu order
    resolved, cur = [], 0
    for s0 in sections or []:
        for it in s0.get("items", []):
            if not isinstance(it, list) or len(it) < 3:
                continue
            name, desc, price = (str(x or "").strip() for x in it[:3])
            pub, pos = locate(name)
            if pub is not None:
                q = norm(pub)
                k2 = N.find(q, cur)
                if k2 >= 0:
                    pos = k2
                cur = pos + len(q)
            resolved.append((s0.get("name") or "Menu", name, pub, pos, desc, price))
    starts = sorted({r[3] for r in resolved if r[3] >= 0})
    kept, dropped, nprice_ok, blanked_desc = {}, [], 0, 0
    order = []
    seen = {}
    for sec, name, pub, pos, desc, price in resolved:
        if pub is None:
            dropped.append(name)
            continue
        nn = norm(pub)
        if desc and norm(desc) not in N:
            nd = norm(desc)
            if not (len(nd) > 40 and nd[:40] in N and nd[-25:] in N):
                desc = ""
                blanked_desc += 1
        if price:
            m = re.search(r"\d+(?:\.\d{1,2})?", price.replace(",", "."))
            ok = False
            if m:
                val = float(m.group())
                j = bisect.bisect_right(starts, pos)
                nxt = starts[j] if j < len(starts) else len(N)
                window = N[pos + len(nn): min(nxt, pos + len(nn) + 400 + len(norm(desc)))]
                ok = any(abs(float(pm.group()) - val) < 0.001 for pm in re.finditer(r"\d+(?:\.\d{1,2})?", window))
            if ok:
                price = "$%.2f" % val
                nprice_ok += 1
            else:
                price = ""
        key = nn
        if key in seen:
            prev = seen[key]
            if prev[1:] == (norm(desc), price) or prev[0] == sec:
                dropped.append(pub + " (dup)")
                continue
            pub = f"{pub} ({sec})"
            key = norm(pub)
            if key in seen:
                dropped.append(pub + " (dup)")
                continue
        seen[key] = (sec, norm(desc), price)
        if sec not in kept:
            kept[sec] = []
            order.append(sec)
        kept[sec].append([pub, desc, price])
    kept = [{"name": s, "items": kept[s]} for s in order]
    # completeness: priced lines on the page that no kept item accounts for
    names = [norm(i[0].split(" (")[0]) for s in kept for i in s["items"]]
    lines = [l for _, t in texts for l in t.split("\n")]
    priced = [i for i, l in enumerate(lines) if PRICE_STRICT.search(l)]
    nl = [norm(l) for l in lines]
    unmatched = 0
    HOURS = re.compile(r"(?i)\b(mon|tue|wed|thu|fri|sat|sun)[a-z]*\b|\b\d{1,2}\s*(am|pm)\b|price range|minimum|tax|gratuity|delivery fee")
    priced = [i for i in priced if not HOURS.search(lines[i])]
    for i in priced:
        textual = len(re.findall(r"[A-Za-z]", lines[i])) >= 3
        back = 3 if textual else 10
        ctx = " ".join(nl[max(0, i - back): i + 1])
        if not any(n and n in ctx for n in names):
            unmatched += 1
    price_tokens = len(PRICE_STRICT.findall(full))
    return kept, dropped, nprice_ok, blanked_desc, price_tokens, (unmatched, len(priced))


def identity(w, site, texts, got):
    full = norm("\n".join(t for _, t in texts) + " " + site.get("title", ""))
    name_tokens = [t for t in norm(w["name"]).split() if len(t) > 2 and t not in ("the", "and", "restaurant", "cafe", "bar", "grill", "pizza", "kitchen")]
    name_hit = sum(1 for t in name_tokens if t in full) / max(1, len(name_tokens))
    ph = re.sub(r"\D", "", w.get("phone", ""))[-10:]
    ph_osm = re.sub(r"\D", "", (w.get("osm") or {}).get("phone", "") or (w.get("osm") or {}).get("contact:phone", ""))[-10:]
    digits = re.sub(r"\D", "", "\n".join(t for _, t in texts))
    phone_hit = bool((ph and ph in digits) or (ph_osm and ph_osm in digits))
    town = (w.get("town") or (w.get("osm") or {}).get("addr:city", "")).lower()
    town_hit = bool(town and town in full)
    return {"name": round(name_hit, 2), "phone": phone_hit, "town": town_hit}


def process(w, site, got=None):
    slug = w["slug"]
    texts = page_texts(slug, site, (w.get("town") or (w.get("osm") or {}).get("addr:city", "")).lower())
    # keep pages that look like menus (prices or menu words); always keep home for identity
    scored = []
    for u, t in texts:
        np = len(PRICE_STRICT.findall(t))
        scored.append((np, u, t))
    home = site.get("final") or ""
    menu_pages = [(u, t) for np, u, t in scored
                  if np >= 5 or (u != home and MENU_URL.search(u) and (np >= 1 or MENU_WORDS.search(t)))]
    rec = {"slug": slug, "status": "", "pages": [u for u, _ in menu_pages]}
    if not menu_pages:
        rec["status"] = "no-menu-text"
        return rec
    # de-dup identical pages, cap size
    blob, seen = [], set()
    for u, t in menu_pages:
        h = hash(t[:2000])
        if h in seen:
            continue
        seen.add(h)
        blob.append("### " + u + "\n" + t[:60000])
    groups, cur = [], ""
    for b in blob:
        if cur and len(cur) + len(b) > 45000:
            groups.append(cur)
            cur = ""
        cur += b[:45000] + "\n\n"
    if cur:
        groups.append(cur)
    if got is not None:
        groups = []
    else:
        got = {"has_menu": False, "sections": []}
    try:
        for g in groups[:6]:
            part = gemini(PROMPT + g)
            if isinstance(part, list):
                part = part[0] if part else {}
            if part.get("has_menu"):
                got["has_menu"] = True
                got["sections"] += part.get("sections") or []
            for k in ("name_on_site", "address", "phone", "cuisine", "cuisine_es"):
                if part.get(k) and not got.get(k):
                    got[k] = part[k]
            if isinstance(part.get("hours"), dict) and any(part["hours"].values()) and not got.get("hours"):
                got["hours"] = part["hours"]
    except SystemExit as e:
        rec["status"] = "llm-failed"
        rec["error"] = str(e)[:200]
        return rec
    if not got.get("has_menu"):
        rec["status"] = "no-menu"
        return rec
    kept, dropped, nprice, blanked, ptok, (unm, npl) = verify(got.get("sections"), menu_pages)
    n = sum(len(s["items"]) for s in kept)
    idt = identity(w, site, texts, got)
    rec.update({"items": n, "dropped": len(dropped), "dropped_examples": dropped[:8], "prices_kept": nprice,
                "price_tokens": ptok, "desc_blanked": blanked, "identity": idt})
    miss = unm / npl if npl else 0.0
    rec["unmatched_priced_lines"] = [unm, npl]
    rec["coverage"] = round(1 - miss, 2)
    real_drops = [d for d in dropped if not d.endswith("(dup)")]
    problems = []
    if n < 8: problems.append("few-items")
    if real_drops and len(real_drops) > max(3, 0.1 * (n + len(real_drops))): problems.append("many-dropped")
    if npl >= 10 and miss > 0.25: problems.append("low-coverage")
    if idt["name"] < 0.5: problems.append("name-not-on-site")
    phone_matched = (w.get("osm_match") == "phone") or ((w.get("overture") or {}).get("match") == "phone")
    if not (idt["phone"] or idt["town"] or phone_matched): problems.append("location-unconfirmed")
    rec["problems"] = problems
    rec["status"] = "ok" if not problems else "review"
    draft = {"slug": slug, "name": w["name"], "sources": rec["pages"], "dropped": dropped, "checked": time.strftime("%Y-%m-%d"),
             "extracted": got, "sections": kept}
    json.dump(draft, open(os.path.join(DRAFTS, slug + ".json"), "w"), indent=1, ensure_ascii=False)
    return rec


def main():
    a = sys.argv[1:]
    only = set(a[a.index("--only") + 1].split(",")) if "--only" in a else None
    limit = int(a[a.index("--limit") + 1]) if "--limit" in a else None
    workers = int(a[a.index("--workers") + 1]) if "--workers" in a else 3
    work = {w["slug"]: w for w in json.load(open(os.path.join(DATA, "worklist.json")))}
    sites = json.load(open(os.path.join(DATA, "sites.json")))
    outp = os.path.join(DATA, "extract.json")
    res = json.load(open(outp)) if os.path.exists(outp) else {}
    todo = [s for s in sites if s in work and (only and s in only or (not only and (s not in res or res[s].get("status") in ("llm-failed", "error"))))]
    todo = [s for s in todo if sites[s].get("pages") or only]
    if limit:
        todo = todo[:limit]
    print("extracting", len(todo), flush=True)
    lock = threading.Lock()

    def run(s):
        try:
            r = process(work[s], sites[s])
        except Exception as e:
            r = {"slug": s, "status": "error", "error": repr(e)[:200]}
        with lock:
            res[s] = r
            json.dump(res, open(outp, "w"), indent=0, ensure_ascii=False)
            print(s, r["status"], r.get("items", ""), r.get("problems", ""), flush=True)

    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(run, todo))


if __name__ == "__main__":
    main()
