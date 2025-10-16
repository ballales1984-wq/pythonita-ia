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


# ═══════════════════════════════════════════════════════════════════
# NUOVI OGGETTI 3D - FASE 2.2
# ═══════════════════════════════════════════════════════════════════

# ─── STRUMENTI ───

class Martello(Oggetto3D):
    """Martello da carpentiere."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Martello", posizione)
        self.lunghezza = 25.0  # cm
        self.larghezza_testa = 5.0
        self.colore = (0.4, 0.4, 0.4)  # Grigio metallo
        self.proprieta = ProprietaFisiche(
            massa=0.5,
            afferrabile=True,
            dimensioni=(self.larghezza_testa, self.lunghezza, self.larghezza_testa)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Mesh semplificata del martello (cilindro + box)."""
        # Manico (cilindro)
        theta = np.linspace(0, 2 * np.pi, 20)
        z = np.linspace(0, self.lunghezza * 0.7, 10)
        theta_grid, z_grid = np.meshgrid(theta, z)
        
        raggio_manico = 1.5
        x = raggio_manico * np.cos(theta_grid) + self.posizione[0]
        y = raggio_manico * np.sin(theta_grid) + self.posizione[1]
        z = z_grid + self.posizione[2] - self.lunghezza/3
        
        return x, y, z


class Cacciavite(Oggetto3D):
    """Cacciavite a croce."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Cacciavite", posizione)
        self.lunghezza = 20.0  # cm
        self.colore = (1.0, 0.8, 0.0)  # Giallo (manico)
        self.proprieta = ProprietaFisiche(
            massa=0.15,
            afferrabile=True,
            dimensioni=(2.0, self.lunghezza, 2.0)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Mesh semplificata del cacciavite (cilindro)."""
        theta = np.linspace(0, 2 * np.pi, 20)
        z = np.linspace(0, self.lunghezza, 15)
        theta_grid, z_grid = np.meshgrid(theta, z)
        
        raggio = 1.0
        x = raggio * np.cos(theta_grid) + self.posizione[0]
        y = raggio * np.sin(theta_grid) + self.posizione[1]
        z = z_grid + self.posizione[2] - self.lunghezza/2
        
        return x, y, z


class ChiaveInglese(Oggetto3D):
    """Chiave inglese regolabile."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Chiave Inglese", posizione)
        self.lunghezza = 18.0  # cm
        self.colore = (0.6, 0.6, 0.65)  # Grigio acciaio
        self.proprieta = ProprietaFisiche(
            massa=0.3,
            afferrabile=True,
            dimensioni=(3.0, self.lunghezza, 3.0)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Mesh semplificata della chiave (box allungato)."""
        # Box allungato
        x = np.array([[0, 2], [0, 2]]) + self.posizione[0] - 1
        y = np.array([[0, 0], [self.lunghezza, self.lunghezza]]) + self.posizione[1] - self.lunghezza/2
        z = np.array([[0, 0], [0, 0]]) + self.posizione[2]
        
        return x, y, z


class Pinza(Oggetto3D):
    """Pinza da lavoro."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Pinza", posizione)
        self.lunghezza = 15.0  # cm
        self.colore = (0.3, 0.3, 0.35)  # Grigio scuro
        self.proprieta = ProprietaFisiche(
            massa=0.2,
            afferrabile=True,
            dimensioni=(2.5, self.lunghezza, 2.5)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Mesh semplificata della pinza (cilindro)."""
        theta = np.linspace(0, 2 * np.pi, 20)
        z = np.linspace(0, self.lunghezza, 12)
        theta_grid, z_grid = np.meshgrid(theta, z)
        
        raggio = 1.2
        x = raggio * np.cos(theta_grid) + self.posizione[0]
        y = raggio * np.sin(theta_grid) + self.posizione[1]
        z = z_grid + self.posizione[2] - self.lunghezza/2
        
        return x, y, z


# ─── CIBO ───

class Banana(Oggetto3D):
    """Banana gialla."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Banana", posizione)
        self.lunghezza = 18.0  # cm
        self.raggio = 3.0
        self.colore = (1.0, 0.9, 0.0)  # Giallo banana
        self.proprieta = ProprietaFisiche(
            massa=0.12,
            afferrabile=True,
            dimensioni=(self.raggio*2, self.lunghezza, self.raggio*2)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Mesh semplificata della banana (cilindro curvo)."""
        theta = np.linspace(0, 2 * np.pi, 20)
        z = np.linspace(0, self.lunghezza, 15)
        theta_grid, z_grid = np.meshgrid(theta, z)
        
        # Leggera curvatura
        curva = np.sin(z_grid / self.lunghezza * np.pi) * 3
        
        x = self.raggio * np.cos(theta_grid) + self.posizione[0] + curva
        y = self.raggio * np.sin(theta_grid) + self.posizione[1]
        z = z_grid + self.posizione[2] - self.lunghezza/2
        
        return x, y, z


class Arancia(Oggetto3D):
    """Arancia (sfera arancione)."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Arancia", posizione)
        self.raggio = 6.0  # cm (diametro 12cm)
        self.colore = (1.0, 0.5, 0.0)  # Arancione
        self.proprieta = ProprietaFisiche(
            massa=0.18,
            afferrabile=True,
            dimensioni=(self.raggio*2, self.raggio*2, self.raggio*2)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Mesh sferica per l'arancia."""
        u = np.linspace(0, 2 * np.pi, 25)
        v = np.linspace(0, np.pi, 20)
        
        x = self.raggio * np.outer(np.cos(u), np.sin(v)) + self.posizione[0]
        y = self.raggio * np.outer(np.sin(u), np.sin(v)) + self.posizione[1]
        z = self.raggio * np.outer(np.ones(np.size(u)), np.cos(v)) + self.posizione[2]
        
        return x, y, z


