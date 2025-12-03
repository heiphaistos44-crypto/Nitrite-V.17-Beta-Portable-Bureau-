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

REM 4. Lancer le build
pyinstaller --noconfirm --onefile --console --clean --add-data "data;data" --add-data "assets;assets" --add-data "src;src" src/v14_mvp/main_app.py --name NiTriTe_V17_Portable

REM 5. Déplacer build et dist dans le dossier final
if not exist "NiTriTe V.17 Portable" mkdir "NiTriTe V.17 Portable"
if exist build move build "NiTriTe V.17 Portable"
if exist dist move dist "NiTriTe V.17 Portable"

REM 6. Afficher le résultat
if exist "NiTriTe V.17 Portable\dist\NiTriTe_V17_Portable.exe" (
    echo.
    echo [OK] Build termine !
    echo Fichier pret : NiTriTe V.17 Portable\dist\NiTriTe_V17_Portable.exe
    echo.
) else (
    echo.
    echo [ERREUR] Le build a echoue !
    echo.
)
pause