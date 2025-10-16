# 📋 Changelog v3.4 - Speech & Arduino

## 🎤 Comandi Vocali (Speech-to-Text)

### Nuove Funzionalità
- ✅ **Modulo Speech Recognition** (`pythonita/utils/speech_recognition_module.py`)
  - Classe `SpeechRecognizer` per riconoscimento vocale
  - Supporto multi-lingua (Italiano, Inglese, Spagnolo, Francese)
  - Engine multipli: Google Speech Recognition (default), Sphinx (offline)
  - Calibrazione automatica rumore ambiente
  - Test microfono integrato

- ✅ **Integrazione GUI**
  - Pulsante 🎤 **Registra** nella colonna input
  - Feedback visivo durante registrazione (pulsante rosso)
  - Auto-generazione codice dopo riconoscimento vocale
  - Tooltip informativi
  - Gestione errori user-friendly

### API Speech Recognition
```python
from pythonita.utils.speech_recognition_module import get_speech_recognizer

recognizer = get_speech_recognizer(language='it-IT')
success, text = recognizer.listen_from_microphone(timeout=5)
```

---

## 🤖 Controllo Arduino

### Nuove Funzionalità
- ✅ **Arduino Controller** (`pythonita/hardware/arduino_controller.py`)
  - Classe `ArduinoController` per comunicazione seriale
  - Auto-detect porta COM
  - Supporto comandi:
    - **Digital Write**: LED, relè, pin digitali
    - **Analog Write (PWM)**: Motori DC, dimming LED
    - **Analog Read**: Sensori analogici (temperatura, luce, etc.)
    - **Servo Control**: Servomotori 0-180°
  
- ✅ **Template Comandi Arduino** (`core/arduino_commands.py`)
  - 8 template predefiniti:
    - `accendi_led`, `spegni_led`, `lampeggia_led`
    - `leggi_sensore`, `monitor_sensore`
    - `muovi_servo`, `controlla_motore`
    - `sequenza_led`
  - Estrazione automatica parametri (pin, angolo, velocità)
  - Sinonimi italiani per numeri e angoli

- ✅ **Pannello Arduino GUI**
  - Bottone 🤖 **Arduino** per aprire pannello
  - **Sezione Connessione**:
    - Selezione porta COM (auto-detect)
    - Configurazione baud rate (9600-115200)
    - Pulsanti Connetti/Disconnetti
    - Refresh porte disponibili
  - **Controllo Manuale**:
    - **LED**: ON/OFF/Blink su pin selezionabile
    - **Servo**: Slider 0-180° con preview angolo
    - **Sensore**: Lettura analogica real-time
  - **Console Arduino**: Output comandi e risposte

### Sketch Arduino
- ✅ **File** `examples/arduino_sketch.ino`
  - Sketch completo per Arduino Uno/Nano/Mega
  - Supporto tutti i tipi di comando
  - Validazione input
  - Messaggi debug Serial Monitor
  - Test integrati

### API Arduino Controller
```python
from pythonita.hardware.arduino_controller import get_arduino_controller

arduino = get_arduino_controller()
arduino.connect(port='COM3', baudrate=9600)

# LED
arduino.led_on(13)
arduino.led_blink(13, times=3)

# Servo
arduino.servo_write(9, 90)

# Sensore
success, value = arduino.analog_read(0)
print(f"Sensore: {value}/1023")

arduino.disconnect()
```

---

## 📚 Documentazione

### Nuovi File
- ✅ **VOICE_AND_ARDUINO_GUIDE.md** - Guida completa 25+ pagine
  - Installazione dipendenze (SpeechRecognition, PyAudio, pyserial)
  - Tutorial comandi vocali
  - Schema collegamento hardware Arduino
  - Sketch Arduino documentato
  - Template comandi con esempi
  - 3 esempi pratici completi
  - Troubleshooting dettagliato

- ✅ **examples/arduino_sketch.ino** - Sketch Arduino production-ready
  - 250+ righe di codice commentato
  - Supporto 4 tipi di comando
  - Test integrati
  - Validazione input robusta

### Aggiornamenti File Esistenti
- ✅ **requirements.txt** - Aggiunte dipendenze:
  ```
  SpeechRecognition>=3.10.0
  pyaudio>=0.2.13
  pyserial>=3.5
  ```

---

## 🎯 Esempi Pratici

### Esempio 1: Controllo Vocale LED
```python
# Dì: "accendi led pin tredici"
# Pythonita:
# 1. Riconosce voce -> testo
# 2. Genera codice Python per Arduino
# 3. Arduino accende LED
```

### Esempio 2: Servo Vocale
```python
# Dì: "muovi servo a novanta gradi"
# Pythonita:
# 1. Estrae angolo (90°)
# 2. Genera codice servo_write()
# 3. Arduino muove servo a 90°
```

