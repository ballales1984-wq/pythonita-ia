"""
License Manager - Gestione centralizzata licenze.
Design Pattern: Singleton + Repository
"""

import hashlib
import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Optional, Tuple
import logging

from .tier import Tier

logger = logging.getLogger(__name__)


@dataclass
class License:
    """Rappresenta una licenza attiva."""
    key: str
    tier: Tier
    email: str
    activated_at: datetime
    expires_at: Optional[datetime]
    hardware_id: str
    activations_count: int = 1
    max_activations: int = 1
    is_valid: bool = True


class LicenseManager:
    """
    Gestore licenze - Singleton.
    Gestisce validazione, attivazione e persistenza.
    """
    
    _instance: Optional['LicenseManager'] = None
    SECRET_KEY = "PYTHONITA_SECRET_2025_CHANGE_ME"  # CAMBIARE in production!
    
    def __init__(self):
        """Inizializza license manager."""
        self.license_file = Path.home() / ".pythonita" / "license.json"
        self.license_file.parent.mkdir(parents=True, exist_ok=True)
        self.current_license: Optional[License] = None
        self._load_license()
    
    @classmethod
    def get_instance(cls) -> 'LicenseManager':
        """Ottiene istanza singleton."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _load_license(self):
        """Carica licenza da disco se esiste."""
        if self.license_file.exists():
            try:
                with open(self.license_file, 'r') as f:
                    data = json.load(f)
                
                # Ricostruisci oggetto License
                data['tier'] = Tier(data['tier'])
                data['activated_at'] = datetime.fromisoformat(data['activated_at'])
                if data.get('expires_at'):
                    data['expires_at'] = datetime.fromisoformat(data['expires_at'])
                
                self.current_license = License(**data)
                logger.info(f"Licenza caricata: {self.current_license.tier}")
                
            except Exception as e:
                logger.error(f"Errore caricamento licenza: {e}")
    
    def _save_license(self, license_obj: License):
        """Salva licenza su disco."""
        try:
            data = asdict(license_obj)
            data['tier'] = license_obj.tier.value
            data['activated_at'] = license_obj.activated_at.isoformat()
            if license_obj.expires_at:
                data['expires_at'] = license_obj.expires_at.isoformat()
            
            with open(self.license_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info("Licenza salvata")
        except Exception as e:
            logger.error(f"Errore salvataggio licenza: {e}")
    
    def validate_key(self, key: str) -> Tuple[bool, Tier, str]:
        """
        Valida una chiave licenza.
        
        Returns:
            (valida, tier, messaggio)
        """
        key_clean = key.replace("-", "").replace(" ", "").upper()
        
        # Chiavi speciali
        if key_clean == "TRIAL123":
            return True, Tier.TRIAL, "Trial 14 giorni"
        
        if key_clean == "FREE456":
            return True, Tier.FREE, "Versione gratuita"
        
        # TODO: Validazione con server online
        # Per ora: chiavi di test
        test_keys = {
            "PERSONAL2025TEST": Tier.PERSONAL,
            "PRO2025TESTKEY1": Tier.PRO,
            "ENTERPRISE2025K": Tier.ENTERPRISE,
        }
        
        if key_clean in test_keys:
            tier = test_keys[key_clean]
            return True, tier, f"Licenza {tier} valida"
        
        return False, Tier.FREE, "Chiave non valida"
    
    def activate_license(self, key: str, email: str = "") -> Tuple[bool, str]:
        """
        Attiva una licenza.
        
        Returns:
            (success, messaggio)
        """
        valid, tier, msg = self.validate_key(key)
        
        if not valid:
            return False, msg
        
        # Crea licenza
        now = datetime.now()
        expires = None
        
        if tier == Tier.TRIAL:
            expires = now + timedelta(days=14)
        elif tier in [Tier.PERSONAL, Tier.PRO]:
            expires = now + timedelta(days=365)  # 1 anno
        # ENTERPRISE: nessuna scadenza
        
        license_obj = License(
            key=key,
            tier=tier,
            email=email,
            activated_at=now,
            expires_at=expires,
            hardware_id=self._get_hardware_id(),
            activations_count=1,
            max_activations=self._get_max_activations(tier)
        )
        
        self.current_license = license_obj
        self._save_license(license_obj)
        
        return True, f"Licenza {tier} attivata con successo!"
    
    def check_active_license(self) -> Tuple[bool, Tier, str]:
        """
        Verifica se licenza attiva è valida.
        
        Returns:
            (attiva, tier, messaggio)
        """
        if not self.current_license:
            return False, Tier.FREE, "Nessuna licenza attiva"
        
        # Check scadenza
        if self.current_license.expires_at:
            if datetime.now() > self.current_license.expires_at:
                return False, Tier.FREE, "Licenza scaduta"
        
        # Revalida chiave
        valid, tier, msg = self.validate_key(self.current_license.key)
        
        if not valid:
            return False, Tier.FREE, "Licenza non più valida"
        
        return True, self.current_license.tier, "Licenza attiva"
    
    def get_current_tier(self) -> Tier:
        """Ottiene tier corrente (FREE se nessuna licenza)."""
        if self.current_license and self.current_license.is_valid:
            return self.current_license.tier
        return Tier.FREE
    
    def _get_hardware_id(self) -> str:
        """Genera ID univoco hardware."""
        try:
            mac = uuid.getnode()
            mac_str = ':'.join(['{:02x}'.format((mac >> i) & 0xff) 
                               for i in range(0, 48, 8)])
            return hashlib.md5(mac_str.encode()).hexdigest()[:16]
        except:
            return "unknown"
    
    def _get_max_activations(self, tier: Tier) -> int:
        """Numero massimo attivazioni per tier."""
        limits = {
            Tier.FREE: 1,
            Tier.TRIAL: 1,
            Tier.PERSONAL: 1,
            Tier.PRO: 3,
            Tier.ENTERPRISE: -1  # illimitate
        }
        return limits.get(tier, 1)


def check_license() -> Tuple[bool, Tier, str]:
    """Helper function per check licenza."""
    return LicenseManager.get_instance().check_active_license()

