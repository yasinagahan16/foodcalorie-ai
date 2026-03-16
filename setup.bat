@echo off
chcp 65001 >nul
echo.
echo  ═══════════════════════════════════════
echo   🍽  FoodCalorie AI - Kurulum
echo  ═══════════════════════════════════════
echo.

:: Python kontrolü
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  ❌ Python bulunamadı!
    echo  Python'u https://www.python.org/downloads/ adresinden indirin.
    echo  Kurulumda "Add Python to PATH" seçeneğini işaretleyin.
    pause
    exit /b 1
)

echo  ✓ Python bulundu
python --version

:: Sanal ortam oluştur
if not exist ".venv" (
    echo.
    echo  📦 Sanal ortam oluşturuluyor...
    python -m venv .venv
    echo  ✓ Sanal ortam oluşturuldu
) else (
    echo  ✓ Sanal ortam zaten mevcut
)

:: Bağımlılıkları kur
echo.
echo  📦 Bağımlılıklar kuruluyor...
.venv\Scripts\pip install -r requirements.txt --quiet
echo  ✓ Bağımlılıklar kuruldu

echo.
echo  ═══════════════════════════════════════
echo   ✅ Kurulum tamamlandı!
echo  ═══════════════════════════════════════
echo.
echo  Kullanım:
echo    predict.bat yemek.jpg     — Tek görsel analiz
echo    python app.py             — Masaüstü uygulama
echo.
pause
