"""
Performance Optimizer per Visualizzatore 3D.
Implementa caching, object pooling e ottimizzazioni rendering.
"""

import numpy as np
from functools import lru_cache
from typing import Dict, List, Tuple, Optional
import time


class MeshCache:
    """
    Cache per mesh 3D pre-calcolate.
    Evita di rigenerare geometrie identiche.
    """
    
    def __init__(self, max_size=100):
        """Inizializza cache."""
        self.cache: Dict[str, Tuple] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Tuple]:
        """Recupera mesh da cache."""
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None
    
    def set(self, key: str, mesh: Tuple):
        """Salva mesh in cache."""
        # Evita crescita infinita
        if len(self.cache) >= self.max_size:
            # Rimuovi primo elemento (FIFO semplice)
            first_key = next(iter(self.cache))
            del self.cache[first_key]
        
        self.cache[key] = mesh
    
    def clear(self):
        """Svuota cache."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> Dict:
        """Statistiche cache."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'size': len(self.cache),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate
        }


class ObjectPool:
    """
    Pool di oggetti matplotlib riutilizzabili.
    Evita creazione/distruzione continua.
    """
    
    def __init__(self):
        """Inizializza pool."""
        self.surfaces = []
        self.collections = []
        self.texts = []
        self.active_surfaces = []
        self.active_collections = []
        self.active_texts = []
    
    def get_surface(self):
        """Ottiene una surface dal pool o ne crea una nuova."""
        if self.surfaces:
            surf = self.surfaces.pop()
            self.active_surfaces.append(surf)
            return surf
        # Pool vuoto, crea nuovo (lasciamo a matplotlib gestire)
        return None
    
    def return_surface(self, surf):
        """Restituisce surface al pool."""
        if surf in self.active_surfaces:
            self.active_surfaces.remove(surf)
            self.surfaces.append(surf)
    
    def reset(self):
        """Reset pool per nuovo frame."""
        # Tutti gli oggetti attivi tornano disponibili
        self.surfaces.extend(self.active_surfaces)
        self.collections.extend(self.active_collections)
        self.texts.extend(self.active_texts)
        
        self.active_surfaces.clear()
        self.active_collections.clear()
        self.active_texts.clear()


class PerformanceMonitor:
    """
    Monitora FPS e tempi di rendering.
    """
    
    def __init__(self, window_size=30):
        """
        Inizializza monitor.
        
        Args:
            window_size: Numero frame per calcolare FPS medio
        """
        self.window_size = window_size
        self.frame_times = []
        self.last_frame_time = time.time()
        self.total_frames = 0
        self.start_time = time.time()
    
    def start_frame(self):
        """Marca inizio frame."""
        self.last_frame_time = time.time()
    
    def end_frame(self):
        """Marca fine frame e calcola tempo."""
        now = time.time()
        frame_time = now - self.last_frame_time
        
        self.frame_times.append(frame_time)
        
        # Mantieni solo ultimi N frame
        if len(self.frame_times) > self.window_size:
            self.frame_times.pop(0)
        
        self.total_frames += 1
    
    def get_fps(self) -> float:
        """Calcola FPS medio."""
        if not self.frame_times:
            return 0.0
        
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        
        if avg_frame_time == 0:
            return 0.0
        
        return 1.0 / avg_frame_time
    
    def get_average_fps(self) -> float:
        """FPS medio dall'inizio."""
        elapsed = time.time() - self.start_time
        if elapsed == 0:
            return 0.0
        return self.total_frames / elapsed
    
    def get_stats(self) -> Dict:
        """Statistiche complete."""
        return {
            'fps_current': self.get_fps(),
            'fps_average': self.get_average_fps(),
            'total_frames': self.total_frames,
            'frame_time_avg': sum(self.frame_times) / len(self.frame_times) if self.frame_times else 0,
            'frame_time_min': min(self.frame_times) if self.frame_times else 0,
            'frame_time_max': max(self.frame_times) if self.frame_times else 0,
        }


