"""Sistema cache LRU per performance."""

from collections import OrderedDict
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """Cache LRU con persistenza disco - Singleton."""
    
    _instance = None
    
    def __init__(self, max_size=100, cache_file=None):
        self.max_size = max_size
        self.cache = OrderedDict()
        self.cache_file = cache_file or (Path.home() / ".pythonita" / "cache.json")
        self.hits = 0
        self.misses = 0
        
        self._load()
    
    @classmethod
    def get_instance(cls, **kwargs):
        if cls._instance is None:
            cls._instance = cls(**kwargs)
        return cls._instance
    
    def get(self, key: str):
        """Ottiene valore da cache."""
        if key in self.cache:
            # Move to end (LRU)
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, key: str, value: str):
        """Salva in cache."""
        if key in self.cache:
            del self.cache[key]
        
        self.cache[key] = value
        self.cache.move_to_end(key)
        
        # Evict se troppo grande
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
        
        # Auto-save ogni 10 modifiche
        if len(self.cache) % 10 == 0:
            self._save()
    
    def _load(self):
        """Carica cache da disco."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.cache = OrderedDict(data)
                logger.info(f"Cache caricata: {len(self.cache)} elementi")
            except:
                pass
    
    def _save(self):
        """Salva cache su disco."""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(dict(self.cache), f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"Errore salvataggio cache: {e}")
    
    def stats(self):
        """Statistiche cache."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "size": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%"
        }

