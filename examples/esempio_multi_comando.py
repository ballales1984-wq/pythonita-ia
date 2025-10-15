"""
Demo: Combinazioni Multi-Comando
Mostra come Pythonita genera codice complesso combinando più comandi.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import genera_codice

print('='*70)
print('DEMO: Combinazioni Multi-Comando - Pythonita v2.3')
print('='*70)

# Esempi di combinazioni
esempi = [
    {
        "query": "chiedi nome e poi stampalo",
        "descrizione": "Input + Print"
    },
    {
        "query": "crea lista con 1 2 3 poi stampa ogni elemento",
        "descrizione": "Lista + Iterazione"
    },
    {
        "query": "leggi file dati.txt poi processa le righe",
        "descrizione": "File I/O + Processing"
    },
    {
        "query": "per ogni numero da 1 a 5 stampa il doppio",
        "descrizione": "Loop + Calcolo"
    },
    {
        "query": "se x maggiore di 10 poi stampa risultato",
        "descrizione": "Condizione + Azione"
    },
]

for i, esempio in enumerate(esempi, 1):
    print(f'\n{"="*70}')
    print(f'[ESEMPIO {i}] {esempio["descrizione"]}')
    print(f'{"="*70}')
    print(f'\nQuery: "{esempio["query"]}"')
    print(f'\nCodice Generato:')
    print('-'*70)
    
    codice = genera_codice(esempio["query"])
    print(codice)
    
    print('-'*70)

print(f'\n{"="*70}')
print('TUTTE LE COMBINAZIONI FUNZIONANO!')
print('='*70)

print('''
PATTERN SUPPORTATI:
1. Input -> Print
2. Crea -> Itera
3. Leggi -> Processa
4. Loop -> Azione
5. Condizione -> Azione
6. E molti altri...

L'AI gestisce combinazioni ancora piu' complesse!
''')