class RenderingOptimizer:
    """
    Ottimizzatore rendering 3D.
    Implementa LOD, culling e adaptive quality.
    """
    
    def __init__(self):
        """Inizializza optimizer."""
        self.quality_level = 'high'  # high, medium, low
        self.target_fps = 30
        self.adaptive_quality = True
        
        # Livelli di dettaglio (LOD)
        self.lod_settings = {
            'high': {
                'sphere_resolution': 20,
                'antialiasing': True,
                'shadows': True,
                'max_vertices': 10000
            },
            'medium': {
                'sphere_resolution': 12,
                'antialiasing': True,
                'shadows': False,
                'max_vertices': 5000
            },
            'low': {
                'sphere_resolution': 8,
                'antialiasing': False,
                'shadows': False,
                'max_vertices': 2000
            }
        }
    
    def adjust_quality(self, current_fps: float):
        """
        Adatta qualità in base a FPS.
        
        Args:
            current_fps: FPS corrente
        """
        if not self.adaptive_quality:
            return
        
        # Se FPS troppo basso, riduci qualità
        if current_fps < self.target_fps * 0.8:  # < 24 FPS con target 30
            if self.quality_level == 'high':
                self.quality_level = 'medium'
                print("[OPTIMIZER] Qualità ridotta a MEDIUM")
            elif self.quality_level == 'medium':
                self.quality_level = 'low'
                print("[OPTIMIZER] Qualità ridotta a LOW")
        
        # Se FPS molto alto, aumenta qualità
        elif current_fps > self.target_fps * 1.5:  # > 45 FPS
            if self.quality_level == 'low':
                self.quality_level = 'medium'
                print("[OPTIMIZER] Qualità aumentata a MEDIUM")
            elif self.quality_level == 'medium':
                self.quality_level = 'high'
                print("[OPTIMIZER] Qualità aumentata a HIGH")
    
    def get_settings(self) -> Dict:
        """Ottiene settings correnti."""
        return self.lod_settings[self.quality_level]
    
    def should_render_object(self, distance: float, importance: float = 1.0) -> bool:
        """
        Frustum culling semplificato.
        
        Args:
            distance: Distanza oggetto da camera
            importance: Importanza oggetto (1.0 = sempre visibile)
            
        Returns:
            True se oggetto dovrebbe essere renderizzato
        """
        # Oggetti importanti sempre visibili
        if importance >= 1.0:
            return True
        
        # Culling basato su distanza e qualità
        max_distance = {
            'high': 100,
            'medium': 50,
            'low': 30
        }[self.quality_level]
        
        return distance <= max_distance


