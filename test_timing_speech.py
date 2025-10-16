#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test per misurare i tempi di inizializzazione del speech recognizer"""

import time
import speech_recognition as sr
from pythonita.utils.speech_recognition_module import get_speech_recognizer

print('=' * 70)
print('🕐 MISURAZIONE TEMPI SPEECH RECOGNITION')
print('=' * 70)

# Test 1: Inizializzazione recognizer
print('\n📌 Test 1: Tempo inizializzazione recognizer')
start = time.time()
rec = get_speech_recognizer(language='it-IT', engine='sphinx')
init_time = time.time() - start
print(f'   ⏱️  Tempo: {init_time:.3f} secondi')

# Test 2: Tempo apertura microfono
print('\n📌 Test 2: Tempo apertura microfono')
start = time.time()
with sr.Microphone() as source:
    pass
mic_time = time.time() - start
print(f'   ⏱️  Tempo: {mic_time:.3f} secondi')

# Test 3: Tempo calibrazione rumore
print('\n📌 Test 3: Tempo calibrazione rumore ambiente')
start = time.time()
with sr.Microphone() as source:
    rec.recognizer.adjust_for_ambient_noise(source, duration=0.5)
calibration_time = time.time() - start
print(f'   ⏱️  Tempo: {calibration_time:.3f} secondi')

# Test 4: Tempo totale prima che inizi ad ascoltare
print('\n📌 Test 4: Tempo TOTALE prima di ascoltare')
start_total = time.time()
with sr.Microphone() as source:
    print('   🎤 Calibrando...')
    rec.recognizer.adjust_for_ambient_noise(source, duration=0.5)
    print('   🎤 PRONTO AD ASCOLTARE!')
    ready_time = time.time() - start_total
    print(f'   ⏱️  Tempo totale: {ready_time:.3f} secondi')

# Riepilogo
print('\n' + '=' * 70)
print('📊 RIEPILOGO TEMPI')
print('=' * 70)
print(f'Inizializzazione recognizer: {init_time:.3f}s')
print(f'Apertura microfono:          {mic_time:.3f}s')
print(f'Calibrazione rumore:         {calibration_time:.3f}s')
print(f'TEMPO TOTALE PRIMA ASCOLTO:  {ready_time:.3f}s')
print('=' * 70)

print('\n💡 SOLUZIONE:')
print(f'   - Mostra "Calibrando..." per {ready_time:.1f} secondi')
print(f'   - Poi mostra "PARLA ORA!" quando è pronto')
print(f'   - Usa pulsante STOP per terminare')
print('=' * 70)

