#!/usr/bin/env python3
"""Re-run the deterministic checks on saved drafts (no new Gemini calls)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import extract_menu as E
work = {w["slug"]: w for w in json.load(open(os.path.join(E.DATA, "worklist.json")))}
sites = json.load(open(os.path.join(E.DATA, "sites.json")))
p = os.path.join(E.DATA, "extract.json"); res = json.load(open(p))
a = sys.argv[1:]; only = set(a[a.index("--only") + 1].split(",")) if "--only" in a else None
for slug, r in list(res.items()):
    if only and slug not in only: continue
    dp = os.path.join(E.DRAFTS, slug + ".json")
    if slug not in work or not os.path.exists(dp) or r["status"] not in ("ok", "review"): continue
    dd = json.load(open(dp))
    if dd.get("method") == "chownow" or r.get("method") == "chownow": continue
    got = dd["extracted"]
    nr = E.process(work[slug], sites[slug], got=got)
    res[slug] = nr
    print(slug, r["status"], "->", nr["status"], r.get("items"), "->", nr.get("items"), nr.get("problems"))
json.dump(res, open(p, "w"), indent=0, ensure_ascii=False)
