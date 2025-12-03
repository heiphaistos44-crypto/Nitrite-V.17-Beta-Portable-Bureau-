@echo off
chcp 65001 >nul
title NiTriTe V14 - Lanceur Automatique

echo.
echo ═══════════════════════════════════════════════════════════════
echo   🚀 NiTriTe V14 MVP - Maintenance Informatique Pro
echo ═══════════════════════════════════════════════════════════════
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERREUR: Python n'est pas installé ou pas dans le PATH
    echo.
    echo 📥 Téléchargez Python 3.8-3.12:
    echo    https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version

REM Vérifier dépendances principales
echo.
echo 🔍 Vérification des dépendances...

REM Vérifier CustomTkinter
python -c "import customtkinter" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  CustomTkinter manquant
    set NEED_INSTALL=1
) else (
    echo ✅ CustomTkinter OK
)

REM Vérifier requests
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  requests manquant
    set NEED_INSTALL=1
) else (
    echo ✅ requests OK
)

REM Vérifier psutil
python -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  psutil manquant
    set NEED_INSTALL=1
) else (
    echo ✅ psutil OK
)

REM Installer si nécessaire
if defined NEED_INSTALL (
    echo.
    echo 📦 Installation des dépendances manquantes...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ❌ Échec installation des dépendances
        pause
        exit /b 1
    )
    echo.
    echo ✅ Installation terminée
)

REM Lancer l'application
echo.
echo ═══════════════════════════════════════════════════════════════
echo   ▶️  LANCEMENT DE L'APPLICATION
echo ═══════════════════════════════════════════════════════════════
echo.

python -m src.v17_mvp.main_app

REM Gestion sortie
if errorlevel 1 (
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo   ❌ L'APPLICATION S'EST TERMINÉE AVEC UNE ERREUR
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo 💡 Vérifiez:
    echo    • Tous les fichiers sont présents dans src/v14_mvp/
    echo    • Le fichier data/programs.json existe
    echo    • Python 3.8-3.12 est installé
    echo.
    pause
) else (
    echo.
    echo ✅ Application fermée normalement
)