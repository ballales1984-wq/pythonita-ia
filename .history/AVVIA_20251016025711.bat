@echo off
REM ============================================
REM Avvio Rapido Pythonita IA v3.1
REM ============================================

title Pythonita IA v3.1

REM Vai alla cartella del programma
cd /d "%~dp0"

REM Avvia launcher unificato
python avvia_pythonita.py

REM Se python non funziona, prova py
if %errorlevel% neq 0 (
    py avvia_pythonita.py
)

REM Pausa finale
pause

