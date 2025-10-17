#!/usr/bin/env python3
"""
Test sistema logging Pythonita IA.
"""

from pythonita.utils.error_logger import get_error_logger
import time

print("═══════════════════════════════════════════")
print("TEST SISTEMA LOGGING")
print("═══════════════════════════════════════════\n")

# Inizializza logger
logger = get_error_logger()

print(f"📁 Cartella log: {logger.log_dir}")
print(f"📄 File log: {logger.log_file}\n")

# Test 1: Log info
print("1️⃣  Test log info...")
logger.log_info("Applicazione avviata")
logger.log_info("AI inizializzata correttamente")
print("   ✅ Info logged\n")

# Test 2: Log comando
print("2️⃣  Test log comando...")
logger.log_comando("somma 3 piu 5", successo=True)
logger.log_comando("comando invalido", successo=False)
print("   ✅ Comandi logged\n")

# Test 3: Log generazione
print("3️⃣  Test log generazione...")
logger.log_generazione("calcola area cerchio", "import math...", 2500)
print("   ✅ Generazione logged\n")

# Test 4: Log esecuzione
print("4️⃣  Test log esecuzione...")
logger.log_esecuzione(successo=True, output="Area: 78.54")
logger.log_esecuzione(successo=False, errore="NameError: 'x' is not defined")
print("   ✅ Esecuzioni logged\n")

# Test 5: Log errore
print("5️⃣  Test log errore...")
try:
    raise ValueError("Errore di test per logging")
except Exception as e:
    logger.log_error("Test errore catturato", e)
print("   ✅ Errore logged\n")

# Test 6: Report sessione
print("6️⃣  Report sessione...")
report = logger.genera_report_sessione()
print(report)

# Test 7: Apri cartella log
print("7️⃣  Test apertura cartella...")
print(f"   Apro: {logger.log_dir}")
logger.apri_cartella_log()
print("   ✅ Cartella aperta!\n")

print("═══════════════════════════════════════════")
print("✅ TUTTI I TEST LOGGING PASSANO!")
print("═══════════════════════════════════════════")

