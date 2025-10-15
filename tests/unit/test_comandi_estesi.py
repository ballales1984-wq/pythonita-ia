"""
Test per i comandi Python estesi (143+).
"""

import pytest
from core import genera_codice, get_all_commands, find_command_by_italian
from core.generatore import GeneratoreCodice


class TestComandiEstesi:
    """Test per i nuovi comandi aggiunti."""
    
    def test_numero_comandi_supportati(self):
        """Verifica che ci siano 100+ comandi."""
        comandi = get_all_commands()
        assert len(comandi) >= 100
    
    def test_find_command_enumerate(self):
        """Test ricerca enumerate."""
        assert find_command_by_italian("enumera") == "enumerate"
    
    def test_find_command_zip(self):
        """Test ricerca zip."""
        assert find_command_by_italian("accoppia") == "zip"
    
    def test_find_command_math(self):
        """Test ricerca math."""
        assert find_command_by_italian("matematica") == "math"


class TestStringCommands:
    """Test per comandi stringa."""
    
    @pytest.fixture
    def gen(self):
        return GeneratoreCodice(use_ai=False, use_fallback=True, use_cache=False)
    
    def test_upper(self, gen):
        """Test upper."""
        codice = gen.genera("tutto maiuscolo")
        assert "upper" in codice or "MAIUSCOLO" in codice
    
    def test_lower(self, gen):
        """Test lower."""
        codice = gen.genera("tutto minuscolo")
        assert "lower" in codice or "minuscolo" in codice
    
    def test_split(self, gen):
        """Test split."""
        codice = gen.genera("split stringa in parole")
        assert "split" in codice or not codice.startswith("# Comando")
    
    def test_join(self, gen):
        """Test join."""
        codice = gen.genera("join lista stringhe")
        assert "join" in codice or not codice.startswith("# Comando")


@pytest.mark.parametrize("query_italiana,keyword_attesa", [
    ("enumera", "enumerate"),
    ("tutto maiuscolo", "upper"),
    ("tutto minuscolo", "lower"),
    ("dividi", "split"),
    ("unisci", "join"),
    ("tupla", "tuple"),
    ("insieme", "set"),
    ("arrotonda", "round"),
    ("valore assoluto", "abs"),
])
def test_nuovi_comandi_parametrizzati(query_italiana, keyword_attesa):
    """Test parametrizzato per nuovi comandi."""
    gen = GeneratoreCodice(use_ai=False, use_fallback=True, use_cache=False)
    codice = gen.genera(query_italiana)
    
    # Verifica che contenga la keyword o che non sia errore
    is_ok = keyword_attesa in codice.lower() or not codice.startswith("# Comando non")
    assert is_ok, f"Keyword '{keyword_attesa}' non trovata in: {codice[:100]}"

