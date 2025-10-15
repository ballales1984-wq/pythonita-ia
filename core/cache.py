"""
Sistema di cache per Pythonita IA.
Memorizza query e risposte per migliorare le performance.
"""

import json
import time
import hashlib
import logging
from typing import Dict, Optional, Tuple
from pathlib import Path
from collections import OrderedDict


class CacheManager:
    """
    Gestore cache intelligente con LRU e persistenza.
    
    Features:
    - LRU (Least Recently Used) eviction
    - Persistenza su disco
    - Statistiche hit/miss
    - TTL (Time To Live) configurabile
    """
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        """
        Inizializza il cache manager.
        
        Args:
            max_size: Numero massimo di elementi in cache (default: 1000)
            ttl_seconds: Time-to-live in secondi (default: 1 ora)
        """
        self.max_size = max_size
        self.ttl = ttl_seconds
        
        # OrderedDict per LRU automatico
        self.cache: OrderedDict[str, Tuple[str, float]] = OrderedDict()
        
        # Statistiche
        self.hits = 0
        self.misses = 0
        
        # Logging
        self.logger = logging.getLogger(__name__)
        
        # Setup percorso cache
        self.cache_dir = Path.home() / ".pythonita"
        self.cache_file = self.cache_dir / "cache.json"
        
        # Crea directory se non esiste
        self.cache_dir.mkdir(exist_ok=True)
        
        # Carica cache esistente
        self._load_from_disk()
        
        self.logger.info(f"Cache inizializzata: {len(self.cache)} elementi caricati")
    
    def _hash_query(self, frase: str) -> str:
        """
        Genera hash per la query (per chiave cache).
        
        Args:
            frase: Query dell'utente
            
        Returns:
            Hash MD5 della frase normalizzata
        """
        normalized = frase.lower().strip()
        return hashlib.md5(normalized.encode('utf-8')).hexdigest()
    
    def get(self, frase: str) -> Optional[str]:
        """
        Recupera codice dalla cache.
        
        Args:
            frase: Query dell'utente
            
        Returns:
            Codice cached o None se non trovato/expired
        """
        hash_key = self._hash_query(frase)
        
        if hash_key in self.cache:
            codice, timestamp = self.cache[hash_key]
            
            # Verifica TTL
            if time.time() - timestamp < self.ttl:
                # Sposta in fondo (LRU: più recente)
                self.cache.move_to_end(hash_key)
                self.hits += 1
                self.logger.debug(f"Cache HIT per: '{frase[:30]}...'")
                return codice
            else:
                # Expired, rimuovi
                del self.cache[hash_key]
                self.logger.debug(f"Cache EXPIRED per: '{frase[:30]}...'")
        
        self.misses += 1
        self.logger.debug(f"Cache MISS per: '{frase[:30]}...'")
        return None
    
    def set(self, frase: str, codice: str):
        """
        Salva codice in cache.
        
        Args:
            frase: Query dell'utente
            codice: Codice generato
        """
        hash_key = self._hash_query(frase)
        
        # Se già esiste, rimuovi (per re-inserire in fondo)
        if hash_key in self.cache:
            del self.cache[hash_key]
        
        # Se raggiunto limite, rimuovi il più vecchio (LRU)
        if len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            self.logger.debug(f"Cache piena: rimosso elemento più vecchio")
        
        # Aggiungi in fondo (più recente)
        self.cache[hash_key] = (codice, time.time())
        self.logger.debug(f"Cache SET per: '{frase[:30]}...'")
        
        # Salva su disco periodicamente (ogni 10 inserimenti)
        if len(self.cache) % 10 == 0:
            self._save_to_disk()
    
    def clear(self):
        """Pulisce tutta la cache."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        self._save_to_disk()
        self.logger.info("Cache completamente pulita")
    
    def stats(self) -> Dict:
        """
        Ritorna statistiche cache.
        
        Returns:
            Dizionario con statistiche dettagliate
        """
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "total_queries": total,
            "hit_rate": f"{hit_rate:.1f}%",
            "ttl_seconds": self.ttl
        }
    
    def _load_from_disk(self):
        """Carica cache da disco."""
        if not self.cache_file.exists():
            self.logger.debug("Nessuna cache su disco da caricare")
            return
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Ricostruisci OrderedDict
            for key, value in data.items():
                if isinstance(value, list) and len(value) == 2:
                    self.cache[key] = tuple(value)
            
            self.logger.info(f"Cache caricata da disco: {len(self.cache)} elementi")
            
        except Exception as e:
            self.logger.warning(f"Errore caricamento cache: {e}")
            self.cache.clear()
    
    def _save_to_disk(self):
        """Salva cache su disco."""
        try:
            # Converti OrderedDict a dict normale per JSON
            data = {k: list(v) for k, v in self.cache.items()}
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.debug(f"Cache salvata su disco: {len(self.cache)} elementi")
            
        except Exception as e:
            self.logger.warning(f"Errore salvataggio cache: {e}")
    
    def __del__(self):
        """Salva cache quando l'oggetto viene distrutto."""
        try:
            self._save_to_disk()
        except:
            pass


# Istanza singleton globale
_cache_manager: Optional[CacheManager] = None


def get_cache() -> CacheManager:
    """
    Ottieni istanza globale del cache manager (singleton).
    
    Returns:
        Istanza condivisa di CacheManager
    """
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager

