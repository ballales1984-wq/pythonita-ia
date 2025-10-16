# 🤖 Guida Setup Arduino con Pythonita IA

## 📋 Indice

1. [Introduzione](#introduzione)
2. [Hardware Necessario](#hardware-necessario)
3. [Setup Arduino (Sketch)](#setup-arduino-sketch)
4. [Setup Python](#setup-python)
5. [Collegamento e Test](#collegamento-e-test)
6. [Comandi Disponibili](#comandi-disponibili)
7. [Esempi Pratici](#esempi-pratici)
8. [Simulatore Arduino](#simulatore-arduino)

---

## 🌟 Introduzione

Pythonita IA può **controllare Arduino** tramite porta seriale (USB).

**Cosa puoi fare:**
- 💡 Accendi/spegni LED
- 🔄 Lampeggia LED
- 🎚️ Controlla servomotori (0-180°)
- 📊 Leggi sensori analogici
- ⚡ PWM per motori

**Due modalità:**
1. **Arduino REALE** - Hardware fisico collegato via USB
2. **Arduino SIMULATO** - Test senza hardware

---

## 🔧 Hardware Necessario

### Opzione 1: Setup Minimo
```
✅ Arduino Uno/Nano (qualsiasi clone va bene)
✅ Cavo USB
```
**Costo:** ~10€

### Opzione 2: Setup Completo
```
✅ Arduino Uno
✅ LED + resistenze 220Ω
✅ Servomotore SG90
✅ Breadboard
✅ Cavetti jumper
✅ Sensore (temperatura, luce, distanza, ecc.)
```
**Costo:** ~25€

---

## 📝 Setup Arduino (Sketch)

### Passo 1: Apri Arduino IDE

Scarica da: https://www.arduino.cc/en/software

### Passo 2: Copia questo Sketch

```cpp
/*
  PYTHONITA IA - Arduino Controller
  Comandi via seriale: LED, Servo, Sensori, PWM
*/

#include <Servo.h>

Servo servo;
int servoPin = 9;

void setup() {
  Serial.begin(9600);
  
  // LED built-in su pin 13
  pinMode(13, OUTPUT);
  
  Serial.println("Arduino Ready!");
  Serial.println("Pythonita IA Controller v1.0");
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    // Formato comandi:
    // LED_ON,13      → Accendi LED pin 13
    // LED_OFF,13     → Spegni LED pin 13
    // SERVO,9,90     → Muovi servo pin 9 a 90°
    // READ,A0        → Leggi sensore pin A0
    // PWM,3,128      → PWM pin 3 a 128/255
    
    if (cmd.startsWith("LED_ON,")) {
      int pin = cmd.substring(7).toInt();
      pinMode(pin, OUTPUT);
      digitalWrite(pin, HIGH);
      Serial.println("OK:LED_ON");
    }
    else if (cmd.startsWith("LED_OFF,")) {
      int pin = cmd.substring(8).toInt();
      pinMode(pin, OUTPUT);
      digitalWrite(pin, LOW);
      Serial.println("OK:LED_OFF");
    }
    else if (cmd.startsWith("SERVO,")) {
      // Formato: SERVO,pin,angle
      int idx1 = cmd.indexOf(',');
      int idx2 = cmd.indexOf(',', idx1 + 1);
      int pin = cmd.substring(idx1 + 1, idx2).toInt();
      int angle = cmd.substring(idx2 + 1).toInt();
      
      servo.attach(pin);
      servo.write(angle);
      delay(15);
      Serial.println("OK:SERVO");
    }
    else if (cmd.startsWith("READ,")) {
      String pinStr = cmd.substring(5);
      int pin = pinStr.substring(1).toInt(); // A0 → 0
      int value = analogRead(pin);
      Serial.println("VALUE:" + String(value));
    }
    else if (cmd.startsWith("PWM,")) {
      // Formato: PWM,pin,value
      int idx1 = cmd.indexOf(',');
      int idx2 = cmd.indexOf(',', idx1 + 1);
      int pin = cmd.substring(idx1 + 1, idx2).toInt();
      int value = cmd.substring(idx2 + 1).toInt();
      
      pinMode(pin, OUTPUT);
      analogWrite(pin, value);
      Serial.println("OK:PWM");
    }
    else {
      Serial.println("ERROR:Unknown command");
    }
  }
}
```

### Passo 3: Carica sull'Arduino

1. Collega Arduino via USB
2. Seleziona **Strumenti → Scheda → Arduino Uno**
3. Seleziona **Strumenti → Porta → COM3** (o la tua porta)
4. Clicca **Carica** ↑

---

## 🐍 Setup Python

### Passo 1: Installa Libreria

```bash
pip install pyserial
```

### Passo 2: Verifica Porta COM

```bash
python -c "import serial.tools.list_ports; [print(f'{p.device}: {p.description}') for p in serial.tools.list_ports.comports()]"
```

Output esempio:
```
COM3: USB Serial Port (Arduino Uno)
COM4: Bluetooth Device
```

### Passo 3: Test Connessione

```python
from pythonita.hardware.arduino_controller import get_arduino_controller

# Connetti
arduino = get_arduino_controller()
success, msg = arduino.connect(port='COM3', baudrate=9600)

if success:
    print("✅ Arduino connesso!")
    
    # Test LED
    arduino.led_on(13)
    print("LED acceso!")
    
    arduino.disconnect()
else:
    print(f"❌ Errore: {msg}")
```

---

## 🔌 Collegamento e Test

### Test 1: LED Built-in

Arduino Uno ha un LED già collegato al **pin 13**!

```python
from pythonita.hardware.arduino_controller import get_arduino_controller
import time

arduino = get_arduino_controller()
arduino.connect(port='COM3')

# Lampeggia 5 volte
for i in range(5):
    arduino.led_on(13)
    time.sleep(0.5)
    arduino.led_off(13)
    time.sleep(0.5)
    print(f"Lampeggio {i+1}/5")

arduino.disconnect()
print("Test completato!")
```

### Test 2: Servomotore

**Collegamento servo:**
```
Servo SG90:
  Rosso    → 5V Arduino
  Marrone  → GND Arduino
  Arancione → Pin 9 Arduino
```

**Codice Python:**
```python
arduino.connect(port='COM3')

# Muovi servo
for angolo in [0, 45, 90, 135, 180]:
    arduino.servo_write(9, angolo)
    print(f"Servo a {angolo}°")
    time.sleep(1)

arduino.disconnect()
```

### Test 3: Sensore Analogico

**Collegamento sensore (es: potenziometro):**
```
Pin centrale → A0
Pin laterali → 5V e GND
```

**Codice Python:**
```python
arduino.connect(port='COM3')

# Leggi sensore
for _ in range(10):
    success, value = arduino.analog_read(0)
    if success:
        percentuale = (value / 1023) * 100
        print(f"Sensore A0: {value} ({percentuale:.1f}%)")
    time.sleep(0.5)

arduino.disconnect()
```

---

## 🎮 Comandi Disponibili nella GUI

### Nella GUI Robot 3D:

1. **Clicca bottone 🤖 Arduino**
2. **Seleziona porta:** COM3 (la tua)
3. **Clicca Connetti**
4. **Usa i controlli:**
   - 💡 LED: Accendi/Spegni/Lampeggia
   - 🎚️ Servo: Slider 0-180°
   - 📊 Sensore: Leggi valore A0

---

## 🖥️ Simulatore Arduino (SENZA HARDWARE)

Se **NON hai Arduino fisico**, puoi testare con il **simulatore**:

### Passo 1: Crea file `arduino_simulator.py`

```python
"""Simulatore Arduino - risponde come Arduino vero"""
import threading
import time

class ArduinoSimulator:
    def __init__(self):
        self.led_states = {}
        self.servo_angles = {}
        self.running = True
        
    def connect(self):
        print("🤖 [SIMULATORE] Arduino connesso (simulato)")
        return True, "Simulatore connesso"
    
    def send_command(self, cmd):
        print(f"📤 [SIM] Ricevuto: {cmd}")
        
        if "LED_ON" in cmd:
            pin = int(cmd.split(',')[1])
            self.led_states[pin] = True
            print(f"💡 [SIM] LED pin {pin} ACCESO")
            return True, "OK:LED_ON"
            
        elif "LED_OFF" in cmd:
            pin = int(cmd.split(',')[1])
            self.led_states[pin] = False
            print(f"⚫ [SIM] LED pin {pin} SPENTO")
            return True, "OK:LED_OFF"
            
        elif "SERVO" in cmd:
            parts = cmd.split(',')
            pin, angle = int(parts[1]), int(parts[2])
            self.servo_angles[pin] = angle
            print(f"🎚️  [SIM] Servo pin {pin} → {angle}°")
            return True, "OK:SERVO"
            
        elif "READ" in cmd:
            # Simula valore sensore random
            import random
            value = random.randint(0, 1023)
            print(f"📊 [SIM] Sensore A0 → {value}")
            return True, f"VALUE:{value}"
        
        return True, "OK"
    
    def disconnect(self):
        print("👋 [SIM] Arduino disconnesso")
```

### Passo 2: Usa il simulatore

```python
from arduino_simulator import ArduinoSimulator

# Usa simulatore invece di Arduino reale
arduino = ArduinoSimulator()
arduino.connect()

# Test comandi
arduino.send_command("LED_ON,13")
time.sleep(1)
arduino.send_command("LED_OFF,13")
arduino.send_command("SERVO,9,90")

arduino.disconnect()
```

---

## 📚 Esempi Pratici

### Esempio 1: Semaforo

```python
from pythonita.hardware.arduino_controller import get_arduino_controller
import time

arduino = get_arduino_controller()
arduino.connect(port='COM3')

# Pin LED
LED_ROSSO = 11
LED_GIALLO = 12
LED_VERDE = 13

while True:
    # Rosso
    arduino.led_on(LED_ROSSO)
    print("🔴 STOP")
    time.sleep(3)
    arduino.led_off(LED_ROSSO)
    
    # Giallo
    arduino.led_on(LED_GIALLO)
    print("🟡 ATTENZIONE")
    time.sleep(1)
    arduino.led_off(LED_GIALLO)
    
    # Verde
    arduino.led_on(LED_VERDE)
    print("🟢 VAI")
    time.sleep(3)
    arduino.led_off(LED_VERDE)
```

### Esempio 2: Servo Sweep

```python
arduino.connect(port='COM3')

# Sweep servo da 0 a 180°
for angolo in range(0, 181, 5):
    arduino.servo_write(9, angolo)
    print(f"Angolo: {angolo}°")
    time.sleep(0.05)

# Torna a 90°
arduino.servo_write(9, 90)
arduino.disconnect()
```

### Esempio 3: Monitor Sensore

```python
arduino.connect(port='COM3')

print("Monitor sensore temperatura (Ctrl+C per uscire)")

try:
    while True:
        success, value = arduino.analog_read(0)
        if success:
            # Converti in temperatura (esempio TMP36)
            voltage = value * (5.0 / 1023.0)
            temp_c = (voltage - 0.5) * 100
            print(f"🌡️  Temperatura: {temp_c:.1f}°C (raw: {value})")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nMonitor fermato")
    
arduino.disconnect()
```

---

## 🎯 Comandi da Pythonita GUI

Nella GUI puoi scrivere comandi in italiano:

```
"accendi led pin 13"     → arduino.led_on(13)
"spegni led pin 13"      → arduino.led_off(13)
"lampeggia led 5 volte"  → loop con led_on/off
"muovi servo a 90 gradi" → arduino.servo_write(9, 90)
"leggi sensore pin A0"   → arduino.analog_read(0)
```

---

## 🔍 Troubleshooting

### ❌ "Porta COM non trovata"
```bash
# Lista porte disponibili
python -c "import serial.tools.list_ports; [print(p.device) for p in serial.tools.list_ports.comports()]"
```

### ❌ "Porta occupata"
- Chiudi Arduino IDE Serial Monitor
- Scollega e ricollega Arduino
- Riavvia il PC

### ❌ Arduino non risponde
- Verifica sketch caricato
- Controlla baud rate (deve essere 9600)
- Premi reset su Arduino

---

## 💻 Test Rapido Setup

Salva questo come `test_arduino_setup.py`:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test setup Arduino completo"""

import serial.tools.list_ports
from pythonita.hardware.arduino_controller import get_arduino_controller

print("=" * 70)
print("TEST SETUP ARDUINO")
print("=" * 70)

# 1. Trova porte COM
print("\n1. PORTE COM DISPONIBILI:")
ports = list(serial.tools.list_ports.comports())
if not ports:
    print("   ❌ Nessuna porta COM trovata!")
    print("   Collega Arduino via USB")
    exit(1)

for p in ports:
    print(f"   ✅ {p.device}: {p.description}")

# 2. Chiedi quale porta
porta = input(f"\nQuale porta usare? (default: {ports[0].device}): ").strip()
if not porta:
    porta = ports[0].device

# 3. Connetti
print(f"\n2. CONNESSIONE a {porta}...")
arduino = get_arduino_controller()
success, msg = arduino.connect(port=porta, baudrate=9600)

if not success:
    print(f"   ❌ Errore: {msg}")
    exit(1)

print(f"   ✅ Connesso!")

# 4. Test LED
print(f"\n3. TEST LED pin 13...")
print("   Accendo LED...")
arduino.led_on(13)
input("   Premi INVIO (dovresti vedere il LED acceso)")

print("   Spengo LED...")
arduino.led_off(13)
input("   Premi INVIO (LED dovrebbe essere spento)")

# 5. Test lampeggio
print(f"\n4. TEST LAMPEGGIO...")
arduino.led_blink(13, times=3, delay=0.5)
print("   ✅ LED lampeggiato 3 volte!")

# 6. Disconnetti
arduino.disconnect()

print("\n" + "=" * 70)
print("✅ SETUP COMPLETATO CON SUCCESSO!")
print("=" * 70)
print("\nOra puoi usare Arduino dalla GUI Pythonita!")
print("Clicca il bottone 🤖 Arduino nella GUI")
```

---

## 🎨 Usa nella GUI

1. **Avvia GUI:**
   ```bash
   python gui_robot_3d.py
   ```

2. **Clicca bottone 🤖 Arduino** (se disponibile)

3. **Seleziona porta COM** (es: COM3)

4. **Clicca Connetti**

5. **Prova i controlli:**
   - LED ON/OFF
   - Servo slider
   - Read sensor

---

## 🔄 Modalità Simulata (SENZA Arduino)

Se NON hai Arduino, modifica `gui_robot_3d.py`:

```python
# Riga ~104 circa
if ARDUINO_AVAILABLE:
    # self.arduino = get_arduino_controller()  # Hardware reale
    from arduino_simulator import ArduinoSimulator
    self.arduino = ArduinoSimulator()  # Simulatore
```

---

**Pronto per configurare Arduino?** 🤖

Hai già Arduino fisico o vuoi iniziare con il simulatore? 🔌

