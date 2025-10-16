"""
Tier system e feature gating.
Controlla quali features sono disponibili per ogni tier di licenza.
"""

from enum import Enum
from typing import Set
import logging

logger = logging.getLogger(__name__)


class Tier(Enum):
    """Tier di licenza disponibili."""
    FREE = "free"
    TRIAL = "trial"
    PERSONAL = "personal"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    
    def __str__(self):
        return self.value.upper()


class Feature(Enum):
    """Features disponibili in Pythonita."""
    BASIC_COMMANDS = "basic_commands"              # 20 comandi base
    ADVANCED_COMMANDS = "advanced_commands"        # 143 comandi completi
    GUI_CLASSIC = "gui_classic"                    # GUI senza 3D
    VISUALIZER_3D = "visualizer_3d"                # Visualizzatore 3D mano
    OBJECTS_3D = "objects_3d"                      # Oggetti interattivi
    TEMPLATE_ROBOTICS = "template_robotics"        # Template robot
    MULTI_COMMAND = "multi_command"                # Multi-comando
    AI_ENGINE = "ai_engine"                        # AI locale (Ollama)
    CACHE_SYSTEM = "cache_system"                  # Cache intelligente
    SOURCE_CODE = "source_code"                    # Accesso codice sorgente
    PRIORITY_SUPPORT = "priority_support"          # Supporto prioritario
    CUSTOM_TEMPLATES = "custom_templates"          # Template personalizzati


class FeatureGate:
    """
    Feature gating per tier.
    Controlla accesso features basato su licenza.
    """
    
    # Matrice features per tier
    FEATURE_MATRIX: Dict[Feature, Set[Tier]] = {
        Feature.BASIC_COMMANDS: {
            Tier.FREE, Tier.TRIAL, Tier.PERSONAL, Tier.PRO, Tier.ENTERPRISE
        },
        Feature.ADVANCED_COMMANDS: {
            Tier.TRIAL, Tier.PERSONAL, Tier.PRO, Tier.ENTERPRISE
        },
        Feature.GUI_CLASSIC: {
            Tier.TRIAL, Tier.PERSONAL, Tier.PRO, Tier.ENTERPRISE
        },
        Feature.VISUALIZER_3D: {
            Tier.TRIAL, Tier.PRO, Tier.ENTERPRISE
        },
        Feature.OBJECTS_3D: {
            Tier.TRIAL, Tier.PRO, Tier.ENTERPRISE
        },
        Feature.TEMPLATE_ROBOTICS: {
            Tier.TRIAL, Tier.PRO, Tier.ENTERPRISE
        },
        Feature.MULTI_COMMAND: {
            Tier.TRIAL, Tier.PRO, Tier.ENTERPRISE
        },
        Feature.AI_ENGINE: {
            Tier.TRIAL, Tier.PRO, Tier.ENTERPRISE
        },
        Feature.CACHE_SYSTEM: {
            Tier.PERSONAL, Tier.PRO, Tier.ENTERPRISE
        },
        Feature.SOURCE_CODE: {
            Tier.ENTERPRISE
        },
        Feature.PRIORITY_SUPPORT: {
            Tier.PRO, Tier.ENTERPRISE
        },
        Feature.CUSTOM_TEMPLATES: {
            Tier.ENTERPRISE
        },
    }
    
    # Limiti per tier
    TIER_LIMITS = {
        Tier.FREE: {
            "max_commands_per_day": 50,
            "max_cache_size": 0,
            "max_pcs": 1,
        },
        Tier.TRIAL: {
            "max_commands_per_day": -1,  # illimitati
            "max_cache_size": 100,
            "max_pcs": 1,
            "trial_days": 14,
        },
        Tier.PERSONAL: {
            "max_commands_per_day": -1,
            "max_cache_size": 100,
            "max_pcs": 1,
        },
        Tier.PRO: {
            "max_commands_per_day": -1,
            "max_cache_size": 500,
            "max_pcs": 3,
        },
        Tier.ENTERPRISE: {
            "max_commands_per_day": -1,
            "max_cache_size": -1,  # illimitata
            "max_pcs": -1,  # illimitati
        },
    }
    
    @staticmethod
    def can_use(feature: Feature, tier: Tier) -> bool:
        """
        Verifica se un tier può usare una feature.
        
        Args:
            feature: Feature da controllare
            tier: Tier utente
            
        Returns:
            True se feature disponibile
        """
        allowed_tiers = FeatureGate.FEATURE_MATRIX.get(feature, set())
        can = tier in allowed_tiers
        
        if not can:
            logger.warning(f"Feature {feature} non disponibile per tier {tier}")
        
        return can
    
    @staticmethod
    def get_limit(tier: Tier, limit_name: str) -> int:
        """Ottiene limite per tier."""
        limits = FeatureGate.TIER_LIMITS.get(tier, {})
        return limits.get(limit_name, 0)
    
    @staticmethod
    def get_available_features(tier: Tier) -> List[Feature]:
        """Ottiene lista features disponibili per tier."""
        return [
            feature for feature, tiers in FeatureGate.FEATURE_MATRIX.items()
            if tier in tiers
        ]


# Helper function
def can_use_feature(feature: Feature, tier: Tier) -> bool:
    """Helper rapido per check feature."""
    return FeatureGate.can_use(feature, tier)

