@echo off
title Starting CryptoLedger Local Server...
cd /d "%~dp0"
call venv\Scripts\activate
timeout /t 2 >nul
python manage.py runserver 8020
pause
start http://localhost:8020