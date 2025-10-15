"""
Configurazione centralizzata per Pythonita.
"""

import os
from pathlib import Path


class Config:
    """Configurazione dell'applicazione."""
    
    # Directory base
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    FUNZIONI_SALVATE_DIR = DATA_DIR / "funzioni_salvate"
    
    # File di dati
    FRASI_CSV = BASE_DIR / "frasi.csv"
    SINONIMI_JSON = BASE_DIR / "sinonimi.json"
    OUTPUT_FILE = BASE_DIR / "output.py"
    
    # Configurazione AI
    AI_ENABLED = True
    AI_MODEL = "llama3.2"
    AI_FALLBACK_TO_RULES = True
    
    # Configurazione NLP
    SPACY_MODEL = "it_core_news_sm"
    
    # Logging
    LOG_LEVEL = os.getenv("PYTHONITA_LOG_LEVEL", "INFO")
    
    # GUI
    GUI_TITLE = "Pythonita IA 🇮🇹"
    GUI_INPUT_HEIGHT = 10
    GUI_OUTPUT_HEIGHT = 10
    GUI_WIDTH = 40
    
    @classmethod
    def assicura_directories(cls):
        """Crea le directory necessarie se non esistono."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.FUNZIONI_SALVATE_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def get_ai_config(cls) -> dict:
        """Ritorna configurazione AI."""
        return {
            "enabled": cls.AI_ENABLED,
            "model": cls.AI_MODEL,
            "fallback": cls.AI_FALLBACK_TO_RULES
        }
    
    @classmethod
    def get_nlp_config(cls) -> dict:
        """Ritorna configurazione NLP."""
        return {
            "model": cls.SPACY_MODEL
        }


# Assicura che le directory esistano all'import
Config.assicura_directories()

