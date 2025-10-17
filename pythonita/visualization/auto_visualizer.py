"""
Sistema di visualizzazione automatica intelligente.

Analizza il comando e risultato, poi genera il grafico appropriato.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Optional, Dict, Any
import re


class AutoVisualizer:
    """Visualizzatore automatico intelligente."""
    
    def __init__(self):
        """Inizializza visualizzatore."""
        plt.style.use('dark_background')  # Tema scuro per consistenza
    
    def analizza_e_visualizza(self, comando: str, codice: str, risultato: str) -> bool:
        """
        Analizza comando/risultato e crea visualizzazione appropriata.
        
        Args:
            comando: Comando originale utente
            codice: Codice Python generato
            risultato: Output esecuzione
            
        Returns:
            True se ha generato visualizzazione
        """
        comando_lower = comando.lower()
        
        # CERCHIO / AREA CERCHIO
        if 'cerchio' in comando_lower and ('area' in comando_lower or 'raggio' in comando_lower):
            raggio = self._estrai_numero(comando, ["raggio"])
            if raggio:
                area = np.pi * raggio**2
                self._visualizza_cerchio(raggio, area)
                return True
        
        # QUADRATO / RETTANGOLO
        elif 'quadrato' in comando_lower or 'rettangolo' in comando_lower:
            lato = self._estrai_numero(comando, ["lato", "base", "altezza"])
            if lato:
                self._visualizza_quadrato(lato)
                return True
        
        # TRIANGOLO
        elif 'triangolo' in comando_lower:
            lati = self._estrai_numeri(comando)
            if len(lati) >= 2:
                self._visualizza_triangolo(lati)
                return True
        
        # FUNZIONE MATEMATICA (seno, coseno, ecc)
        elif any(func in comando_lower for func in ['seno', 'coseno', 'sin', 'cos', 'tan', 'funzione']):
            self._visualizza_funzione_matematica(comando)
            return True
        
        # GRAFICO LINEARE / DATI
        elif 'grafico' in comando_lower or 'plot' in comando_lower:
            self._visualizza_grafico_generico(risultato)
            return True
        
        # LISTA NUMERI / ARRAY
        elif '[' in risultato and ']' in risultato:
            try:
                # Prova ad estrarre lista
                numeri = eval(risultato.split('[')[1].split(']')[0])
                if isinstance(numeri, (list, tuple)) and len(numeri) > 0:
                    self._visualizza_lista(numeri, comando)
                    return True
            except:
                pass
        
        return False
    
    def _estrai_numero(self, testo: str, keywords: list) -> Optional[float]:
        """Estrae numero da testo dopo keyword."""
        for keyword in keywords:
            pattern = f"{keyword}\\s*(\\d+(?:\\.\\d+)?)"
            match = re.search(pattern, testo.lower())
            if match:
                return float(match.group(1))
        
        # Fallback: cerca qualsiasi numero
        match = re.search(r'(\d+(?:\.\d+)?)', testo)
        if match:
            return float(match.group(1))
        
        return None
    
    def _estrai_numeri(self, testo: str) -> list:
        """Estrae tutti i numeri dal testo."""
        return [float(n) for n in re.findall(r'\d+(?:\.\d+)?', testo)]
    
    def _visualizza_cerchio(self, raggio: float, area: float):
        """Visualizza cerchio con area."""
        fig, ax = plt.subplots(figsize=(8, 8))
        fig.patch.set_facecolor('#1e1e2e')
        ax.set_facecolor('#0d1117')
        
        # Disegna cerchio
        circle = patches.Circle((0, 0), raggio, 
                               fill=True, 
                               facecolor='#00d4ff', 
                               edgecolor='#00ff88',
                               linewidth=3,
                               alpha=0.6)
        ax.add_patch(circle)
        
        # Centro
        ax.plot(0, 0, 'o', color='#ff4466', markersize=10, label='Centro')
        
        # Raggio linea
        ax.plot([0, raggio], [0, 0], '--', color='#ffaa00', linewidth=2, label=f'Raggio = {raggio}')
        
        # Testo
        ax.text(0, raggio + 0.5, f'Area = {area:.2f}', 
               ha='center', va='bottom',
               fontsize=16, fontweight='bold',
               color='#00ff88',
               bbox=dict(boxstyle='round', facecolor='#1e1e2e', edgecolor='#00ff88', linewidth=2))
        
        # Setup assi
        lim = raggio * 1.5
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.2, color='#3d3d5c')
        ax.legend(loc='upper right', facecolor='#1e1e2e', edgecolor='#00d4ff')
        ax.set_title(f'Cerchio - Raggio {raggio}', 
                    fontsize=18, fontweight='bold', color='#00d4ff', pad=20)
        
        plt.tight_layout()
        plt.show()
    
    def _visualizza_quadrato(self, lato: float):
        """Visualizza quadrato/rettangolo."""
        fig, ax = plt.subplots(figsize=(8, 8))
        fig.patch.set_facecolor('#1e1e2e')
        ax.set_facecolor('#0d1117')
        
        # Disegna quadrato
        square = patches.Rectangle((-lato/2, -lato/2), lato, lato,
                                   fill=True,
                                   facecolor='#00d4ff',
                                   edgecolor='#00ff88',
                                   linewidth=3,
                                   alpha=0.6)
        ax.add_patch(square)
        
        area = lato * lato
        ax.text(0, lato/2 + 0.5, f'Area = {area:.2f}',
               ha='center', va='bottom',
               fontsize=16, fontweight='bold',
               color='#00ff88',
               bbox=dict(boxstyle='round', facecolor='#1e1e2e', edgecolor='#00ff88', linewidth=2))
        
        lim = lato
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.2, color='#3d3d5c')
        ax.set_title(f'Quadrato - Lato {lato}',
                    fontsize=18, fontweight='bold', color='#00d4ff', pad=20)
        
        plt.tight_layout()
        plt.show()
    
    def _visualizza_triangolo(self, lati: list):
        """Visualizza triangolo."""
        fig, ax = plt.subplots(figsize=(8, 8))
        fig.patch.set_facecolor('#1e1e2e')
        ax.set_facecolor('#0d1117')
        
        # Triangolo semplice (isoscele o equilatero)
        if len(lati) >= 2:
            base = lati[0]
            altezza = lati[1] if len(lati) > 1 else lati[0] * 0.866  # sqrt(3)/2
            
            # Vertici
            vertices = np.array([
                [0, 0],
                [base, 0],
                [base/2, altezza]
            ])
            
            triangle = patches.Polygon(vertices,
                                      fill=True,
                                      facecolor='#00d4ff',
                                      edgecolor='#00ff88',
                                      linewidth=3,
                                      alpha=0.6)
            ax.add_patch(triangle)
            
            area = (base * altezza) / 2
            ax.text(base/2, altezza + 0.5, f'Area = {area:.2f}',
                   ha='center', va='bottom',
                   fontsize=16, fontweight='bold',
                   color='#00ff88',
                   bbox=dict(boxstyle='round', facecolor='#1e1e2e', edgecolor='#00ff88', linewidth=2))
            
            ax.set_xlim(-1, base + 1)
            ax.set_ylim(-1, altezza + 2)
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.2, color='#3d3d5c')
            ax.set_title(f'Triangolo',
                        fontsize=18, fontweight='bold', color='#00d4ff', pad=20)
            
            plt.tight_layout()
            plt.show()
    
    def _visualizza_funzione_matematica(self, comando: str):
        """Visualizza funzione matematica."""
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#1e1e2e')
        ax.set_facecolor('#0d1117')
        
        x = np.linspace(-2*np.pi, 2*np.pi, 1000)
        
        # Determina funzione
        if 'seno' in comando.lower() or 'sin' in comando.lower():
            y = np.sin(x)
            title = 'Funzione Seno: y = sin(x)'
        elif 'coseno' in comando.lower() or 'cos' in comando.lower():
            y = np.cos(x)
            title = 'Funzione Coseno: y = cos(x)'
        elif 'tan' in comando.lower():
            y = np.tan(x)
            y = np.clip(y, -10, 10)  # Limita tangente
            title = 'Funzione Tangente: y = tan(x)'
        else:
            y = np.sin(x)  # Default
            title = 'Funzione Matematica'
        
        # Plot
        ax.plot(x, y, color='#00d4ff', linewidth=2.5, label=title)
        ax.axhline(0, color='#3d3d5c', linewidth=1, linestyle='--')
        ax.axvline(0, color='#3d3d5c', linewidth=1, linestyle='--')
        ax.grid(True, alpha=0.2, color='#3d3d5c')
        ax.legend(loc='upper right', facecolor='#1e1e2e', edgecolor='#00d4ff', fontsize=12)
        ax.set_title(title, fontsize=18, fontweight='bold', color='#00d4ff', pad=20)
        ax.set_xlabel('x', fontsize=14, color='#e0e0e0')
        ax.set_ylabel('y', fontsize=14, color='#e0e0e0')
        
        plt.tight_layout()
        plt.show()
    
    def _visualizza_grafico_generico(self, dati: str):
        """Visualizza grafico generico da dati."""
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#1e1e2e')
        ax.set_facecolor('#0d1117')
        
        # Dati esempio
        x = np.arange(10)
        y = np.random.rand(10) * 100
        
        ax.bar(x, y, color='#00d4ff', edgecolor='#00ff88', linewidth=2, alpha=0.7)
        ax.grid(True, alpha=0.2, color='#3d3d5c', axis='y')
        ax.set_title('Grafico Dati', fontsize=18, fontweight='bold', color='#00d4ff', pad=20)
        ax.set_xlabel('Indice', fontsize=14, color='#e0e0e0')
        ax.set_ylabel('Valore', fontsize=14, color='#e0e0e0')
        
        plt.tight_layout()
        plt.show()
    
    def _visualizza_lista(self, numeri: list, comando: str):
        """Visualizza lista numeri."""
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#1e1e2e')
        ax.set_facecolor('#0d1117')
        
        x = list(range(len(numeri)))
        
        # Determina tipo grafico
        if 'fibonacci' in comando.lower():
            ax.plot(x, numeri, 'o-', color='#00d4ff', linewidth=2.5, markersize=10, 
                   markeredgecolor='#00ff88', markeredgewidth=2, label='Fibonacci')
            title = 'Sequenza Fibonacci'
        else:
            ax.bar(x, numeri, color='#00d4ff', edgecolor='#00ff88', linewidth=2, alpha=0.7)
            title = 'Valori'
        
        ax.grid(True, alpha=0.2, color='#3d3d5c', axis='y')
        ax.legend(loc='upper left', facecolor='#1e1e2e', edgecolor='#00d4ff', fontsize=12)
        ax.set_title(title, fontsize=18, fontweight='bold', color='#00d4ff', pad=20)
        ax.set_xlabel('Indice', fontsize=14, color='#e0e0e0')
        ax.set_ylabel('Valore', fontsize=14, color='#e0e0e0')
        
        plt.tight_layout()
        plt.show()


def get_auto_visualizer():
    """Restituisce istanza singleton."""
    if not hasattr(get_auto_visualizer, '_instance'):
        get_auto_visualizer._instance = AutoVisualizer()
    return get_auto_visualizer._instance

