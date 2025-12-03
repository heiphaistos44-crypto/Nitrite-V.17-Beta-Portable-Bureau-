@echo off
chcp 65001 >nul
title NiTriTe V14 MVP - Lancement avec Python 3.12
color 0A

echo.
echo ══════════════════════════════════════════════════════════
echo   🚀 NiTriTe V14 MVP - Python 3.12 Forcé
echo ══════════════════════════════════════════════════════════
echo.

REM Chemins possibles pour Python 3.12
set PYTHON312_PATHS=^
    "C:\Python312\python.exe" ^
    "C:\Program Files\Python312\python.exe" ^
    "C:\Program Files (x86)\Python312\python.exe" ^
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" ^
    "%APPDATA%\Python\Python312\python.exe"

set PYTHON_FOUND=0

echo 🔍 Recherche de Python 3.12...
echo.

for %%p in (%PYTHON312_PATHS%) do (
    if exist %%p (
        echo ✅ Python 3.12 trouvé: %%p
        set PYTHON_EXE=%%p
        set PYTHON_FOUND=1
        goto :found
    )
)

:notfound
echo ❌ Python 3.12 introuvable dans les chemins standards
echo.
echo 📥 Téléchargez Python 3.12:
echo    https://www.python.org/downloads/release/python-3120/
echo.
echo ⚠️  Lors de l'installation:
echo    1. Cochez "Add Python to PATH"
echo    2. Choisissez "Customize installation"
echo    3. Notez le chemin d'installation
echo.
pause
exit /b 1

:found
echo.
%PYTHON_EXE% --version
echo.

REM Vérifier CustomTkinter
echo 🔍 Vérification CustomTkinter...
%PYTHON_EXE% -c "import customtkinter; print('✅ CustomTkinter', customtkinter.__version__)" 2>nul
if errorlevel 1 (
    echo ⚠️  CustomTkinter non installé pour Python 3.12
    echo 📦 Installation en cours...
    %PYTHON_EXE% -m pip install customtkinter
    if errorlevel 1 (
        echo ❌ Échec installation CustomTkinter
        pause
        exit /b 1
    )
    echo ✅ CustomTkinter installé
)
echo.

REM Lancer application
echo 🚀 Lancement NiTriTe V14 MVP avec Python 3.12...
echo.
%PYTHON_EXE% -m src.v14_mvp.main_app

REM Pause si erreur
if errorlevel 1 (
    echo.
    echo ❌ L'application s'est terminée avec une erreur
    pause
)