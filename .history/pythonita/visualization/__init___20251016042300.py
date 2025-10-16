"""
Sistema di visualizzazione 3D per Pythonita IA.
Rendering robot, oggetti e animazioni.
"""

from .renderer import Renderer3D, Scene3D
from .robot import RoboticHand, RoboticArm
from .objects import Object3D, Apple, Ball, Cube
from .animations import Animation, GraspAnimation, OpenHandAnimation

__all__ = [
    # Rendering
    'Renderer3D',
    'Scene3D',
    
    # Robot models
    'RoboticHand',
    'RoboticArm',
    
    # Objects
    'Object3D',
    'Apple',
    'Ball',
    'Cube',
    
    # Animations
    'Animation',
    'GraspAnimation',
    'OpenHandAnimation',
]

