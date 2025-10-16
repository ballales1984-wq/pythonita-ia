"""Test veloce dell'ultima registrazione audio."""
import speech_recognition as sr
import wave
import numpy as np
from glob import glob

# Trova ultimo file
files = sorted(glob("registrazione_*.wav"), reverse=True)
if not files:
    print("❌ Nessun file trovato!")
    exit()

filename = files[0]
print(f"🎧 File: {filename}\n")

# Analizza volume
with wave.open(filename, 'rb') as wf:
    audio_data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
    volume_max = np.max(np.abs(audio_data))
    print(f"🔊 Volume MAX: {volume_max}")

# Riconosci con Google
print(f"\n🔄 Riconoscimento Google...")
recognizer = sr.Recognizer()

with sr.AudioFile(filename) as source:
    audio = recognizer.record(source)
    
try:
    text = recognizer.recognize_google(audio, language='it-IT')
    print(f"\n✅ RICONOSCIUTO: '{text}'")
except sr.UnknownValueError:
    print(f"\n❌ Google NON ha riconosciuto nessuna parola")
    print(f"   Volume: {volume_max}")
    print(f"\n💡 Possibili cause:")
    print(f"   - Parlato troppo veloce")
    print(f"   - Rumore di fondo troppo alto")
    print(f"   - Microfono troppo lontano dalla bocca")
    print(f"   - Parole pronunciate male")
    print(f"\n🎯 PROVA:")
    print(f"   - Parla PIÙ LENTAMENTE")
    print(f"   - Parla PIÙ VICINO al microfono")
    print(f"   - Di' parole più semplici: 'uno due tre'")
except sr.RequestError as e:
    print(f"\n❌ Errore Google: {e}")


