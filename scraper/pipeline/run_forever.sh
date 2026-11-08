#!/bin/bash
# Repeats run_pipeline.sh until nothing new gets built. When the free Gemini quota for the day is
# used up, waits for the daily reset (midnight US Pacific) and continues.
cd "$(dirname "$0")/../.."
P=scraper/pipeline
for round in $(seq 1 40); do
  before=$(python3 -c "import json;print(len(json.load(open('data/verified-menus.json'))))")
  echo "=== round $round $(date) verified=$before"
  bash $P/run_pipeline.sh
  after=$(python3 -c "import json;print(len(json.load(open('data/verified-menus.json'))))")
  echo "=== round $round done verified=$after"
  if python3 -c "import sys;sys.path.insert(0,'scraper');import build_real_menu as B;sys.exit(0 if B.daily_quota_hit() else 1)"; then
    # sleep until the Pacific date changes (+5 min)
    secs=$(python3 -c "import time;t=time.time()-8*3600;print(int(86400-(t%86400))+300)")
    echo "quota used up; sleeping ${secs}s until reset"; sleep $secs; continue
  fi
  if [ "$after" = "$before" ]; then echo "no progress; stopping"; break; fi
done
