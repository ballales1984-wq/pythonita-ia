"""Gestione attivazione licenze online."""

from typing import Tuple
from .license_manager import LicenseManager
from .tier import Tier

def activate_license(key: str, email: str = "") -> Tuple[bool, str]:
    """
    Attiva licenza.
    
    Args:
        key: Chiave licenza
        email: Email utente
        
    Returns:
        (success, messaggio)
    """
    manager = LicenseManager.get_instance()
    return manager.activate_license(key, email)


def check_activation() -> Tuple[bool, Tier, str]:
    """
    Verifica se licenza è attivata e valida.
    
    Returns:
        (attiva, tier, messaggio)
    """
    manager = LicenseManager.get_instance()
    return manager.check_active_license()

