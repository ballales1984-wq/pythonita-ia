"""
Sistema di oggetti 3D afferrabili.
Mesh 3D con colori, fisica base e interazioni.
"""

import numpy as np
from typing import Tuple, List, Optional
from dataclasses import dataclass


@dataclass
class ProprietaFisiche:
    """Proprietà fisiche di un oggetto."""
    massa: float  # kg
    afferrabile: bool = True
    fragile: bool = False
    dimensioni: Tuple[float, float, float] = (10, 10, 10)  # cm


class Oggetto3D:
    """Classe base per oggetti 3D nella scena."""
    
    def __init__(self, nome: str, posizione: Tuple[float, float, float] = (0, 15, 0)):
        """
        Inizializza oggetto 3D.
        
        Args:
            nome: Nome dell'oggetto
            posizione: Posizione (x, y, z) in cm
        """
        self.nome = nome
        self.posizione = np.array(posizione, dtype=float)
        self.rotazione = np.array([0, 0, 0], dtype=float)  # Euler angles (gradi)
        self.scala = 1.0
        self.colore = (0.5, 0.5, 0.5)  # RGB
        self.alpha = 1.0  # Trasparenza
        self.visibile = True
        self.afferrato = False
        self.proprieta = ProprietaFisiche(massa=0.1)
        
    def get_bounding_box(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Ritorna bounding box dell'oggetto.
        
        Returns:
            (min_point, max_point) in coordinate mondo
        """
        dim = np.array(self.proprieta.dimensioni) / 2
        min_p = self.posizione - dim
        max_p = self.posizione + dim
        return min_p, max_p
    
    def distanza_da(self, punto: np.ndarray) -> float:
        """Calcola distanza da un punto."""
        return np.linalg.norm(self.posizione - punto)
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Ritorna mesh 3D dell'oggetto (X, Y, Z arrays per plot_surface).
        Override in sottoclassi.
        """
        raise NotImplementedError


class Mela(Oggetto3D):
    """Mela rossa afferrabile (sfera)."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Mela", posizione)
        self.raggio = 4.0  # cm (diametro 8cm)
        self.colore = (0.9, 0.1, 0.1)  # Rosso
        self.proprieta = ProprietaFisiche(
            massa=0.2,  # kg
            afferrabile=True,
            dimensioni=(self.raggio*2, self.raggio*2, self.raggio*2)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Genera mesh sferica per la mela."""
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 20)
        
        x = self.raggio * np.outer(np.cos(u), np.sin(v)) + self.posizione[0]
        y = self.raggio * np.outer(np.sin(u), np.sin(v)) + self.posizione[1]
        z = self.raggio * np.outer(np.ones(np.size(u)), np.cos(v)) + self.posizione[2]
        
        return x, y, z


class Palla(Oggetto3D):
    """Palla da basket (sfera arancione)."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Palla", posizione)
        self.raggio = 11.0  # cm (diametro 22cm)
        self.colore = (1.0, 0.6, 0.0)  # Arancione
        self.proprieta = ProprietaFisiche(
            massa=0.6,
            afferrabile=True,
            dimensioni=(self.raggio*2, self.raggio*2, self.raggio*2)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Genera mesh sferica."""
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 20)
        
        x = self.raggio * np.outer(np.cos(u), np.sin(v)) + self.posizione[0]
        y = self.raggio * np.outer(np.sin(u), np.sin(v)) + self.posizione[1]
        z = self.raggio * np.outer(np.ones(np.size(u)), np.cos(v)) + self.posizione[2]
        
        return x, y, z


