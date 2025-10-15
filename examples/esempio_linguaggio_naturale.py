"""
Demo: Analisi Linguistica Avanzata - Pythonita v3.0
Mostra come Pythonita analizza strutture linguistiche complete.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.linguaggio_naturale import analizza_linguaggio

print('='*70)
print('DEMO: Analisi Linguistica - Pythonita v3.0')
print('='*70)

# Frasi di esempio con varie strutture
frasi_test = [
    # Soggetto-Verbo-Complemento
    "il robot muove la mano destra",
    "la mano afferra l'oggetto",
    "il braccio solleva il peso",
    
    # Interrogativi
    "quando il robot muove la mano",
    "come funziona il sensore",
    "dove si trova l'oggetto",
    "chi controlla il robot",
    "perche' la mano si chiude",
    
    # Imperativi
    "muovi la mano",
    "afferra l'oggetto",
    "alza il braccio",
    
    # Comandi complessi
    "il robot deve afferrare l'oggetto quando rileva la presenza",
]

for i, frase in enumerate(frasi_test, 1):
    print(f'\n{"="*70}')
    print(f'[ANALISI {i}]')
    print(f'{"="*70}')
    print(f'Frase: "{frase}"')
    
    # Analizza
    struttura = analizza_linguaggio(frase)
    
    print(f'\nSTRUTTURA LINGUISTICA:')
    print(f'  Soggetto:    {struttura.soggetto}')
    print(f'  Verbo:       {struttura.verbo}')
    print(f'  Complemento: {struttura.complemento_oggetto}')
    print(f'  Interrogativo: {struttura.interrogativo}')
    print(f'  Modalita:    {struttura.modalita}')
    print(f'  Tempo:       {struttura.tempo_verbale}')
    
    if struttura.complementi:
        print(f'  Complementi: {", ".join(struttura.complementi)}')

print(f'\n{"="*70}')
print('ANALISI LINGUISTICA COMPLETA!')
print('='*70)

print('''
ELEMENTI RICONOSCIUTI:
- Soggetto (chi fa l'azione)
- Verbo (l'azione)
- Complemento oggetto (su cosa)
- Interrogativi: chi, cosa, quando, dove, come, perche'
- Tempo verbale: presente, passato, futuro
- Modalita': imperativo, indicativo, condizionale

QUESTO AIUTA L'AI A CAPIRE MEGLIO IL CONTESTO!
''')

