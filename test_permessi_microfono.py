"""
Test permessi accesso microfono in Windows.
Verifica se Python può accedere al microfono Realtek.
"""

import speech_recognition as sr
import time

print("=" * 70)
print("🔐 TEST PERMESSI ACCESSO MICROFONO")
print("=" * 70)

print("\nTest 1: Verifica se Python può elencare i microfoni...")
try:
    microfoni = sr.Microphone.list_microphone_names()
    print(f"✅ OK - Trovati {len(microfoni)} dispositivi")
except Exception as e:
    print(f"❌ ERRORE: {e}")
    exit(1)

print("\nTest 2: Prova ad aprire il microfono [7] Realtek...")
try:
    with sr.Microphone(device_index=7) as source:
        print("✅ OK - Microfono aperto!")
        print("   Tipo:", type(source))
except PermissionError as e:
    print(f"❌ ERRORE DI PERMESSI: {e}")
    print("\n💡 SOLUZIONE:")
    print("   Windows sta BLOCCANDO l'accesso al microfono!")
    print("   Vai in: Impostazioni → Privacy → Microfono")
    print("   Abilita 'Consenti alle app di accedere al microfono'")
    exit(1)
except Exception as e:
    print(f"❌ ERRORE: {e}")
    exit(1)

print("\nTest 3: Prova a catturare audio di 2 secondi...")
recognizer = sr.Recognizer()

try:
    with sr.Microphone(device_index=7) as source:
        print("⏳ Calibrazione...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        print("🔴 FACCIO RUMORE per 2 secondi (batti le mani, parla, ecc)...")
        print("   Sto catturando...")
        
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=2)
        
        print("✅ Audio catturato!")
        
        # Analizza
        import numpy as np
        audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
        volume_max = np.max(np.abs(audio_data))
        
        print(f"   Volume: {volume_max}")
        
        if volume_max < 100:
            print("\n❌ NESSUN AUDIO CATTURATO!")
            print("   → Python probabilmente NON ha accesso al microfono")
            print("\n💡 VAI IN:")
            print("   Impostazioni Windows → Privacy e sicurezza → Microfono")
            print("   Abilita: 'Consenti alle app di accedere al microfono'")
            print("   Abilita: 'Consenti alle app desktop di accedere al microfono'")
        elif volume_max > 30000:
            print(f"\n⚠️  Volume TROPPO ALTO (distorto)")
            print(f"   → Abbassa volume microfono in Windows a 60-70%")
        else:
            print(f"\n✅ VOLUME OK! Python ha accesso al microfono!")
            print(f"   Il problema NON sono i permessi.")
            
except sr.WaitTimeoutError:
    print("\n❌ TIMEOUT - Nessun audio rilevato")
    print("   → Possibile problema permessi o microfono non funzionante")
except Exception as e:
    print(f"\n❌ ERRORE: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("TEST COMPLETATO")
print("=" * 70)

