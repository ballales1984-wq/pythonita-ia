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


class VisualizzatoreMano3D:
    """
    Visualizzatore 3D per mano robotica.
    Mostra in tempo reale apertura/chiusura con misure reali.
    """
    
    def __init__(self, titolo="Mano Robotica 3D"):
        """Inizializza visualizzatore."""
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.mano = ManoRobotica()
        self.titolo = titolo
        
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
    
    def disegna_mano(self):
        """Disegna la mano nello stato corrente."""
        self.ax.clear()
        self._setup_grafico()
        
        # Disegna palmo
        self._disegna_palmo()
        
        # Disegna ogni dito
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
    
    def mostra(self):
        """Mostra la finestra."""
        plt.legend(loc='upper right')
        plt.show()


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

