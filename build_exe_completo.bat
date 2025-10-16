@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║  RICOSTRUZIONE EXE COMPLETO - Con tutte le dipendenze           ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

echo [1] Pulizia build precedente...
if exist build rmdir /s /q build
if exist dist\PythonitaIA.exe del /f /q dist\PythonitaIA.exe

echo [2] Creazione exe con TUTTE le dipendenze...
echo     (Attendere 3-5 minuti)
echo.

pyinstaller --name=PythonitaIA ^
    --onefile ^
    --windowed ^
    --clean ^
    --add-data="core:core" ^
    --add-data="visualizzatore:visualizzatore" ^
    --hidden-import=numpy ^
    --hidden-import=matplotlib ^
    --hidden-import=matplotlib.pyplot ^
    --hidden-import=tkinter ^
    --hidden-import=spacy ^
    --hidden-import=spacy.cli ^
    --hidden-import=core ^
    --hidden-import=core.parser ^
    --hidden-import=core.generatore ^
    --hidden-import=visualizzatore ^
    --collect-all=matplotlib ^
    --collect-all=numpy ^
    --collect-all=spacy ^
    --collect-submodules=spacy ^
    --optimize=2 ^
    gui_robot_3d.py

if %errorlevel%==0 (
    echo.
    echo ╔══════════════════════════════════════════════════════════════════╗
    echo ║  ✅ EXE CREATO CON SUCCESSO!                                      ║
    echo ╚══════════════════════════════════════════════════════════════════╝
    echo.
    echo File: dist\PythonitaIA.exe
    echo.
    
    REM Copia sul desktop
    copy /y dist\PythonitaIA.exe "%USERPROFILE%\Desktop\PythonitaIA.exe"
    echo.
    echo ✅ Copiato anche sul Desktop!
    echo.
    echo Ora prova: Desktop\PythonitaIA.exe
    echo.
) else (
    echo.
    echo ❌ BUILD FALLITA!
    echo.
)

pause

