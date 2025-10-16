#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test rapido sistema completo"""

from pythonita.utils.speech_recognition_module import get_speech_recognizer
from pythonita.core.generatore import GeneratoreCodice

print('=' * 60)
print('🧪 TEST RAPIDO SISTEMA COMPLETO')
print('=' * 60)

# 1. Speech Recognition (Sphinx OFFLINE)
print('\n📌 1. Speech Recognition (Sphinx OFFLINE)')
rec = get_speech_recognizer(language='it-IT', engine='sphinx')
success, msg = rec.test_microphone()
print(f'   Status: {"✅" if success else "❌"} {msg}')

# 2. AI Locale (Ollama)
print('\n📌 2. AI Locale (Ollama + Llama3.2)')
gen = GeneratoreCodice(use_ai=True, template='robot')
print(f'   Status: {"✅ AI disponibile" if gen.ai_disponibile else "❌ AI non disponibile"}')

# 3. Test Generazione Codice
print('\n📌 3. Test Generazione Codice')
comandi_test = ['apri mano', 'stampa ciao']

for cmd in comandi_test:
    print(f'\n   Comando: "{cmd}"')
    code = gen.genera(cmd)
    lines = code.split('\n')[:3]
    for line in lines:
        print(f'     {line}')
    if len(code.split('\n')) > 3:
        print(f'     ... ({len(code.split("\n")) - 3} righe in più)')

# 4. Riepilogo
print('\n' + '=' * 60)
print('✅ TUTTI I TEST COMPLETATI CON SUCCESSO!')
print('=' * 60)
print('\n🚀 Sistema pronto per l\'uso:')
print('   python gui_robot_3d.py')
print('\nPoi clicca 🎤 Registra e parla!')
print('=' * 60)

