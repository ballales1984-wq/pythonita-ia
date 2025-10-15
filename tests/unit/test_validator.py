"""
Test per il modulo validator.
"""

import pytest
from core.validator import InputValidator, validate_input, ValidationResult, get_validator


class TestInputValidator:
    """Test per la classe InputValidator."""
    
    def test_inizializzazione(self, validator):
        """Test inizializzazione validator."""
        assert validator is not None
        assert validator.MAX_LENGTH == 1000
        assert validator.MIN_LENGTH == 1
        assert validator.MAX_WORDS == 50
    
    def test_input_valido_semplice(self, validator):
        """Test con input valido semplice."""
        result = validator.validate("stampa ciao mondo")
        
        assert result.is_valid
        assert result.message == "Input valido"
        assert result.sanitized_input == "stampa ciao mondo"
    
    def test_input_none(self, validator):
        """Test con input None."""
        result = validator.validate(None)
        
        assert not result.is_valid
        assert "None" in result.message
    
    def test_input_tipo_errato(self, validator):
        """Test con tipo non stringa."""
        result = validator.validate(12345)
        
        assert not result.is_valid
        assert "stringa" in result.message.lower()
    
    def test_input_vuoto(self, validator):
        """Test con stringa vuota."""
        result = validator.validate("")
        
        assert not result.is_valid
        assert "corto" in result.message.lower()
    
    def test_input_troppo_lungo(self, validator):
        """Test con input troppo lungo."""
        long_input = "a" * 2000
        result = validator.validate(long_input)
        
        assert not result.is_valid
        assert "lungo" in result.message.lower()
        assert "2000" in result.message
    
    def test_troppe_parole(self, validator):
        """Test con troppe parole."""
        many_words = " ".join(["parola"] * 100)
        result = validator.validate(many_words)
        
        assert not result.is_valid
        assert "parole" in result.message.lower() or "Tropp" in result.message
    
    def test_pattern_pericolosi_import(self, validator):
        """Test blocco __import__."""
        result = validator.validate('__import__("os")')
        
        assert not result.is_valid
        assert "pericoloso" in result.message.lower()
    
    def test_pattern_pericolosi_eval(self, validator):
        """Test blocco eval."""
        result = validator.validate('eval("malicious")')
        
        assert not result.is_valid
        assert "pericoloso" in result.message.lower()
    
    def test_pattern_pericolosi_exec(self, validator):
        """Test blocco exec."""
        result = validator.validate('exec("bad code")')
        
        assert not result.is_valid
        assert "pericoloso" in result.message.lower()
    
    def test_sanitizzazione_spazi_multipli(self, validator):
        """Test sanitizzazione spazi multipli."""
        result = validator.validate("stampa    ciao    mondo")
        
        assert result.is_valid
        assert result.sanitized_input == "stampa ciao mondo"
    
    def test_sanitizzazione_trim(self, validator):
        """Test rimozione spazi iniziali/finali."""
        result = validator.validate("  stampa test  ")
        
        assert result.is_valid
        assert result.sanitized_input == "stampa test"
        assert not result.sanitized_input.startswith(" ")
        assert not result.sanitized_input.endswith(" ")
    
    def test_validate_and_sanitize(self, validator):
        """Test metodo combinato."""
        is_valid, message, sanitized = validator.validate_and_sanitize("  test  ")
        
        assert is_valid
        assert message == "Input valido"
        assert sanitized == "test"


class TestValidateInputFunction:
    """Test per la funzione helper validate_input."""
    
    def test_function_exists(self):
        """Test che la funzione sia importabile."""
        assert validate_input is not None
    
    def test_function_works(self):
        """Test funzionamento base."""
        result = validate_input("stampa test")
        
        assert isinstance(result, ValidationResult)
        assert result.is_valid
    
    def test_function_invalid_input(self):
        """Test con input invalido."""
        result = validate_input("")
        
        assert not result.is_valid


class TestGetValidator:
    """Test per la funzione get_validator (singleton)."""
    
    def test_singleton(self):
        """Test pattern singleton."""
        validator1 = get_validator()
        validator2 = get_validator()
        
        assert validator1 is validator2


@pytest.mark.parametrize("input_text,expected_valid", [
    ("stampa ciao", True),
    ("somma 5 e 3", True),
    ("crea lista", True),
    ("", False),
    (None, False),
    ("a" * 2000, False),
    ('__import__("os")', False),
    ('eval("x")', False),
    ("  spazi  multipli  ", True),  # Sanitizzato ma valido
])
def test_validator_parametrizzato(input_text, expected_valid):
    """Test parametrizzato con vari input."""
    result = validate_input(input_text)
    assert result.is_valid == expected_valid


class TestSecurityPatterns:
    """Test specifici per pattern di sicurezza."""
    
    @pytest.mark.parametrize("dangerous_input", [
        '__import__("os").system("rm -rf /")',
        'eval("malicious")',
        'exec("bad")',
        'compile("x", "file", "exec")',
        'os.system("cmd")',
        '__builtins__',
        'globals()',
        'locals()',
    ])
    def test_block_dangerous_patterns(self, validator, dangerous_input):
        """Test che tutti i pattern pericolosi siano bloccati."""
        result = validator.validate(dangerous_input)
        assert not result.is_valid
        assert "pericoloso" in result.message.lower()

