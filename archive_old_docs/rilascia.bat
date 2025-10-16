@echo off
REM ============================================
REM Script per rilasciare Pythonita IA v3.1.0
REM ============================================

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║         RILASCIO PYTHONITA IA v3.1.0 SU GITHUB                   ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Verifica tag locale
echo [1] Verifico tag locale...
git tag -l | findstr "v3.1.0" >nul
if %errorlevel%==0 (
    echo     [OK] Tag v3.1.0 trovato localmente
) else (
    echo     [ERRORE] Tag v3.1.0 non trovato!
    echo     Esegui: git tag -a v3.1.0 -m "Release v3.1.0"
    pause
    exit /b 1
)

echo.
echo [2] Verifica stato repository...
git status --short
echo.

REM Chiedi conferma
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║  PRONTO PER RILASCIARE v3.1.0                                    ║
echo ║                                                                  ║
echo ║  Azioni:                                                         ║
echo ║  1. Push tag v3.1.0 su GitHub                                    ║
echo ║  2. Apri browser per creare release                              ║
echo ║                                                                  ║
echo ║  Vuoi continuare? (S/N)                                          ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

set /p conferma="Conferma (S/N): "

if /i "%conferma%" neq "S" (
    echo.
    echo [ANNULLATO] Rilascio annullato.
    pause
    exit /b 0
)

echo.
echo [3] Push tag su GitHub...
git push origin v3.1.0

if %errorlevel%==0 (
    echo     [OK] Tag pushato con successo!
) else (
    echo     [ERRORE] Push fallito!
    pause
    exit /b 1
)

echo.
echo [4] Apro browser per creare release...
timeout /t 2 /nobreak >nul
start https://github.com/ballales1984-wq/pythonita-ia/releases/new?tag=v3.1.0

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║  ✅ TAG PUSHATO SU GITHUB!                                        ║
echo ║                                                                  ║
echo ║  PROSSIMI PASSI:                                                 ║
echo ║  1. Browser aperto automaticamente                               ║
echo ║  2. Title: v3.1.0 - Oggetti 3D + Grafica Avanzata                ║
echo ║  3. Description: Copia da COME_RILASCIARE.md                     ║
echo ║  4. Click "Publish release"                                      ║
echo ║                                                                  ║
echo ║  FATTO! 🎉                                                       ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

pause

