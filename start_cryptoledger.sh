echo "[`date '+%Y-%m-%d %H:%M:%S'`] Starting CryptoLedger" >> startup_log.txt
cd "$(dirname "$0")"
source venv/bin/activate
echo "[`date '+%Y-%m-%d %H:%M:%S'`] Virtualenv activated" >> startup_log.txt
sleep 2
python manage.py runserver 8020 >> startup_log.txt 2>&1 &
echo "[`date '+%Y-%m-%d %H:%M:%S'`] Finished runserver" >> startup_log.txt
xdg-open http://localhost:8020
echo "[`date '+%Y-%m-%d %H:%M:%S'`] CryptoLedger boot sequence complete" >> startup_log.txt