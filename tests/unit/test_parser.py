"""
Test per il modulo parser.
"""

import pytest
from core.parser import ParserItaliano, get_parser, analizza_frase


class TestParserItaliano:
    """Test per la classe ParserItaliano."""
    
    def test_inizializzazione(self, parser):
        """Test inizializzazione parser."""
        assert parser is not None
    
    def test_analizza_semplice_frase_base(self, parser):
        """Test analisi semplice con frase base."""
        risultato = parser.analizza_semplice("stampa ciao")
        
        assert risultato['testo'] == "stampa ciao"
        assert risultato['verbo'] == "stampa"
        assert 'ciao' in risultato['args']
        assert len(risultato['parole']) == 2
    
    def test_analizza_semplice_frase_vuota(self, parser):
        """Test con frase vuota."""
        risultato = parser.analizza_semplice("")
        
        assert risultato['testo'] == ""
        assert risultato['verbo'] == ""
        assert risultato['args'] == []
    
    def test_estrai_numeri(self, parser):
        """Test estrazione numeri."""
        # Con numeri
        numeri = parser.estrai_numeri("somma 5 e 10")
        assert 5 in numeri
        assert 10 in numeri
        
        # Senza numeri
        numeri = parser.estrai_numeri("stampa ciao")
        assert numeri == []
    
    def test_estrai_numeri_multipli(self, parser):
        """Test con più numeri."""
        numeri = parser.estrai_numeri("lista con 1 2 3 4 5")
        assert len(numeri) == 5
        assert numeri == [1, 2, 3, 4, 5]


class TestGetParser:
    """Test per la funzione get_parser (singleton)."""
    
    def test_singleton(self):
        """Test pattern singleton."""
        parser1 = get_parser()
        parser2 = get_parser()
        
        assert parser1 is parser2


class TestAnalizzaFrase:
    """Test per la funzione helper analizza_frase."""
    
    def test_funzione_base(self):
        """Test funzionamento base."""
        risultato = analizza_frase("stampa test")
        
        assert 'verbo' in risultato
        assert 'args' in risultato
        assert risultato['verbo'] == "stampa"


@pytest.mark.parametrize("frase,verbo_atteso,num_args", [
    ("stampa ciao", "stampa", 1),
    ("somma 1 e 2", "somma", 3),
    ("crea lista", "crea", 1),
    ("", "", 0),
    ("test", "test", 0),
])
def test_parser_parametrizzato(frase, verbo_atteso, num_args):
    """Test parametrizzato per varie frasi."""
    parser = get_parser()
    risultato = parser.analizza_semplice(frase)
    
    assert risultato['verbo'] == verbo_atteso
    assert len(risultato['args']) == num_args

