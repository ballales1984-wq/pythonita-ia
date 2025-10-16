"""
Test diagnostico completo per microfono e riconoscimento vocale.
Verifica se il microfono cattura audio e se Google riesce a riconoscere.
"""

import speech_recognition as sr
import numpy as np
import wave
import os
from datetime import datetime

def test_microfono_dettagliato():
    """Test completo del microfono con diagnostica."""
    
    print("=" * 70)
    print("TEST DIAGNOSTICO MICROFONO E RICONOSCIMENTO VOCALE")
    print("=" * 70)
    
    # Lista microfoni
    print("\n1. MICROFONI DISPONIBILI:")
    print("-" * 70)
    recognizer = sr.Recognizer()
    microfoni = sr.Microphone.list_microphone_names()
    
    for idx, nome in enumerate(microfoni):
        print(f"   [{idx}] {nome}")
    
    # Chiedi quale microfono testare
    print("\n" + "-" * 70)
    mic_idx = input("Inserisci il numero del microfono da testare (default: 7): ").strip()
    mic_idx = int(mic_idx) if mic_idx else 7
    
    if mic_idx < 0 or mic_idx >= len(microfoni):
        print(f"❌ Indice {mic_idx} non valido!")
        return
    
    print(f"\n✅ Microfono selezionato: [{mic_idx}] {microfoni[mic_idx]}")
    
    # Test 1: Cattura audio grezzo
    print("\n" + "=" * 70)
    print("2. TEST CATTURA AUDIO GREZZO")
    print("-" * 70)
    print("Parla nel microfono per 3 secondi...")
    print("(Controlla se l'audio viene catturato)")
    
    try:
        with sr.Microphone(device_index=mic_idx, sample_rate=16000) as source:
            # Mostra info microfono
            print(f"\n📊 Configurazione:")
            print(f"   - Sample Rate: {source.SAMPLE_RATE} Hz")
            print(f"   - Sample Width: {source.SAMPLE_WIDTH} bytes")
            print(f"   - Chunk Size: {source.CHUNK} samples")
            
            # Calibrazione
            print(f"\n⏳ Calibrazione rumore ambiente (1s)...")
            recognizer.adjust_for_ambient_noise(source, duration=1.0)
            print(f"   - Energy Threshold: {recognizer.energy_threshold}")
            print(f"   - Dynamic Threshold: {recognizer.dynamic_energy_threshold}")
            
            # Cattura audio
            print(f"\n🔴 PARLA ORA! (3 secondi)")
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=3)
            
            # Analizza audio catturato
            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
            
            print(f"\n✅ Audio catturato!")
            print(f"   - Durata: {len(audio_data) / audio.sample_rate:.2f} secondi")
            print(f"   - Campioni: {len(audio_data)}")
            print(f"   - Volume MAX: {np.max(np.abs(audio_data))}")
            print(f"   - Volume AVG: {np.mean(np.abs(audio_data)):.0f}")
            print(f"   - Sample Rate: {audio.sample_rate} Hz")
            
            # Salva file audio per verifica
            filename = f"test_audio_{datetime.now().strftime('%H%M%S')}.wav"
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(audio.sample_width)
                wf.setframerate(audio.sample_rate)
                wf.writeframes(audio.get_raw_data())
            
            print(f"   - File salvato: {filename}")
            
            # Verifica se c'è audio significativo
            volume_max = np.max(np.abs(audio_data))
            if volume_max < 100:
                print(f"\n⚠️  ATTENZIONE: Volume molto basso! ({volume_max})")
                print(f"   Possibili cause:")
                print(f"   - Microfono troppo lontano")
                print(f"   - Volume microfono Windows troppo basso")
                print(f"   - Microfono non funzionante")
            elif volume_max < 500:
                print(f"\n⚠️  Volume basso ({volume_max}), ma potrebbe funzionare")
            else:
                print(f"\n✅ Volume OK! ({volume_max})")
            
    except sr.WaitTimeoutError:
        print("\n❌ Timeout: nessun audio rilevato!")
        print("   Il microfono potrebbe essere spento o non funzionante.")
        return
    except Exception as e:
        print(f"\n❌ Errore cattura audio: {e}")
        return
    
    # Test 2: Riconoscimento Google
    print("\n" + "=" * 70)
    print("3. TEST RICONOSCIMENTO GOOGLE")
    print("-" * 70)
    print("Provo a riconoscere l'audio catturato con Google...")
    
    try:
        text = recognizer.recognize_google(audio, language='it-IT')
        print(f"\n✅ SUCCESSO!")
        print(f"   Testo riconosciuto: '{text}'")
        
    except sr.UnknownValueError:
        print(f"\n❌ Google non ha riconosciuto nessun testo.")
        print(f"   Possibili cause:")
        print(f"   - Volume troppo basso")
        print(f"   - Audio non comprensibile (rumore, distorsione)")
        print(f"   - Nessuna parola pronunciata")
        print(f"\n💡 SUGGERIMENTI:")
        print(f"   1. Controlla il volume del microfono in Windows")
        print(f"   2. Parla più forte e più vicino al microfono")
        print(f"   3. Verifica che il microfono sia quello giusto")
        print(f"   4. Ascolta il file '{filename}' per verificare l'audio")
        
    except sr.RequestError as e:
        print(f"\n❌ Errore connessione Google: {e}")
        print(f"   Verifica la connessione internet!")
    
    # Test 3: Secondo tentativo interattivo
    print("\n" + "=" * 70)
    print("4. SECONDO TENTATIVO")
    print("-" * 70)
    risposta = input("Vuoi fare un altro tentativo? (s/n): ").strip().lower()
    
    if risposta == 's':
        print("\nParla CHIARAMENTE e FORTE per 5 secondi...")
        try:
            with sr.Microphone(device_index=mic_idx) as source:
                recognizer.adjust_for_ambient_noise(source, duration=1.0)
                print("🔴 PARLA ORA!")
                audio2 = recognizer.listen(source, timeout=15, phrase_time_limit=5)
                
                audio_data2 = np.frombuffer(audio2.get_raw_data(), dtype=np.int16)
                volume2 = np.max(np.abs(audio_data2))
                print(f"   Volume: {volume2}")
                
                print("🔄 Riconoscendo...")
                text2 = recognizer.recognize_google(audio2, language='it-IT')
                print(f"\n✅ Testo: '{text2}'")
                
        except sr.UnknownValueError:
            print("\n❌ Ancora nessun testo riconosciuto.")
        except Exception as e:
            print(f"\n❌ Errore: {e}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETATO")
    print("=" * 70)
    print("\n💡 PROSSIMI PASSI:")
    print("   1. Se volume < 500: aumenta volume microfono in Windows")
    print("   2. Se audio non riconosciuto: prova un microfono diverso")
    print("   3. Ascolta il file WAV salvato per verificare la qualità")
    print()

if __name__ == "__main__":
    try:
        test_microfono_dettagliato()
    except KeyboardInterrupt:
        print("\n\nTest interrotto dall'utente.")
    except Exception as e:
        print(f"\n\n❌ Errore generale: {e}")
        import traceback
        traceback.print_exc()

