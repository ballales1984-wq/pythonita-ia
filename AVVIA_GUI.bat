@echo off
REM ========================================
REM PYTHONITA IA - GUI Robot 3D
REM Con Speech Recognition OFFLINE (Sphinx)
REM ========================================

echo.
echo ================================================
echo    PYTHONITA IA - Avvio GUI Robot 3D
echo ================================================
echo.

cd /d "C:\Users\user\pythonita-ia"

echo [1/3] Verifico Python...
python --version
if errorlevel 1 (
    echo.
    echo ERRORE: Python non trovato!
    echo Installa Python da: https://www.python.org/
    pause
    exit /b 1
)

echo.
echo [2/3] Verifico Ollama...
ollama --version
if errorlevel 1 (
    echo.
    echo ATTENZIONE: Ollama non trovato
    echo L'AI locale non sara' disponibile
    echo.
)

echo.
echo [3/3] Avvio GUI...
echo.
echo ================================================
echo  Funzioni disponibili:
echo  - Riconoscimento vocale OFFLINE (Sphinx)
echo  - Generazione codice con AI (Ollama)
echo  - Visualizzatore 3D Robot
echo  - 22 Oggetti 3D interattivi
echo ================================================
echo.
echo Per usare il microfono:
echo  1. Clicca sul pulsante: [Microfono Registra]
echo  2. Parla chiaramente: "apri mano", "stampa ciao"
echo  3. Il testo verra' riconosciuto automaticamente
echo.
echo Avvio in corso...
echo.

python gui_robot_3d.py

if errorlevel 1 (
    echo.
    echo ERRORE durante l'avvio!
    echo Controlla i log sopra per dettagli.
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo  GUI chiusa correttamente
echo ================================================
pause

