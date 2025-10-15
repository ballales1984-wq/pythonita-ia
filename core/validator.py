"""
Validazione e sanitizzazione input utente per Pythonita IA.
Previene DoS, code injection, e input malformati.
"""

import re
from typing import Union
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Risultato validazione input."""
    is_valid: bool
    message: str
    sanitized_input: str = ""


class InputValidator:
    """
    Validatore input per Pythonita IA.
    
    Controlla:
    - Tipo (deve essere stringa)
    - Lunghezza (max 1000 caratteri)
    - Numero parole (max 50)
    - Pattern pericolosi (injection, eval, etc)
    - Sanitizza spazi e caratteri di controllo
    """
    
    # Configurazione limiti
    MAX_LENGTH = 1000  # caratteri
    MIN_LENGTH = 1
    MAX_WORDS = 50
    
    # Pattern pericolosi da bloccare
    DANGEROUS_PATTERNS = [
        r'__import__',           # Import dinamici
        r'eval\s*\(',            # Eval
        r'exec\s*\(',            # Exec
        r'compile\s*\(',         # Compile
        r'os\.system',           # System calls
        r'subprocess',           # Subprocess
        r'open\s*\([^)]*["\']w', # Scrittura file
        r'__\w+__',              # Dunder methods
        r'globals\s*\(',         # Globals
        r'locals\s*\(',          # Locals
        r'vars\s*\(',            # Vars
        r'dir\s*\(',             # Dir
        r'delattr',              # Delete attributes
        r'setattr',              # Set attributes
        r'getattr',              # Get attributes
    ]
    
    def __init__(self):
        """Inizializza il validator."""
        # Compila pattern pericolosi in regex unica
        self.dangerous_regex = re.compile(
            '|'.join(self.DANGEROUS_PATTERNS),
            re.IGNORECASE
        )
    
    def validate(self, input_text: Union[str, None]) -> ValidationResult:
        """
        Valida input utente.
        
        Args:
            input_text: Input da validare
            
        Returns:
            ValidationResult con esito, messaggio e input sanitizzato
        """
        # 1. Controllo tipo
        if input_text is None:
            return ValidationResult(
                is_valid=False,
                message="Input non può essere None"
            )
        
        if not isinstance(input_text, str):
            return ValidationResult(
                is_valid=False,
                message=f"Input deve essere stringa, ricevuto {type(input_text).__name__}"
            )
        
        # 2. Controllo lunghezza minima
        if len(input_text) < self.MIN_LENGTH:
            return ValidationResult(
                is_valid=False,
                message="Input troppo corto (minimo 1 carattere)"
            )
        
        # 3. Controllo lunghezza massima
        if len(input_text) > self.MAX_LENGTH:
            return ValidationResult(
                is_valid=False,
                message=f"Input troppo lungo: {len(input_text)} caratteri (max {self.MAX_LENGTH})"
            )
        
        # 4. Controllo numero parole
        words = input_text.split()
        if len(words) > self.MAX_WORDS:
            return ValidationResult(
                is_valid=False,
                message=f"Troppe parole: {len(words)} (max {self.MAX_WORDS})"
            )
        
        # 5. Controllo pattern pericolosi
        if self.dangerous_regex.search(input_text):
            match = self.dangerous_regex.search(input_text)
            return ValidationResult(
                is_valid=False,
                message=f"Input contiene pattern potenzialmente pericoloso: {match.group()}"
            )
        
        # 6. Sanitizzazione
        sanitized = self._sanitize(input_text)
        
        # 7. Verifica che dopo sanitizzazione non sia vuoto
        if not sanitized:
            return ValidationResult(
                is_valid=False,
                message="Input vuoto dopo sanitizzazione"
            )
        
        return ValidationResult(
            is_valid=True,
            message="Input valido",
            sanitized_input=sanitized
        )
    
    def _sanitize(self, text: str) -> str:
        """
        Sanitizza input.
        
        Operazioni:
        - Rimuove spazi multipli
        - Rimuove caratteri di controllo
        - Trim spazi iniziali/finali
        
        Args:
            text: Testo da sanitizzare
            
        Returns:
            Testo sanitizzato
        """
        # Rimuovi caratteri di controllo (ma mantieni spazi/newline)
        text = ''.join(
            char for char in text 
            if char.isprintable() or char.isspace()
        )
        
        # Rimuovi spazi multipli
        text = re.sub(r'\s+', ' ', text)
        
        # Trim
        text = text.strip()
        
        return text
    
    def validate_and_sanitize(self, input_text: Union[str, None]) -> tuple[bool, str, str]:
        """
        Valida e sanitizza in un colpo solo.
        
        Args:
            input_text: Input da validare
            
        Returns:
            Tupla (is_valid, message, sanitized_input)
        """
        result = self.validate(input_text)
        return result.is_valid, result.message, result.sanitized_input


# Istanza singleton globale
_validator: Union[InputValidator, None] = None


def get_validator() -> InputValidator:
    """
    Ottieni istanza globale del validator (singleton).
    
    Returns:
        Istanza condivisa di InputValidator
    """
    global _validator
    if _validator is None:
        _validator = InputValidator()
    return _validator


def validate_input(text: Union[str, None]) -> ValidationResult:
    """
    Helper function per validazione rapida.
    
    Args:
        text: Testo da validare
        
    Returns:
        ValidationResult con esito validazione
    """
    return get_validator().validate(text)