class Cubo(Oggetto3D):
    """Cubo afferrabile."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0), lato: float = 10):
        super().__init__("Cubo", posizione)
        self.lato = lato  # cm
        self.colore = (0.2, 0.4, 0.9)  # Blu
        self.proprieta = ProprietaFisiche(
            massa=0.5,
            afferrabile=True,
            dimensioni=(lato, lato, lato)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Genera mesh cubica (6 facce)."""
        l = self.lato / 2
        p = self.posizione
        
        # Definisci i 6 lati del cubo
        faces = []
        
        # Faccia superiore (z+)
        x = np.array([[p[0]-l, p[0]+l], [p[0]-l, p[0]+l]])
        y = np.array([[p[1]-l, p[1]-l], [p[1]+l, p[1]+l]])
        z = np.array([[p[2]+l, p[2]+l], [p[2]+l, p[2]+l]])
        faces.append((x, y, z))
        
        # Faccia inferiore (z-)
        z = np.array([[p[2]-l, p[2]-l], [p[2]-l, p[2]-l]])
        faces.append((x, y, z))
        
        # Faccia frontale (y+)
        x = np.array([[p[0]-l, p[0]+l], [p[0]-l, p[0]+l]])
        y = np.array([[p[1]+l, p[1]+l], [p[1]+l, p[1]+l]])
        z = np.array([[p[2]-l, p[2]-l], [p[2]+l, p[2]+l]])
        faces.append((x, y, z))
        
        # Faccia posteriore (y-)
        y = np.array([[p[1]-l, p[1]-l], [p[1]-l, p[1]-l]])
        faces.append((x, y, z))
        
        # Faccia destra (x+)
        x = np.array([[p[0]+l, p[0]+l], [p[0]+l, p[0]+l]])
        y = np.array([[p[1]-l, p[1]+l], [p[1]-l, p[1]+l]])
        z = np.array([[p[2]-l, p[2]-l], [p[2]+l, p[2]+l]])
        faces.append((x, y, z))
        
        # Faccia sinistra (x-)
        x = np.array([[p[0]-l, p[0]-l], [p[0]-l, p[0]-l]])
        faces.append((x, y, z))
        
        # Ritorna prima faccia (per semplicità, plot_surface fa una alla volta)
        return faces[0]


class Bottiglia(Oggetto3D):
    """Bottiglia afferrabile (cilindro)."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Bottiglia", posizione)
        self.raggio = 3.5  # cm
        self.altezza = 25.0  # cm
        self.colore = (0.1, 0.7, 0.2)  # Verde
        self.alpha = 0.6  # Trasparente
        self.proprieta = ProprietaFisiche(
            massa=0.5,
            afferrabile=True,
            fragile=True,
            dimensioni=(self.raggio*2, self.raggio*2, self.altezza)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Genera mesh cilindrica."""
        theta = np.linspace(0, 2 * np.pi, 30)
        z = np.linspace(-self.altezza/2, self.altezza/2, 20)
        
        theta_grid, z_grid = np.meshgrid(theta, z)
        
        x = self.raggio * np.cos(theta_grid) + self.posizione[0]
        y = self.raggio * np.sin(theta_grid) + self.posizione[1]
        z = z_grid + self.posizione[2]
        
        return x, y, z


class Smartphone(Oggetto3D):
    """Smartphone afferrabile (box sottile)."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Smartphone", posizione)
        self.larghezza = 7.0  # cm
        self.altezza = 15.0  # cm
        self.spessore = 0.8  # cm
        self.colore = (0.1, 0.1, 0.1)  # Nero
        self.proprieta = ProprietaFisiche(
            massa=0.18,
            afferrabile=True,
            fragile=True,
            dimensioni=(self.larghezza, self.altezza, self.spessore)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Genera mesh box sottile."""
        l = self.larghezza / 2
        h = self.altezza / 2
        s = self.spessore / 2
        p = self.posizione
        
        # Faccia principale (schermo)
        x = np.array([[p[0]-l, p[0]+l], [p[0]-l, p[0]+l]])
        y = np.array([[p[1]-h, p[1]-h], [p[1]+h, p[1]+h]])
        z = np.array([[p[2]+s, p[2]+s], [p[2]+s, p[2]+s]])
        
        return x, y, z


