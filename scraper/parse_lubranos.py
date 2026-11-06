#!/usr/bin/env python3
import json, re

with open("/tmp/lubranos_raw.txt") as f:
    lines = [l.strip() for l in f if l.strip()]

# Section headers in Slice Life
sections = [
    "Appetizers", "Specials", "Pizza", "Gluten Free Pizza", "Stromboli & Calzones",
    "Hot Subs", "Philly Cheese Steaks", "Salads", "Pasta", "Baked Dishes",
    "Italian Specialties", "Seafood", "Kid's Menu", "Desserts", "Beverages"
]

items = []
current_section = "Appetizers"

i = 0
while i < len(lines):
    line = lines[i]
    if line in sections:
        current_section = line
        i += 1
        continue
    
    # Check if lines[i+1] or lines[i+2] is a price like $10.00
    if i + 1 < len(lines) and re.match(r"^\$[0-9]+(?:\.[0-9]{2})?$", lines[i+1]):
        name = line
        price = lines[i+1]
        desc = ""
        items.append((current_section, name, price, desc))
        i += 2
        continue
    elif i + 2 < len(lines) and re.match(r"^\$[0-9]+(?:\.[0-9]{2})?$", lines[i+2]):
        name = line
        desc = lines[i+1]
        price = lines[i+2]
        # Skip if name is a generic descriptor
        if not any(k in name.lower() for k in ["arrow", "skip to", "house favorites", "popular items"]):
            items.append((current_section, name, price, desc))
        i += 3
        continue
    
    i += 1

print(f"Total raw items parsed: {len(items)}")
# Deduplicate while preserving order
unique_items = []
seen = set()
for s, n, p, d in items:
    key = n.lower().strip()
    if key not in seen:
        seen.add(key)
        unique_items.append((s, n, p, d))

print(f"Unique items: {len(unique_items)}")
for it in unique_items[:25]:
    print(f"[{it[0]}] {it[1]} | {it[2]} | {it[3][:50]}")
