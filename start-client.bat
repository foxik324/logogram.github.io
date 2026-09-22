@echo off
chcp 65001 >nul
title Logogram Client

echo ============================================
echo   Logogram: запуск сервера и GUI-клиента
echo ============================================
echo.

cd /d "%~dp0Logogram"

where node >nul 2>nul
if errorlevel 1 (
    echo [!] Node.js не найден в PATH.
    pause
    exit /b 1
)

echo Запускаю сервер Logogram на http://localhost:3000 ...
start "Logogram Server" cmd /k "node server.js"

echo Жду запуск сервера...
timeout /t 2 /nobreak >nul

echo Открываю GUI-клиент в браузере...
start "" "http://localhost:3000/client.html"

echo.
echo Готово. Сервер работает в отдельном окне.
echo Клиент: http://localhost:3000/client.html
echo.
echo Чтобы закрыть сервер — закройте окно "Logogram Server".
echo.
pause