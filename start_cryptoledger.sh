#!/bin/bash

cd "$(dirname "$0")"
mkdir -p logs

LOGFILE="logs/startup_log.txt"
echo "[`date '+%Y-%m-%d %H:%M:%S'`] Starting CryptoLedger" >> "$LOGFILE"

source venv/bin/activate
echo "[`date '+%Y-%m-%d %H:%M:%S'`] Virtualenv activated" >> "$LOGFILE"

# Run Django server in foreground so systemd can track it
exec python manage.py runserver 0.0.0.0:8020 >> "$LOGFILE" 2>&1