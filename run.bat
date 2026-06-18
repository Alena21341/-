@echo off
chcp 65001 >nul
echo.
echo ========================================
echo Ozon Reviews Auto Responder
echo ========================================
echo.
echo Запуск программы...
echo.
python main.py
echo.
if errorlevel 1 (
    echo.
    echo ❌ Ошибка при запуске программы!
    echo.
    echo Убедитесь, что:
    echo 1. Python установлен и добавлен в PATH
    echo    Проверка: python --version
    echo.
    echo 2. Установлены все зависимости
    echo    Запустите: pip install -r requirements.txt
    echo.
    echo 3. Вы в папке с программой
    echo.
    pause
)
