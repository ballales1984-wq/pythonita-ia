@echo off
REM ============================================
REM Script per creare EXE di Pythonita IA
REM ============================================

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║         PYTHONITA IA - CREA ESEGUIBILE .EXE                      ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Verifica PyInstaller
echo [1] Verifico PyInstaller...
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo     PyInstaller non trovato, installo...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo     [ERRORE] Installazione PyInstaller fallita!
        pause
        exit /b 1
    )
)
echo     [OK] PyInstaller trovato

echo.
echo [2] Quale versione vuoi compilare?
echo.
echo     1. GUI con Visualizzatore 3D (Consigliato) - ~150MB
echo     2. CLI Riga di comando (Leggero) - ~80MB
echo     3. Entrambe
echo.

set /p scelta="Scelta (1-3): "

if "%scelta%"=="1" goto build_gui
if "%scelta%"=="2" goto build_cli
if "%scelta%"=="3" goto build_both
goto build_gui

:build_gui
echo.
echo [3] Costruendo GUI con Visualizzatore 3D...
echo     Attendere 2-5 minuti...
echo.

pyinstaller --name=PythonitaIA ^
    --onefile ^
    --windowed ^
    --clean ^
    --add-data=core;core ^
    --add-data=visualizzatore;visualizzatore ^
    --hidden-import=numpy ^
    --hidden-import=matplotlib ^
    --hidden-import=tkinter ^
    --collect-all=matplotlib ^
    --collect-all=numpy ^
    --optimize=2 ^
    gui_robot_3d.py

if %errorlevel%==0 (
    echo.
    echo ╔══════════════════════════════════════════════════════════════════╗
    echo ║  ✅ EXE CREATO CON SUCCESSO!                                      ║
    echo ╚══════════════════════════════════════════════════════════════════╝
    echo.
    echo 📦 File: dist\PythonitaIA.exe
    echo.
    echo 🚀 Esegui con:
    echo    dist\PythonitaIA.exe
    echo.
) else (
    echo [ERRORE] Build fallita!
)
goto end

:build_cli
echo.
echo [3] Costruendo CLI...
echo.

pyinstaller --name=PythonitaIA_CLI ^
    --onefile ^
    --console ^
    --clean ^
    --add-data=core;core ^
    --hidden-import=core ^
    --optimize=2 ^
    main.py

if %errorlevel%==0 (
    echo ✅ CLI EXE creato: dist\PythonitaIA_CLI.exe
)
goto end

:build_both
echo.
echo [3] Costruendo entrambe le versioni...
echo.
call :build_gui
call :build_cli
goto end

:end
echo.
echo ✅ Build completata!
echo    Controlla la cartella 'dist\'
echo.
pause

