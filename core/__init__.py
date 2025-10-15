"""
Core package di Pythonita.
Contiene i moduli fondamentali per il parsing e la generazione di codice.
"""

from .parser import ParserItaliano, get_parser, analizza_frase
from .generatore import GeneratoreCodice, get_generatore, genera_codice
from .cache import CacheManager, get_cache
from .validator import InputValidator, get_validator, validate_input, ValidationResult
from .comandi_python import (
    COMANDI_PYTHON,
    BUILTIN_FUNCTIONS,
    STANDARD_LIBRARY,
    find_command_by_italian,
    get_all_commands
)

__all__ = [
    "ParserItaliano",
    "get_parser",
    "analizza_frase",
    "GeneratoreCodice",
    "get_generatore",
    "genera_codice",
    "CacheManager",
    "get_cache",
    "InputValidator",
    "get_validator",
    "validate_input",
    "ValidationResult",
    "COMANDI_PYTHON",
    "BUILTIN_FUNCTIONS",
    "STANDARD_LIBRARY",
    "find_command_by_italian",
    "get_all_commands"
]

