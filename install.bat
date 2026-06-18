@echo off
chcp 65001 >nul
echo.
echo ========================================
echo Ozon Reviews Auto Responder - Установка
echo ========================================
echo.

echo Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo Пожалуйста, установите Python с https://python.org
    echo Убедитесь, что выбран "Add Python to PATH"
    pause
    exit /b 1
)

echo ✓ Python найден

echo.
echo Установка зависимостей...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Ошибка при установке зависимостей
    pause
    exit /b 1
)

echo.
echo ✓ Установка завершена!
echo.
echo Для запуска программы используйте:
echo   python main.py
echo.
pause
