#!/usr/bin/env python3
"""Hand Claude the smallest possible task text and apply its compact answers.

  tr  slug [slug..]       print the English strings of each source menu that still need Spanish
                          (numbered; strings already in the translation memory are skipped)
  apply-tr FILE           FILE has blocks "### slug" then lines "N<TAB>spanish" ("=" = same as English);
                          writes scraper/real_menus/<slug>.es.json (+ updates the memory)
Translation memory: scraper/pipeline/data/tm_es.json (English -> Spanish), reused across menus.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..")
RM = os.path.join(ROOT, "scraper", "real_menus")
TM_P = os.path.join(HERE, "data", "tm_es.json")
TM = json.load(open(TM_P)) if os.path.exists(TM_P) else {}


def entries(slug):
    src = json.load(open(os.path.join(RM, slug + ".json")))
    out = []
    for si, sec in enumerate(src["sections"]):
        out.append((f"s{si}", sec["name"]))
        for ii, it in enumerate(sec["items"]):
            out.append((f"n{si}_{ii}", it[0]))
            if it[1]:
                out.append((f"d{si}_{ii}", it[1]))
    return out


def tr(slugs):
    for slug in slugs:
        todo = []
        for k, en in entries(slug):
            if en not in TM and en not in todo:
                todo.append(en)
        print(f"### {slug} ({len(todo)})")
        for i, en in enumerate(todo, 1):
            print(f"{i}\t{en}")
        json.dump(todo, open(os.path.join(HERE, "data", f"tr_{slug}.json"), "w"), ensure_ascii=False)


def apply_tr(path):
    blocks = re.split(r"^### ", open(path).read(), flags=re.M)
    for b in blocks:
        if not b.strip():
            continue
        head, *lines = b.split("\n")
        slug = head.split()[0]
        todo = json.load(open(os.path.join(HERE, "data", f"tr_{slug}.json")))
        got, mac = {}, {}
        for l in lines:
            m = re.match(r"^@(\w+)\t(.*)$", l)  # macro: "@A<TAB>text", used as {A} in later lines
            if m:
                mac[m.group(1)] = re.sub(r"\{(\w+)\}", lambda x: mac.get(x.group(1), x.group(0)), m.group(2).strip()); continue
            m = re.match(r"^(\d+)\t(.*)$", l)
            if m:
                v = re.sub(r"\{(\w+)\}", lambda x: mac.get(x.group(1), x.group(0)), m.group(2).strip())
                got[int(m.group(1))] = v.replace("\\n", "\n")
        missing = [i for i in range(1, len(todo) + 1) if not got.get(i) or re.search(r"\{\w+\}", got[i])]
        if missing:
            print(slug, "MISSING", missing[:10]); continue
        for i, en in enumerate(todo, 1):
            TM[en] = en if got[i] == "=" else got[i]
        es = {k: TM[en] for k, en in entries(slug)}
        json.dump(es, open(os.path.join(RM, slug + ".es.json"), "w"), ensure_ascii=False, indent=0)
        print(slug, "ok", len(es))
    json.dump(TM, open(TM_P, "w"), ensure_ascii=False, indent=0)


if __name__ == "__main__":
    if sys.argv[1] == "tr":
        tr(sys.argv[2:])
    elif sys.argv[1] == "apply-tr":
        apply_tr(sys.argv[2])
