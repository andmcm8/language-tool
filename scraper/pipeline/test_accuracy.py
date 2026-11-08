#!/usr/bin/env python3
"""Accuracy test: run the extractor on restaurants whose menus were transcribed by hand
(scraper/real_menus/) and compare item names and prices."""
import sys, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import extract_menu as E
d = json.load(open(os.path.join(HERE, "data", "test_sites.json")))
for t in d["tests"]:
    slug = t["slug"]; real = t["slug"][2:]
    r = E.process(t, d["sites"][slug])
    man = json.load(open(os.path.join(HERE, "..", "real_menus", real + ".json")))
    M = {E.norm(i[0]): i[2] for s in man["sections"] for i in s["items"]}
    dr = json.load(open(os.path.join(E.DRAFTS, slug + ".json"))) if os.path.exists(os.path.join(E.DRAFTS, slug + ".json")) else {"sections": []}
    A = {E.norm(i[0]): i[2] for s in dr["sections"] for i in s["items"]}
    both = set(M) & set(A)
    pm = sum(1 for k in both if M[k] == A[k] or not M[k] and not A[k])
    print(f"{real}: status={r['status']} problems={r.get('problems')} manual={len(M)} auto={len(A)} matched={len(both)} price_agree={pm}/{len(both)}")
    print("   only manual:", sorted(set(M) - set(A))[:12])
    print("   only auto  :", sorted(set(A) - set(M))[:12])
    print("   price diffs:", [(k, M[k], A[k]) for k in both if M[k] != A[k]][:8])
