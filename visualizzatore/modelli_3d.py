"""
Modelli 3D per visualizzazione robot.
Definisce geometrie e dimensioni reali di mani e bracci robotici.
"""

import numpy as np
from typing import List, Tuple, Dict


class DimensioniReali:
    """Dimensioni reali in cm di componenti robotici."""
    
    # Mano umana adulta (misure medie)
    LUNGHEZZA_PALMO = 10.0  # cm
    LARGHEZZA_PALMO = 8.5   # cm
    
    # Dita (lunghezze falangeprossimale-intermedia-distale)
    POLLICE = [3.8, 2.5, 2.0]      # cm
    INDICE = [4.5, 2.7, 2.0]       # cm
    MEDIO = [5.0, 3.0, 2.2]        # cm
    ANULARE = [4.6, 2.8, 2.1]      # cm
    MIGNOLO = [3.8, 2.2, 1.8]      # cm
    
    # Braccio (misure medie)
    LUNGHEZZA_BRACCIO_SUPERIORE = 30.0  # cm (omero)
    LUNGHEZZA_AVAMBRACCIO = 25.0        # cm (ulna/radio)
    
    # Angoli massimi (gradi)
    ANGOLO_MAX_DITO = 90      # gradi
    ANGOLO_MAX_POLSO = 180    # gradi
    ANGOLO_MAX_GOMITO = 150   # gradi
    ANGOLO_MAX_SPALLA = 180   # gradi


class ManoRobotica:
    """
    Modello 3D di una mano robotica con 5 dita.
    Ogni dito ha 3 falangi con angoli controllabili.
    """
    
    def __init__(self):
        """Inizializza modello mano."""
        self.dimensioni = DimensioniReali()
        
        # Stato angoli (0 = aperto, 90 = chiuso)
        self.angoli_dita = {
            'pollice': [0, 0, 0],
            'indice': [0, 0, 0],
            'medio': [0, 0, 0],
            'anulare': [0, 0, 0],
            'mignolo': [0, 0, 0]
        }
        
        self.angolo_polso = 0  # Rotazione polso
        
    def apri_mano(self):
        """Apre completamente la mano."""
        for dito in self.angoli_dita:
            self.angoli_dita[dito] = [0, 0, 0]
    
    def chiudi_mano(self, percentuale=100):
        """
        Chiude la mano.
        
        Args:
            percentuale: Percentuale chiusura (0-100)
        """
        angolo = (percentuale / 100) * self.dimensioni.ANGOLO_MAX_DITO
        
        for dito in self.angoli_dita:
            self.angoli_dita[dito] = [angolo, angolo * 0.8, angolo * 0.6]
    
    def chiudi_dito(self, nome_dito: str, angolo: float):
        """Chiude un singolo dito."""
        if nome_dito in self.angoli_dita:
            self.angoli_dita[nome_dito] = [angolo, angolo * 0.8, angolo * 0.6]
    
    def posizione_pinza(self, apertura_mm: float = 20):
        """
        Posizione per presa a pinza.
        
        Args:
            apertura_mm: Distanza tra pollice e indice in mm
        """
        # Apri dita non usate
        self.angoli_dita['medio'] = [0, 0, 0]
        self.angoli_dita['anulare'] = [0, 0, 0]
        self.angoli_dita['mignolo'] = [0, 0, 0]
        
        # Posiziona pollice e indice
        angolo_pinza = 45  # Circa metà chiusura
        self.angoli_dita['pollice'] = [angolo_pinza, angolo_pinza, angolo_pinza]
        self.angoli_dita['indice'] = [angolo_pinza, angolo_pinza, angolo_pinza]
    
    def get_vertici_dito(self, nome_dito: str) -> List[Tuple[float, float, float]]:
        """
        Calcola vertici 3D di un dito basati su angoli.
        
        Returns:
            Lista di coordinate (x, y, z) per ogni segmento
        """
        lunghezze = self._get_lunghezze_dito(nome_dito)
        angoli = self.angoli_dita[nome_dito]
        
        # Calcola posizione 3D di ogni falange
        vertici = [(0, 0, 0)]  # Punto iniziale (base dito)
        
        x, y, z = 0, 0, 0
        angolo_accumulato = 0
        
        for i, (lunghezza, angolo) in enumerate(zip(lunghezze, angoli)):
            angolo_accumulato += np.radians(angolo)
            
            # Calcola nuova posizione
            x += lunghezza * np.cos(angolo_accumulato)
            y += lunghezza * np.sin(angolo_accumulato)
            
            vertici.append((x, y, z))
        
        return vertici
    
    def _get_lunghezze_dito(self, nome_dito: str) -> List[float]:
        """Ottiene lunghezze falangi di un dito."""
        mapping = {
            'pollice': self.dimensioni.POLLICE,
            'indice': self.dimensioni.INDICE,
            'medio': self.dimensioni.MEDIO,
            'anulare': self.dimensioni.ANULARE,
            'mignolo': self.dimensioni.MIGNOLO
        }
        return mapping.get(nome_dito, [4.0, 2.5, 2.0])
    
    def get_posizione_base_dito(self, nome_dito: str) -> Tuple[float, float, float]:
        """Posizione iniziale di ogni dito sul palmo."""
        posizioni = {
            'pollice': (-2.0, 0, 0),
            'indice': (0, self.dimensioni.LUNGHEZZA_PALMO, 0),
            'medio': (0, self.dimensioni.LUNGHEZZA_PALMO + 0.5, 0),
            'anulare': (0, self.dimensioni.LUNGHEZZA_PALMO, 0),
            'mignolo': (0, self.dimensioni.LUNGHEZZA_PALMO - 1, 0)
        }
        return posizioni.get(nome_dito, (0, 0, 0))


