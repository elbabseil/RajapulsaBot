@echo off
title STOP RAJAPULSA SYSTEM

color 0C

echo ==================================================
echo             STOP RAJAPULSA SYSTEM
echo ==================================================
echo.
echo Sistem akan menghentikan:
echo.
echo [1] FastAPI Server (Uvicorn)
echo [2] Telegram Bot (Python)
echo.
echo ==================================================

echo.
echo Mengecek proses aktif...


echo.
echo Menghentikan FastAPI Server...
taskkill /F /FI "WINDOWTITLE eq RAJAPULSA API SERVER*" > nul 2>&1


echo.
echo Menghentikan Telegram Bot...
taskkill /F /FI "WINDOWTITLE eq RAJAPULSA TELEGRAM BOT*" > nul 2>&1


echo.
echo Membersihkan proses Python yang masih berjalan...
taskkill /F /IM python.exe > nul 2>&1


echo.
echo ==================================================
echo RAJAPULSA SYSTEM SUDAH DIHENTIKAN
echo ==================================================
echo.
echo Semua service:
echo  - FastAPI API
echo  - Telegram Bot
echo  - Python Worker
echo.
echo sudah berhenti.
echo.

pause