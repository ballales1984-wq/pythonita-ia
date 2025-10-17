"""
Connettore tra risultati AI e visualizzatore 3D.

Converte risultati numerici in visualizzazioni 3D interattive.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import Dict, Optional


class Visualizer3DConnector:
    """Connette risultati con visualizzatore 3D."""
    
    def __init__(self):
        """Inizializza connettore."""
        self.fig_3d = None
        self.ax_3d = None
    
    def visualizza_da_risultato(self, comando: str, risultato: str, codice: str) -> bool:
        """
        Analizza risultato e crea visualizzazione 3D appropriata.
        
        Args:
            comando: Comando originale
            risultato: Output esecuzione
            codice: Codice generato
            
        Returns:
            True se ha generato visualizzazione 3D
        """
        comando_lower = comando.lower()
        
        # CERCHIO / SFERA 3D
        if 'cerchio' in comando_lower or 'sfera' in comando_lower:
            raggio = self._estrai_numero(comando, risultato)
            if raggio:
                return self._crea_sfera_3d(raggio)
        
        # CUBO / BOX 3D
        elif 'cubo' in comando_lower or 'box' in comando_lower:
            lato = self._estrai_numero(comando, risultato)
            if lato:
                return self._crea_cubo_3d(lato)
        
        # CILINDRO 3D
        elif 'cilindro' in comando_lower:
            raggio = self._estrai_numero(comando, risultato)
            if raggio:
                return self._crea_cilindro_3d(raggio, raggio * 2)
        
        # GRAFICO 3D FUNZIONE
        elif 'funzione' in comando_lower and '3d' in comando_lower:
            return self._crea_funzione_3d()
        
        # SUPERFICIE
        elif 'superficie' in comando_lower:
            return self._crea_superficie_3d()
        
        return False
    
    def _estrai_numero(self, comando: str, risultato: str) -> Optional[float]:
        """Estrae numero da comando o risultato."""
        import re
        
        # Cerca nel comando
        match = re.search(r'raggio\s*(\d+(?:\.\d+)?)', comando.lower())
        if match:
            return float(match.group(1))
        
        match = re.search(r'lato\s*(\d+(?:\.\d+)?)', comando.lower())
        if match:
            return float(match.group(1))
        
        # Cerca nel risultato
        match = re.search(r'(\d+(?:\.\d+)?)', risultato)
        if match:
            return float(match.group(1))
        
        return None
    
    def _crea_sfera_3d(self, raggio: float) -> bool:
        """Crea visualizzazione sfera 3D."""
        fig = plt.figure(figsize=(10, 8))
        fig.patch.set_facecolor('#1e1e2e')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#0d1117')
        
        # Genera mesh sfera
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        x = raggio * np.outer(np.cos(u), np.sin(v))
        y = raggio * np.outer(np.sin(u), np.sin(v))
        z = raggio * np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Plot superficie
        surf = ax.plot_surface(x, y, z, 
                              color='#00d4ff', 
                              alpha=0.7,
                              edgecolor='#00ff88',
                              linewidth=0.5)
        
        # Titolo e label
        ax.set_title(f'Sfera 3D - Raggio {raggio}',
                    fontsize=16, fontweight='bold', color='#00d4ff', pad=20)
        ax.set_xlabel('X', fontsize=12, color='#e0e0e0')
        ax.set_ylabel('Y', fontsize=12, color='#e0e0e0')
        ax.set_zlabel('Z', fontsize=12, color='#e0e0e0')
        
        # Colori assi
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('#3d3d5c')
        ax.yaxis.pane.set_edgecolor('#3d3d5c')
        ax.zaxis.pane.set_edgecolor('#3d3d5c')
        ax.grid(True, alpha=0.2, color='#3d3d5c')
        
        # Testo volume
        volume = (4/3) * np.pi * raggio**3
        ax.text2D(0.05, 0.95, f'Volume: {volume:.2f}',
                 transform=ax.transAxes,
                 fontsize=14, fontweight='bold',
                 color='#00ff88',
                 bbox=dict(boxstyle='round', facecolor='#1e1e2e', edgecolor='#00ff88'))
        
        plt.tight_layout()
        plt.show()
        return True
    
    def _crea_cubo_3d(self, lato: float) -> bool:
        """Crea cubo 3D."""
        fig = plt.figure(figsize=(10, 8))
        fig.patch.set_facecolor('#1e1e2e')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#0d1117')
        
        # Vertici cubo
        r = lato / 2
        vertices = np.array([
            [-r, -r, -r], [r, -r, -r], [r, r, -r], [-r, r, -r],  # Base inferiore
            [-r, -r, r], [r, -r, r], [r, r, r], [-r, r, r]       # Base superiore
        ])
        
        # Facce
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        
        faces = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # Bottom
            [vertices[4], vertices[5], vertices[6], vertices[7]],  # Top
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # Front
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # Back
            [vertices[0], vertices[3], vertices[7], vertices[4]],  # Left
            [vertices[1], vertices[2], vertices[6], vertices[5]]   # Right
        ]
        
        poly = Poly3DCollection(faces, 
                               facecolors='#00d4ff', 
                               linewidths=2,
                               edgecolors='#00ff88',
                               alpha=0.7)
        ax.add_collection3d(poly)
        
        # Limiti
        ax.set_xlim(-r*1.5, r*1.5)
        ax.set_ylim(-r*1.5, r*1.5)
        ax.set_zlim(-r*1.5, r*1.5)
        
        ax.set_title(f'Cubo 3D - Lato {lato}',
                    fontsize=16, fontweight='bold', color='#00d4ff', pad=20)
        ax.set_xlabel('X', fontsize=12, color='#e0e0e0')
        ax.set_ylabel('Y', fontsize=12, color='#e0e0e0')
        ax.set_zlabel('Z', fontsize=12, color='#e0e0e0')
        
        volume = lato ** 3
        ax.text2D(0.05, 0.95, f'Volume: {volume:.2f}',
                 transform=ax.transAxes,
                 fontsize=14, fontweight='bold',
                 color='#00ff88',
                 bbox=dict(boxstyle='round', facecolor='#1e1e2e', edgecolor='#00ff88'))
        
        plt.tight_layout()
        plt.show()
        return True
    
    def _crea_cilindro_3d(self, raggio: float, altezza: float) -> bool:
        """Crea cilindro 3D."""
        fig = plt.figure(figsize=(10, 8))
        fig.patch.set_facecolor('#1e1e2e')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#0d1117')
        
        # Parametri
        theta = np.linspace(0, 2*np.pi, 50)
        z = np.linspace(0, altezza, 50)
        
        # Mesh
        Theta, Z = np.meshgrid(theta, z)
        X = raggio * np.cos(Theta)
        Y = raggio * np.sin(Theta)
        
        # Plot
        ax.plot_surface(X, Y, Z,
                       color='#00d4ff',
                       alpha=0.7,
                       edgecolor='#00ff88',
                       linewidth=0.5)
        
        ax.set_title(f'Cilindro 3D - R={raggio}, H={altezza}',
                    fontsize=16, fontweight='bold', color='#00d4ff', pad=20)
        
        volume = np.pi * raggio**2 * altezza
        ax.text2D(0.05, 0.95, f'Volume: {volume:.2f}',
                 transform=ax.transAxes,
                 fontsize=14, fontweight='bold',
                 color='#00ff88',
                 bbox=dict(boxstyle='round', facecolor='#1e1e2e', edgecolor='#00ff88'))
        
        plt.tight_layout()
        plt.show()
        return True
    
    def _crea_funzione_3d(self) -> bool:
        """Crea plot 3D di funzione."""
        fig = plt.figure(figsize=(10, 8))
        fig.patch.set_facecolor('#1e1e2e')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#0d1117')
        
        # Mesh
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(np.sqrt(X**2 + Y**2))
        
        # Plot
        surf = ax.plot_surface(X, Y, Z,
                              cmap='viridis',
                              alpha=0.8,
                              edgecolor='none')
        
        ax.set_title('Funzione 3D: z = sin(√(x²+y²))',
                    fontsize=16, fontweight='bold', color='#00d4ff', pad=20)
        
        plt.colorbar(surf, ax=ax, shrink=0.5)
        plt.tight_layout()
        plt.show()
        return True
    
    def _crea_superficie_3d(self) -> bool:
        """Crea superficie 3D generica."""
        return self._crea_funzione_3d()


def get_viz_3d_connector():
    """Restituisce istanza singleton."""
    if not hasattr(get_viz_3d_connector, '_instance'):
        get_viz_3d_connector._instance = Visualizer3DConnector()
    return get_viz_3d_connector._instance

