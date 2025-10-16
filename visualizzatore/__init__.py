"""
Modulo di visualizzazione 3D per Pythonita IA.
Include modelli robot, oggetti 3D interattivi e rendering avanzato.
"""

from .modelli_3d import ManoRobotica, BraccioRobotico, RobotCompleto, DimensioniReali
from .viewer_3d import VisualizzatoreMano3D, VisualizzatoreBraccio3D
from .oggetti_3d import (
    Oggetto3D, Mela, Palla, Cubo, Bottiglia,
    Smartphone, Tazza, GestoreOggetti, crea_oggetto
)

__all__ = [
    # Modelli robot
    'ManoRobotica',
    'BraccioRobotico',
    'RobotCompleto',
    'DimensioniReali',
    
    # Visualizzatori
    'VisualizzatoreMano3D',
    'VisualizzatoreBraccio3D',
    
    # Oggetti 3D
    'Oggetto3D',
    'Mela',
    'Palla',
    'Cubo',
    'Bottiglia',
    'Smartphone',
    'Tazza',
    'GestoreOggetti',
    'crea_oggetto',
]

