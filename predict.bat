@echo off
chcp 65001 >nul

if not exist ".venv" (
    echo  ❌ Önce setup.bat çalıştırın!
    pause
    exit /b 1
)

if "%~1"=="" (
    echo.
    echo  🍽  FoodCalorie AI
    echo.
    echo  Kullanım: predict.bat [görsel_yolu]
    echo  Örnek:    predict.bat yemek.jpg
    echo.
    pause
    exit /b 0
)

.venv\Scripts\python predict.py %*
