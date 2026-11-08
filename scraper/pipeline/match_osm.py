#!/usr/bin/env python3
"""Step 1: build worklist.json (generated menus not yet researched) and match each place
to OpenStreetMap (data/osm_ct.json) by exact name+town, phone, or close name in the same town."""
import json, re, glob, os, collections, difflib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..")
osm = json.load(open(os.path.join(HERE, "data", "osm_ct.json")))["elements"]
ver = set(json.load(open(os.path.join(ROOT, "data", "verified-menus.json"))))
rl = {k for k in json.load(open(os.path.join(ROOT, "scraper", "research_log.json"))) if not k.startswith("_")}
STOP = r"\b(the|restaurant|restaurants|and|cafe|caffe|bar|grill|grille|pizzeria|pizza|llc|inc|co|kitchen|of|ct|tavern|house|eatery)\b"
def norm(n, strip=True):
    n = n.lower().replace("&", " and ").replace("'", "").replace("’", "")
    n = re.sub(r"[^a-z0-9 ]", " ", n)
    if strip: n = re.sub(STOP, " ", n)
    return " ".join(n.split())
def digits(p): return re.sub(r"\D", "", p or "")[-10:]
def town(a):
    m = re.search(r"([A-Za-z .']+?),\s*(CT|Connecticut)\b", a or "")
    if not m: return ""
    t = m.group(1).strip().lower()
    return t.split(",")[-1].strip()
bytown = collections.defaultdict(list); byphone = {}
for e in osm:
    t = e["tags"]; c = (t.get("addr:city") or "").lower().strip()
    bytown[c].append(e)
    for k in ("phone", "contact:phone"):
        if t.get(k): byphone[digits(t[k])] = e
byname = collections.defaultdict(list)
for e in osm: byname[norm(e["tags"]["name"], False)].append(e)
work = []
for f in sorted(glob.glob(os.path.join(ROOT, "data", "merchants", "*.json"))):
    s = os.path.basename(f)[:-5]
    if s in ver or s in rl or s in ("demo", "elsol"): continue
    si = json.load(open(f))["storeInfo"]
    w = {"slug": s, "name": si["name"], "address": si.get("address", ""), "phone": si.get("phone", ""), "town": town(si.get("address", ""))}
    best, how = None, None
    ph = digits(w["phone"])
    if len(ph) == 10 and ph in byphone and difflib.SequenceMatcher(None, norm(w["name"]), norm(byphone[ph]["tags"]["name"])).ratio() > 0.5:
        best, how = byphone[ph], "phone"
    if not best:
        cands = bytown.get(w["town"], [])
        nn = norm(w["name"]); nf = norm(w["name"], False)
        scored = []
        for e in cands:
            on = norm(e["tags"]["name"]); of = norm(e["tags"]["name"], False)
            r = 1.0 if (on == nn and nn) or of == nf else difflib.SequenceMatcher(None, nn or nf, on or of).ratio()
            scored.append((r, e))
        scored.sort(key=lambda x: -x[0])
        if scored and scored[0][0] >= 0.88:
            best, how = scored[0][1], "name%.2f" % scored[0][0]
    if not best:
        c = byname.get(norm(w["name"], False), [])
        if len(c) == 1 and len(norm(w["name"], False)) >= 6:
            ct = (c[0]["tags"].get("addr:city") or "").lower()
            if not ct or not w["town"] or ct == w["town"]:
                best, how = c[0], "uniq"
    if best:
        t = best["tags"]
        w["osm"] = {k: t[k] for k in t if k in ("name", "website", "contact:website", "phone", "contact:phone", "addr:housenumber", "addr:street", "addr:city", "addr:postcode", "opening_hours", "cuisine", "amenity", "shop")}
        w["osm_match"] = how
    work.append(w)
json.dump(work, open(os.path.join(HERE, "data", "worklist.json"), "w"), indent=0, ensure_ascii=False)
m = [w for w in work if w.get("osm")]
print("work", len(work), "matched", len(m), "with website", sum(1 for w in m if w["osm"].get("website") or w["osm"].get("contact:website")))
print(collections.Counter(w["osm_match"][:4] for w in m))
