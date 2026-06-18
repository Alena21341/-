@echo off
chcp 65001 >nul
python main.py
if errorlevel 1 (
    echo.
    echo ❌ Ошибка при запуске программы!
    echo.
    echo Убедитесь, что:
    echo 1. Python установлен и добавлен в PATH
    echo 2. Установлены все зависимости (запустите install.bat)
    echo 3. Вы в директории с программой
    echo.
    pause
)
