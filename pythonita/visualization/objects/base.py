"""Classe base per oggetti 3D."""

import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PhysicsProperties:
    """Proprietà fisiche oggetto."""
    mass: float = 0.1  # kg
    graspable: bool = True
    fragile: bool = False


class Object3D(ABC):
    """Classe base astratta per oggetti 3D nella scena."""
    
    def __init__(self, name: str, position: tuple = (0, 15, 0)):
        self.name = name
        self.position = np.array(position, dtype=float)
        self.rotation = np.array([0, 0, 0], dtype=float)
        self.color = (0.5, 0.5, 0.5)  # RGB
        self.alpha = 1.0
        self.physics = PhysicsProperties()
        self.visible = True
        self.grasped = False
    
    @abstractmethod
    def get_mesh(self):
        """Ritorna mesh 3D (X, Y, Z arrays)."""
        pass
    
    def render(self, ax):
        """Renderizza oggetto su axes matplotlib."""
        if not self.visible:
            return
        
        try:
            X, Y, Z = self.get_mesh()
            ax.plot_surface(X, Y, Z, color=self.color, alpha=self.alpha,
                          shade=True, antialiased=True, edgecolor='none')
            
            # Label
            ax.text(self.position[0], self.position[1], self.position[2] + 8,
                   self.name, fontsize=8, ha='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        except Exception:
            pass  # Silently fail if mesh errors

