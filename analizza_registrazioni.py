"""
Analizza e riconosce le registrazioni audio salvate.
Utile per verificare cosa è stato registrato e se Google lo riconosce.
"""

import os
import wave
import numpy as np
import speech_recognition as sr
from glob import glob

def analizza_file_audio(filename):
    """Analizza un file audio e prova a riconoscerlo."""
    
    print("\n" + "=" * 70)
    print(f"ANALISI: {filename}")
    print("=" * 70)
    
    # Leggi file WAV
    try:
        with wave.open(filename, 'rb') as wf:
            sample_rate = wf.getframerate()
            n_channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            n_frames = wf.getnframes()
            duration = n_frames / sample_rate
            
            # Leggi dati audio
            audio_data = np.frombuffer(wf.readframes(n_frames), dtype=np.int16)
            
        # Statistiche audio
        volume_max = np.max(np.abs(audio_data))
        volume_avg = np.mean(np.abs(audio_data))
        volume_rms = np.sqrt(np.mean(audio_data.astype(float)**2))
        
        print(f"\n📊 INFORMAZIONI FILE:")
        print(f"  - Durata: {duration:.2f} secondi")
        print(f"  - Sample Rate: {sample_rate} Hz")
        print(f"  - Canali: {n_channels}")
        print(f"  - Bit Depth: {sample_width * 8} bit")
        print(f"  - Campioni: {n_frames}")
        
        print(f"\n🔊 VOLUME:")
        print(f"  - MAX: {volume_max}")
        print(f"  - AVG: {volume_avg:.0f}")
        print(f"  - RMS: {volume_rms:.0f}")
        
        # Diagnosi
        print(f"\n💡 DIAGNOSI:")
        if volume_max < 100:
            print(f"  ❌ VOLUME TROPPO BASSO! (<100)")
            print(f"  ❌ Google NON può riconoscere")
            print(f"  👉 SOLUZIONE: Aumenta volume microfono in Windows a 100%")
            return False
        elif volume_max < 500:
            print(f"  ⚠️  Volume BASSO (100-500)")
            print(f"  ⚠️  Riconoscimento non garantito")
        elif volume_max < 2000:
            print(f"  ✅ Volume BUONO (500-2000)")
        else:
            print(f"  ✅ Volume OTTIMO! (>2000)")
        
        # Riconoscimento con Google
        print(f"\n🔄 RICONOSCIMENTO GOOGLE:")
        print(f"  Invio a Google Speech Recognition...")
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
            
        try:
            text = recognizer.recognize_google(audio, language='it-IT')
            print(f"\n  ✅ SUCCESSO!")
            print(f"  📝 Testo riconosciuto: '{text}'")
            return True
            
        except sr.UnknownValueError:
            print(f"\n  ❌ Google NON ha riconosciuto il testo")
            print(f"  Possibili cause:")
            print(f"    - Volume troppo basso")
            print(f"    - Audio non comprensibile")
            print(f"    - Rumore di fondo")
            print(f"    - Nessuna parola pronunciata")
            return False
            
        except sr.RequestError as e:
            print(f"\n  ❌ Errore connessione: {e}")
            return False
            
    except Exception as e:
        print(f"\n❌ Errore lettura file: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Analizza tutte le registrazioni disponibili."""
    
    print("=" * 70)
    print("ANALISI REGISTRAZIONI AUDIO")
    print("=" * 70)
    
    # Trova tutti i file registrazione_*.wav
    files = glob("registrazione_*.wav")
    
    if not files:
        print("\n❌ Nessun file 'registrazione_*.wav' trovato!")
        print("Prima registra qualcosa dalla GUI premendo REC")
        return
    
    # Ordina per data (più recente prima)
    files.sort(reverse=True)
    
    print(f"\n✅ Trovati {len(files)} file di registrazione:")
    for i, f in enumerate(files, 1):
        size_kb = os.path.getsize(f) / 1024
        print(f"  [{i}] {f} ({size_kb:.1f} KB)")
    
    # Chiedi quale analizzare
    print("\n" + "-" * 70)
    scelta = input("Quale file vuoi analizzare? (1=più recente, 0=tutti): ").strip()
    
    if scelta == '0':
        # Analizza tutti
        print("\n🔍 Analisi di tutti i file...")
        for f in files:
            analizza_file_audio(f)
    else:
        # Analizza uno specifico
        try:
            idx = int(scelta) - 1
            if 0 <= idx < len(files):
                analizza_file_audio(files[idx])
                
                # Chiedi se vuoi ascoltare
                print("\n" + "-" * 70)
                risposta = input("\nVuoi ascoltare il file con Windows Media Player? (s/n): ").strip().lower()
                if risposta == 's':
                    os.startfile(files[idx])
                    print(f"✅ Aperto: {files[idx]}")
            else:
                print(f"❌ Scelta non valida!")
        except ValueError:
            print(f"❌ Inserisci un numero!")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAnalisi interrotta.")
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()

