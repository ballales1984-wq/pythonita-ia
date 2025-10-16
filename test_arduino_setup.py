#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test setup Arduino completo - Guida interattiva"""

import serial.tools.list_ports
import time
import sys

print("=" * 70)
print("🤖 SETUP ARDUINO - GUIDA INTERATTIVA")
print("=" * 70)

# Passo 1: Verifica pyserial
print("\n📦 Passo 1: Verifica libreria pyserial...")
try:
    import serial
    print(f"   ✅ pyserial installato (versione {serial.__version__})")
except ImportError:
    print("   ❌ pyserial NON installato!")
    print("\n   Installa con:")
    print("   pip install pyserial")
    sys.exit(1)

# Passo 2: Trova porte COM
print("\n🔌 Passo 2: Ricerca porte COM...")
ports = list(serial.tools.list_ports.comports())

if not ports:
    print("   ❌ Nessuna porta COM trovata!")
    print("\n   Possibili cause:")
    print("   - Arduino non collegato via USB")
    print("   - Driver USB non installati")
    print("   - Porta USB difettosa")
    print("\n   💡 SOLUZIONE:")
    print("   1. Collega Arduino via USB")
    print("   2. Installa driver CH340 (per cloni): https://sparks.gogo.co.nz/ch340.html")
    print("   3. Riavvia il computer")
    print("\n   OPPURE usa il SIMULATORE (senza hardware):")
    print("   - Modifica gui_robot_3d.py per usare ArduinoSimulator")
    sys.exit(1)

print(f"   ✅ Trovate {len(ports)} porte:")
for p in ports:
    print(f"      {p.device}: {p.description}")

# Passo 3: Scegli porta
print("\n📍 Passo 3: Seleziona porta Arduino...")
porta_default = ports[0].device
porta = input(f"   Quale porta? (default {porta_default}): ").strip()
if not porta:
    porta = porta_default

print(f"   ✅ Porta selezionata: {porta}")

# Passo 4: Test connessione
print(f"\n🔗 Passo 4: Test connessione...")
print(f"   Tentativo connessione a {porta}...")

try:
    from pythonita.hardware.arduino_controller import get_arduino_controller
    
    arduino = get_arduino_controller()
    success, msg = arduino.connect(port=porta, baudrate=9600)
    
    if not success:
        print(f"   ❌ Connessione fallita: {msg}")
        print("\n   💡 VERIFICA:")
        print("   1. Sketch Arduino caricato correttamente?")
        print("   2. Arduino acceso? (LED power acceso?)")
        print("   3. Porta corretta?")
        print("   4. Chiuso Arduino IDE Serial Monitor?")
        sys.exit(1)
    
    print(f"   ✅ Connesso!")
    
except Exception as e:
    print(f"   ❌ Errore: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Passo 5: Test LED built-in (pin 13)
print(f"\n💡 Passo 5: Test LED built-in (pin 13)...")
print("   Questo LED è già sulla board Arduino!")

print("   Accendo LED...")
arduino.led_on(13)
input("   👀 Vedi il LED acceso? Premi INVIO...")

print("   Spengo LED...")
arduino.led_off(13)
input("   👀 LED spento? Premi INVIO...")

# Passo 6: Test lampeggio
print(f"\n✨ Passo 6: Test lampeggio...")
print("   Lampeggio 3 volte...")
for i in range(3):
    arduino.led_on(13)
    time.sleep(0.3)
    arduino.led_off(13)
    time.sleep(0.3)
    print(f"   Lampeggio {i+1}/3")

print("   ✅ Lampeggio completato!")

# Passo 7: Disconnetti
arduino.disconnect()

# Risultato finale
print("\n" + "=" * 70)
print("✅✅✅ SETUP ARDUINO COMPLETATO CON SUCCESSO! ✅✅✅")
print("=" * 70)

print("\n🎉 IL TUO ARDUINO È PRONTO!")
print(f"   Porta: {porta}")
print(f"   Baudrate: 9600")
print(f"   Status: Funzionante")

print("\n📝 PROSSIMI PASSI:")
print(f"   1. Nella GUI clicca bottone 🤖 Arduino")
print(f"   2. Seleziona porta: {porta}")
print(f"   3. Clicca Connetti")
print(f"   4. Usa i controlli LED, Servo, Sensori!")

print("\n📚 DOCUMENTAZIONE:")
print("   - GUIDA_SETUP_ARDUINO.md")
print("   - VOICE_AND_ARDUINO_GUIDE.md")
print("   - examples/arduino_sketch.ino")

print("\n" + "=" * 70)

