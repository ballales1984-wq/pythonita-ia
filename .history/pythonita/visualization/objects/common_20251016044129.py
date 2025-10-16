"""Oggetti 3D comuni (mela, palla, cubo, ecc)."""

import numpy as np
from .base import Object3D, PhysicsProperties


class Apple(Object3D):
    """Mela rossa 3D."""
    
    def __init__(self, position=(0, 15, 0)):
        super().__init__("Apple", position)
        self.radius = 4.0  # cm
        self.color = (0.9, 0.1, 0.1)  # Rosso
        self.physics = PhysicsProperties(mass=0.2, graspable=True)
    
    def get_mesh(self):
        """Genera mesh sferica."""
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 20)
        
        x = self.radius * np.outer(np.cos(u), np.sin(v)) + self.position[0]
        y = self.radius * np.outer(np.sin(u), np.sin(v)) + self.position[1]
        z = self.radius * np.outer(np.ones(np.size(u)), np.cos(v)) + self.position[2]
        
        return x, y, z


class Ball(Object3D):
    """Palla da basket."""
    
    def __init__(self, position=(0, 15, 0)):
        super().__init__("Ball", position)
        self.radius = 11.0  # cm
        self.color = (1.0, 0.6, 0.0)  # Arancione
        self.physics = PhysicsProperties(mass=0.6, graspable=True)
    
    def get_mesh(self):
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 20)
        
        x = self.radius * np.outer(np.cos(u), np.sin(v)) + self.position[0]
        y = self.radius * np.outer(np.sin(u), np.sin(v)) + self.position[1]
        z = self.radius * np.outer(np.ones(np.size(u)), np.cos(v)) + self.position[2]
        
        return x, y, z


class Cube(Object3D):
    """Cubo 3D."""
    
    def __init__(self, position=(0, 15, 0), size=10):
        super().__init__("Cube", position)
        self.size = size
        self.color = (0.2, 0.4, 0.9)  # Blu
        self.physics = PhysicsProperties(mass=0.5, graspable=True)
    
    def get_mesh(self):
        """Genera mesh cubica (faccia superiore semplificata)."""
        l = self.size / 2
        p = self.position
        
        x = np.array([[p[0]-l, p[0]+l], [p[0]-l, p[0]+l]])
        y = np.array([[p[1]-l, p[1]-l], [p[1]+l, p[1]+l]])
        z = np.array([[p[2]+l, p[2]+l], [p[2]+l, p[2]+l]])
        
        return x, y, z


class Bottle(Object3D):
    """Bottiglia cilindrica."""
    
    def __init__(self, position=(0, 15, 0)):
        super().__init__("Bottle", position)
        self.radius = 3.5
        self.height = 25.0
        self.color = (0.1, 0.7, 0.2)  # Verde
        self.alpha = 0.6  # Trasparente
        self.physics = PhysicsProperties(mass=0.5, graspable=True, fragile=True)
    
    def get_mesh(self):
        theta = np.linspace(0, 2 * np.pi, 30)
        z = np.linspace(-self.height/2, self.height/2, 20)
        
        theta_grid, z_grid = np.meshgrid(theta, z)
        
        x = self.radius * np.cos(theta_grid) + self.position[0]
        y = self.radius * np.sin(theta_grid) + self.position[1]
        z = z_grid + self.position[2]
        
        return x, y, z

