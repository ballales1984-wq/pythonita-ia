"""
Core package di Pythonita.
Contiene i moduli fondamentali per il parsing e la generazione di codice.
"""

from .parser import ParserItaliano, get_parser, analizza_frase
from .generatore import GeneratoreCodice, get_generatore, genera_codice

__all__ = [
    "ParserItaliano",
    "get_parser",
    "analizza_frase",
    "GeneratoreCodice",
    "get_generatore",
    "genera_codice"
]

