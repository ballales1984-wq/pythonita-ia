"""
Core business logic di Pythonita IA.
Parser NLP + Code Generator + AI Engine.
"""

from .nlp_parser import ItalianNLPParser, parse_italian
from .code_generator import CodeGenerator, generate_code
from .command_registry import CommandRegistry, get_command

__all__ = [
    'ItalianNLPParser',
    'parse_italian',
    'CodeGenerator',
    'generate_code',
    'CommandRegistry',
    'get_command',
]

