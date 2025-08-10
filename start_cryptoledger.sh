#!/bin/bash

cd "$(dirname "$0")"
mkdir -p logs

echo "[`date '+%Y-%m-%d %H:%M:%S'`] Starting CryptoLedger" >> logs/startup_log.txt

# Check if server is already running
if lsof -i:8020 > /dev/null; then
  echo "[`date '+%Y-%m-%d %H:%M:%S'`] Server already running on port 8020" >> logs/startup_log.txt
  exit 0
fi

source venv/bin/activate
echo "[`date '+%Y-%m-%d %H:%M:%S'`] Virtualenv activated" >> logs/startup_log.txt

sleep 2

nohup python manage.py runserver 8020 >> logs/startup_log.txt 2>&1 &
echo "[`date '+%Y-%m-%d %H:%M:%S'`] Finished runserver" >> logs/startup_log.txt

xdg-open http://localhost:8020
echo "[`date '+%Y-%m-%d %H:%M:%S'`] CryptoLedger boot sequence complete" >> logs/startup_log.txt