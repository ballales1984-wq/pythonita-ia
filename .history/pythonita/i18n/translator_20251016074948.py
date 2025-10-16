"""
Translator - Sistema di traduzione per interfaccia multilingua.
"""

import json
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class Translator:
    """Gestisce traduzioni interfaccia."""
    
    SUPPORTED_LANGUAGES = ['it', 'en']
    DEFAULT_LANGUAGE = 'it'
    
    def __init__(self):
        """Inizializza translator."""
        self.current_language = self.DEFAULT_LANGUAGE
        self.translations: Dict[str, Dict[str, str]] = {}
        self.preferences_file = Path.home() / '.pythonita' / 'language.txt'
        
        # Carica traduzioni
        self._load_translations()
        
        # Carica lingua salvata
        self._load_language_preference()
    
    def _load_translations(self):
        """Carica tutti i file di traduzione."""
        translations_dir = Path(__file__).parent / 'translations'
        
        for lang in self.SUPPORTED_LANGUAGES:
            trans_file = translations_dir / f'{lang}.json'
            if trans_file.exists():
                try:
                    with open(trans_file, 'r', encoding='utf-8') as f:
                        self.translations[lang] = json.load(f)
                    logger.info(f"Traduzioni caricate: {lang}")
                except Exception as e:
                    logger.error(f"Errore caricamento traduzioni {lang}: {e}")
                    self.translations[lang] = {}
            else:
                logger.warning(f"File traduzione non trovato: {trans_file}")
                self.translations[lang] = {}
    
    def _load_language_preference(self):
        """Carica lingua salvata dall'utente."""
        if self.preferences_file.exists():
            try:
                with open(self.preferences_file, 'r') as f:
                    lang = f.read().strip()
                    if lang in self.SUPPORTED_LANGUAGES:
                        self.current_language = lang
                        logger.info(f"Lingua caricata: {lang}")
            except Exception as e:
                logger.error(f"Errore caricamento preferenza lingua: {e}")
    
    def _save_language_preference(self):
        """Salva lingua corrente."""
        try:
            self.preferences_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.preferences_file, 'w') as f:
                f.write(self.current_language)
        except Exception as e:
            logger.error(f"Errore salvataggio preferenza lingua: {e}")
    
    def set_language(self, language: str):
        """
        Imposta lingua corrente.
        
        Args:
            language: Codice lingua ('it' o 'en')
        """
        if language not in self.SUPPORTED_LANGUAGES:
            logger.warning(f"Lingua non supportata: {language}")
            return
        
        self.current_language = language
        self._save_language_preference()
        logger.info(f"Lingua impostata: {language}")
    
    def get_language(self) -> str:
        """Ritorna lingua corrente."""
        return self.current_language
    
    def translate(self, key: str, **kwargs) -> str:
        """
        Traduci una chiave.
        
        Args:
            key: Chiave traduzione (es: "gui.button.generate")
            **kwargs: Variabili da sostituire nella traduzione
            
        Returns:
            Stringa tradotta
        """
        # Ottieni traduzione per lingua corrente
        trans = self.translations.get(self.current_language, {})
        text = trans.get(key, key)  # Se non trovata, usa la chiave stessa
        
        # Sostituisci variabili
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError as e:
                logger.warning(f"Variabile mancante in traduzione '{key}': {e}")
        
        return text
    
    def __call__(self, key: str, **kwargs) -> str:
        """Shortcut per translate()."""
        return self.translate(key, **kwargs)


# Singleton instance
_translator = None


def get_translator() -> Translator:
    """Ottiene istanza singleton translator."""
    global _translator
    if _translator is None:
        _translator = Translator()
    return _translator


def set_language(language: str):
    """Imposta lingua corrente."""
    get_translator().set_language(language)


def _(key: str, **kwargs) -> str:
    """
    Funzione shortcut per traduzioni.
    
    Usage:
        from pythonita.i18n import _
        print(_("gui.welcome"))
    """
    return get_translator().translate(key, **kwargs)

