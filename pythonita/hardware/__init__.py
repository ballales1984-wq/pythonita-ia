"""
Pythonita Hardware Module.
Supporto per Arduino, sensori, attuatori, robot fisici.
"""

from .arduino_controller import (
    ArduinoController,
    get_arduino_controller,
    ARDUINO_TEMPLATES
)

__all__ = [
    'ArduinoController',
    'get_arduino_controller',
    'ARDUINO_TEMPLATES'
]

