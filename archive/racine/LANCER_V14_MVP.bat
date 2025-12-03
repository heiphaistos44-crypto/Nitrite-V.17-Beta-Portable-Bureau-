@echo off
chcp 65001 >nul
title NiTriTe V14 MVP - Lancement
color 0A

echo.
echo ══════════════════════════════════════════════════════════
echo   🚀 NiTriTe V14 MVP - Maintenance Informatique Pro
echo ══════════════════════════════════════════════════════════
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans PATH
    echo.
    echo 📥 Téléchargez Python 3.12: https://www.python.org/downloads/
    echo    ⚠️  Cochez "Add Python to PATH" lors de l'installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version
echo.

REM Vérifier CustomTkinter
echo 🔍 Vérification CustomTkinter...
python -c "import customtkinter; print('✅ CustomTkinter', customtkinter.__version__)" 2>nul
if errorlevel 1 (
    echo ⚠️  CustomTkinter non installé
    echo 📦 Installation en cours...
    pip install customtkinter
    if errorlevel 1 (
        echo ❌ Échec installation CustomTkinter
        pause
        exit /b 1
    )
    echo ✅ CustomTkinter installé
)
echo.

REM Lancer application
echo 🚀 Lancement NiTriTe V14 MVP...
echo.
python -m src.v14_mvp.main_app

REM Pause si erreur
if errorlevel 1 (
    echo.
    echo ❌ L'application s'est terminée avec une erreur
    pause
)