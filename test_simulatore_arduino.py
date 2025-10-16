#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test completo simulatore Arduino 3D"""

from pythonita.hardware.arduino_simulator_3d import get_arduino_simulator
import time

print("=" * 70)
print("🤖 TEST SIMULATORE ARDUINO 3D VIRTUALE")
print("=" * 70)
print("\nNON serve hardware fisico!")
print("Tutto simulato virtualmente.\n")

# Inizializza simulatore
sim = get_arduino_simulator()

# Connetti
success, msg = sim.connect(port='VIRTUAL', baudrate=9600)
print(f"\n✅ {msg}")

# Test 1: LED Built-in
print("\n" + "=" * 70)
print("TEST 1: LED BUILT-IN (Pin 13)")
print("=" * 70)

print("Accendo LED...")
sim.led_on(13)
time.sleep(1)

print("Spengo LED...")
sim.led_off(13)
time.sleep(1)

print("Lampeggio 5 volte...")
sim.led_blink(13, times=5, delay=0.3)

# Test 2: LED multipli
print("\n" + "=" * 70)
print("TEST 2: LED MULTIPLI (Semaforo virtuale)")
print("=" * 70)

LED_ROSSO = 11
LED_GIALLO = 12
LED_VERDE = 13

for ciclo in range(2):
    print(f"\nCiclo {ciclo+1}/2:")
    
    # Rosso
    sim.led_on(LED_ROSSO)
    print("  🔴 ROSSO ON")
    time.sleep(1)
    sim.led_off(LED_ROSSO)
    
    # Giallo
    sim.led_on(LED_GIALLO)
    print("  🟡 GIALLO ON")
    time.sleep(0.5)
    sim.led_off(LED_GIALLO)
    
    # Verde
    sim.led_on(LED_VERDE)
    print("  🟢 VERDE ON")
    time.sleep(1)
    sim.led_off(LED_VERDE)

# Test 3: Servomotore
print("\n" + "=" * 70)
print("TEST 3: SERVOMOTORE (Pin 9)")
print("=" * 70)

print("Sweep 0° → 180°...")
for angle in range(0, 181, 30):
    sim.servo_write(9, angle)
    print(f"  Angolo: {angle}°")
    time.sleep(0.3)

print("Torno a 90°...")
sim.servo_write(9, 90)

# Test 4: Sensore analogico
print("\n" + "=" * 70)
print("TEST 4: SENSORE ANALOGICO (Pin A0)")
print("=" * 70)

print("Letture sensore (simulato con rumore):")
for i in range(10):
    success, value = sim.analog_read(0)
    percentuale = (value / 1023) * 100
    barra = '█' * int(percentuale / 10)
    print(f"  [{i+1:2d}] {value:4d}/1023 ({percentuale:5.1f}%) {barra}")
    time.sleep(0.2)

# Test 5: PWM (LED fade)
print("\n" + "=" * 70)
print("TEST 5: PWM - LED FADE (Pin 11)")
print("=" * 70)

print("Fade IN (0 → 255)...")
for pwm in range(0, 256, 16):
    sim.analog_write(11, pwm)
    time.sleep(0.05)

print("Fade OUT (255 → 0)...")
for pwm in range(255, -1, -16):
    sim.analog_write(11, pwm)
    time.sleep(0.05)

# Test 6: Stato board
print("\n" + "=" * 70)
print("TEST 6: STATO BOARD")
print("=" * 70)

stati = sim.get_all_states()
print(f"Totale pin: {len(stati)}")

print("\nPin con componenti attivi:")
for pin_num, componente in sim.componenti.items():
    print(f"  Pin {pin_num}: {componente.nome} → {componente.stato}")

# Disconnetti
sim.disconnect()

# Riepilogo
print("\n" + "=" * 70)
print("✅ TUTTI I TEST COMPLETATI!")
print("=" * 70)

print("\n📊 COMANDI ESEGUITI:")
for cmd in sim.command_log[-10:]:  # Ultimi 10
    print(f"  - {cmd}")

print("\n🎯 SIMULATORE PRONTO PER LA GUI!")
print("   Usa il simulatore invece di Arduino reale")
print("   per testare senza hardware fisico.")

print("\n" + "=" * 70)

