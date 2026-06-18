@echo off
chcp 65001 >nul
cls
echo.
echo ========================================
echo    Ozon Reviews Auto Responder
echo    РЕЖИМ ОТЛАДКИ (с видимой консолью)
echo ========================================
echo.
echo Запуск программы...
echo Вы увидите все ошибки и сообщения отладки в этом окне
echo.
python main.py
echo.
echo Программа закончила работу.
pause
