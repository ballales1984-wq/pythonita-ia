#!/usr/bin/env python3
"""
Test rapido per verificare generazione codice manuale.
"""

from pythonita.core.generatore import GeneratoreCodice

print("=== TEST GENERAZIONE MANUALE ===\n")

# Test 1: Generatore base
print("1. Test generatore base...")
gen = GeneratoreCodice(use_ai=True, use_cache=True)
print(f"   AI disponibile: {gen.ai_disponibile}")

# Test 2: Genera codice semplice
print("\n2. Test comando semplice...")
codice1 = gen.genera("apri mano")
print(f"   Input: 'apri mano'")
print(f"   Output ({len(codice1)} caratteri):")
print(f"   {codice1[:100]}...")

# Test 3: Genera codice complesso con AI
print("\n3. Test comando complesso con AI...")
codice2 = gen.genera("calcola triangolo isoscele 4 4")
print(f"   Input: 'calcola triangolo isoscele 4 4'")
print(f"   Output ({len(codice2)} caratteri):")
print(f"   {codice2[:150]}...")

# Test 4: Verifica che non sia vuoto
print("\n4. Verifica output...")
if codice1 and len(codice1) > 10:
    print("   ✅ Codice semplice OK")
else:
    print("   ❌ Codice semplice VUOTO")

if codice2 and len(codice2) > 10:
    print("   ✅ Codice complesso OK")
else:
    print("   ❌ Codice complesso VUOTO")

print("\n=== TEST COMPLETATO ===")

