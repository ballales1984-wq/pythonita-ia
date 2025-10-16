"""
Visualizzatore 3D per robot e mani bioniche.
Mostra animazioni in tempo reale dei movimenti con grafica avanzata.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from matplotlib.animation import FuncAnimation
from typing import Optional, List
from .modelli_3d import ManoRobotica, BraccioRobotico, RobotCompleto
from .oggetti_3d import GestoreOggetti, Oggetto3D, crea_oggetto

# Performance optimization
try:
    from .performance_optimizer import (
        MeshCache, PerformanceMonitor, RenderingOptimizer, 
        generate_sphere_mesh, generate_cube_vertices
    )
    OPTIMIZATION_AVAILABLE = True
except ImportError:
    OPTIMIZATION_AVAILABLE = False


class VisualizzatoreMano3D:
    """
    Visualizzatore 3D per mano robotica.
    Mostra in tempo reale apertura/chiusura con misure reali.
    """
    
    def __init__(self, titolo="Mano Robotica 3D", enable_optimization=True):
        """Inizializza visualizzatore."""
        self.fig = plt.figure(figsize=(14, 9))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.mano = ManoRobotica()
        self.titolo = titolo
        
        # Gestore oggetti nella scena
        self.gestore_oggetti = GestoreOggetti()
        
        # Abilita rendering avanzato
        self.rendering_avanzato = True
        
        # Performance optimization
        self.optimization_enabled = enable_optimization and OPTIMIZATION_AVAILABLE
        if self.optimization_enabled:
            self.mesh_cache = MeshCache(max_size=50)
            self.perf_monitor = PerformanceMonitor()
            self.render_optimizer = RenderingOptimizer()
            print("[OPTIMIZER] Performance optimization ENABLED")
        else:
            self.mesh_cache = None
            self.perf_monitor = None
            self.render_optimizer = None
        
        # Setup grafico
        self._setup_grafico()
    
    def _setup_grafico(self):
        """Configura l'aspetto del grafico."""
        self.ax.set_xlabel('X (cm)')
        self.ax.set_ylabel('Y (cm)')
        self.ax.set_zlabel('Z (cm)')
        self.ax.set_title(self.titolo, fontsize=14, fontweight='bold')
        
        # Limiti assi
        limite = 12
        self.ax.set_xlim([-limite, limite])
        self.ax.set_ylim([0, limite])
        self.ax.set_zlim([-limite, limite])
        
        # Vista isometrica
        self.ax.view_init(elev=20, azim=45)
        
        # Griglia
        self.ax.grid(True, alpha=0.3)
        
        # Background colore
        self.ax.set_facecolor((0.95, 0.95, 0.95))
        self.fig.patch.set_facecolor('white')
    
    def aggiungi_oggetto(self, tipo: str, posizione: tuple = (0, 15, 0)):
        """
        Aggiungi oggetto alla scena.
        
        Args:
            tipo: Tipo oggetto ("mela", "palla", "cubo", ecc)
            posizione: Posizione (x, y, z) in cm
        """
        oggetto = crea_oggetto(tipo, posizione)
        self.gestore_oggetti.aggiungi_oggetto(oggetto)
        return oggetto
    
    def _disegna_oggetto(self, oggetto: Oggetto3D):
        """Disegna un oggetto 3D con mesh solida."""
        if not oggetto.visibile:
            return
        
        try:
            X, Y, Z = oggetto.get_mesh()
            
            # Usa plot_surface per mesh 3D solida
            surf = self.ax.plot_surface(
                X, Y, Z,
                color=oggetto.colore,
                alpha=oggetto.alpha,
                shade=True,
                antialiased=True,
                edgecolor='none'
            )
            
            # Aggiungi label
            self.ax.text(
                oggetto.posizione[0],
                oggetto.posizione[1],
                oggetto.posizione[2] + 8,
                oggetto.nome,
                fontsize=8,
                ha='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7)
            )
            
        except Exception as e:
            # Fallback: disegna sfera semplice se mesh fallisce
            u = np.linspace(0, 2 * np.pi, 20)
            v = np.linspace(0, np.pi, 15)
            r = 5
            x = r * np.outer(np.cos(u), np.sin(v)) + oggetto.posizione[0]
            y = r * np.outer(np.sin(u), np.sin(v)) + oggetto.posizione[1]
            z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + oggetto.posizione[2]
            
            self.ax.plot_surface(x, y, z, color=oggetto.colore, alpha=oggetto.alpha)
    
    def _disegna_palmo_avanzato(self):
        """Disegna palmo con rendering 3D solido."""
        larghezza = self.mano.dimensioni.LARGHEZZA_PALMO
        lunghezza = self.mano.dimensioni.LUNGHEZZA_PALMO
        spessore = 1.5  # cm
        
        # Crea mesh palmo (box 3D)
        x = np.array([[-larghezza/2, larghezza/2], [-larghezza/2, larghezza/2]])
        y = np.array([[0, 0], [lunghezza, lunghezza]])
        z_top = np.array([[spessore/2, spessore/2], [spessore/2, spessore/2]])
        z_bottom = np.array([[-spessore/2, -spessore/2], [-spessore/2, -spessore/2]])
        
        # Disegna faccia superiore (pelle chiara)
        self.ax.plot_surface(x, y, z_top, color=(1.0, 0.87, 0.73), alpha=0.9, shade=True)
        # Disegna faccia inferiore
        self.ax.plot_surface(x, y, z_bottom, color=(0.95, 0.82, 0.68), alpha=0.9, shade=True)
    
    def _disegna_dito_avanzato(self, nome_dito: str, colore: tuple):
        """Disegna dito con rendering migliorato (cilindri)."""
        vertici_locali = self.mano.get_vertici_dito(nome_dito)
        pos_base = self.mano.get_posizione_base_dito(nome_dito)
        
        vertici = [(v[0] + pos_base[0], v[1] + pos_base[1], v[2] + pos_base[2]) 
                   for v in vertici_locali]
        
        # Disegna ogni segmento come cilindro
        for i in range(len(vertici) - 1):
            p1 = np.array(vertici[i])
            p2 = np.array(vertici[i+1])
            
            # Linea base
            self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                        color=colore, linewidth=5, solid_capstyle='round')
            
            # Sfere alle giunture
            u = np.linspace(0, 2 * np.pi, 15)
            v = np.linspace(0, np.pi, 10)
            r = 0.5
            x = r * np.outer(np.cos(u), np.sin(v)) + p2[0]
            y = r * np.outer(np.sin(u), np.sin(v)) + p2[1]
            z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + p2[2]
            
            self.ax.plot_surface(x, y, z, color=colore, alpha=0.8, shade=True)
    
    def disegna_mano(self):
        """Disegna la mano nello stato corrente."""
        # Performance monitoring
        if self.optimization_enabled:
            self.perf_monitor.start_frame()
        
        self.ax.clear()
        self._setup_grafico()
        
        # Disegna oggetti nella scena
        for oggetto in self.gestore_oggetti.oggetti:
            self._disegna_oggetto(oggetto)
        
        # Disegna palmo
        if self.rendering_avanzato:
            self._disegna_palmo_avanzato()
        else:
            self._disegna_palmo()
        
        # Disegna ogni dito
        if self.rendering_avanzato:
            # Colori RGB per dita (tonalità pelle)
            colori_avanzati = {
                'pollice': (1.0, 0.85, 0.7),
                'indice': (1.0, 0.87, 0.72),
                'medio': (1.0, 0.86, 0.71),
                'anulare': (1.0, 0.88, 0.73),
                'mignolo': (1.0, 0.84, 0.69)
            }
            for nome_dito, colore in colori_avanzati.items():
                self._disegna_dito_avanzato(nome_dito, colore)
        else:
            # Colori semplici per debug
            colori = {
                'pollice': 'red',
                'indice': 'blue',
                'medio': 'green',
                'anulare': 'orange',
                'mignolo': 'purple'
            }
            for nome_dito, colore in colori.items():
                self._disegna_dito(nome_dito, colore)
        
        # Aggiungi legenda con stato
        self._aggiungi_info_stato()
        
        plt.draw()
        
        # Performance monitoring
        if self.optimization_enabled:
            self.perf_monitor.end_frame()
            
            # Ogni 30 frame, stampa statistiche FPS
            if self.perf_monitor.total_frames % 30 == 0:
                fps = self.perf_monitor.get_fps()
                print(f"[PERF] FPS: {fps:.1f}")
                
                # Adaptive quality adjustment
                self.render_optimizer.adjust_quality(fps)
        
        plt.pause(0.01)
    
    def _disegna_palmo(self):
        """Disegna il palmo della mano."""
        # Palmo rettangolare
        larghezza = self.mano.dimensioni.LARGHEZZA_PALMO
        lunghezza = self.mano.dimensioni.LUNGHEZZA_PALMO
        
        # Vertici palmo
        vertices = np.array([
            [-larghezza/2, 0, -2],
            [larghezza/2, 0, -2],
            [larghezza/2, 0, 2],
            [-larghezza/2, 0, 2],
            [-larghezza/2, 0, -2]
        ])
        
        self.ax.plot(vertices[:, 0], vertices[:, 1], vertices[:, 2],
                    'k-', linewidth=3, label='Palmo')
    
    def _disegna_dito(self, nome_dito: str, colore: str):
        """Disegna un singolo dito."""
        # Ottieni vertici del dito
        vertici_locali = self.mano.get_vertici_dito(nome_dito)
        
        # Trasla alla posizione base sul palmo
        pos_base = self.mano.get_posizione_base_dito(nome_dito)
        
        vertici = [(v[0] + pos_base[0], v[1] + pos_base[1], v[2] + pos_base[2]) 
                   for v in vertici_locali]
        
        # Disegna linee del dito
        xs = [v[0] for v in vertici]
        ys = [v[1] for v in vertici]
        zs = [v[2] for v in vertici]
        
        self.ax.plot(xs, ys, zs, color=colore, linewidth=2.5, 
                    marker='o', markersize=4, label=nome_dito.capitalize())
        
        # Aggiungi sfere alle giunture
        for i, (x, y, z) in enumerate(vertici[1:], 1):
            self.ax.scatter([x], [y], [z], color=colore, s=50, alpha=0.7)
    
    def _aggiungi_info_stato(self):
        """Aggiunge informazioni sullo stato della mano."""
        # Calcola percentuale chiusura media
        percentuale = self._calcola_percentuale_chiusura()
        
        info_text = f"Chiusura: {percentuale:.0f}%\n"
        info_text += f"Angolo polso: {self.mano.angolo_polso}°"
        
        self.ax.text2D(0.02, 0.98, info_text, transform=self.ax.transAxes,
                      fontsize=10, verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def _calcola_percentuale_chiusura(self) -> float:
        """Calcola percentuale media di chiusura."""
        totale = 0
        for angoli in self.mano.angoli_dita.values():
            media_dito = sum(angoli) / len(angoli)
            percentuale_dito = (media_dito / self.mano.dimensioni.ANGOLO_MAX_DITO) * 100
            totale += percentuale_dito
        
        return totale / len(self.mano.angoli_dita)
    
    def anima_apertura(self, steps=20):
        """Anima l'apertura della mano."""
        for i in range(steps, -1, -1):
            percentuale = (i / steps) * 100
            self.mano.chiudi_mano(percentuale)
            self.disegna_mano()
            plt.pause(0.05)
    
    def anima_chiusura(self, steps=20):
        """Anima la chiusura della mano."""
        for i in range(0, steps + 1):
            percentuale = (i / steps) * 100
            self.mano.chiudi_mano(percentuale)
            self.disegna_mano()
            plt.pause(0.05)
    
    def anima_pinza(self, steps=15):
        """Anima movimento a pinza."""
        # Prima apri tutto
        self.mano.apri_mano()
        self.disegna_mano()
        plt.pause(0.5)
        
        # Poi forma pinza progressivamente
        for i in range(0, steps + 1):
            apertura = 30 - (i / steps) * 20  # Da 30mm a 10mm
            self.mano.posizione_pinza(apertura)
            self.disegna_mano()
            plt.pause(0.05)
    
    def anima_afferra_oggetto(self, nome_oggetto: str = "mela", steps=25):
        """
        Anima mano che afferra un oggetto.
        
        Args:
            nome_oggetto: Tipo oggetto da afferrare
            steps: Numero frame animazione
        """
        # Trova o crea oggetto
        oggetto = self.gestore_oggetti.trova_oggetto_vicino(np.array([0, 10, 0]), raggio=50)
        
        if not oggetto:
            # Crea oggetto nella scena
            oggetto = self.aggiungi_oggetto(nome_oggetto, (0, 15, 0))
        
        # 1. Apri mano
        self.mano.apri_mano()
        self.disegna_mano()
        plt.pause(0.3)
        
        # 2. Avvicina mano all'oggetto (opzionale, per ora statico)
        
        # 3. Chiudi mano gradualmente sull'oggetto
        for i in range(0, steps + 1):
            perc = (i / steps) * 70  # Chiudi al 70%
            self.mano.chiudi_mano(perc)
            self.disegna_mano()
            plt.pause(0.04)
        
        # 4. Afferra oggetto
        posizione_mano = np.array([0, 8, 0])  # Centro palmo
        self.gestore_oggetti.afferra_oggetto(oggetto, posizione_mano)
        
        # 5. Mostra oggetto nella mano
        self.disegna_mano()
        plt.pause(0.5)
    
    def anima_rilascia_oggetto(self, steps=20):
        """Anima rilascio oggetto."""
        if not self.gestore_oggetti.oggetto_afferrato:
            return
        
        # 1. Apri mano gradualmente
        for i in range(steps, -1, -1):
            perc = (i / steps) * 70
            self.mano.chiudi_mano(perc)
            
            # Aggiorna posizione oggetto
            self.gestore_oggetti.aggiorna(np.array([0, 8, 0]))
            self.disegna_mano()
            plt.pause(0.04)
        
        # 2. Rilascia oggetto
        if self.gestore_oggetti.oggetto_afferrato:
            # Lascia oggetto in posizione finale
            self.gestore_oggetti.oggetto_afferrato.posizione[1] = 5  # Appoggia a terra
        
        self.gestore_oggetti.rilascia_oggetto()
        self.disegna_mano()
        plt.pause(0.3)
    
    def mostra(self):
        """Mostra la finestra."""
        plt.legend(loc='upper right')
        plt.show()
    
    def print_performance_stats(self):
        """Stampa statistiche performance complete."""
        if not self.optimization_enabled:
            print("[INFO] Performance optimization non abilitata")
            return
        
        print("\n" + "="*70)
        print("STATISTICHE PERFORMANCE - Visualizzatore 3D")
        print("="*70)
        
        # Performance stats
        perf_stats = self.perf_monitor.get_stats()
        print(f"\nRendering:")
        print(f"  FPS Corrente:     {perf_stats['fps_current']:.1f}")
        print(f"  FPS Medio:        {perf_stats['fps_average']:.1f}")
        print(f"  Frame Totali:     {perf_stats['total_frames']}")
        print(f"  Frame Time (avg): {perf_stats['frame_time_avg']*1000:.2f}ms")
        print(f"  Frame Time (min): {perf_stats['frame_time_min']*1000:.2f}ms")
        print(f"  Frame Time (max): {perf_stats['frame_time_max']*1000:.2f}ms")
        
        # Cache stats
        if self.mesh_cache:
            cache_stats = self.mesh_cache.get_stats()
            print(f"\nMesh Cache:")
            print(f"  Dimensione:       {cache_stats['size']} oggetti")
            print(f"  Hit Rate:         {cache_stats['hit_rate']:.1f}%")
            print(f"  Cache Hits:       {cache_stats['hits']}")
            print(f"  Cache Misses:     {cache_stats['misses']}")
        
        # Rendering quality
        if self.render_optimizer:
            settings = self.render_optimizer.get_settings()
            print(f"\nQualità Rendering:")
            print(f"  Livello:          {self.render_optimizer.quality_level.upper()}")
            print(f"  Sfera Risoluzione:{settings['sphere_resolution']}")
            print(f"  Antialiasing:     {'✅' if settings['antialiasing'] else '❌'}")
            print(f"  Ombre:            {'✅' if settings['shadows'] else '❌'}")
            print(f"  Max Vertici:      {settings['max_vertices']}")
        
        print("\n" + "="*70)
        
        # Raccomandazioni
        fps_current = perf_stats['fps_current']
        if fps_current < 20:
            print("⚠️  ATTENZIONE: FPS molto bassi! Suggerimenti:")
            print("   - Chiudi altri programmi")
            print("   - Riduci numero oggetti 3D nella scena")
            print("   - Disabilita rendering avanzato")
        elif fps_current < 30:
            print("ℹ️  FPS accettabili ma potrebbero migliorare")
        else:
            print("✅ Performance ottime!")
        
        print("="*70 + "\n")


class VisualizzatoreBraccio3D:
    """Visualizzatore 3D per braccio robotico completo."""
    
    def __init__(self, titolo="Braccio Robotico 3D"):
        """Inizializza visualizzatore braccio."""
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.braccio = BraccioRobotico()
        self.titolo = titolo
        
        self._setup_grafico()
    
    def _setup_grafico(self):
        """Configura grafico."""
        self.ax.set_xlabel('X (cm)')
        self.ax.set_ylabel('Y (cm)')
        self.ax.set_zlabel('Z (cm)')
        self.ax.set_title(self.titolo, fontsize=14, fontweight='bold')
        
        limite = 40
        self.ax.set_xlim([0, limite])
        self.ax.set_ylim([0, limite])
        self.ax.set_zlim([0, limite])
        
        self.ax.view_init(elev=15, azim=45)
        self.ax.grid(True, alpha=0.3)
    
    def disegna_braccio(self):
        """Disegna braccio nello stato corrente."""
        self.ax.clear()
        self._setup_grafico()
        
        # Calcola posizioni segmenti
        # Origine (spalla)
        p0 = np.array([0, 0, 30])  # Spalla a 30cm da terra
        
        # Braccio superiore
        L1 = self.braccio.dimensioni.LUNGHEZZA_BRACCIO_SUPERIORE
        theta1 = np.radians(self.braccio.angolo_spalla)
        p1 = p0 + np.array([L1 * np.cos(theta1), L1 * np.sin(theta1), 0])
        
        # Avambraccio
        L2 = self.braccio.dimensioni.LUNGHEZZA_AVAMBRACCIO
        theta2 = theta1 + np.radians(self.braccio.angolo_gomito)
        p2 = p1 + np.array([L2 * np.cos(theta2), L2 * np.sin(theta2), 0])
        
        # Disegna segmenti
        self.ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]], 
                    'b-', linewidth=6, label='Braccio superiore')
        self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                    'r-', linewidth=6, label='Avambraccio')
        
        # Giunture
        self.ax.scatter(*p0, color='black', s=100, label='Spalla')
        self.ax.scatter(*p1, color='green', s=100, label='Gomito')
        self.ax.scatter(*p2, color='red', s=100, label='Polso/Mano')
        
        # Info
        info = f"Spalla: {self.braccio.angolo_spalla}°\nGomito: {self.braccio.angolo_gomito}°"
        self.ax.text2D(0.02, 0.98, info, transform=self.ax.transAxes,
                      fontsize=10, verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.draw()
        plt.pause(0.01)
    
    def anima_alza_braccio(self, angolo_target=90, steps=30):
        """Anima sollevamento braccio."""
        angolo_iniziale = self.braccio.angolo_spalla
        
        for i in range(steps + 1):
            angolo = angolo_iniziale + (angolo_target - angolo_iniziale) * (i / steps)
            self.braccio.alza_braccio(angolo)
            self.disegna_braccio()
            plt.pause(0.03)
    
    def mostra(self):
        """Mostra finestra."""
        plt.legend(loc='upper right')
        plt.show()


def demo_mano_3d():
    """Demo visualizzazione mano 3D."""
    viz = VisualizzatoreMano3D("Demo Mano Robotica - Pythonita v3.1")
    
    print("Visualizzando mano 3D...")
    print("Chiudi la finestra per continuare")
    
    # Mostra mano aperta
    viz.mano.apri_mano()
    viz.disegna_mano()
    plt.pause(1)
    
    # Anima chiusura
    print("Animazione: Chiusura mano...")
    viz.anima_chiusura(steps=20)
    plt.pause(1)
    
    # Anima apertura
    print("Animazione: Apertura mano...")
    viz.anima_apertura(steps=20)
    plt.pause(1)
    
    # Mostra pinza
    print("Animazione: Posizione pinza...")
    viz.anima_pinza(steps=15)
    
    viz.mostra()


def demo_braccio_3d():
    """Demo visualizzazione braccio 3D."""
    viz = VisualizzatoreBraccio3D("Demo Braccio Robotico - Pythonita v3.1")
    
    print("Visualizzando braccio 3D...")
    print("Chiudi la finestra per continuare")
    
    # Posizione iniziale
    viz.disegna_braccio()
    plt.pause(1)
    
    # Anima sollevamento
    print("Animazione: Alza braccio...")
    viz.anima_alza_braccio(angolo_target=90, steps=30)
    plt.pause(1)
    
    # Piega gomito
    print("Animazione: Piega gomito...")
    for i in range(31):
        angolo = i * 3  # 0 a 90 gradi
        viz.braccio.piega_gomito(angolo)
        viz.disegna_braccio()
        plt.pause(0.03)
    
    viz.mostra()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'braccio':
        demo_braccio_3d()
    else:
        demo_mano_3d()

