@echo off
title LATEC.IN - Frontend Dev Server
echo ========================================
echo   LATEC.IN - Servidor de desenvolvimento
echo ========================================
echo.
echo Abrindo servidor em http://localhost:5500
echo.

cd /d "%~dp0"

start "" http://localhost:5500
python -m http.server 5500

pause