### Esempio 3: Monitor Sensore
```python
# Dì: "leggi sensore su pin zero"
# Pythonita:
# 1. Genera codice analog_read(0)
# 2. Arduino legge valore
# 3. Mostra risultato 0-1023
```

---

## 🔧 Installazione

### 1. Dipendenze Python
```bash
pip install -r requirements.txt
```

### 2. PyAudio (Windows)
Se errori con pyaudio:
```bash
# Scarica pre-compilato:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

pip install PyAudio‑0.2.13‑cp310‑cp310‑win_amd64.whl
```

### 3. Arduino Setup
1. Apri Arduino IDE
2. Carica `examples/arduino_sketch.ino`
3. Collega Arduino via USB
4. Verifica porta COM in Device Manager (Windows)

### 4. Test
```bash
# Test microfono
python pythonita/utils/speech_recognition_module.py

# Test Arduino
python pythonita/hardware/arduino_controller.py

# Avvia GUI completa
python gui_robot_3d.py
```

---

## 📊 Statistiche v3.4

### Codice Aggiunto
- **3 nuovi moduli Python**: 850+ righe
  - `speech_recognition_module.py`: 260 righe
  - `arduino_controller.py`: 350 righe
  - `arduino_commands.py`: 240 righe
- **Sketch Arduino**: 250+ righe
- **GUI upgrades**: 280+ righe (pannello Arduino, voice button)
- **Documentazione**: 600+ righe (guide, esempi)

### Features
- 🎤 **Speech Recognition**: 4 lingue, 2 engine
- 🤖 **Arduino**: 4 tipi comando, 8 template
- 🖥️ **GUI**: Pannello Arduino completo, pulsante voice
- 📚 **Docs**: 25+ pagine guida, 3 esempi, troubleshooting

### Testing
- ✅ Speech recognition testato: Italiano, Inglese
- ✅ Arduino controller testato: Arduino Uno, Nano
- ✅ GUI pannello Arduino: Tutti i comandi funzionanti
- ✅ Template: 8/8 template validati

---

## 🚀 Prossimi Sviluppi (v3.5)

### Pianificati
- [ ] **Multi-Arduino**: Controllo simultaneo più Arduino
- [ ] **Riconoscimento vocale offline**: Engine Sphinx migliorato
- [ ] **Template ESP32**: Supporto WiFi/Bluetooth
- [ ] **Raspberry Pi GPIO**: Controllo pin GPIO
- [ ] **Video Tutorial**: Guida video completa voice+Arduino
- [ ] **Voice Command Library**: Libreria comandi vocali custom

### In Valutazione
- [ ] App mobile per controllo remoto
- [ ] Web dashboard real-time
- [ ] Integrazione Alexa/Google Home
- [ ] Cloud sync comandi vocali

---

## 🐛 Bug Fix

- ✅ Fixed: Emoji encoding errors in console output (removed ✅ from prints)
- ✅ Fixed: Theme system compatibility con nuovi pannelli
- ✅ Fixed: Export manager import error handling

---

## 💡 Note per Sviluppatori

### Nuove API Pubbliche

#### Speech Recognition
```python
from pythonita.utils.speech_recognition_module import (
    SpeechRecognizer,
    get_speech_recognizer
)
```

#### Arduino Controller
```python
from pythonita.hardware.arduino_controller import (
    ArduinoController,
    get_arduino_controller,
    ARDUINO_TEMPLATES
)
```

#### Template Arduino
```python
from core.arduino_commands import (
    ARDUINO_COMMAND_TEMPLATES,
    get_arduino_template,
    extract_arduino_params
)
```

### Estensibilità

#### Aggiungere Nuovo Comando Arduino
```python
# In arduino_commands.py
ARDUINO_COMMAND_TEMPLATES['tuo_comando'] = {
    'keywords': ['keyword1', 'keyword2'],
    'entities': ['entity1', 'entity2'],
    'template': """# Tuo template
import serial
# ... codice ...
""",
    'default_params': {'param1': value1}
}
```

#### Personalizzare Speech Recognition
```python
recognizer = SpeechRecognizer(
    language='en-US',  # Cambia lingua
    engine='sphinx'     # Usa offline
)

# Personalizza threshold
recognizer.recognizer.energy_threshold = 3000
recognizer.recognizer.pause_threshold = 1.0
```

---

## 📄 Licenza

Pythonita IA v3.4 - Speech & Arduino
Copyright 2025 - Licenza proprietaria
[Vedi LICENSE per dettagli]

---

**Grazie per usare Pythonita IA! 🚀**

*Ora puoi programmare Arduino con la tua voce!*

