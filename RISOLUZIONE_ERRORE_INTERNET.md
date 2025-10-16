# 🔧 Risoluzione Errore "Connection Failed"

## ❌ Problema

Errore durante il riconoscimento vocale:
```
Connection failed. If the problem persists, please check your internet connection or VPN
```

## 🔍 Causa

Il riconoscimento vocale **Google** (default) richiede **connessione internet** per funzionare.

## ✅ Soluzioni

### **Soluzione 1: Usa Sphinx (OFFLINE - CONSIGLIATO)**

Sphinx funziona **completamente offline** senza bisogno di internet.

#### Installazione

```bash
pip install pocketsphinx
```

#### Configurazione GUI

Modifica `gui_robot_3d.py` alla riga ~98:

**Prima (ONLINE):**
```python
self.speech_recognizer = get_speech_recognizer(language='it-IT')
```

**Dopo (OFFLINE):**
```python
self.speech_recognizer = get_speech_recognizer(
    language='it-IT',
    engine='sphinx'  # <- Usa Sphinx offline
)
```

#### Vantaggi Sphinx
- ✅ Funziona offline
- ✅ Nessuna dipendenza da internet
- ✅ Privacy completa (tutto locale)
- ✅ Veloce

#### Svantaggi Sphinx
- ⚠️  Meno accurato per italiano
- ⚠️  Richiede pronuncia chiara

---

### **Soluzione 2: Ripristina Connessione Internet**

Se preferisci usare Google (più accurato):

1. **Verifica connessione**:
   ```bash
   ping google.com
   ```

2. **Controlla VPN/Proxy**:
   - Disabilita VPN temporaneamente
   - Controlla firewall

3. **Test connessione**:
   ```bash
   python -c "import urllib.request; urllib.request.urlopen('https://google.com'); print('✅ Internet OK')"
   ```

---

### **Soluzione 3: Modalità Ibrida (AUTO)**

Usa Google se disponibile, altrimenti Sphinx:

```python
# In gui_robot_3d.py, riga ~98
try:
    # Prova Google (online)
    self.speech_recognizer = get_speech_recognizer(
        language='it-IT',
        engine='google'
    )
    print("[GUI] Speech: Google (online)")
except:
    # Fallback a Sphinx (offline)
    self.speech_recognizer = get_speech_recognizer(
        language='it-IT',
        engine='sphinx'
    )
    print("[GUI] Speech: Sphinx (offline)")
```

---

## 🧪 Test

### Test Offline (Sphinx)

```bash
python test_speech_offline.py
```

### Test Online (Google)

```bash
python test_speech_recognition.py
```

---

## 📊 Confronto Engines

| Feature | Google | Sphinx | Whisper |
|---------|--------|--------|---------|
| **Connessione** | ✅ Online | ✅ Offline | ✅ Offline |
| **Accuratezza IT** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Velocità** | ⚡⚡⚡ | ⚡⚡⚡⚡⚡ | ⚡⚡ |
| **Privacy** | ❌ Dati online | ✅ Locale | ✅ Locale |
| **Installazione** | Semplice | Semplice | Complessa |

---

## 🎯 Raccomandazioni

### Per Uso Normale
- ✅ **Sphinx** (offline, autonomo, veloce)

### Per Massima Accuratezza
- ✅ **Google** (se hai internet stabile)

### Per Progetti Privacy-Sensibili
- ✅ **Sphinx** o **Whisper** (100% locale)

---

## 🔧 Comandi Utili

```bash
# Verifica engine installati
python -c "import speech_recognition as sr; print(sr.__version__)"

# Lista microfoni
python -c "import speech_recognition as sr; [print(f'{i}: {m}') for i, m in enumerate(sr.Microphone.list_microphone_names())]"

# Test Sphinx
python -c "from pythonita.utils.speech_recognition_module import SpeechRecognizer; r = SpeechRecognizer(engine='sphinx'); print('✅ Sphinx OK' if r else '❌ Error')"

# Test Google (richiede internet)
python -c "from pythonita.utils.speech_recognition_module import SpeechRecognizer; r = SpeechRecognizer(engine='google'); print('✅ Google OK' if r else '❌ Error')"
```

---

## ✅ Status Finale

- ✅ **Pocketsphinx installato**
- ✅ **GUI configurata per OFFLINE**
- ✅ **Test passano**
- ✅ **Funziona senza internet**

---

**Pythonita IA v3.4** - *Ora funziona anche offline!* 🎤🔌

