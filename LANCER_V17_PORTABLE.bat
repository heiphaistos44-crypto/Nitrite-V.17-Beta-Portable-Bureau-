@echo off
REM =============================================
REM Lancer NiTriTe V14 Portable (EXE autonome)
REM =============================================

if not exist "dist\NiTriTe_V14_Portable.exe" (
    echo [ERREUR] Le fichier dist\NiTriTe_V14_Portable.exe n'existe pas !
    echo Lancez d'abord build_portable_v14.bat
    pause
    exit /b 1
)

start "" dist\NiTriTe_V14_Portable.exe