class Panino(Oggetto3D):
    """Panino/sandwich."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Panino", posizione)
        self.larghezza = 10.0  # cm
        self.altezza = 4.0
        self.profondita = 8.0
        self.colore = (0.9, 0.8, 0.5)  # Beige pane
        self.proprieta = ProprietaFisiche(
            massa=0.15,
            afferrabile=True,
            fragile=True,
            dimensioni=(self.larghezza, self.altezza, self.profondita)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Mesh semplificata del panino (box arrotondato)."""
        # Box con facce leggermente arrotondate
        x = np.array([[0, self.larghezza], [0, self.larghezza]]) + self.posizione[0] - self.larghezza/2
        y = np.array([[0, 0], [self.profondita, self.profondita]]) + self.posizione[1] - self.profondita/2
        z = np.array([[0, 0], [0, 0]]) + self.posizione[2]
        
        return x, y, z


# ─── ELETTRONICA ───

class Mouse(Oggetto3D):
    """Mouse per computer."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Mouse", posizione)
        self.lunghezza = 10.0  # cm
        self.larghezza = 6.0
        self.altezza = 4.0
        self.colore = (0.1, 0.1, 0.1)  # Nero
        self.proprieta = ProprietaFisiche(
            massa=0.08,
            afferrabile=True,
            dimensioni=(self.larghezza, self.lunghezza, self.altezza)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Mesh semplificata del mouse (ellissoide)."""
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi/2, 15)  # Solo metà superiore
        
        x = (self.larghezza/2) * np.outer(np.cos(u), np.sin(v)) + self.posizione[0]
        y = (self.lunghezza/2) * np.outer(np.sin(u), np.sin(v)) + self.posizione[1]
        z = (self.altezza) * np.outer(np.ones(np.size(u)), np.cos(v)) + self.posizione[2]
        
        return x, y, z


class Tastiera(Oggetto3D):
    """Tastiera per computer."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Tastiera", posizione)
        self.lunghezza = 40.0  # cm
        self.larghezza = 15.0
        self.altezza = 2.5
        self.colore = (0.2, 0.2, 0.2)  # Grigio scuro
        self.proprieta = ProprietaFisiche(
            massa=0.6,
            afferrabile=True,
            dimensioni=(self.larghezza, self.lunghezza, self.altezza)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Mesh semplificata della tastiera (box piatto)."""
        x = np.array([[0, self.larghezza], [0, self.larghezza]]) + self.posizione[0] - self.larghezza/2
        y = np.array([[0, 0], [self.lunghezza, self.lunghezza]]) + self.posizione[1] - self.lunghezza/2
        z = np.array([[0, 0], [0, 0]]) + self.posizione[2]
        
        return x, y, z


# ─── QUOTIDIANO ───

class Libro(Oggetto3D):
    """Libro chiuso."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Libro", posizione)
        self.larghezza = 15.0  # cm
        self.altezza = 20.0
        self.spessore = 3.0
        self.colore = (0.6, 0.3, 0.1)  # Marrone copertina
        self.proprieta = ProprietaFisiche(
            massa=0.4,
            afferrabile=True,
            dimensioni=(self.larghezza, self.altezza, self.spessore)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Mesh semplificata del libro (box)."""
        x = np.array([[0, self.larghezza], [0, self.larghezza]]) + self.posizione[0] - self.larghezza/2
        y = np.array([[0, 0], [self.altezza, self.altezza]]) + self.posizione[1] - self.altezza/2
        z = np.array([[0, 0], [0, 0]]) + self.posizione[2]
        
        return x, y, z


class Penna(Oggetto3D):
    """Penna a sfera."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Penna", posizione)
        self.lunghezza = 14.0  # cm
        self.colore = (0.0, 0.2, 0.8)  # Blu
        self.proprieta = ProprietaFisiche(
            massa=0.01,
            afferrabile=True,
            dimensioni=(0.8, self.lunghezza, 0.8)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Mesh semplificata della penna (cilindro sottile)."""
        theta = np.linspace(0, 2 * np.pi, 15)
        z = np.linspace(0, self.lunghezza, 12)
        theta_grid, z_grid = np.meshgrid(theta, z)
        
        raggio = 0.4
        x = raggio * np.cos(theta_grid) + self.posizione[0]
        y = raggio * np.sin(theta_grid) + self.posizione[1]
        z = z_grid + self.posizione[2] - self.lunghezza/2
        
        return x, y, z


class Orologio(Oggetto3D):
    """Orologio da polso."""
    
    def __init__(self, posizione: Tuple[float, float, float] = (0, 15, 0)):
        super().__init__("Orologio", posizione)
        self.diametro = 4.0  # cm
        self.spessore = 1.2
        self.colore = (0.7, 0.7, 0.7)  # Grigio argento
        self.proprieta = ProprietaFisiche(
            massa=0.05,
            afferrabile=True,
            dimensioni=(self.diametro, self.diametro, self.spessore)
        )
    
    def get_mesh(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Mesh semplificata dell'orologio (cilindro piatto)."""
        theta = np.linspace(0, 2 * np.pi, 25)
        z = np.linspace(0, self.spessore, 5)
        theta_grid, z_grid = np.meshgrid(theta, z)
        
        raggio = self.diametro / 2
        x = raggio * np.cos(theta_grid) + self.posizione[0]
        y = raggio * np.sin(theta_grid) + self.posizione[1]
        z = z_grid + self.posizione[2] - self.spessore/2
        
        return x, y, z


# ═══════════════════════════════════════════════════════════════════


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

