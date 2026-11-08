#!/usr/bin/env python3
"""Step 4: turn verified drafts (drafts/<slug>.json, status "ok" in data/extract.json) into
scraper/real_menus/<slug>.json source files that build_real_menu.py can build.

Store details are only taken from the restaurant's own pages when they can be found verbatim
there; otherwise from OpenStreetMap; otherwise left as "call for hours" / blank. Nothing is
guessed.

usage: python3 scraper/pipeline/finalize.py [--status ok] [--only slug,..]
prints the slugs written
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, HERE)
import extract_menu as E

DAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
DAYN = {"Mo": "Mon", "Tu": "Tue", "We": "Wed", "Th": "Thu", "Fr": "Fri", "Sa": "Sat", "Su": "Sun"}
ORDERING = {"toast", "chownow", "square", "clover", "spoton", "olo", "menufy", "dineonline", "owner"}


def t12(hm):
    h, m = map(int, hm.split(":"))
    if h == 24 or (h == 0 and m == 0):
        return "12:00 AM"
    ap = "AM" if h < 12 else "PM"
    h = h % 12 or 12
    return f"{h}:{m:02d} {ap}"


def osm_hours(oh):
    """Parse common OSM opening_hours ('Mo-Fr 11:00-21:00; Sa,Su 12:00-22:00') into our 3 fields."""
    if not oh or re.search(r"[A-Za-z]{3,}|PH|SH|week|\[", oh.replace("off", "").replace("closed", "")):
        return None
    per = {}
    for rule in oh.split(";"):
        rule = rule.strip()
        if not rule:
            continue
        m = re.match(r"^((?:Mo|Tu|We|Th|Fr|Sa|Su)(?:[-,](?:Mo|Tu|We|Th|Fr|Sa|Su))*)\s+(.+)$", rule)
        if not m:
            if re.match(r"^\d{2}:\d{2}-", rule):
                m = re.match(r"^()(.+)$", "Mo-Su " + rule) and re.match(r"^(Mo-Su)\s+(.+)$", "Mo-Su " + rule)
            else:
                return None
        days = set()
        for part in m.group(1).split(","):
            if "-" in part:
                a, b = part.split("-")
                i, j = DAYS.index(a), DAYS.index(b)
                rng = DAYS[i:j + 1] if i <= j else DAYS[i:] + DAYS[:j + 1]
                days.update(rng)
            else:
                days.add(part)
        times = m.group(2).strip()
        if times in ("off", "closed"):
            val = "Closed"
        else:
            spans = []
            for sp in times.split(","):
                mm = re.match(r"^(\d{1,2}:\d{2})-(\d{1,2}:\d{2})\+?$", sp.strip())
                if not mm:
                    return None
                spans.append(f"{t12(mm.group(1))} - {t12(mm.group(2))}")
            val = ", ".join(spans)
        for d in days:
            per[d] = val
    if not per:
        return None
    wk = [(d, per.get(d, "Closed")) for d in DAYS[:5]]
    groups = []
    for d, v in wk:
        if groups and groups[-1][2] == v:
            groups[-1][1] = d
        else:
            groups.append([d, d, v])
    if len(groups) == 1:
        mf = groups[0][2]
    else:
        mf = "; ".join((DAYN[a] if a == b else f"{DAYN[a]}-{DAYN[b]}") + " " + v for a, b, v in groups)
    return {"monday_friday": mf, "saturday": per.get("Sa", "Closed"), "sunday": per.get("Su", "Closed")}


def on_page(value, N, digits_text):
    if not value:
        return False
    if re.sub(r"\D", "", value) and len(re.sub(r"\D", "", value)) >= 10:
        return re.sub(r"\D", "", value)[-10:] in digits_text
    return E.norm(value) in N


def address_on_page(addr, N):
    m = re.match(r"\s*(\d+[A-Za-z]?)\s+([A-Za-z0-9 .'-]+?)(,|$)", addr or "")
    if not m:
        return False
    num, street = m.group(1).lower(), E.norm(m.group(2)).split()
    return bool(street) and re.search(r"\b" + re.escape(num) + r"\b\s+" + re.escape(street[0]), N) is not None


def hours_on_page(h, N):
    if not isinstance(h, dict) or not any(h.values()):
        return False
    toks = re.findall(r"\d{1,2}(?::\d{2})?", " ".join(str(v) for v in h.values()))
    return bool(toks) and all(t in N for t in toks)


def fmt_phone(p):
    d = re.sub(r"\D", "", p or "")[-10:]
    return f"({d[:3]}) {d[3:6]}-{d[6:]}" if len(d) == 10 else ""


SEASONAL = re.compile(r"(?i)thanksgiving|christmas|xmas|easter|valentine|mother'?s day|father'?s day|new year|halloween|holiday|special|today|this week|feast of|seven fishes|st\.? patrick|super bowl|limited time|seasonal")
STRONG_MENU = re.compile(r"(?i)/[^/?#]*(menu|food|drinks?|dinner|lunch|brunch|breakfast|dessert|cocktails?|wine-list|beer)[^/?#]*/?$")


def uncovered_menu_links(slug, site):
    """Same-site links that look like menu pages but contributed no menu text."""
    import urllib.parse
    home = site.get("final") or site.get("site", "")
    host = urllib.parse.urlparse(home).netloc.replace("www.", "")
    used = {urllib.parse.urlparse(u).path.rstrip("/").lower() for u in site.get("_used", [])}
    found = set()
    for p in site.get("pages", []):
        f = os.path.join(E.CACHE, slug, p["file"])
        if not f.endswith(".html") or not os.path.exists(f):
            continue
        for m in re.finditer(r"href\s*=\s*[\"']([^\"'#]+)[\"']", open(f, errors="ignore").read(), re.I):
            u = urllib.parse.urljoin(p["url"], m.group(1))
            pu = urllib.parse.urlparse(u)
            if pu.netloc.replace("www.", "") == host and STRONG_MENU.search(pu.path) and not re.search(r"(?i)catering|gift|event|private|party|job|career", pu.path):
                found.add(pu.path.rstrip("/").lower())
    return sorted(found - used)


def finalize(slug, w, site, ext, draft):
    texts = E.page_texts(slug, site, (w.get("town") or "").lower())
    site = dict(site, _used=draft.get("sources", []))
    miss = uncovered_menu_links(slug, site)
    if miss:
        return None, "uncovered-menu-pages " + " ".join(miss[:5])
    secs = [s for s in draft["sections"] if not SEASONAL.search(s["name"])]
    if sum(len(s["items"]) for s in secs) < 10:
        return None, "too-few-items"
    draft = dict(draft, sections=secs)
    full = "\n".join(t for _, t in texts)
    N = E.norm(full)
    digits_text = re.sub(r"\D", "", full)
    x = draft.get("extracted", {})
    o = w.get("osm") or {}
    town = (o.get("addr:city") or w.get("town") or "").title()
    # address
    if x.get("address") and address_on_page(x["address"], N):
        address, a_src = x["address"], "website"
    elif o.get("addr:housenumber") and o.get("addr:street"):
        address = f'{o["addr:housenumber"]} {o["addr:street"]}, {o.get("addr:city", town)}, CT {o.get("addr:postcode", "")}'.strip()
        a_src = "OpenStreetMap"
    else:
        address, a_src = "", None
    # phone
    if x.get("phone") and on_page(x["phone"], N, digits_text):
        phone, p_src = fmt_phone(x["phone"]), "website"
    elif o.get("phone") or o.get("contact:phone"):
        phone, p_src = fmt_phone(o.get("phone") or o.get("contact:phone")), "OpenStreetMap"
    else:
        phone, p_src = "", None
    # hours
    if hours_on_page(x.get("hours"), N):
        hours, h_src = {k: x["hours"].get(k) or "Closed" for k in ("monday_friday", "saturday", "sunday")}, "website"
    elif osm_hours(o.get("opening_hours")):
        hours, h_src = osm_hours(o["opening_hours"]), "OpenStreetMap"
    else:
        hours, h_src = {"monday_friday": "Call for hours", "saturday": "Call for hours", "sunday": "Call for hours"}, None
    if not address:
        return None, "no-verified-address"
    cuisine = (x.get("cuisine") or "Restaurant").strip()
    cuisine_es = (x.get("cuisine_es") or "").strip()
    plats = set(site.get("platforms", []))
    amen = ["Bilingual Menu"] + (["Online Ordering"] if plats & ORDERING else [])
    notes = ["Menu copied automatically from the restaurant's own website and checked item by item: every item name appears verbatim on the source page, prices were kept only when found next to the item, and descriptions only when found verbatim."]
    notes.append(f"Address from {a_src}." + (f" Phone from {p_src}." if p_src else " No phone found.") + (f" Hours from {h_src}." if h_src else " Hours not listed online."))
    src = {
        "slug": slug, "name": w["name"],
        "sources": draft["sources"], "checked": draft["checked"], "notes": " ".join(notes),
        "taglineEn": f"{cuisine} in {town}" if town else cuisine,
        "taglineEs": (f"{cuisine_es} en {town}" if town else cuisine_es) if cuisine_es else (f"{cuisine} en {town}" if town else cuisine),
        "amenities": amen, "address": address, "phone": phone, "hours": hours,
        "sections": draft["sections"],
    }
    nos = x.get("name_on_site") or ""
    if nos and E.norm(nos) != E.norm(w["name"]) and E.norm(nos) in N and len(nos) < 60:
        src["displayName"] = nos
    return src, None


def main():
    a = sys.argv[1:]
    status = a[a.index("--status") + 1] if "--status" in a else "ok"
    only = set(a[a.index("--only") + 1].split(",")) if "--only" in a else None
    work = {w["slug"]: w for w in json.load(open(os.path.join(E.DATA, "worklist.json")))}
    sites = json.load(open(os.path.join(E.DATA, "sites.json")))
    ext = json.load(open(os.path.join(E.DATA, "extract.json")))
    done = set(json.load(open(os.path.join(ROOT, "data", "verified-menus.json"))))
    out = []
    for slug, r in ext.items():
        if (only and slug not in only) or (not only and (r.get("status") != status or slug in done)):
            continue
        p = os.path.join(E.DRAFTS, slug + ".json")
        if not os.path.exists(p):
            continue
        src, why = finalize(slug, work[slug], sites[slug], r, json.load(open(p)))
        if not src:
            print("SKIP", slug, why, file=sys.stderr)
            continue
        names = [i[0] for s in src["sections"] for i in s["items"]]
        assert len(names) == len(set(names)), slug
        json.dump(src, open(os.path.join(ROOT, "scraper", "real_menus", slug + ".json"), "w"), indent=1, ensure_ascii=False)
        out.append(slug)
    print(" ".join(out))


if __name__ == "__main__":
    main()
