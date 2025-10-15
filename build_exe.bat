@echo off
REM Script per creare gli eseguibili di Pythonita IA v2.0
REM Richiede PyInstaller installato: pip install pyinstaller

echo ========================================
echo   Pythonita IA - Build Eseguibili
echo ========================================
echo.

REM Verifica che PyInstaller sia installato
python -c "import PyInstaller" 2>NUL
if errorlevel 1 (
    echo [ERRORE] PyInstaller non trovato!
    echo Installalo con: pip install pyinstaller
    pause
    exit /b 1
)

echo [1/4] Pulizia build precedenti...
if exist "build" rmdir /s /q build
if exist "dist\Pythonita_IA.exe" del /q "dist\Pythonita_IA.exe"
if exist "dist\Pythonita_CLI.exe" del /q "dist\Pythonita_CLI.exe"
echo      OK - Pulizia completata
echo.

echo [2/4] Build GUI (Pythonita_IA.exe)...
pyinstaller --clean pythonita.spec
if errorlevel 1 (
    echo [ERRORE] Build GUI fallita!
    pause
    exit /b 1
)
echo      OK - GUI compilata
echo.

echo [3/4] Build CLI (Pythonita_CLI.exe)...
pyinstaller --clean pythonita_cli.spec
if errorlevel 1 (
    echo [ERRORE] Build CLI fallita!
    pause
    exit /b 1
)
echo      OK - CLI compilata
echo.

echo [4/4] Verifica eseguibili...
if exist "dist\Pythonita_IA.exe" (
    echo      OK - dist\Pythonita_IA.exe [GUI]
) else (
    echo [ERRORE] Pythonita_IA.exe non trovato!
)

if exist "dist\Pythonita_CLI.exe" (
    echo      OK - dist\Pythonita_CLI.exe [CLI]
) else (
    echo [ERRORE] Pythonita_CLI.exe non trovato!
)
echo.

echo ========================================
echo   Build completata con successo!
echo ========================================
echo.
echo Eseguibili creati in: dist\
echo - Pythonita_IA.exe  (Interfaccia Grafica)
echo - Pythonita_CLI.exe (Interfaccia Terminale)
echo.
pause

