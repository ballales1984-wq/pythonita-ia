"""Test robot con codice completo visibile"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.generatore import GeneratoreCodice

print('='*70)
print('CODICE COMPLETO GENERATO - Template Robot')
print('='*70)

# Crea generatore con template robot
gen = GeneratoreCodice(template='robot', use_ai=False, use_cache=False)

print('\n[ESEMPIO 1] AFFERRA OGGETTO')
print('='*70)
print('Comando: "afferra oggetto con mano destra"')
print('\nCODICE COMPLETO GENERATO:')
print('-'*70)
codice = gen.genera("afferra oggetto con mano destra")
print(codice)
print('-'*70)

print('\n\n[ESEMPIO 2] LEGGI SENSORE')
print('='*70)
print('Comando: "leggi sensore distanza"')
print('\nCODICE COMPLETO GENERATO:')
print('-'*70)
codice = gen.genera("leggi sensore distanza")
print(codice)
print('-'*70)

print('\n\n[ESEMPIO 3] ALZA BRACCIO')
print('='*70)
print('Comando: "alza braccio destro"')
print('\nCODICE COMPLETO GENERATO:')
print('-'*70)
codice = gen.genera("alza braccio destro")
print(codice)
print('-'*70)

# Ora con mano bionica
gen_mano = GeneratoreCodice(template='mano_bionica', use_ai=False, use_cache=False)

print('\n\n[ESEMPIO 4] MANO BIONICA - CHIUDI PUGNO')
print('='*70)
print('Comando: "chiudi pugno"')
print('\nCODICE COMPLETO GENERATO:')
print('-'*70)
codice = gen_mano.genera("chiudi pugno")
print(codice)
print('-'*70)

print('\n\n[ESEMPIO 5] MANO BIONICA - PINZA')
print('='*70)
print('Comando: "fai pinza con pollice e indice"')
print('\nCODICE COMPLETO GENERATO:')
print('-'*70)
codice = gen_mano.genera("fai pinza con pollice e indice")
print(codice)
print('-'*70)

print('\n\n' + '='*70)
print('QUESTI SONO I CODICI REALI GENERATI!')
print('Pronti per essere usati con hardware vero!')
print('='*70)