class BraccioRobotico:
    """Modello 3D di braccio robotico completo."""
    
    def __init__(self):
        """Inizializza modello braccio."""
        self.dimensioni = DimensioniReali()
        
        # Angoli articolazioni (gradi)
        self.angolo_spalla = 0      # Alzare/abbassare
        self.angolo_gomito = 0      # Piegare braccio
        self.angolo_polso = 0       # Ruotare polso
        
        # Mano attaccata
        self.mano = ManoRobotica()
    
    def alza_braccio(self, angolo: float = 90):
        """Alza il braccio."""
        self.angolo_spalla = min(angolo, self.dimensioni.ANGOLO_MAX_SPALLA)
    
    def piega_gomito(self, angolo: float = 90):
        """Piega il gomito."""
        self.angolo_gomito = min(angolo, self.dimensioni.ANGOLO_MAX_GOMITO)
    
    def get_posizione_endpoint(self) -> Tuple[float, float, float]:
        """
        Calcola posizione punto finale (mano) nello spazio.
        
        Returns:
            Coordinate (x, y, z) della mano
        """
        # Cinematica diretta semplificata
        L1 = self.dimensioni.LUNGHEZZA_BRACCIO_SUPERIORE
        L2 = self.dimensioni.LUNGHEZZA_AVAMBRACCIO
        
        theta1 = np.radians(self.angolo_spalla)
        theta2 = np.radians(self.angolo_gomito)
        
        # Calcola posizione 2D (semplificato)
        x = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
        y = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)
        z = 0
        
        return (x, y, z)


class RobotCompleto:
    """Modello 3D robot completo con 2 bracci."""
    
    def __init__(self):
        """Inizializza robot."""
        self.braccio_destro = BraccioRobotico()
        self.braccio_sinistro = BraccioRobotico()
        self.altezza = 150.0  # cm
        self.posizione = (0, 0, 0)  # Posizione base
    
    def get_stato_completo(self) -> Dict:
        """Ritorna stato completo del robot."""
        return {
            'braccio_destro': {
                'spalla': self.braccio_destro.angolo_spalla,
                'gomito': self.braccio_destro.angolo_gomito,
                'polso': self.braccio_destro.angolo_polso,
                'mano': self.braccio_destro.mano.angoli_dita
            },
            'braccio_sinistro': {
                'spalla': self.braccio_sinistro.angolo_spalla,
                'gomito': self.braccio_sinistro.angolo_gomito,
                'polso': self.braccio_sinistro.angolo_polso,
                'mano': self.braccio_sinistro.mano.angoli_dita
            },
            'posizione': self.posizione,
            'altezza': self.altezza
        }

