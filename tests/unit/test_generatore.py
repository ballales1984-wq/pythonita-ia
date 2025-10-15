"""
Test per il modulo generatore.
"""

import pytest
from core.generatore import GeneratoreCodice, get_generatore, genera_codice


class TestGeneratoreCodice:
    """Test per la classe GeneratoreCodice."""
    
    def test_inizializzazione(self, generatore_senza_ai):
        """Test inizializzazione."""
        assert generatore_senza_ai is not None
        assert generatore_senza_ai.use_ai is False
        assert generatore_senza_ai.use_fallback is True
    
    def test_genera_print(self, generatore_senza_ai):
        """Test generazione comando print."""
        codice = generatore_senza_ai.genera("stampa ciao mondo")
        
        assert 'print' in codice
        assert 'ciao mondo' in codice or 'ciao' in codice
        assert not codice.startswith("# Errore")
    
    def test_genera_somma(self, generatore_senza_ai):
        """Test generazione somma."""
        codice = generatore_senza_ai.genera("somma 5 e 3")
        
        assert 'print' in codice or '5' in codice
        assert not codice.startswith("# Errore")
    
    def test_genera_frase_vuota(self, generatore_senza_ai):
        """Test con frase vuota."""
        codice = generatore_senza_ai.genera("")
        
        assert codice.startswith("# Errore")
    
    def test_identifica_comando_print(self, generatore_senza_ai):
        """Test identificazione comando print."""
        comando = generatore_senza_ai._identifica_comando("stampa ciao")
        assert comando == "print"
    
    def test_identifica_comando_somma(self, generatore_senza_ai):
        """Test identificazione comando somma."""
        comando = generatore_senza_ai._identifica_comando("somma 1 2")
        assert comando == "+"
    
    def test_identifica_comando_lista(self, generatore_senza_ai):
        """Test identificazione comando lista."""
        # Usa parola "lista" invece di "crea" per evitare match con "def"
        comando = generatore_senza_ai._identifica_comando("lista numeri")
        assert comando == "list"
    
    def test_identifica_comando_sconosciuto(self, generatore_senza_ai):
        """Test comando non riconosciuto."""
        # Usa parole che non matchano nessun comando
        comando = generatore_senza_ai._identifica_comando("xyz qwerty asdfgh")
        assert comando is None


class TestCacheIntegration:
    """Test integrazione cache nel generatore."""
    
    def test_genera_con_cache_hit(self, generatore_con_cache):
        """Test cache hit."""
        # Prima generazione
        code1 = generatore_con_cache.genera("stampa test cache")
        
        # Seconda generazione (dovrebbe usare cache)
        code2 = generatore_con_cache.genera("stampa test cache")
        
        # Stesso codice
        assert code1 == code2
        
        # Verifica cache
        assert generatore_con_cache.cache.hits >= 1
    
    def test_cache_statistiche(self, generatore_con_cache):
        """Test statistiche cache."""
        # Genera alcune query
        generatore_con_cache.genera("stampa test1")
        generatore_con_cache.genera("stampa test1")  # Cache hit
        generatore_con_cache.genera("stampa test2")
        
        stats = generatore_con_cache.cache.stats()
        
        assert stats['total_queries'] >= 3
        assert stats['hits'] >= 1


class TestGetGeneratore:
    """Test per la funzione get_generatore (singleton)."""
    
    def test_singleton(self):
        """Test pattern singleton."""
        gen1 = get_generatore()
        gen2 = get_generatore()
        
        assert gen1 is gen2


class TestGeneraCodiceFunction:
    """Test per la funzione helper genera_codice."""
    
    def test_function_works(self):
        """Test funzionamento base."""
        # Nota: usa AI se disponibile, quindi può variare
        codice = genera_codice("stampa test")
        
        assert codice is not None
        assert len(codice) > 0


@pytest.mark.parametrize("comando,frase,parola_attesa", [
    ("print", "stampa hello", "print"),
    ("+", "somma 10 20", "+"),
    ("list", "crea lista con 1 2 3", "lista"),
    ("for", "crea un ciclo", "for"),
    ("if", "se condizione", "if"),
])
def test_applicazione_regole(generatore_senza_ai, comando, frase, parola_attesa):
    """Test parametrizzato per varie regole."""
    codice = generatore_senza_ai._applica_regola(comando, frase)
    assert parola_attesa in codice.lower()

