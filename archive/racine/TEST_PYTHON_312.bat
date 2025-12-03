@echo off
echo ========================================
echo TEST NITRITE V13 AVEC PYTHON 3.12
echo ========================================
echo.

REM Vérifier version Python
echo 1. Verification version Python...
py -3.12 --version
if errorlevel 1 (
    echo.
    echo [ERREUR] Python 3.12 non trouve !
    echo.
    echo Telechargez Python 3.12.7 :
    echo https://www.python.org/downloads/release/python-3127/
    echo.
    pause
    exit /b 1
)

echo.
echo 2. Creation environnement virtuel Python 3.12...
if exist "venv_nitrite" (
    echo    Environnement existe deja, suppression...
    rmdir /s /q venv_nitrite
)
py -3.12 -m venv venv_nitrite
if errorlevel 1 (
    echo [ERREUR] Impossible de creer l'environnement virtuel !
    pause
    exit /b 1
)

echo.
echo 3. Activation environnement virtuel...
call venv_nitrite\Scripts\activate.bat

echo.
echo 4. Installation des dependances...
python -m pip install --upgrade pip
pip install customtkinter==5.2.2 pillow
if errorlevel 1 (
    echo [ERREUR] Echec installation dependances !
    pause
    exit /b 1
)

echo.
echo 5. Verification versions installees...
pip list | findstr "customtkinter pillow"

echo.
echo ========================================
echo ENVIRONNEMENT PRET !
echo ========================================
echo.
echo Python 3.12 : OK
echo CustomTkinter 5.2.2 : OK
echo Pillow : OK
echo.
echo ========================================
echo LANCEMENT DE L'APPLICATION...
echo ========================================
echo.
echo Appuyez sur une touche pour lancer NiTriTe V13...
pause > nul

REM Lancer l'application
python nitrite_v13_modern.py

echo.
echo ========================================
echo APPLICATION FERMEE
echo ========================================
echo.
echo Si l'application a fonctionne sans crash :
echo   - Les 8 pages s'affichent correctement
echo   - La navigation est fluide
echo   - Plus de "carres noirs/gris"
echo   = Python 3.12 a resolu le probleme !
echo.
echo Si des erreurs persistent :
echo   - Verifiez les logs dans : logs\
echo   - Consultez : docs\ANALYSE_COMPLETE_BUGS_V13.md
echo.
pause