@lru_cache(maxsize=128)
def generate_sphere_mesh(resolution: int, radius: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Genera mesh sferica (cached).
    
    Args:
        resolution: Numero punti
        radius: Raggio sfera
        
    Returns:
        (X, Y, Z) coordinate mesh
    """
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    
    X = radius * np.outer(np.cos(u), np.sin(v))
    Y = radius * np.outer(np.sin(u), np.sin(v))
    Z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    return X, Y, Z


@lru_cache(maxsize=128)
def generate_cube_vertices(size: float) -> np.ndarray:
    """
    Genera vertici cubo (cached).
    
    Args:
        size: Dimensione lato
        
    Returns:
        Array vertici (8, 3)
    """
    s = size / 2
    vertices = np.array([
        [-s, -s, -s],
        [ s, -s, -s],
        [ s,  s, -s],
        [-s,  s, -s],
        [-s, -s,  s],
        [ s, -s,  s],
        [ s,  s,  s],
        [-s,  s,  s]
    ])
    return vertices


class PerformanceOptimizedVisualizer:
    """
    Wrapper che applica tutte le ottimizzazioni al visualizzatore.
    """
    
    def __init__(self, visualizer):
        """
        Inizializza wrapper ottimizzato.
        
        Args:
            visualizer: Istanza VisualizzatoreMano3D o simile
        """
        self.visualizer = visualizer
        self.mesh_cache = MeshCache(max_size=50)
        self.object_pool = ObjectPool()
        self.performance_monitor = PerformanceMonitor()
        self.rendering_optimizer = RenderingOptimizer()
        
        # Patch metodi visualizer
        self._patch_visualizer()
    
    def _patch_visualizer(self):
        """Applica patch ai metodi del visualizzatore."""
        # Salva metodi originali
        original_disegna = self.visualizer._disegna_oggetto
        
        def optimized_disegna(oggetto):
            """Versione ottimizzata di _disegna_oggetto."""
            # Check cache
            cache_key = f"{oggetto.nome}_{oggetto.posizione}_{oggetto.dimensione}"
            
            cached_mesh = self.mesh_cache.get(cache_key)
            
            if cached_mesh is None:
                # Genera mesh e cachea
                # (chiamiamo metodo originale interno)
                mesh = oggetto.get_mesh()
                self.mesh_cache.set(cache_key, mesh)
            
            # Renderizza (chiama originale)
            return original_disegna(oggetto)
        
        # Sostituisci metodo
        self.visualizer._disegna_oggetto = optimized_disegna
    
    def start_frame(self):
        """Inizio nuovo frame."""
        self.performance_monitor.start_frame()
        self.object_pool.reset()
    
    def end_frame(self):
        """Fine frame."""
        self.performance_monitor.end_frame()
        
        # Adaptive quality
        current_fps = self.performance_monitor.get_fps()
        self.rendering_optimizer.adjust_quality(current_fps)
    
    def get_stats(self) -> Dict:
        """Statistiche complete."""
        return {
            'performance': self.performance_monitor.get_stats(),
            'cache': self.mesh_cache.get_stats(),
            'rendering': {
                'quality': self.rendering_optimizer.quality_level,
                'settings': self.rendering_optimizer.get_settings()
            }
        }
    
    def print_stats(self):
        """Stampa statistiche formattate."""
        stats = self.get_stats()
        
        print("\n" + "="*60)
        print("PERFORMANCE STATS")
        print("="*60)
        print(f"FPS Corrente:  {stats['performance']['fps_current']:.1f}")
        print(f"FPS Medio:     {stats['performance']['fps_average']:.1f}")
        print(f"Frame Totali:  {stats['performance']['total_frames']}")
        print(f"Frame Time:    {stats['performance']['frame_time_avg']*1000:.2f}ms avg")
        print("-"*60)
        print(f"Cache Mesh:")
        print(f"  Size:       {stats['cache']['size']}")
        print(f"  Hit Rate:   {stats['cache']['hit_rate']:.1f}%")
        print(f"  Hits:       {stats['cache']['hits']}")
        print(f"  Misses:     {stats['cache']['misses']}")
        print("-"*60)
        print(f"Rendering:")
        print(f"  Quality:    {stats['rendering']['quality'].upper()}")
        print(f"  Settings:   {stats['rendering']['settings']}")
        print("="*60 + "\n")


if __name__ == "__main__":
    # Test performance tools
    print("Performance Optimizer - Test")
    
    # Test cache
    cache = MeshCache()
    cache.set("mela", ([1, 2], [3, 4], [5, 6]))
    print(f"Cache get: {cache.get('mela')}")
    print(f"Stats: {cache.get_stats()}")
    
    # Test monitor
    monitor = PerformanceMonitor()
    for i in range(10):
        monitor.start_frame()
        time.sleep(0.033)  # Simula 30 FPS
        monitor.end_frame()
    
    print(f"FPS: {monitor.get_fps():.1f}")
    print(f"Stats: {monitor.get_stats()}")
    
    # Test optimizer
    optimizer = RenderingOptimizer()
    optimizer.adjust_quality(15)  # FPS basso
    print(f"Quality after low FPS: {optimizer.quality_level}")
    
    print("\n[OK] Performance tools tested!")

