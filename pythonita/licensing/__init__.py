"""
Sistema licensing commerciale per Pythonita IA.
Gestisce attivazione, validazione e feature gating.
"""

from .license_manager import LicenseManager, License
from .tier import Tier, FeatureGate, can_use_feature
from .activation import activate_license, check_activation
from .trial import TrialManager, is_trial_active

__all__ = [
    # Core licensing
    'LicenseManager',
    'License',
    
    # Tiers & features
    'Tier',
    'FeatureGate',
    'can_use_feature',
    
    # Activation
    'activate_license',
    'check_activation',
    
    # Trial
    'TrialManager',
    'is_trial_active',
]

# Convenience function
def check_license() -> Tuple[bool, Tier, str]:
    """
    Verifica licenza attiva.
    
    Returns:
        (valida, tier, messaggio)
    """
    manager = LicenseManager.get_instance()
    return manager.check_active_license()

