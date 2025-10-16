"""Configurazione centralizzata."""

from pathlib import Path
import json


class Config:
    """Configurazione applicazione - Singleton."""
    
    _instance = None
    
    def __init__(self):
        self.app_name = "Pythonita IA"
        self.version = "3.1.0"
        self.app_dir = Path.home() / ".pythonita"
        self.cache_file = self.app_dir / "cache.json"
        self.license_file = self.app_dir / "license.json"
        self.log_file = self.app_dir / "pythonita.log"
        
        # Crea directory se non esiste
        self.app_dir.mkdir(parents=True, exist_ok=True)
        
        # Settings
        self.use_ai = True
        self.use_cache = True
        self.cache_size = 100
        self.ai_timeout = 10  # secondi
        self.ollama_url = "http://127.0.0.1:11434"
        self.ollama_model = "llama3.2"
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def save(self):
        """Salva configurazione su disco."""
        config_file = self.app_dir / "config.json"
        data = {
            "use_ai": self.use_ai,
            "use_cache": self.use_cache,
            "cache_size": self.cache_size,
        }
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self):
        """Carica configurazione da disco."""
        config_file = self.app_dir / "config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                self.use_ai = data.get("use_ai", True)
                self.use_cache = data.get("use_cache", True)
                self.cache_size = data.get("cache_size", 100)
            except:
                pass  # Use defaults

