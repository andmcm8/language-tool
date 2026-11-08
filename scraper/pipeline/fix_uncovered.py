#!/usr/bin/env python3
"""Fetch menu pages a site links to that the first pass didn't capture (page cap, PDFs),
add them to the site, and clear the site's extraction so it is redone with everything."""
import json, os, sys, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fetch_sites as F, render_sites as R, extract_menu as E, tempfile, shutil
unc = json.load(open(os.path.join(F.DATA, "uncovered.json")))
sp = os.path.join(F.DATA, "sites.json"); sites = json.load(open(sp))
ep = os.path.join(F.DATA, "extract.json"); ext = json.load(open(ep))
for slug, paths in unc.items():
    site = sites[slug]; base = site.get("final") or site["site"]; d = os.path.join(F.CACHE, slug)
    have = {p["url"] for p in site["pages"]}
    added = 0
    prof = tempfile.mkdtemp()
    for path in paths[:10]:
        u = urllib.parse.urljoin(base, path)
        if u in have: 
            continue
        st, fu, ct, b = F.fetch(u)
        if not b: continue
        k = len(site["pages"])
        if "pdf" in ct or b[:4] == b"%PDF":
            name = f"u{k}.pdf"; open(os.path.join(d, name), "wb").write(b)
        else:
            h = R.render(u, prof) or b.decode("utf-8", "ignore")
            name = f"u{k}.html"; open(os.path.join(d, name), "w").write(h)
        site["pages"].append({"url": u, "file": name, "type": ct}); added += 1
    shutil.rmtree(prof, ignore_errors=True)
    if added:
        ext.pop(slug, None)
    print(slug, "added", added, flush=True)
json.dump(sites, open(sp, "w"), indent=0); json.dump(ext, open(ep, "w"), indent=0, ensure_ascii=False)
