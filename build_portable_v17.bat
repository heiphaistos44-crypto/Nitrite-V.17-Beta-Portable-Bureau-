@echo off
REM =============================================
REM Build NiTriTe V14 Portable (EXE autonome)
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
pyinstaller --noconfirm --onefile --console --clean --add-data "data;data" --add-data "assets;assets" --add-data "src;src" --hidden-import=psutil --hidden-import=requests --hidden-import=wmi --hidden-import=win32com --hidden-import=win32com.client --hidden-import=pythoncom --collect-submodules win32com --collect-submodules wmi --collect-submodules pythoncom src/v14_mvp/main_app.py --name NiTriTe_V17_Portable

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
