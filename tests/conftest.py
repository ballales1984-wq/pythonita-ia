"""
Fixtures condivise per tutti i test di Pythonita IA.
"""

import pytest
from core.parser import ParserItaliano
from core.generatore import GeneratoreCodice
from core.cache import CacheManager
from core.validator import InputValidator


@pytest.fixture
def parser():
    """Fixture per il parser."""
    return ParserItaliano()


@pytest.fixture
def generatore_senza_ai():
    """Generatore con AI disabilitata per test deterministici."""
    return GeneratoreCodice(use_ai=False, use_fallback=True, use_cache=False)


@pytest.fixture
def generatore_con_cache():
    """Generatore con cache abilitata ma senza AI."""
    return GeneratoreCodice(use_ai=False, use_fallback=True, use_cache=True)


@pytest.fixture
def cache_manager():
    """Fixture per cache manager."""
    cache = CacheManager(max_size=100, ttl_seconds=3600)
    cache.clear()  # Pulisci prima di ogni test
    yield cache
    cache.clear()  # Pulisci dopo ogni test


@pytest.fixture
def validator():
    """Fixture per validator."""
    return InputValidator()


@pytest.fixture
def sample_queries():
    """Query di esempio per test."""
    return {
        'semplice': 'stampa ciao mondo',
        'matematica': 'somma 5 e 3',
        'ciclo': 'crea un ciclo da 1 a 5',
        'lista': 'crea una lista con 10 20 30',
        'vuota': '',
        'lunga': 'a' * 2000,
        'pericolosa': '__import__("os")',
    }


@pytest.fixture
def expected_outputs():
    """Output attesi per query di test."""
    return {
        'stampa ciao mondo': 'print("ciao mondo")',
        'somma 5 e 3': 'print(5 + 3)',
    }

