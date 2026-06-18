@echo off
chcp 65001 >nul
cls
echo.
echo ========================================
echo  OZON AUTO ANSWERER
echo ========================================
echo.
echo Запуск программы...
echo.
python auto.py
if errorlevel 1 (
    echo.
    echo ОШИБКА!
    echo.
    echo Убедитесь что:
    echo 1. Python установлен
    echo 2. Интернет подключен (для установки модулей)
    echo.
)
pause
