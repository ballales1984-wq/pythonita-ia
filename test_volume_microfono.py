"""
Test rapido volume microfono - verifica se il problema è il volume.
"""

import speech_recognition as sr
import numpy as np
import time

def test_volume():
    print("=" * 70)
    print("TEST VOLUME MICROFONO")
    print("=" * 70)
    
    # Chiedi quale microfono
    microfoni = sr.Microphone.list_microphone_names()
    print("\nMicrofoni disponibili:")
    for idx, nome in enumerate(microfoni):
        print(f"  [{idx}] {nome}")
    
    mic_idx = input("\nQuale microfono vuoi testare? (default 7): ").strip()
    mic_idx = int(mic_idx) if mic_idx else 7
    
    print(f"\n✅ Microfono: [{mic_idx}] {microfoni[mic_idx]}")
    print("\n" + "=" * 70)
    print("PARLA NEL MICROFONO per 3 secondi...")
    print("Conta ad alta voce: UNO, DUE, TRE, QUATTRO, CINQUE")
    print("=" * 70)
    
    input("\nPremi INVIO quando sei pronto...")
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone(device_index=mic_idx) as source:
            print("\n⏳ Calibrazione (1 secondo)...")
            recognizer.adjust_for_ambient_noise(source, duration=1.0)
            print(f"✅ Energy Threshold: {recognizer.energy_threshold}")
            
            print("\n🔴 PARLA ORA! (conta: uno, due, tre...)")
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=5)
            
            # Analizza volume
            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
            volume_max = np.max(np.abs(audio_data))
            volume_avg = np.mean(np.abs(audio_data))
            
            print("\n" + "=" * 70)
            print("RISULTATI:")
            print("=" * 70)
            print(f"  Volume MASSIMO: {volume_max}")
            print(f"  Volume MEDIO:   {volume_avg:.0f}")
            print(f"  Campioni:       {len(audio_data)}")
            
            # Diagnosi
            print("\n📊 DIAGNOSI:")
            if volume_max < 100:
                print("  ❌ VOLUME TROPPO BASSO! (<100)")
                print("  ❌ Google NON può riconoscere con questo volume")
                print("\n💡 SOLUZIONE:")
                print("  1. Vai in: Impostazioni Windows → Sistema → Audio")
                print("  2. Clicca su 'Microfono' → 'Proprietà dispositivo'")
                print("  3. Alza 'Volume input' al 100%")
                print("  4. Attiva 'Amplificazione microfono' se disponibile")
                return False
                
            elif volume_max < 500:
                print("  ⚠️  Volume BASSO (100-500)")
                print("  ⚠️  Potrebbe funzionare, ma non è garantito")
                print("\n💡 CONSIGLIO: Aumenta il volume del microfono in Windows")
                
            elif volume_max < 2000:
                print("  ✅ Volume BUONO (500-2000)")
                print("  ✅ Dovrebbe funzionare!")
                
            else:
                print("  ✅ Volume OTTIMO! (>2000)")
                print("  ✅ Perfetto per il riconoscimento!")
            
            # Prova riconoscimento
            print("\n" + "=" * 70)
            print("TEST RICONOSCIMENTO GOOGLE:")
            print("=" * 70)
            print("🔄 Invio audio a Google...")
            
            try:
                text = recognizer.recognize_google(audio, language='it-IT')
                print(f"\n🎉 SUCCESSO!")
                print(f"  Testo riconosciuto: '{text}'")
                print("\n✅ Il microfono funziona correttamente!")
                return True
                
            except sr.UnknownValueError:
                print(f"\n❌ Google NON ha riconosciuto il testo")
                print(f"  (ma ha ricevuto l'audio - volume: {volume_max})")
                print("\n💡 POSSIBILI CAUSE:")
                print("  - Volume troppo basso")
                print("  - Parlato troppo piano o veloce")
                print("  - Troppo rumore di fondo")
                print("  - Parole non chiare")
                print("\n💡 PROVA:")
                print("  1. Aumenta il volume del microfono al 100%")
                print("  2. Parla PIÙ FORTE e VICINO al microfono")
                print("  3. Parla LENTAMENTE e CHIARAMENTE")
                return False
                
            except sr.RequestError as e:
                print(f"\n❌ Errore connessione Google: {e}")
                print("  Controlla la connessione internet!")
                return False
    
    except sr.WaitTimeoutError:
        print("\n❌ TIMEOUT: Nessun audio rilevato!")
        print("\n💡 POSSIBILI CAUSE:")
        print("  - Microfono disabilitato in Windows")
        print("  - Microfono sbagliato selezionato")
        print("  - Microfono non funzionante")
        return False
        
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🎤 TEST VOLUME E RICONOSCIMENTO MICROFONO")
    print("Questo script ti dirà se il volume è troppo basso\n")
    
    try:
        success = test_volume()
        
        print("\n" + "=" * 70)
        if success:
            print("✅ TUTTO OK! Il microfono funziona nella GUI!")
        else:
            print("❌ PROBLEMA RILEVATO - Segui le istruzioni sopra")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\nTest interrotto.")


