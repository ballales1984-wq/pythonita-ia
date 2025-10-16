@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║         PUBBLICA RELEASE v3.1.0 SU GITHUB - AUTOMATICO           ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

echo [1] Apro browser su GitHub Release...
start https://github.com/ballales1984-wq/pythonita-ia/releases/new?tag=v3.1.0

timeout /t 3 /nobreak >nul

echo.
echo [2] Apro file con descrizione da copiare...
notepad RELEASE_DESCRIPTION.md

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║  ISTRUZIONI FINALI:                                              ║
echo ║                                                                  ║
echo ║  1. Nel Notepad: Ctrl+A (seleziona tutto)                        ║
echo ║  2. Ctrl+C (copia)                                               ║
echo ║  3. Nel browser GitHub: Ctrl+V (incolla in Description)          ║
echo ║  4. Title: v3.1.0 - Oggetti 3D + Grafica + Commerciale           ║
echo ║  5. Spunta: [✓] Set as the latest release                        ║
echo ║  6. Click: [Publish release]                                     ║
echo ║                                                                  ║
echo ║  FATTO! Release pubblica! ✅                                      ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

pause

