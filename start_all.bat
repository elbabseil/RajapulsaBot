@echo off
title RAJAPULSA BOT SYSTEM

color 0A

echo ==================================================
echo              RAJAPULSA BOT SYSTEM
echo ==================================================
echo.
echo Sistem ini akan menjalankan:
echo.
echo [1] FastAPI Backend
echo     - API Server RajaPulsa
echo     - Swagger Documentation
echo     - Payment Gateway Xendit
echo     - Database Service
echo.
echo [2] Telegram Bot
echo     - Customer Service Bot
echo     - Produk Pulsa
echo     - Paket Data
echo     - Token PLN
echo     - Voucher Game
echo     - Tagihan Pascabayar
echo.
echo ==================================================
echo CARA PENGGUNAAN
echo ==================================================
echo.
echo 1. Jalankan file ini dengan klik 2 kali.
echo.
echo 2. Tunggu sampai muncul:
echo.
echo    Uvicorn running on:
echo    http://127.0.0.1:8000
echo.
echo 3. Buka Swagger API:
echo.
echo    http://127.0.0.1:8000/docs
echo.
echo 4. Jalankan Telegram:
echo.
echo    Buka aplikasi Telegram
echo    Cari bot RajaPulsa
echo    Tekan tombol START
echo.
echo 5. Jangan menutup jendela:
echo.
echo    - RAJAPULSA API
echo    - RAJAPULSA TELEGRAM BOT
echo.
echo ==================================================
echo FITUR SISTEM
echo ==================================================
echo.
echo API:
echo  - Product Management
echo  - User Management
echo  - Transaction Processing
echo  - QRIS Payment
echo.
echo BOT:
echo  - Pembelian Pulsa
echo  - Paket Internet
echo  - Token PLN
echo  - Voucher Digital
echo  - Pembayaran Tagihan
echo.
echo ==================================================
echo START SYSTEM
echo ==================================================

cd /d C:\RajapulsaBot


echo.
echo [1/2] Mengaktifkan Virtual Environment...
call venv\Scripts\activate


echo.
echo [2/2] Menjalankan FastAPI...
start "RAJAPULSA API SERVER" cmd /k "uvicorn api.main:app"


timeout /t 3 > nul


echo.
echo Menjalankan Telegram Bot...
start "RAJAPULSA TELEGRAM BOT" cmd /k "python main.py"


echo.
echo ==================================================
echo RAJAPULSA SYSTEM SUDAH AKTIF
echo ==================================================
echo.
echo Swagger:
echo http://127.0.0.1:8000/docs
echo.
echo Tekan tombol apapun untuk keluar.
pause > nul