"""
Identifica e testa il microfono integrato del portatile.
"""

import speech_recognition as sr
import re

def identifica_microfono_integrato():
    """Identifica quale microfono è quello integrato del portatile."""
    
    print("=" * 70)
    print("IDENTIFICAZIONE MICROFONO INTEGRATO PORTATILE")
    print("=" * 70)
    
    microfoni = sr.Microphone.list_microphone_names()
    
    print(f"\n📋 Trovati {len(microfoni)} dispositivi audio:\n")
    
    # Parole chiave per identificare microfono integrato
    keywords_integrato = [
        'realtek',
        'integrated',
        'internal', 
        'built-in',
        'laptop',
        'notebook',
        'conexant',
        'intel',
        'smart sound'
    ]
    
    # Parole chiave per dispositivi ESTERNI (da escludere)
    keywords_esterni = [
        'webcam',
        'usb',
        'bluetooth',
        'm-audio',
        'focusrite',
        'behringer',
        'logitech',
        'speaker',  # altoparlanti, non microfoni
        'output',   # uscite audio
        'stereo mix',
        'wave out'
    ]
    
    candidati_integrati = []
    candidati_esterni = []
    
    for idx, nome in enumerate(microfoni):
        nome_lower = nome.lower()
        
        # Classifica come esterno
        is_esterno = any(keyword in nome_lower for keyword in keywords_esterni)
        
        # Classifica come integrato
        is_integrato = any(keyword in nome_lower for keyword in keywords_integrato)
        
        # Mostra con colore
        if is_integrato and not is_esterno:
            print(f"   🟢 [{idx:2d}] {nome}  ← PROBABILMENTE INTEGRATO")
            candidati_integrati.append((idx, nome))
        elif is_esterno:
            print(f"   🔴 [{idx:2d}] {nome}  (esterno)")
            candidati_esterni.append((idx, nome))
        else:
            print(f"   ⚪ [{idx:2d}] {nome}")
    
    print("\n" + "-" * 70)
    
    if candidati_integrati:
        print(f"\n✅ MICROFONO INTEGRATO IDENTIFICATO:")
        for idx, nome in candidati_integrati:
            print(f"   [{idx}] {nome}")
        
        # Usa il primo candidato
        mic_integrato_idx = candidati_integrati[0][0]
        mic_integrato_nome = candidati_integrati[0][1]
        
    else:
        print(f"\n⚠️  Nessun microfono integrato identificato automaticamente.")
        print(f"Elenco dispositivi senza 'webcam' o 'usb':\n")
        
        possibili = [(idx, nome) for idx, nome in enumerate(microfoni) 
                     if not any(kw in nome.lower() for kw in keywords_esterni)]
        
        for idx, nome in possibili:
            print(f"   [{idx}] {nome}")
        
        if possibili:
            mic_integrato_idx = possibili[0][0]
            mic_integrato_nome = possibili[0][1]
            print(f"\n💡 Suggerimento: prova [{mic_integrato_idx}] {mic_integrato_nome}")
        else:
            print("\n❌ Impossibile identificare il microfono integrato.")
            return
    
    # Test del microfono identificato
    print("\n" + "=" * 70)
    print(f"TEST MICROFONO: [{mic_integrato_idx}] {mic_integrato_nome}")
    print("=" * 70)
    
    risposta = input(f"\nVuoi testare questo microfono? (s/n): ").strip().lower()
    
    if risposta != 's':
        print("Test annullato.")
        return
    
    # Test riconoscimento
    print(f"\n🎤 Preparazione microfono [{mic_integrato_idx}]...")
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone(device_index=mic_integrato_idx) as source:
            print(f"✅ Microfono aperto!")
            print(f"\n⏳ Calibrazione (1 secondo)...")
            recognizer.adjust_for_ambient_noise(source, duration=1.0)
            print(f"   Energy Threshold: {recognizer.energy_threshold}")
            
            print(f"\n🔴 PARLA ORA! (5 secondi)")
            print(f"   Prova a dire: 'crea una lista con mele e pere'")
            
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=5)
            
            # Analizza volume
            import numpy as np
            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
            volume = np.max(np.abs(audio_data))
            
            print(f"\n✅ Audio catturato!")
            print(f"   Volume: {volume}")
            
            if volume < 100:
                print(f"   ⚠️  VOLUME TROPPO BASSO!")
                print(f"   Vai in Impostazioni Windows → Suono → Microfono")
                print(f"   e aumenta il volume al 100%")
            elif volume < 500:
                print(f"   ⚠️  Volume basso, potrebbe non funzionare")
            else:
                print(f"   ✅ Volume OK!")
            
            # Riconoscimento
            print(f"\n🔄 Riconoscimento con Google...")
            text = recognizer.recognize_google(audio, language='it-IT')
            
            print(f"\n🎉 SUCCESSO!")
            print(f"   Testo riconosciuto: '{text}'")
            print(f"\n✅ Il microfono [{mic_integrato_idx}] funziona correttamente!")
            
    except sr.WaitTimeoutError:
        print(f"\n❌ Timeout: nessun audio rilevato")
        print(f"   Il microfono potrebbe essere disabilitato in Windows")
    except sr.UnknownValueError:
        print(f"\n❌ Audio catturato ma NON riconosciuto")
        print(f"   Possibili cause:")
        print(f"   - Volume troppo basso (controlla in Windows)")
        print(f"   - Parlato troppo piano o lontano")
        print(f"   - Rumore di fondo troppo alto")
    except sr.RequestError as e:
        print(f"\n❌ Errore connessione Google: {e}")
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print(f"\n💡 CONFIGURAZIONE PER LA GUI:")
    print(f"   Nella GUI, seleziona dal menu a tendina:")
    print(f"   [{mic_integrato_idx}] {mic_integrato_nome[:50]}")
    print("=" * 70)

if __name__ == "__main__":
    try:
        identifica_microfono_integrato()
    except KeyboardInterrupt:
        print("\n\nTest interrotto.")
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()


