"""
Renderer 3D - Engine di rendering per visualizzazione robot e oggetti.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class Scene3D:
    """Scena 3D contenente oggetti e robot."""
    
    def __init__(self):
        self.objects: List = []
        self.robot = None
        self.background_color = (0.95, 0.95, 0.95)
    
    def add_object(self, obj):
        """Aggiungi oggetto alla scena."""
        self.objects.append(obj)
    
    def remove_object(self, obj):
        """Rimuovi oggetto dalla scena."""
        if obj in self.objects:
            self.objects.remove(obj)
    
    def set_robot(self, robot):
        """Imposta robot nella scena."""
        self.robot = robot


class Renderer3D:
    """
    Engine di rendering 3D.
    Gestisce finestra, assi, camera e rendering loop.
    """
    
    def __init__(self, title="Pythonita IA 3D", size=(14, 9)):
        """
        Inizializza renderer.
        
        Args:
            title: Titolo finestra
            size: Dimensioni figura (width, height) in inches
        """
        self.fig = plt.figure(figsize=size)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.title = title
        self.scene = Scene3D()
        self.setup_axes()
    
    def setup_axes(self):
        """Configura assi 3D."""
        self.ax.set_xlabel('X (cm)', fontsize=9)
        self.ax.set_ylabel('Y (cm)', fontsize=9)
        self.ax.set_zlabel('Z (cm)', fontsize=9)
        self.ax.set_title(self.title, fontsize=12, fontweight='bold')
        
        # Limiti default
        self.set_view_limits([-15, 15], [0, 15], [-15, 15])
        
        # Vista isometrica
        self.ax.view_init(elev=20, azim=45)
        
        # Grid e background
        self.ax.grid(True, alpha=0.3)
        self.ax.set_facecolor(self.scene.background_color)
        self.fig.patch.set_facecolor('white')
    
    def set_view_limits(self, x_lim, y_lim, z_lim):
        """Imposta limiti vista."""
        self.ax.set_xlim(x_lim)
        self.ax.set_ylim(y_lim)
        self.ax.set_zlim(z_lim)
    
    def clear(self):
        """Pulisce scena."""
        self.ax.clear()
        self.setup_axes()
    
    def render_frame(self):
        """
        Renderizza un frame della scena.
        Disegna robot e tutti gli oggetti.
        """
        self.clear()
        
        # Render robot
        if self.scene.robot:
            self.scene.robot.render(self.ax)
        
        # Render oggetti
        for obj in self.scene.objects:
            obj.render(self.ax)
        
        # Update display
        plt.draw()
        plt.pause(0.01)
    
    def show(self):
        """Mostra finestra (blocking)."""
        plt.show()
    
    def close(self):
        """Chiudi finestra."""
        plt.close(self.fig)

