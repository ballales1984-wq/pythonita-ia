"""Modello 3D braccio robotico."""

import numpy as np


class RoboticArm:
    """Braccio robotico con spalla, gomito e mano."""
    
    # Dimensioni reali (cm)
    UPPER_ARM_LENGTH = 30.0  # Omero
    FOREARM_LENGTH = 25.0    # Ulna/radio
    
    def __init__(self):
        self.shoulder_angle = 0  # gradi
        self.elbow_angle = 0
        self.wrist_angle = 0
        self.hand = None  # RoboticHand opzionale
    
    def lift(self, angle: float):
        """Alza braccio (spalla)."""
        self.shoulder_angle = min(angle, 180)
    
    def bend_elbow(self, angle: float):
        """Piega gomito."""
        self.elbow_angle = min(angle, 150)
    
    def get_endpoint_position(self) -> tuple:
        """
        Calcola posizione endpoint (mano) - Forward Kinematics.
        
        Returns:
            (x, y, z) coordinate in cm
        """
        L1 = self.UPPER_ARM_LENGTH
        L2 = self.FOREARM_LENGTH
        
        theta1 = np.radians(self.shoulder_angle)
        theta2 = np.radians(self.elbow_angle)
        
        x = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
        y = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)
        z = 0
        
        return (x, y, z)
    
    def render(self, ax):
        """Renderizza braccio su axes matplotlib."""
        # Origine (spalla)
        p0 = np.array([0, 0, 30])
        
        # Braccio superiore
        L1 = self.UPPER_ARM_LENGTH
        theta1 = np.radians(self.shoulder_angle)
        p1 = p0 + np.array([L1 * np.cos(theta1), L1 * np.sin(theta1), 0])
        
        # Avambraccio
        L2 = self.FOREARM_LENGTH
        theta2 = theta1 + np.radians(self.elbow_angle)
        p2 = p1 + np.array([L2 * np.cos(theta2), L2 * np.sin(theta2), 0])
        
        # Disegna segmenti
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]],
               'b-', linewidth=6, label='Upper Arm')
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
               'r-', linewidth=6, label='Forearm')
        
        # Giunture
        ax.scatter(*p0, color='black', s=100)
        ax.scatter(*p1, color='green', s=100)
        ax.scatter(*p2, color='red', s=100)

