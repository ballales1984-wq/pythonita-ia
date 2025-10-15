"""
Test per il modulo cache.
"""

import pytest
import time
from core.cache import CacheManager, get_cache


class TestCacheManager:
    """Test per la classe CacheManager."""
    
    def test_inizializzazione(self, cache_manager):
        """Test inizializzazione cache."""
        assert cache_manager is not None
        assert cache_manager.max_size == 100
        assert cache_manager.ttl == 3600
        assert len(cache_manager.cache) == 0
    
    def test_set_and_get(self, cache_manager):
        """Test salvataggio e recupero."""
        # Salva
        cache_manager.set("test query", "test code")
        
        # Recupera
        result = cache_manager.get("test query")
        
        assert result == "test code"
        assert cache_manager.hits == 1
        assert cache_manager.misses == 0
    
    def test_get_miss(self, cache_manager):
        """Test cache miss."""
        result = cache_manager.get("query non esistente")
        
        assert result is None
        assert cache_manager.hits == 0
        assert cache_manager.misses == 1
    
    def test_case_insensitive(self, cache_manager):
        """Test che la cache sia case-insensitive."""
        cache_manager.set("Stampa Test", "print('test')")
        
        # Recupera con diversa capitalizzazione
        result = cache_manager.get("stampa test")
        
        assert result == "print('test')"
    
    def test_max_size_lru(self):
        """Test che rispetti max_size con LRU."""
        cache = CacheManager(max_size=3, ttl_seconds=3600)
        cache.clear()
        
        # Aggiungi 4 elementi (max è 3)
        cache.set("query1", "code1")
        cache.set("query2", "code2")
        cache.set("query3", "code3")
        cache.set("query4", "code4")  # Questo dovrebbe rimuovere query1
        
        # Verifica dimensione
        assert len(cache.cache) == 3
        
        # Verifica che query1 sia stata rimossa (LRU)
        assert cache.get("query1") is None
        assert cache.get("query4") == "code4"
    
    def test_stats(self, cache_manager):
        """Test statistiche cache."""
        # Stato iniziale
        stats = cache_manager.stats()
        assert stats['size'] == 0
        assert stats['hits'] == 0
        assert stats['misses'] == 0
        
        # Dopo operazioni
        cache_manager.set("q1", "c1")
        cache_manager.get("q1")  # Hit
        cache_manager.get("q2")  # Miss
        
        stats = cache_manager.stats()
        assert stats['size'] == 1
        assert stats['hits'] == 1
        assert stats['misses'] == 1
        assert stats['hit_rate'] == '50.0%'
    
    def test_clear(self, cache_manager):
        """Test pulizia cache."""
        # Aggiungi elementi
        cache_manager.set("q1", "c1")
        cache_manager.set("q2", "c2")
        cache_manager.get("q1")
        
        # Pulisci
        cache_manager.clear()
        
        # Verifica
        assert len(cache_manager.cache) == 0
        assert cache_manager.hits == 0
        assert cache_manager.misses == 0
    
    def test_ttl_expiration(self):
        """Test che gli elementi scadano dopo TTL."""
        cache = CacheManager(max_size=100, ttl_seconds=1)  # 1 secondo TTL
        cache.clear()
        
        # Aggiungi elemento
        cache.set("query", "code")
        
        # Subito disponibile
        assert cache.get("query") == "code"
        
        # Aspetta scadenza
        time.sleep(1.1)
        
        # Ora dovrebbe essere None (expired)
        assert cache.get("query") is None


class TestGetCache:
    """Test per la funzione get_cache (singleton)."""
    
    def test_singleton(self):
        """Test pattern singleton."""
        cache1 = get_cache()
        cache2 = get_cache()
        
        # Stessa istanza
        assert cache1 is cache2
    
    def test_shared_state(self):
        """Test che lo stato sia condiviso."""
        cache1 = get_cache()
        cache2 = get_cache()
        
        cache1.set("shared", "value")
        
        # Disponibile anche da cache2
        assert cache2.get("shared") == "value"


@pytest.mark.parametrize("query,expected_in_cache", [
    ("stampa test", True),
    ("", False),  # Vuoto non dovrebbe essere cached
    ("query normale", True),
])
def test_cache_parametrizzato(cache_manager, query, expected_in_cache):
    """Test parametrizzato per varie query."""
    if expected_in_cache:
        cache_manager.set(query, f"code for {query}")
        result = cache_manager.get(query)
        assert result is not None
        assert f"code for {query}" in result

