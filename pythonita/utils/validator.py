"""Input validation per sicurezza."""

from dataclasses import dataclass
import re


@dataclass
class ValidationResult:
    """Risultato validazione input."""
    is_valid: bool
    message: str
    sanitized_input: str


class InputValidator:
    """Validatore input - Protegge da DoS e code injection."""
    
    MIN_LENGTH = 3
    MAX_LENGTH = 500
    
    DANGEROUS_PATTERNS = [
        r'__import__',
        r'eval\s*\(',
        r'exec\s*\(',
        r'os\.system',
        r'subprocess\.',
        r'open\s*\(',
        r'__\w+__',
    ]
    
    @staticmethod
    def validate(text: str) -> ValidationResult:
        """
        Valida input utente.
        
        Returns:
            ValidationResult con dettagli
        """
        # Check lunghezza
        if len(text) < InputValidator.MIN_LENGTH:
            return ValidationResult(
                False, 
                f"Input troppo corto (min {InputValidator.MIN_LENGTH} caratteri)",
                text
            )
        
        if len(text) > InputValidator.MAX_LENGTH:
            return ValidationResult(
                False,
                f"Input troppo lungo (max {InputValidator.MAX_LENGTH} caratteri)",
                text[:InputValidator.MAX_LENGTH]
            )
        
        # Check pattern pericolosi
        for pattern in InputValidator.DANGEROUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return ValidationResult(
                    False,
                    f"Pattern pericoloso rilevato: {pattern}",
                    text
                )
        
        # Sanitizza
        sanitized = InputValidator._sanitize(text)
        
        return ValidationResult(True, "Input valido", sanitized)
    
    @staticmethod
    def _sanitize(text: str) -> str:
        """Rimuove caratteri non-stampabili."""
        return ''.join(c for c in text if c.isprintable() or c.isspace())


def validate_input(text: str) -> ValidationResult:
    """Helper rapido per validazione."""
    return InputValidator.validate(text)

