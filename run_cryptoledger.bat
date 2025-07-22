@echo on
title Starting CryptoLedger Local Server...
cd /d "%~dp0"
echo [%DATE% %TIME%] Starting CryptoLedger >> startup_log.txt
call venv\Scripts\activate
timeout /t 2 >nul
python manage.py runserver 8020 >> startup_log.txt 2>&1
echo [%DATE% %TIME%] Finished runserver >> startup_log.txt
pause
start http://localhost:8020