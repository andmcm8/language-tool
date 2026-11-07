#!/usr/bin/env python3
"""
Build a merchant page from a VERIFIED source menu.

  python3 scraper/build_real_menu.py scraper/real_menus/<slug>.json [...]

Source files (scraper/real_menus/*.json) hold the menu exactly as published by
the restaurant (item names, descriptions, prices), plus the source URLs and the
date it was checked. This script:
  1. Replaces products/categories in data/merchants/<slug>.json with that menu.
  2. Overwrites address/phone/hours/tagline/amenities with the sourced values,
     clears unsourced FAQs and payment methods.
  3. Uses Gemini ONLY to translate names/descriptions into Spanish
     (prices and items are never generated).
  4. Records the slug in data/verified-menus.json.
"""
import json, os, re, sys, unicodedata, urllib.request, urllib.error

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MODELS = ["gemini-3.5-flash", "gemini-3.8-flash", "gemini-flash-latest", "gemini-3.5-flash-lite"]


def api_key():
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    for line in open(os.path.join(ROOT, ".env.local")):
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip().strip("\"'")
    raise SystemExit("GEMINI_API_KEY not found")


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def gemini_json(prompt):
    body = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2},
    }).encode()
    last = None
    for m in MODELS:
        req = urllib.request.Request(
            f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
            data=body, headers={"Content-Type": "application/json", "x-goog-api-key": api_key()})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.load(r)
            text = "".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"])
            return json.loads(text)
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, json.JSONDecodeError, TimeoutError) as e:
            last = e
            print(f"  {m} failed: {e}", file=sys.stderr)
    raise SystemExit(f"All Gemini models failed: {last}")


PROMPT = (
    "Translate these restaurant menu strings from English into natural Latin American Spanish "
    "for Spanish-speaking diners in Connecticut. Rules: keep Italian/foreign dish names as they are "
    "(e.g. 'Pasta e Fagioli', 'Tiramisu', 'Pollo Scarpariello'), but translate English words around them; "
    "keep brand names, wine producers and regions unchanged; keep every number, size and price exactly; "
    "do not add or remove information. Return a JSON object mapping each k to its Spanish string.\n\n")


def translate(src):
    entries = []
    for si, sec in enumerate(src["sections"]):
        entries.append({"k": f"s{si}", "en": sec["name"]})
        for ii, (name, desc, _price) in enumerate(sec["items"]):
            entries.append({"k": f"n{si}_{ii}", "en": name})
            if desc:
                entries.append({"k": f"d{si}_{ii}", "en": desc})
    out = {}
    for start in range(0, len(entries), 80):  # chunk: long single calls truncate or change shape
        chunk = entries[start:start + 80]
        for _attempt in range(3):
            got = gemini_json(PROMPT + json.dumps(chunk, ensure_ascii=False))
            if isinstance(got, list):  # some models answer [{"k":..,"es":..}] instead of {k: es}
                got = {g.get("k"): g.get("es") or g.get("v") or g.get("text") for g in got if isinstance(g, dict)}
            if isinstance(got, dict) and all(got.get(e["k"]) for e in chunk):
                out.update(got)
                break
        else:
            raise SystemExit(f"Translation incomplete for keys starting at {chunk[0]['k']}")
    return out


def build(path):
    src = json.load(open(path))
    slug = src["slug"]
    dest = os.path.join(ROOT, "data", "merchants", f"{slug}.json")
    merchant = json.load(open(dest))
    print(f"{slug}: translating {sum(len(s['items']) for s in src['sections'])} items...")
    es = translate(src)

    categories = [{"id": "all", "nameEs": "Todo el Menú", "nameEn": "All Items", "icon": "Utensils"}]
    products, seen = [], set()
    for si, sec in enumerate(src["sections"]):
        cat_id = slugify(sec["name"]) or f"section-{si}"
        categories.append({"id": cat_id, "nameEs": es[f"s{si}"], "nameEn": sec["name"], "icon": "Utensils"})
        for ii, (name, desc, price) in enumerate(sec["items"]):
            pid = slugify(name)
            while pid in seen:
                pid += "-2"
            seen.add(pid)
            products.append({
                "id": pid,
                "categoryId": cat_id,
                "nameEs": es[f"n{si}_{ii}"],
                "nameEn": name,
                "descriptionEs": es.get(f"d{si}_{ii}", ""),
                "descriptionEn": desc,
                "price": price,
                "ctaType": "in_store",
            })

    info = merchant["storeInfo"]
    info.update({
        "address": src["address"],
        "phone": src["phone"],
        "hours": src["hours"],
        "tagline": f"{src['taglineEn']} | {src['taglineEs']}",
        "amenities": src.get("amenities", ["Bilingual Menu"]),
        "paymentMethods": src.get("paymentMethods", []),
    })
    if src.get("displayName"):
        info["name"] = src["displayName"]
    merchant.update({"categories": categories, "products": products, "faqs": src.get("faqs", [])})
    with open(dest, "w") as f:
        json.dump(merchant, f, indent=2, ensure_ascii=False)
        f.write("\n")

    vpath = os.path.join(ROOT, "data", "verified-menus.json")
    verified = json.load(open(vpath))
    verified[slug] = {"source": src["sources"][0], "checked": src["checked"]}
    with open(vpath, "w") as f:
        json.dump(verified, f, indent=2)
        f.write("\n")
    print(f"  wrote {len(products)} items in {len(categories) - 1} sections -> {dest}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        build(p)
