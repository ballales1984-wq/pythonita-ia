"""Modello 3D mano robotica - Version refactorata."""

import numpy as np


class Dimensions:
    """Dimensioni antropometriche."""
    PALM_LENGTH = 10.0  # cm
    PALM_WIDTH = 8.5
    FINGER_MAX_ANGLE = 90  # gradi


class RoboticHand:
    """Mano robotica 3D con 5 dita."""
    
    def __init__(self):
        self.dimensions = Dimensions()
        self.finger_angles = {
            'thumb': [0, 0, 0],
            'index': [0, 0, 0],
            'middle': [0, 0, 0],
            'ring': [0, 0, 0],
            'pinky': [0, 0, 0]
        }
        self.wrist_angle = 0
    
    def open(self, speed=1.0):
        """Apri mano."""
        for finger in self.finger_angles:
            self.finger_angles[finger] = [0, 0, 0]
    
    def close(self, force=1.0):
        """Chiudi mano."""
        angle = force * self.dimensions.FINGER_MAX_ANGLE
        for finger in self.finger_angles:
            self.finger_angles[finger] = [angle, angle * 0.8, angle * 0.6]
    
    def pinch(self, aperture=20):
        """Posizione pinza."""
        self.finger_angles['thumb'] = [45, 45, 45]
        self.finger_angles['index'] = [45, 45, 45]
        self.finger_angles['middle'] = [0, 0, 0]
        self.finger_angles['ring'] = [0, 0, 0]
        self.finger_angles['pinky'] = [0, 0, 0]
    
    def render(self, ax):
        """Renderizza mano su axes matplotlib."""
        # Disegna palmo
        w = self.dimensions.PALM_WIDTH
        vertices = np.array([
            [-w/2, 0, -2], [w/2, 0, -2],
            [w/2, 0, 2], [-w/2, 0, 2], [-w/2, 0, -2]
        ])
        ax.plot(vertices[:, 0], vertices[:, 1], vertices[:, 2],
               'k-', linewidth=3, label='Palm')
        
        # Disegna dita (semplificato)
        colors = {'thumb': 'red', 'index': 'blue', 'middle': 'green',
                 'ring': 'orange', 'pinky': 'purple'}
        
        for name, color in colors.items():
            # Calcola posizione dita basata su angoli
            # (semplificato per refactoring)
            ax.plot([0], [10], [0], color=color, marker='o', markersize=5)

