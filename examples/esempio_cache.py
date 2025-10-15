"""
Esempio pratico: Sistema di Cache
Dimostra come la cache migliorerebbe drasticamente le performance.
"""

import time
from typing import Optional


# Simulazione SENZA cache
def genera_codice_senza_cache(frase: str) -> str:
    """Simula generazione senza cache."""
    print(f"[GENERA] Generando codice per: '{frase}'...")
    time.sleep(0.5)  # Simula latenza AI (in realtà 4-5s)
    return f'print("{frase}")'


# Simulazione CON cache
class SimpleCache:
    def __init__(self):
        self.cache = {}
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[str]:
        if key in self.cache:
            self.hits += 1
            print(f"[CACHE] HIT! Recuperato da cache")
            return self.cache[key]
        self.misses += 1
        print(f"[CACHE] MISS. Non in cache")
        return None
    
    def set(self, key: str, value: str):
        self.cache[key] = value
        print(f"[CACHE] Salvato in cache")


cache = SimpleCache()


def genera_codice_con_cache(frase: str) -> str:
    """Simula generazione con cache."""
    # Controlla cache
    cached = cache.get(frase)
    if cached:
        return cached
    
    # Genera
    print(f"[GENERA] Generando codice per: '{frase}'...")
    time.sleep(0.5)  # Simula latenza
    codice = f'print("{frase}")'
    
    # Salva in cache
    cache.set(frase, codice)
    
    return codice


def demo():
    """Demo comparativa."""
    print("="*70)
    print("DEMO: Confronto Performance CON e SENZA Cache")
    print("="*70)
    
    # Test SENZA cache
    print("\n[SCENARIO 1] SENZA CACHE")
    print("-" * 70)
    
    queries = ["stampa ciao"] * 3
    
    start = time.time()
    for i, query in enumerate(queries, 1):
        print(f"\n[Query {i}]")
        codice = genera_codice_senza_cache(query)
        print(f"Risultato: {codice}")
    
    tempo_senza = time.time() - start
    print(f"\nTempo totale SENZA cache: {tempo_senza:.2f}s")
    
    # Test CON cache
    print("\n\n[SCENARIO 2] CON CACHE")
    print("-" * 70)
    
    start = time.time()
    for i, query in enumerate(queries, 1):
        print(f"\n[Query {i}]")
        codice = genera_codice_con_cache(query)
        print(f"Risultato: {codice}")
    
    tempo_con = time.time() - start
    print(f"\nTempo totale CON cache: {tempo_con:.2f}s")
    
    # Statistiche
    print("\n" + "="*70)
    print("[STATISTICHE CACHE]")
    print("="*70)
    print(f"Cache Hits: {cache.hits}")
    print(f"Cache Misses: {cache.misses}")
    print(f"Hit Rate: {cache.hits / (cache.hits + cache.misses) * 100:.1f}%")
    
    # Confronto
    print("\n" + "="*70)
    print("[CONFRONTO FINALE]")
    print("="*70)
    print(f"Tempo SENZA cache: {tempo_senza:.2f}s")
    print(f"Tempo CON cache:   {tempo_con:.2f}s")
    print(f"Risparmio:         {tempo_senza - tempo_con:.2f}s ({(1 - tempo_con/tempo_senza)*100:.0f}%)")
    print(f"\n*** La cache rende il sistema {tempo_senza/tempo_con:.1f}x piu' veloce! ***")


if __name__ == "__main__":
    demo()

