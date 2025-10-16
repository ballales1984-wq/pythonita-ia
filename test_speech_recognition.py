#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test completo Speech Recognition + AI + Code Generation
Simula il workflow: Voce → Testo → AI → Codice Python
"""

import logging
from pythonita.utils.speech_recognition_module import get_speech_recognizer
from pythonita.core.generatore import GeneratoreCodice

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_complete_workflow():
    """Test workflow completo: Voce → AI → Codice."""
    
    print("=" * 70)
    print("🎤 TEST COMPLETO SPEECH RECOGNITION + AI")
    print("=" * 70)
    
    # 1. Test Microfono
    print("\n📌 STEP 1: Test Microfono")
    print("-" * 70)
    recognizer = get_speech_recognizer(language='it-IT', engine='google')
    success, message = recognizer.test_microphone()
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        return
    
    # 2. Test AI
    print("\n📌 STEP 2: Test AI (Ollama + Llama3.2)")
    print("-" * 70)
    gen_robot = GeneratoreCodice(use_ai=True, use_cache=False, template='robot')
    gen_generico = GeneratoreCodice(use_ai=True, use_cache=False, template='generico')
    
    if gen_robot.ai_disponibile:
        print("✅ AI disponibile e connessa")
    else:
        print("⚠️  AI non disponibile, usa sistema a regole")
    
    # 3. Simulazione comandi vocali
    print("\n📌 STEP 3: Simulazione Comandi Vocali → Codice")
    print("-" * 70)
    
    comandi_test = [
        ("apri mano", gen_robot, "Template Robot"),
        ("chiudi pugno", gen_robot, "Template Robot"),
        ("stampa ciao mondo", gen_generico, "Template Generico"),
        ("somma 10 e 20", gen_generico, "Template Generico"),
    ]
    
    for i, (comando, generatore, template) in enumerate(comandi_test, 1):
        print(f"\n{i}. Comando vocale simulato: '{comando}'")
        print(f"   Template: {template}")
        
        # Genera codice
        codice = generatore.genera(comando)
        
        # Mostra codice generato
        print("\n   📝 Codice generato:")
        for line in codice.split('\n')[:5]:  # Prime 5 righe
            print(f"      {line}")
        if len(codice.split('\n')) > 5:
            num_righe = len(codice.split('\n')) - 5
            print(f"      ... ({num_righe} righe in più)")
        print()
    
    # 4. Istruzioni uso reale
    print("=" * 70)
    print("🚀 COME USARE IL RICONOSCIMENTO VOCALE REALE")
    print("=" * 70)
    print("""
1. Avvia la GUI:
   python gui_robot_3d.py

2. Clicca sul pulsante: 🎤 Registra

3. Parla chiaramente uno dei comandi:
   • "apri mano"
   • "chiudi pugno"
   • "afferra mela"
   • "accendi led pin 13"
   • "stampa ciao"

4. Il testo verrà riconosciuto automaticamente

5. Il codice Python verrà generato dall'AI

6. Premi "Genera Codice" per vedere il risultato!

📖 Guida completa: VOICE_AND_ARDUINO_GUIDE.md
""")
    
    print("=" * 70)
    print("✅ TEST COMPLETATO CON SUCCESSO!")
    print("=" * 70)


if __name__ == "__main__":
    test_complete_workflow()

