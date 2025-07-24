cd "$(dirname "$0")"
echo "[`date '+%Y-%m-%d %H:%M:%S'`] Starting CryptoLedger" >> logs/startup_log.txt
source venv/bin/activate
echo "[`date '+%Y-%m-%d %H:%M:%S'`] Virtualenv activated" >> logs/startup_log.txt
sleep 2
python manage.py runserver 8020 >> logs/startup_log.txt 2>&1 &
echo "[`date '+%Y-%m-%d %H:%M:%S'`] Finished runserver" >> logs/startup_log.txt
xdg-open http://localhost:8020
echo "[`date '+%Y-%m-%d %H:%M:%S'`] CryptoLedger boot sequence complete" >> logs/startup_log.txt