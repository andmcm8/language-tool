#!/usr/bin/env python3
"""Step 1b: for worklist places without a website from OpenStreetMap, look them up in Overture
Maps places (data/overture_ct.parquet) by phone or by close name in the same town."""
import json, os, re, difflib, collections, duckdb
HERE = os.path.dirname(os.path.abspath(__file__))
STOP = r"\b(the|restaurant|restaurants|and|cafe|caffe|bar|grill|grille|pizzeria|pizza|llc|inc|co|kitchen|of|ct|tavern|house|eatery)\b"
def norm(n, strip=True):
    n = n.lower().replace("&", " and ").replace("'", "").replace("\u2019", "")
    n = re.sub(r"[^a-z0-9 ]", " ", n)
    if strip: n = re.sub(STOP, " ", n)
    return " ".join(n.split())
def digits(p): return re.sub(r"\D", "", p or "")[-10:]
rows = duckdb.connect().execute("select name, cat, tax, confidence, operating_status, websites, phones, street, city, zip from '" + os.path.join(HERE, "data", "overture_ct.parquet") + "' where name is not null").fetchall()
BAD = re.compile(r"(?i)facebook|instagram|yelp|tripadvisor|doordash|ubereats|grubhub|seamless|postmates|slicelife|menupages|allmenus|google\.|linktr|twitter|tiktok|opentable|resy|foursquare|zmenu|menufy\.com/?$|toasttab\.com/?$")
byphone, bytown = {}, collections.defaultdict(list)
for r in rows:
    for p in r[6] or []:
        byphone.setdefault(digits(p), r)
    bytown[(r[8] or "").lower()].append(r)
wl_path = os.path.join(HERE, "data", "worklist.json")
work = json.load(open(wl_path))
n = nw = 0
for w in work:
    if (w.get("osm") or {}).get("website") or (w.get("osm") or {}).get("contact:website"):
        continue
    best, how = None, None
    ph = digits(w.get("phone") or (w.get("osm") or {}).get("phone", ""))
    if len(ph) == 10 and ph in byphone and difflib.SequenceMatcher(None, norm(w["name"]), norm(byphone[ph][0])).ratio() > 0.5:
        best, how = byphone[ph], "phone"
    if not best:
        town = (w.get("town") or (w.get("osm") or {}).get("addr:city", "")).lower()
        nn, nf = norm(w["name"]), norm(w["name"], False)
        sc = []
        for r in bytown.get(town, []):
            on, of = norm(r[0]), norm(r[0], False)
            s = 1.0 if (nn and on == nn) or of == nf else difflib.SequenceMatcher(None, nn or nf, on or of).ratio()
            if s >= 0.88:
                sc.append((s, r[3] or 0, r))
        if sc:
            sc.sort(key=lambda x: (-x[0], -x[1]))
            best, how = sc[0][2], "name%.2f" % sc[0][0]
    if not best:
        continue
    n += 1
    sites = [u for u in (best[5] or []) if not BAD.search(u)]
    w["overture"] = {"name": best[0], "cat": best[1], "confidence": best[3], "status": best[4], "websites": best[5],
                     "phones": best[6], "street": best[7], "city": best[8], "zip": best[9], "match": how}
    if sites:
        w["website"] = sites[0]
        nw += 1
json.dump(work, open(wl_path, "w"), indent=0, ensure_ascii=False)
print("overture matched", n, "new websites", nw)
print(collections.Counter((w.get("overture") or {}).get("status") for w in work if w.get("overture")))
