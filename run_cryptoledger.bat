:: Cap log file size (e.g. 1MB = 1048576 bytes)
set "LOG_PATH=logs\startup_log.txt"
for %%A in ("%LOG_PATH%") do set "LOG_SIZE=%%~zA"
if %LOG_SIZE% GEQ 1048576 (
    echo [LOG ROTATION] %DATE% %TIME% Log exceeded size limit, truncating... > "%LOG_PATH%"
) else (
    echo [LOG CHECK] %DATE% %TIME% Log size OK (%LOG_SIZE% bytes) >> "%LOG_PATH%"
)

@echo off
title Starting CryptoLedger Local Server...
cd /d "%~dp0"

:: Log init timestamp
echo [STARTUP INIT] [%DATE% %TIME%] Boot script triggered >> logs\startup_log.txt

:: Ensure Windows Time Service is running
sc query w32time | find "RUNNING" >nul
if errorlevel 1 (
    echo [TIME SERVICE] Not running — starting now >> logs\startup_log.txt
    net start w32time >> logs\startup_log.txt 2>&1
) else (
    echo [TIME SERVICE] Already running >> logs\startup_log.txt
)

:: Sync system time
w32tm /resync >> logs\startup_log.txt 2>&1
if errorlevel 1 (
    echo [TIME SYNC] System time resync FAILED >> logs\startup_log.txt
    timeout /t 5 >nul
    echo [TIME SYNC] Retrying time sync... >> logs\startup_log.txt
    w32tm /resync >> logs\startup_log.txt 2>&1
    if errorlevel 1 (
        echo [TIME SYNC] Retry also failed — continuing anyway >> logs\startup_log.txt
    ) else (
        echo [TIME SYNC] Retry successful >> logs\startup_log.txt
    )
) else (
    echo [TIME SYNC] System time resynced successfully >> logs\startup_log.txt
)

:: Log post-sync timestamp
echo [POST-SYNC TIME] [%DATE% %TIME%] Time check complete >> logs\startup_log.txt

:: Activate Python environment
call venv\Scripts\activate
echo [ENV] [%DATE% %TIME%] Virtualenv activated >> logs\startup_log.txt

:: Wait for service readiness
timeout /t 10 >nul

:: Launch Django server
python manage.py runserver 8020 >> logs\startup_log.txt 2>&1
echo [DJANGO] [%DATE% %TIME%] Finished runserver >> logs\startup_log.txt

:: Open browser to local server
start http://localhost:8020
echo [COMPLETE] [%DATE% %TIME%] CryptoLedger boot sequence complete >> logs\startup_log.txt