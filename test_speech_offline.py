#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Speech Recognition OFFLINE (senza internet)
Usa Sphinx invece di Google
"""

import logging
from pythonita.utils.speech_recognition_module import SpeechRecognizer
from pythonita.core.generatore import GeneratoreCodice

logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_offline():
    """Test riconoscimento vocale OFFLINE."""
    
    print("=" * 70)
    print("🎤 TEST SPEECH RECOGNITION OFFLINE (Sphinx)")
    print("=" * 70)
    print("\nQuesta versione funziona SENZA internet!")
    print("Usa Pocketsphinx per il riconoscimento locale.\n")
    
    # 1. Inizializza con engine offline
    print("📌 Inizializzazione engine OFFLINE...")
    print("-" * 70)
    
    try:
        recognizer = SpeechRecognizer(language='it-IT', engine='sphinx')
        print("✅ Sphinx engine caricato (OFFLINE)")
    except Exception as e:
        print(f"❌ Errore: {e}")
        print("\nInstalla Pocketsphinx:")
        print("  pip install pocketsphinx")
        return
    
    # 2. Test microfono
    print("\n📌 Test Microfono...")
    print("-" * 70)
    success, message = recognizer.test_microphone()
    print(f"{'✅' if success else '❌'} {message}")
    
    if not success:
        return
    
    # 3. Test AI locale (non richiede internet)
    print("\n📌 Test AI Locale (Ollama)...")
    print("-" * 70)
    gen = GeneratoreCodice(use_ai=True, use_cache=False)
    
    if gen.ai_disponibile:
        print("✅ AI locale disponibile (Ollama funziona offline)")
    else:
        print("⚠️  AI non disponibile, userò sistema a regole")
    
    # 4. Istruzioni uso
    print("\n" + "=" * 70)
    print("🚀 COME USARE SPEECH OFFLINE")
    print("=" * 70)
    print("""
Per usare il riconoscimento vocale OFFLINE nella GUI:

1. Modifica gui_robot_3d.py, riga ~98:
   
   Prima (ONLINE):
     self.speech_recognizer = get_speech_recognizer(language='it-IT')
   
   Dopo (OFFLINE):
     self.speech_recognizer = get_speech_recognizer(
         language='it-IT', 
         engine='sphinx'  # <- Usa Sphinx offline
     )

2. Avvia GUI:
   python gui_robot_3d.py

3. Usa il pulsante 🎤 normalmente
   - NON serve internet
   - Funziona completamente offline
   - Meno accurato di Google ma autonomo

NOTA: Sphinx è meno accurato per l'italiano.
      Parla chiaramente e lentamente.
""")
    
    print("=" * 70)
    print("✅ CONFIGURAZIONE OFFLINE PRONTA!")
    print("=" * 70)


if __name__ == "__main__":
    test_offline()

