#!/bin/bash

cd "$(dirname "$0")"
mkdir -p logs

LOGFILE="logs/startup_log.txt"
echo "[`date '+%Y-%m-%d %H:%M:%S'`] Starting CryptoLedger" >> "$LOGFILE"

PYTHON_BIN="/home/techie-guy92/Projects/Django/CryptoLedger/venv/bin/python"
GUNICORN="/home/techie-guy92/Projects/Django/CryptoLedger/venv/bin/gunicorn"

echo "[`date '+%Y-%m-%d %H:%M:%S'`] Using Python: $PYTHON_BIN" >> "$LOGFILE"

exec "$GUNICORN" config.asgi:application \
  --worker-class uvicorn.workers.UvicornWorker \
  --workers 4 \
  --bind 0.0.0.0:8020 \
  --log-level info \
  --pid logs/gunicorn.pid \
  --timeout 120 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log >> "$LOGFILE" 2>&1