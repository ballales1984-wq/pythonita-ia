"""
Demo: Template Robot - Pythonita IA v3.0
Genera codice Python per controllare robot umanoidi e mani bioniche.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.generatore import GeneratoreCodice
from core.template_domini import get_sistema_template

print('='*70)
print('DEMO: Template Robotica - Pythonita v3.0')
print('='*70)

# ===== PARTE 1: ROBOT UMANOIDE =====
print('\n[PARTE 1] ROBOT UMANOIDE SENZA RUOTE')
print('-'*70)

# Crea generatore con template robot
gen_robot = GeneratoreCodice(use_ai=False, use_fallback=True, use_cache=False, template='robot')

print(f'\nTemplate attivo: {gen_robot.sistema_template.get_template_attivo()}')

comandi_robot = [
    "muovi mano destra",
    "afferra oggetto con mano sinistra",
    "alza braccio destro",
    "rilascia oggetto",
    "leggi sensore distanza",
]

for i, comando in enumerate(comandi_robot, 1):
    print(f'\n[Robot {i}] Comando: "{comando}"')
    print('Codice generato:')
    print('-'*70)
    codice = gen_robot.genera(comando)
    # Mostra prime 3 righe
    righe = codice.split('\n')[:5]
    for riga in righe:
        print(riga)
    print('... (continua)')
    print('-'*70)

# ===== PARTE 2: MANO BIONICA =====
print('\n\n[PARTE 2] MANO BIONICA / PROTESI')
print('-'*70)

# Cambia template
gen_robot.sistema_template.scegli_template('mano_bionica')
print(f'\nTemplate attivo: {gen_robot.sistema_template.get_template_attivo()}')

comandi_mano = [
    "chiudi pugno",
    "fai pinza con pollice e indice",
    "gesto ok",
]

for i, comando in enumerate(comandi_mano, 1):
    print(f'\n[Mano {i}] Comando: "{comando}"')
    print('Codice generato:')
    print('-'*70)
    codice = gen_robot.genera(comando)
    # Mostra prime 4 righe
    righe = codice.split('\n')[:6]
    for riga in righe:
        print(riga)
    print('... (continua)')
    print('-'*70)

# ===== RIEPILOGO =====
print('\n' + '='*70)
print('TEMPLATE ROBOTICA FUNZIONA!')
print('='*70)

print('''
TEMPLATE DISPONIBILI:
1. robot        - Robot umanoidi senza ruote
2. mano_bionica - Mani bioniche/protesi
3. generico     - Codice Python normale

COMANDI ROBOT:
- muovi mano destra/sinistra
- afferra oggetto
- rilascia oggetto
- alza/abbassa braccio
- leggi sensore

COMANDI MANO BIONICA:
- chiudi pugno
- apri mano
- fai pinza
- gesti: ok, pollice su, punta

USO:
gen = GeneratoreCodice(template='robot')
codice = gen.genera("afferra oggetto con mano destra")
''')

