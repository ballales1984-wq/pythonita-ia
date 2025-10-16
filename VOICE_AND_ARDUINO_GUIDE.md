# 🎤 Comandi Vocali + 🤖 Arduino - Guida Completa

## 📋 Indice

1. [Introduzione](#introduzione)
2. [Installazione](#installazione)
3. [Comandi Vocali](#comandi-vocali)
4. [Controllo Arduino](#controllo-arduino)
5. [Template Arduino](#template-arduino)
6. [Esempi Pratici](#esempi-pratici)
7. [Troubleshooting](#troubleshooting)

---

## 🌟 Introduzione

Pythonita IA v3.4 include due nuove potenti funzionalità:

- **🎤 Speech-to-Text**: Converti comandi vocali in testo
- **🤖 Arduino Controller**: Controlla Arduino tramite porta seriale

Ora puoi dire "accendi led pin 13" e il programma:
1. Riconosce la tua voce
2. Genera il codice Python per Arduino
3. Invia il comando direttamente all'Arduino

---

## 📦 Installazione

### 1. Dipendenze Python

```bash
pip install SpeechRecognition pyaudio pyserial
```

### 2. Installazione PyAudio (Windows)

Se hai errori con `pyaudio`, scaricalo pre-compilato:

```bash
# Scarica il file .whl corrispondente al tuo Python:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

# Installa il file .whl scaricato:
pip install PyAudio‑0.2.13‑cp310‑cp310‑win_amd64.whl
```

### 3. Test Microfono

Verifica che il microfono funzioni:

```bash
python pythonita/utils/speech_recognition_module.py
```

### 4. Test Arduino

Collega Arduino via USB e testa:

```bash
python pythonita/hardware/arduino_controller.py
```

---

## 🎤 Comandi Vocali

### Come Usare

1. **Apri Pythonita IA GUI**
   ```bash
   python gui_robot_3d.py
   ```

2. **Premi il pulsante 🎤 Registra**
   - Il pulsante diventerà rosso: **🔴 Registrando...**

3. **Parla chiaramente** (hai 5-10 secondi)
   - Esempio: *"apri mano"*
   - Esempio: *"accendi led pin tredici"*

4. **Il testo riconosciuto apparirà** nel campo input
   - Il codice Python verrà generato automaticamente

### Lingue Supportate

- **Italiano** (default): `it-IT`
- **Inglese**: `en-US`
- **Spagnolo**: `es-ES`
- **Francese**: `fr-FR`

### Esempi Comandi Vocali

#### Robot/Mano
- *"apri mano"*
- *"chiudi pugno"*
- *"fai pinza"*
- *"afferra mela"*
- *"alza braccio"*

#### Arduino
- *"accendi led pin tredici"*
- *"spegni led pin cinque"*
- *"lampeggia led tre volte"*
- *"leggi sensore su pin zero"*
- *"muovi servo a novanta gradi"*

### Configurazione Avanzata

Modifica i parametri del riconoscimento vocale in `gui_robot_3d.py`:

```python
self.speech_recognizer = get_speech_recognizer(
    language='it-IT',    # Cambia lingua
    engine='google'      # Usa 'sphinx' per offline
)
```

---

## 🤖 Controllo Arduino

### Hardware Necessario

- **Arduino Uno/Nano/Mega** (o compatibile)
- **Cavo USB** per connessione al PC
- **LED** (opzionale, già presente su pin 13)
- **Servomotore** (opzionale)
- **Sensori analogici** (opzionale)

### Schema Arduino Base

```
Arduino Uno
├─ Pin 13: LED built-in (già presente sulla board)
├─ Pin 9:  Servomotore (segnale)
├─ Pin A0: Sensore analogico (temperatura, luce, etc.)
└─ GND:    Ground comune
```

### Sketch Arduino

Carica questo sketch sull'Arduino:

```cpp
/*
  Pythonita IA - Arduino Controller
  Supporta: LED, Servo, Sensori, PWM
*/

#include <Servo.h>

Servo servo;

void setup() {
  Serial.begin(9600);
  
  // Inizializza pin LED
  pinMode(13, OUTPUT);
  
  Serial.println("Arduino Ready!");
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    // Formato comando:
    // D<pin>,<value>  - Digital Write (es: D13,1)
    // A<pin>,<value>  - Analog Write / PWM (es: A3,128)
    // R<pin>          - Read Analog (es: R0)
    // S<pin>,<angle>  - Servo (es: S9,90)
    
    char type = cmd.charAt(0);
    
    if (type == 'D') {
      // Digital Write
      int pin = cmd.substring(1, cmd.indexOf(',')).toInt();
      int value = cmd.substring(cmd.indexOf(',') + 1).toInt();
      pinMode(pin, OUTPUT);
      digitalWrite(pin, value);
      Serial.println("OK");
    }
    else if (type == 'A') {
      // Analog Write (PWM)
      int pin = cmd.substring(1, cmd.indexOf(',')).toInt();
      int value = cmd.substring(cmd.indexOf(',') + 1).toInt();
      pinMode(pin, OUTPUT);
      analogWrite(pin, value);
      Serial.println("OK");
    }
    else if (type == 'R') {
      // Read Analog
      int pin = cmd.substring(1).toInt();
      int value = analogRead(pin);
      Serial.println(value);
    }
    else if (type == 'S') {
      // Servo
      int pin = cmd.substring(1, cmd.indexOf(',')).toInt();
      int angle = cmd.substring(cmd.indexOf(',') + 1).toInt();
      servo.attach(pin);
      servo.write(angle);
      delay(15);
      Serial.println("OK");
    }
  }
}
```

### Come Usare il Pannello Arduino

1. **Apri il pannello Arduino**
   - Clicca sul bottone **🤖 Arduino** nella GUI

2. **Seleziona porta COM**
   - Scegli la porta (es: COM3, COM4)
   - Se non appare, clicca **🔄 Aggiorna Porte**

3. **Connetti**
   - Premi **Connetti**
   - Lo status diventerà verde: **✓ Connesso**

4. **Controlla Arduino**
   - **LED**: Accendi/Spegni/Lampeggia LED su un pin
   - **Servo**: Muovi servomotore da 0° a 180°
   - **Sensore**: Leggi valore analogico (0-1023)

5. **Console**
   - Vedi tutti i comandi inviati nella console verde

### Comandi API Arduino

Usa questi metodi in Python:

```python
from pythonita.hardware.arduino_controller import get_arduino_controller

# Inizializza
arduino = get_arduino_controller()

# Connetti
success, msg = arduino.connect(port='COM3', baudrate=9600)

# LED
arduino.led_on(13)       # Accendi LED pin 13
arduino.led_off(13)      # Spegni LED pin 13
arduino.led_blink(13, times=3, delay=0.5)  # Lampeggia 3 volte

# Servo
arduino.servo_write(9, 90)  # Muovi servo pin 9 a 90 gradi

# Sensore
success, value = arduino.analog_read(0)  # Leggi pin A0
print(f"Valore sensore: {value} / 1023")

# PWM Motore
arduino.analog_write(3, 128)  # Velocità media (128/255)

# Disconnetti
arduino.disconnect()
```

---

## 📝 Template Arduino

Pythonita IA genera automaticamente codice Python per Arduino!

### Esempi Template

#### 1. Accendi LED

**Comando**: *"accendi led pin 13"*

**Codice Generato**:
```python
# Accendi LED su pin 13
import serial
import time

arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Attendi reset Arduino

# Accendi LED
arduino.write(b'D13,1\n')
print("LED pin 13 acceso")

arduino.close()
```

#### 2. Lampeggia LED

**Comando**: *"lampeggia led 5 volte"*

**Codice Generato**:
```python
# Lampeggia LED su pin 13
import serial
import time

arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# Lampeggia 5 volte
for i in range(5):
    arduino.write(b'D13,1\n')  # Accendi
    time.sleep(0.5)
    arduino.write(b'D13,0\n')  # Spegni
    time.sleep(0.5)
    print(f"Lampeggio {i+1}/5")

arduino.close()
print("Lampeggio completato")
```

#### 3. Leggi Sensore

**Comando**: *"leggi sensore su pin zero"*

**Codice Generato**:
```python
# Leggi sensore analogico su pin A0
import serial
import time

arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# Richiedi lettura sensore
arduino.write(b'R0\n')
time.sleep(0.1)

# Leggi risposta
if arduino.in_waiting > 0:
    valore = arduino.readline().decode('utf-8').strip()
    print(f"Valore sensore pin A0: {valore}")
else:
    print("Nessuna risposta dall'Arduino")

arduino.close()
```

#### 4. Muovi Servo

**Comando**: *"muovi servo a 90 gradi"*

**Codice Generato**:
```python
# Muovi servomotore su pin 9
import serial
import time

arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# Muovi servo a 90 gradi
arduino.write(b'S9,90\n')
print(f"Servo pin 9 mosso a 90 gradi")

arduino.close()
```

---

## 🚀 Esempi Pratici

### Esempio 1: Controllo Vocale LED

```python
from pythonita.utils.speech_recognition_module import get_speech_recognizer
from pythonita.hardware.arduino_controller import get_arduino_controller

# Inizializza
recognizer = get_speech_recognizer(language='it-IT')
arduino = get_arduino_controller()

# Connetti Arduino
success, msg = arduino.connect()
if not success:
    print(f"Errore: {msg}")
    exit(1)

print("Parla per controllare l'Arduino (es: 'accendi led')...")

# Loop comandi vocali
while True:
    success, text = recognizer.listen_from_microphone(timeout=10)
    
    if success:
        print(f"Riconosciuto: {text}")
        
        # Interpreta comando
        if "accendi" in text.lower():
            arduino.led_on(13)
            print("✓ LED acceso")
        elif "spegni" in text.lower():
            arduino.led_off(13)
            print("✓ LED spento")
        elif "esci" in text.lower():
            break
    else:
        print(f"Errore: {text}")

arduino.disconnect()
```

### Esempio 2: Monitor Sensore Vocale

```python
# Monitora sensore e leggi valore con comando vocale

import time

# ... (inizializza recognizer e arduino come sopra) ...

print("Dì 'leggi' per leggere il sensore, 'esci' per uscire")

while True:
    success, text = recognizer.listen_from_microphone(timeout=10)
    
    if success and "leggi" in text.lower():
        success, value = arduino.analog_read(0)
        if success:
            print(f"📊 Sensore A0: {value} / 1023 ({value/1023*100:.1f}%)")
        else:
            print("❌ Errore lettura sensore")
    elif success and "esci" in text.lower():
        break

arduino.disconnect()
```

### Esempio 3: Servo Vocale

```python
# Controlla servomotore con comandi vocali

sinonimi_angoli = {
    'zero': 0,
    'quarantacinque': 45,
    'novanta': 90,
    'centotrentacinque': 135,
    'centottanta': 180
}

print("Dì l'angolo (es: 'novanta', 'zero', 'centottanta')...")

while True:
    success, text = recognizer.listen_from_microphone(timeout=10)
    
    if success:
        text_lower = text.lower()
        
        # Cerca angolo
        angle = None
        for parola, ang in sinonimi_angoli.items():
            if parola in text_lower:
                angle = ang
                break
        
        if angle is not None:
            arduino.servo_write(9, angle)
            print(f"✓ Servo mosso a {angle}°")
        elif "esci" in text_lower:
            break
        else:
            print("Angolo non riconosciuto. Prova: zero, novanta, centottanta")

arduino.disconnect()
```

---

## 🔧 Troubleshooting

### Problemi Speech Recognition

#### ❌ "Nessun microfono trovato"
**Soluzione**:
- Collega microfono USB o cuffie con microfono
- In Windows: Impostazioni > Privacy > Microfono > Consenti app
- Testa con `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`

#### ❌ "Timeout: nessun audio rilevato"
**Soluzione**:
- Parla più forte e vicino al microfono
- Aumenta timeout: `listen_from_microphone(timeout=10)`
- Disabilita AGC (Automatic Gain Control) in Windows

#### ❌ "Audio non comprensibile"
**Soluzione**:
- Parla più lentamente e chiaramente
- Riduci rumore ambiente
- Calibra: `recognizer.adjust_for_ambient_noise(source, duration=2)`

#### ❌ Errore PyAudio su Windows
**Soluzione**:
```bash
# Scarica PyAudio pre-compilato:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

# Installa:
pip install PyAudio‑0.2.13‑cp310‑cp310‑win_amd64.whl
```

### Problemi Arduino

#### ❌ "Nessuna porta seriale trovata"
**Soluzione**:
- Collega Arduino via USB
- Installa driver CH340 (per Arduino clone): https://sparks.gogo.co.nz/ch340.html
- Riavvia computer

#### ❌ "Porta COM occupata"
**Soluzione**:
- Chiudi Arduino IDE (Serial Monitor)
- Chiudi altre app che usano la porta COM
- Riavvia Arduino (scollega/ricollega USB)

#### ❌ Arduino non risponde
**Soluzione**:
- Verifica che lo sketch sia caricato correttamente
- Controlla baud rate (deve essere 9600)
- Prova reset manuale Arduino

#### ❌ LED non si accende
**Soluzione**:
- Verifica pin (LED built-in è su pin 13)
- Se usi LED esterno: LED → Resistenza 220Ω → GND
- Controlla che lo sketch Arduino sia in esecuzione

#### ❌ Servo non si muove
**Soluzione**:
- Collega servo:
  - Rosso → 5V
  - Marrone → GND
  - Arancione → Pin 9
- Verifica alimentazione (servo richiede corrente)
- Usa alimentazione esterna se hai più servo

---

## 📚 Risorse Aggiuntive

### Documentazione Moduli

- `pythonita/utils/speech_recognition_module.py` - Speech-to-text
- `pythonita/hardware/arduino_controller.py` - Arduino controller
- `core/arduino_commands.py` - Template comandi Arduino

### Test Scripts

```bash
# Test speech recognition
python pythonita/utils/speech_recognition_module.py

# Test Arduino
python pythonita/hardware/arduino_controller.py

# Test template Arduino
python core/arduino_commands.py
```

### Video Tutorial

*(TODO: Creare video tutorial e aggiungere link)*

---

## 🎉 Conclusione

Ora puoi controllare Arduino con la voce usando Pythonita IA!

**Workflow completo**:
1. 🎤 Parla: *"lampeggia led 5 volte"*
2. 📝 Pythonita riconosce e genera codice Python
3. 🤖 Arduino esegue il comando
4. ✅ Vedi risultato (LED lampeggia)

**Prossimi passi**:
- Aggiungi più sensori (ultrasuoni, temperatura, umidità)
- Crea robot con motori DC
- Integra con progetti IoT
- Crea skill vocali personalizzate

Buon coding! 🚀

---

**Pythonita IA v3.4** - *Genera Python parlando!*

