@echo off
title Starting CryptoLedger Local Server...
cd /d "%~dp0"

echo [STARTUP INIT] [%DATE% %TIME%] Boot script triggered >> logs\startup_log.txt

:: Sync system time before launch (protects against drift)
timeout /t 3 >nul
w32tm /resync
echo [TIME SYNC] [%DATE% %TIME%] System time resynced >> logs\startup_log.txt
timeout /t 3 >nul

echo [POST-SYNC TIME] %DATE% %TIME% >> logs\startup_log.txt

call venv\Scripts\activate
echo [ENV] [%DATE% %TIME%] Virtualenv activated >> logs\startup_log.txt

timeout /t 10 >nul
python manage.py runserver 8020 >> logs\startup_log.txt 2>&1
echo [DJANGO] [%DATE% %TIME%] Finished runserver >> logs\startup_log.txt

start http://localhost:8020
echo [COMPLETE] [%DATE% %TIME%] CryptoLedger boot sequence complete >> logs\startup_log.txt