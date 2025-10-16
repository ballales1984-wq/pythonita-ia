"""
Test per il sistema multi-comando.
"""

import pytest
from pythonita.core.multi_comando import MultiComandoParser, CombinatoreCodice, combina_comandi


class TestMultiComandoParser:
    """Test per MultiComandoParser."""
    
    @pytest.fixture
    def parser(self):
        return MultiComandoParser()
    
    def test_identifica_multi_comando_con_poi(self, parser):
        """Test identificazione con 'poi'."""
        assert parser.identifica_multi_comando("crea lista poi stampa")
    
    def test_identifica_multi_comando_con_dopo(self, parser):
        """Test identificazione con 'dopo'."""
        assert parser.identifica_multi_comando("leggi file dopo processalo")
    
    def test_identifica_multi_comando_con_e(self, parser):
        """Test identificazione con 'e'."""
        assert parser.identifica_multi_comando("chiedi nome e poi stampalo")
    
    def test_non_multi_comando(self, parser):
        """Test con comando singolo."""
        assert not parser.identifica_multi_comando("stampa ciao")
    
    def test_separa_comandi_con_poi(self, parser):
        """Test separazione comandi."""
        comandi = parser.separa_comandi("crea lista poi stampa")
        
        assert len(comandi) == 2
        assert "crea lista" in comandi
        assert "stampa" in comandi
    
    def test_separa_comandi_multipli(self, parser):
        """Test con più di 2 comandi."""
        comandi = parser.separa_comandi("crea lista poi ordina poi stampa")
        
        assert len(comandi) >= 2
    
    def test_analizza_struttura(self, parser):
        """Test analisi struttura completa."""
        analisi = parser.analizza_struttura("chiedi nome e poi stampalo")
        
        assert analisi['è_multi_comando']
        assert 'pattern' in analisi
        assert analisi['numero_comandi'] >= 1
    
    def test_identifica_pattern_input_print(self, parser):
        """Test identificazione pattern input_then_print."""
        pattern = parser._identifica_pattern("chiedi nome poi stampalo")
        assert pattern == "input_then_print"
    
    def test_identifica_pattern_loop_action(self, parser):
        """Test identificazione pattern loop_with_action."""
        pattern = parser._identifica_pattern("per ogni elemento stampa valore")
        assert pattern == "loop_with_action"


class TestCombinatoreCodice:
    """Test per CombinatoreCodice."""
    
    @pytest.fixture
    def combinatore(self):
        return CombinatoreCodice()
    
    def test_combina_vuoto(self, combinatore):
        """Test con lista vuota."""
        risultato = combinatore.combina([])
        assert "Nessun codice" in risultato
    
    def test_combina_singolo(self, combinatore):
        """Test con singolo codice."""
        risultato = combinatore.combina(['print("test")'])
        assert risultato == 'print("test")'
    
    def test_combina_multipli(self, combinatore):
        """Test combinazione multipla."""
        codici = [
            'lista = [1, 2, 3]',
            'print(lista)'
        ]
        
        risultato = combinatore.combina(codici)
        
        assert 'lista = [1, 2, 3]' in risultato
        assert 'print(lista)' in risultato
    
    def test_template_input_print(self, combinatore):
        """Test template input_then_print."""
        codice = combinatore.genera_da_template("input_then_print", "chiedi nome poi stampalo")
        
        assert 'input' in codice
        assert 'print' in codice
    
    def test_template_create_iterate(self, combinatore):
        """Test template create_then_iterate."""
        codice = combinatore.genera_da_template("create_then_iterate", "crea lista poi itera")
        
        assert 'lista' in codice
        assert 'for' in codice
    
    def test_template_loop_action(self, combinatore):
        """Test template loop_with_action."""
        codice = combinatore.genera_da_template("loop_with_action", "per ogni elemento stampa")
        
        assert 'for' in codice or 'range' in codice


class TestCombinaComandiFunzione:
    """Test per la funzione helper combina_comandi."""
    
    def test_function_works(self):
        """Test funzionamento base."""
        codici = ['x = 10', 'print(x)']
        risultato = combina_comandi("test", codici)
        
        assert 'x = 10' in risultato
        assert 'print(x)' in risultato


@pytest.mark.parametrize("frase,contiene_parole", [
    ("chiedi nome poi stampalo", ["input", "print"]),
    ("crea lista poi itera", ["lista", "for"]),
    ("leggi file poi processa", ["open", "for"]),
])
def test_multi_comando_end_to_end(frase, contiene_parole):
    """Test end-to-end generazione multi-comando."""
    from core import genera_codice
    
    # Genera con AI se disponibile, altrimenti con regole
    codice = genera_codice(frase)
    
    # Verifica che contenga almeno una delle parole attese
    codice_lower = codice.lower()
    assert any(parola in codice_lower for parola in contiene_parole) or "def" in codice_lower

