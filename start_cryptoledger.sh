#!/bin/bash

cd "$(dirname "$0")"
mkdir -p logs

LOGFILE="logs/startup_log.txt"
echo "[`date '+%Y-%m-%d %H:%M:%S'`] Starting CryptoLedger" >> "$LOGFILE"

PYTHON_BIN="/home/techie-guy92/Projects/Django/CryptoLedger/venv/bin/python"
echo "[`date '+%Y-%m-%d %H:%M:%S'`] Using Python: $PYTHON_BIN" >> "$LOGFILE"

exec "$PYTHON_BIN" manage.py runserver 0.0.0.0:8020 >> "$LOGFILE" 2>&1