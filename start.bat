@echo off
chcp 65001 >nul
cls

echo.
echo ========================================
echo    Ozon Reviews Helper - ПРОСТАЯ ВЕРСИЯ
echo ========================================
echo.

REM Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo Установите Python с https://python.org
    pause
    exit /b 1
)

REM Устанавливаем зависимости
echo Установка зависимостей...
pip install -q pyperclip

REM Запускаем программу
echo.
echo Запускаю приложение...
echo.
python simple_main.py

pause
