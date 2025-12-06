@echo off
REM =============================================
REM Build NiTriTe V17 Portable (EXE autonome)
REM =============================================

REM 1. Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    pause
    exit /b 1
)

REM 2. Installer PyInstaller si besoin
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation de PyInstaller...
    pip install pyinstaller
)

REM 3. Nettoyer l'ancien build
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__

REM 4. Lancer le build avec le fichier .spec (plus propre et maintenable)
echo [INFO] Utilisation du fichier NiTriTe_V17_Portable.spec pour le build...
pyinstaller --noconfirm --clean NiTriTe_V17_Portable.spec

REM 5. Afficher le résultat
if exist dist\NiTriTe_V17_Portable.exe (
    echo.
    echo [OK] Build termine !
    echo Fichier pret : dist\NiTriTe_V17_Portable.exe
    echo.
) else (
    echo.
    echo [ERREUR] Le build a echoue !
    echo.
)
pause
