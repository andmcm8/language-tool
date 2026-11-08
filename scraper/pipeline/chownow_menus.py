#!/usr/bin/env python3
"""Step 3b: restaurants that take orders through ChowNow (linked from their own website) - read
the exact structured menu (names, descriptions, prices) from ChowNow's public menu API. Used for
sites whose website extraction did not pass the checks.

usage: python3 scraper/pipeline/chownow_menus.py [--only slug,..] [--force]
writes drafts/<slug>.json with "trusted_store" and sets status "ok" (method chownow) in extract.json
"""
import json, os, re, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import extract_menu as E

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def clean(s):
    return re.sub(r"\s+", " ", s or "").strip()


def money(p):
    return "" if p in (None, 0) else f"${float(p):.2f}"


def sections(m):
    allitems = {i["id"]: i for c in m.get("menu_categories", []) for i in c["items"]}
    child = set()
    for i in allitems.values():
        for cid in (i.get("meta_item_details") or {}).get("serving_size_group", {}).get("child_ids", []):
            child.add(cid)
    secs, seen, names = [], set(), set()
    for c in m.get("menu_categories", []):
        if clean(c["name"]).lower() in ("popular items", "popular", "most popular", "featured items", "featured"):
            continue
        items = []
        for i in c["items"]:
            if i["id"] in child or i["id"] in seen:
                continue
            seen.add(i["id"])
            rows = []
            if i.get("is_meta"):
                for cid in i["meta_item_details"]["serving_size_group"]["child_ids"]:
                    ch = allitems.get(cid)
                    if ch:
                        seen.add(cid)
                        rows.append([f"{clean(i['name'])} ({clean(ch.get('size'))})", clean(i.get("description") or ch.get("description")), money(ch.get("price"))])
            else:
                rows.append([clean(i["name"]), clean(i.get("description")), money(i.get("price"))])
            for r in rows:
                k = r[0].lower()
                if k in names:
                    r[0] = f"{r[0]} ({clean(c['name'])})"
                    k = r[0].lower()
                if k in names:
                    continue
                names.add(k)
                items.append(r)
        if items:
            secs.append({"name": clean(c["name"]), "items": items})
    return secs


def fmt_hours(r):
    """ChowNow display_hours -> our 3 fields."""
    f = (r.get("fulfillment") or {}).get("pickup") or (r.get("fulfillment") or {}).get("dine_in") or {}
    dh = f.get("display_hours") or []
    per = {}
    for d in dh:
        spans = []
        for rg in d.get("ranges", []):
            def t(x):
                h, m = map(int, x.split(":")); ap = "AM" if h < 12 or h == 24 else "PM"; return f"{h % 12 or 12}:{m:02d} {ap}"
            spans.append(f"{t(rg['from'])} - {t(rg['to'])}")
        per[d["dow"][:3]] = ", ".join(spans) if spans else "Closed"
    if not per:
        return None
    wk = [(d, per.get(d, "Closed")) for d in ("Mon", "Tue", "Wed", "Thu", "Fri")]
    groups = []
    for d, v in wk:
        if groups and groups[-1][2] == v:
            groups[-1][1] = d
        else:
            groups.append([d, d, v])
    mf = groups[0][2] if len(groups) == 1 else "; ".join((a if a == b else f"{a}-{b}") + " " + v for a, b, v in groups)
    return {"monday_friday": mf, "saturday": per.get("Sat", "Closed"), "sunday": per.get("Sun", "Closed")}


def process(w, site):
    links = [l for l in site.get("platform_links", []) if "chownow.com" in l]
    comp = None
    loc = None
    for l in links:
        m = re.search(r"/(?:order|direct|catering)/(\d+)/locations(?:/(\d+))?", l)
        if m:
            comp = comp or m.group(1)
            if m.group(2) and "catering" not in l:
                loc = loc or m.group(2)
    if not comp:
        return None, "no-company"
    town = (w.get("town") or (w.get("osm") or {}).get("addr:city", "") or (w.get("overture") or {}).get("city", "")).lower()
    if not loc:
        c = get(f"https://api.chownow.com/api/company/{comp}")
        locs = c.get("locations") or []
        pick = [x for x in locs if (x.get("address") or {}).get("city", "").lower() == town] or (locs if len(locs) == 1 else [])
        if not pick:
            return None, "location-ambiguous"
        loc = str(pick[0]["id"])
    r = get(f"https://api.chownow.com/api/restaurant/{loc}")
    m = get(f"https://api.chownow.com/api/restaurant/{loc}/menu/" + time.strftime("%Y%m%d") + "1900")
    secs = sections(m)
    a = r.get("address") or {}
    city = clean(a.get("city"))
    ours = re.sub(r"\D", "", w.get("phone") or "")[-10:]
    same_phone = ours and ours == re.sub(r"\D", "", r.get("phone") or "")[-10:]
    if town and city.lower() != town and town not in clean(a.get("street_address1")).lower() and not same_phone:
        return None, f"town-mismatch {city}"
    n = sum(len(s["items"]) for s in secs)
    if n < 8:
        return None, "few-items"
    store = {"address": f"{clean(a.get('street_address1'))}, {city}, {a.get('state') or 'CT'} {a.get('zip') or ''}".strip(),
             "phone": clean(r.get("phone")), "hours": fmt_hours(r)}
    url = f"https://direct.chownow.com/order/{comp}/locations/{loc}"
    draft = {"slug": w["slug"], "name": w["name"], "sources": [url, site.get("final") or site.get("site")], "checked": time.strftime("%Y-%m-%d"),
             "method": "chownow", "extracted": {"name_on_site": clean(r.get("name")), "cuisine": "", "cuisine_es": ""},
             "trusted_store": store, "sections": secs}
    json.dump(draft, open(os.path.join(E.DRAFTS, w["slug"] + ".json"), "w"), indent=1, ensure_ascii=False)
    return {"slug": w["slug"], "status": "ok", "method": "chownow", "items": n, "pages": [url], "problems": []}, None


def main():
    a = sys.argv[1:]
    only = set(a[a.index("--only") + 1].split(",")) if "--only" in a else None
    work = {w["slug"]: w for w in json.load(open(os.path.join(E.DATA, "worklist.json")))}
    sites = json.load(open(os.path.join(E.DATA, "sites.json")))
    p = os.path.join(E.DATA, "extract.json"); res = json.load(open(p))
    for slug, site in sites.items():
        if slug not in work or (only and slug not in only):
            continue
        if not any("chownow.com" in l for l in site.get("platform_links", [])):
            continue
        if res.get(slug, {}).get("status") == "ok" and "--force" not in a:
            continue
        try:
            rec, why = process(work[slug], site)
        except Exception as e:
            rec, why = None, repr(e)[:120]
        print(slug, "ok %d" % rec["items"] if rec else why, flush=True)
        if rec:
            res[slug] = rec
    json.dump(res, open(p, "w"), indent=0, ensure_ascii=False)


if __name__ == "__main__":
    main()
