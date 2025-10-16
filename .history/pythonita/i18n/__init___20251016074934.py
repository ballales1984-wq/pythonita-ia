"""
Internationalization (i18n) - Sistema di localizzazione.
Supporta italiano e inglese.
"""

from .translator import Translator, get_translator, set_language, _

__all__ = ['Translator', 'get_translator', 'set_language', '_']

