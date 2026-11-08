import json, sys, collections
ok = True
for slug in sys.argv[1:]:
    src = json.load(open(f"scraper/real_menus/{slug}.json"))
    m = json.load(open(f"data/merchants/{slug}.json"))
    want = collections.Counter((i[0], i[2]) for s in src["sections"] for i in s["items"])
    got = collections.Counter((p["nameEn"], p.get("price", "")) for p in m["products"])
    miss, extra = want - got, got - want
    empty_es = [p["nameEn"] for p in m["products"] if not p.get("nameEs")]
    info = m["storeInfo"]
    hdr = info["address"] == src["address"] and info["phone"] == src["phone"] and info["hours"] == src["hours"]
    status = "OK" if not miss and not extra and not empty_es and hdr else "MISMATCH"
    if status != "OK": ok = False
    print(f"{slug}: {sum(want.values())} src / {sum(got.values())} page -> {status}", ("missing", list(miss)[:5]) if miss else "", ("extra", list(extra)[:5]) if extra else "", ("no ES", empty_es[:5]) if empty_es else "", "" if hdr else "HEADER DIFF")
sys.exit(0 if ok else 1)
