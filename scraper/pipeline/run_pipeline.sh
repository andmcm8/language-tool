#!/bin/bash
# Runs the pipeline steps one after another (several steps write the same JSON files, so they
# must never overlap). Log: scraper/pipeline/data/pipeline.log
cd "$(dirname "$0")/../.."
P=scraper/pipeline
log(){ echo "[$(date +%H:%M:%S)] $*"; }
while pgrep -f "extract_menu.py|fetch_sites.py|render_sites.py|ocr_menus.py|fix_uncovered.py" >/dev/null; do sleep 20; done
log "fetch"; python3 $P/fetch_sites.py | tail -1
log "render"; python3 $P/render_sites.py --workers 5 | tail -1
log "extract 1"; python3 $P/extract_menu.py --workers 4 | grep -c . 
log "ocr"; python3 $P/ocr_menus.py | tail -1
python3 - <<'PY'
import json
s=json.load(open('scraper/pipeline/data/sites.json'));p='scraper/pipeline/data/extract.json';r=json.load(open(p))
for k,v in s.items():
    if any(x.get('type')=='ocr' for x in v.get('pages',[])) and r.get(k,{}).get('status') in ('no-menu-text','no-menu'): r.pop(k)
json.dump(r,open(p,'w'),indent=0)
PY
log "extract 2 (ocr)"; python3 $P/extract_menu.py --workers 4 | grep -c .
log "uncovered"; python3 $P/finalize.py --uncovered
python3 $P/fix_uncovered.py | grep -c added
log "extract 3 (uncovered)"; python3 $P/extract_menu.py --workers 4 | grep -c .
log "chownow"; python3 $P/chownow_menus.py | grep -c ok
log "reverify"; python3 $P/reverify.py | grep -c .
log "finalize"; python3 $P/finalize.py 2>/dev/null | wc -w
log "builds"; python3 $P/run_builds.py --batch 15
log "DONE"
