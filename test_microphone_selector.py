#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test selettore microfoni"""

import speech_recognition as sr

print('=' * 70)
print('🎤 TEST SELETTORE MICROFONI')
print('=' * 70)

# Ottieni lista completa
all_mics = sr.Microphone.list_microphone_names()
print(f'\n📊 Totale dispositivi audio: {len(all_mics)}')

# Filtra microfoni (non speaker)
mic_inputs = [(i, mic) for i, mic in enumerate(all_mics)
              if 'mic' in mic.lower() or 'audio' in mic.lower()]

print(f'🎙️  Microfoni di input: {len(mic_inputs)}')
print('\n📋 LISTA MICROFONI DISPONIBILI:')
print('-' * 70)

for i, mic in mic_inputs:
    # Evidenzia Realtek e M-Audio
    marker = ''
    if 'realtek' in mic.lower():
        marker = '  ← REALTEK'
    elif 'm-audio' in mic.lower() or 'm audio' in mic.lower():
        marker = '  ← M-AUDIO'
    elif 'iriun' in mic.lower():
        marker = '  ← IRIUN WEBCAM'
    
    print(f'  [{i:2d}] {mic}{marker}')

print('-' * 70)

# Suggerimenti
print('\n💡 SUGGERIMENTI:')
print('   - Realtek: Scheda audio integrata')
print('   - M-Audio: Scheda audio professionale (se presente)')
print('   - Iriun: Webcam con microfono')

print('\n✅ Nella GUI vedrai una tendina per scegliere!')
print('=' * 70)

