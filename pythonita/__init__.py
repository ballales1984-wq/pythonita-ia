"""
Pythonita IA - Sistema Professionale di Traduzione NLP Italiano → Python

Software commerciale per generazione codice da linguaggio naturale
con visualizzatore 3D robot integrato.

Copyright © 2025 - Tutti i diritti riservati
Licenza: Proprietaria (vedi LICENSE)
"""

__version__ = "3.1.0"
__author__ = "Pythonita Team"
__license__ = "Proprietary"

# API pubblica principale
from .core import CodeGenerator, parse_italian
from .visualization import RoboticHand, Renderer3D
from .licensing import LicenseManager, check_license

__all__ = [
    # Version info
    '__version__',
    
    # Core API
    'CodeGenerator',
    'parse_italian',
    
    # Visualization
    'RoboticHand',
    'Renderer3D',
    
    # Licensing
    'LicenseManager',
    'check_license',
]

