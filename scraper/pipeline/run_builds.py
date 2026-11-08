#!/usr/bin/env python3
"""Step 5: build every finalized source file that isn't built yet, verify each page against its
source, and commit + push in batches. usage: python3 scraper/pipeline/run_builds.py [--batch 10]"""
import json, os, subprocess, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
os.chdir(ROOT)
a = sys.argv[1:]
batch = int(a[a.index("--batch") + 1]) if "--batch" in a else 10
def sh(*c, **k): return subprocess.run(c, capture_output=True, text=True, **k)
done = set(json.load(open("data/verified-menus.json")))
todo = sorted(os.path.basename(f)[:-5] for f in glob.glob("scraper/real_menus/*.json") if os.path.basename(f)[:-5] not in done and os.path.exists("data/merchants/" + os.path.basename(f)))
print("to build:", len(todo), flush=True)
built = []
def commit(slugs):
    if not slugs: return
    sh("python3", "scraper/audit_menus.py")
    files = [f"scraper/real_menus/{s}.json" for s in slugs] + [f"data/merchants/{s}.json" for s in slugs] + ["data/verified-menus.json", "data/MENU_AUDIT.md"]
    sh("git", "add", *files)
    msg = f"feat(menus): {len(slugs)} menus from official websites (auto-extracted, verified)\n\n" + ", ".join(slugs) + "\n\nEach item name was matched verbatim against the restaurant's own page; prices kept only\nwhen found next to the item. See scraper/pipeline/.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"
    r = sh("git", "commit", "-q", "-m", msg)
    p = sh("git", "push", "-q", "origin", "main")
    print("COMMIT", len(slugs), r.returncode, p.returncode, p.stderr[-200:], flush=True)
for s in todo:
    r = sh("python3", "scraper/build_real_menu.py", f"scraper/real_menus/{s}.json")
    v = sh("python3", "scraper/pipeline/verify_build.py", s)
    print(s, "build", r.returncode, v.stdout.strip()[:200], flush=True)
    if r.returncode == 0 and v.returncode == 0:
        built.append(s)
    else:
        sh("git", "checkout", "--", f"data/merchants/{s}.json")
        vm = json.load(open("data/verified-menus.json"))
        if s in vm:
            del vm[s]
            json.dump(vm, open("data/verified-menus.json", "w"), indent=1, ensure_ascii=False)
    if len(built) >= batch:
        commit(built); built = []
commit(built)