class Tazza(Oggetto3D):
    """Tazza con manico."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Tazza", posizione)
        self.raggio = 4.0  # cm
        self.altezza = 10.0  # cm
        self.colore = (0.9, 0.9, 0.9)  # Bianco
        self.proprieta = ProprietaFisiche(
            massa=0.3,
            afferrabile=True,
            fragile=True,
            dimensioni=(self.raggio*2 + 2, self.raggio*2, self.altezza)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Genera mesh cilindrica (corpo tazza)."""
        theta = np.linspace(0, 2 * np.pi, 30)
        z = np.linspace(0, self.altezza, 15)
        
        theta_grid, z_grid = np.meshgrid(theta, z)
        
        x = self.raggio * np.cos(theta_grid) + self.posizione[0]
        y = self.raggio * np.sin(theta_grid) + self.posizione[1]
        z = z_grid + self.posizione[2] - self.altezza/2
        
        return x, y, z


class GestoreOggetti:
    """Gestisce tutti gli oggetti nella scena 3D."""
    
    def __init__(self):
        self.oggetti: List[Oggetto3D] = []
        self.oggetto_afferrato: Optional[Oggetto3D] = None
    
    def aggiungi_oggetto(self, oggetto: Oggetto3D):
        """Aggiunge oggetto alla scena."""
        self.oggetti.append(oggetto)
    
    def rimuovi_oggetto(self, oggetto: Oggetto3D):
        """Rimuove oggetto dalla scena."""
        if oggetto in self.oggetti:
            self.oggetti.remove(oggetto)
    
    def trova_oggetto_vicino(self, posizione: np.ndarray, raggio: float = 10.0) -> Optional[Oggetto3D]:
        """
        Trova oggetto più vicino a una posizione.
        
        Args:
            posizione: Punto 3D
            raggio: Raggio di ricerca (cm)
            
        Returns:
            Oggetto più vicino o None
        """
        oggetto_vicino = None
        distanza_min = raggio
        
        for obj in self.oggetti:
            if not obj.visibile or obj.afferrato:
                continue
                
            dist = obj.distanza_da(posizione)
            if dist < distanza_min:
                distanza_min = dist
                oggetto_vicino = obj
        
        return oggetto_vicino
    
    def afferra_oggetto(self, oggetto: Oggetto3D, posizione_mano: np.ndarray):
        """
        Afferra un oggetto con la mano.
        
        Args:
            oggetto: Oggetto da afferrare
            posizione_mano: Posizione della mano
        """
        if oggetto and oggetto.proprieta.afferrabile:
            oggetto.afferrato = True
            oggetto.posizione = posizione_mano.copy()
            self.oggetto_afferrato = oggetto
    
    def rilascia_oggetto(self):
        """Rilascia oggetto afferrato."""
        if self.oggetto_afferrato:
            self.oggetto_afferrato.afferrato = False
            self.oggetto_afferrato = None
    
    def aggiorna(self, posizione_mano: Optional[np.ndarray] = None):
        """
        Aggiorna stato oggetti (es. oggetto segue mano se afferrato).
        
        Args:
            posizione_mano: Posizione corrente della mano
        """
        if self.oggetto_afferrato and posizione_mano is not None:
            # Oggetto segue la mano
            self.oggetto_afferrato.posizione = posizione_mano.copy()


# Factory per creare oggetti rapidamente
def crea_oggetto(tipo: str, posizione: Tuple[float, float, float] = (0, 15, 0)) -> Oggetto3D:
    """
    Factory per creare oggetti 3D.
    
    Args:
        tipo: Tipo oggetto ("mela", "palla", "cubo", ecc)
        posizione: Posizione iniziale
        
    Returns:
        Oggetto3D creato
    """
    tipi = {
        "mela": Mela,
        "palla": Palla,
        "cubo": Cubo,
        "bottiglia": Bottiglia,
        "smartphone": Smartphone,
        "telefono": Smartphone,
        "tazza": Tazza,
    }
    
    classe = tipi.get(tipo.lower(), Cubo)
    return classe(posizione)

