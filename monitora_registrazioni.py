"""
Monitor automatico delle registrazioni audio.
Analizza ogni nuovo file e mostra cosa Google riconosce.
"""

import time
import os
import speech_recognition as sr
import wave
import numpy as np
from glob import glob
from datetime import datetime

print("=" * 70)
print("🎧 MONITOR REGISTRAZIONI AUDIO - In attesa...")
print("=" * 70)
print("Fai le tue prove nella GUI, io ti dirò cosa viene riconosciuto!\n")

# File già visti
seen_files = set(glob("registrazione_*.wav"))
recognizer = sr.Recognizer()

try:
    while True:
        # Controlla nuovi file
        current_files = set(glob("registrazione_*.wav"))
        new_files = current_files - seen_files
        
        for filename in sorted(new_files):
            # Aspetta che il file sia completo
            time.sleep(0.5)
            
            print("\n" + "=" * 70)
            print(f"📁 NUOVO FILE: {filename}")
            print("=" * 70)
            
            try:
                # Analizza volume
                with wave.open(filename, 'rb') as wf:
                    audio_data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
                    volume_max = np.max(np.abs(audio_data))
                    volume_avg = np.mean(np.abs(audio_data))
                    duration = wf.getnframes() / wf.getframerate()
                
                print(f"📊 Durata: {duration:.1f}s")
                print(f"🔊 Volume MAX: {volume_max}, AVG: {volume_avg:.0f}")
                
                # Diagnosi volume
                if volume_max < 100:
                    print(f"❌ VOLUME TROPPO BASSO!")
                    print(f"   → Aumenta volume microfono in Windows")
                elif volume_max < 500:
                    print(f"⚠️  Volume basso, potrebbe non funzionare")
                elif volume_max > 30000:
                    print(f"❌ VOLUME TROPPO ALTO! Audio DISTORTO")
                    print(f"   → Abbassa volume microfono a 60-70% in Windows")
                else:
                    print(f"✅ Volume OK!")
                
                # Riconoscimento Google
                print(f"\n🔄 Invio a Google Speech Recognition...")
                
                with sr.AudioFile(filename) as source:
                    audio = recognizer.record(source)
                
                text = recognizer.recognize_google(audio, language='it-IT')
                
                print(f"\n✅✅✅ RICONOSCIUTO: '{text}' ✅✅✅")
                print(f"Lunghezza: {len(text)} caratteri")
                
            except sr.UnknownValueError:
                print(f"\n❌ Google NON ha riconosciuto parole")
                if volume_max > 30000:
                    print(f"   Causa: Audio distorto (volume troppo alto)")
                    print(f"   → Abbassa volume microfono a 60-70%")
                elif volume_max < 500:
                    print(f"   Causa: Volume troppo basso")
                    print(f"   → Aumenta volume microfono")
                else:
                    print(f"   Possibili cause:")
                    print(f"   - Parlato troppo veloce/non chiaro")
                    print(f"   - Troppo rumore di fondo")
                    print(f"   - Microfono sbagliato")
                    
            except sr.RequestError as e:
                print(f"\n❌ Errore Google: {e}")
                print(f"   Controlla connessione internet!")
            except Exception as e:
                print(f"\n❌ Errore: {e}")
            
            seen_files.add(filename)
            
            print("\n" + "=" * 70)
            print("⏳ In attesa di nuove registrazioni...")
            print("=" * 70)
        
        # Aspetta un po' prima di controllare di nuovo
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\n\n👋 Monitor fermato. Ciao!")


