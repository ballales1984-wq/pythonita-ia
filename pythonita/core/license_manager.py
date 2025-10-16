"""
Sistema di Gestione Licenze per Pythonita IA
Protegge il software da uso non autorizzato.
"""

import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import uuid


class LicenseManager:
    """Gestisce validazione e attivazione licenze."""
    
    def __init__(self):
        """Inizializza license manager."""
        self.license_file = Path.home() / ".pythonita" / "license.dat"
        self.license_file.parent.mkdir(exist_ok=True)
        
        # Chiave segreta per generare licenze
        # CAMBIALA CON UNA TUA!
        self.secret_key = "PYTHONITA_SECRET_KEY_2025"
    
    def genera_chiave_licenza(self, tipo="PERSONALE", email="", durata_giorni=365):
        """
        Genera chiave licenza.
        
        Args:
            tipo: PERSONALE, PRO, ENTERPRISE, TRIAL
            email: Email cliente
            durata_giorni: Durata licenza in giorni
            
        Returns:
            Chiave licenza formato: XXXX-XXXX-XXXX-XXXX
        """
        # Crea dati licenza
        scadenza = (datetime.now() + timedelta(days=durata_giorni)).isoformat()
        
        data = f"{tipo}|{email}|{scadenza}|{self.secret_key}"
        
        # Genera hash
        hash_obj = hashlib.sha256(data.encode())
        hash_hex = hash_obj.hexdigest()[:16].upper()
        
        # Formatta come XXXX-XXXX-XXXX-XXXX
        key = "-".join([hash_hex[i:i+4] for i in range(0, 16, 4)])
        
        # Salva info licenza (per debug)
        license_info = {
            "key": key,
            "tipo": tipo,
            "email": email,
            "scadenza": scadenza,
            "generata": datetime.now().isoformat()
        }
        
        return key, license_info
    
    def valida_licenza(self, chiave):
        """
        Valida una chiave licenza.
        
        Returns:
            (valida: bool, messaggio: str, tipo: str)
        """
        if not chiave or len(chiave) < 10:
            return False, "Chiave licenza non valida", "NESSUNA"
        
        # Rimuovi trattini
        chiave_pulita = chiave.replace("-", "").upper()
        
        # Controlla licenze speciali
        if chiave_pulita == "TRIAL123":
            return self._valida_trial()
        
        if chiave_pulita == "FREE456":
            return True, "Licenza FREE valida (funzioni limitate)", "FREE"
        
        # TODO: Implementa validazione con database o API
        # Per ora accetta chiavi di test
        chiavi_test = [
            "1234567890ABCDEF",  # Test personale
            "ABCD1234EFGH5678",  # Test pro
            "ENTERPRISE2025YEAR"  # Test enterprise
        ]
        
        if chiave_pulita in [k.replace("-", "") for k in chiavi_test]:
            return True, "Licenza di test valida", "PRO"
        
        return False, "Chiave licenza non riconosciuta", "NESSUNA"
    
    def _valida_trial(self):
        """Valida licenza trial (14 giorni)."""
        # Controlla se già usata
        if self.license_file.exists():
            try:
                with open(self.license_file, 'r') as f:
                    data = json.load(f)
                
                if "trial_start" in data:
                    start = datetime.fromisoformat(data["trial_start"])
                    if (datetime.now() - start).days > 14:
                        return False, "Trial scaduto (14 giorni)", "TRIAL_SCADUTO"
                    
                    return True, f"Trial valido (giorni rimasti: {14 - (datetime.now() - start).days})", "TRIAL"
            except:
                pass
        
        # Prima volta: crea trial
        self._salva_licenza({
            "tipo": "TRIAL",
            "trial_start": datetime.now().isoformat(),
            "key": "TRIAL123"
        })
        
        return True, "Trial attivato (14 giorni)", "TRIAL"
    
    def attiva_licenza(self, chiave):
        """
        Attiva licenza sul sistema.
        
        Returns:
            (success: bool, messaggio: str)
        """
        valida, msg, tipo = self.valida_licenza(chiave)
        
        if not valida:
            return False, msg
        
        # Salva licenza
        license_data = {
            "key": chiave,
            "tipo": tipo,
            "attivata": datetime.now().isoformat(),
            "hardware_id": self._get_hardware_id(),
            "attivazioni": 1
        }
        
        self._salva_licenza(license_data)
        
        return True, f"Licenza {tipo} attivata con successo!"
    
    def controlla_licenza_attiva(self):
        """
        Controlla se esiste licenza attiva.
        
        Returns:
            (attiva: bool, tipo: str, messaggio: str)
        """
        if not self.license_file.exists():
            return False, "NESSUNA", "Nessuna licenza trovata"
        
        try:
            with open(self.license_file, 'r') as f:
                data = json.load(f)
            
            # Rivalidazione
            valida, msg, tipo = self.valida_licenza(data.get("key", ""))
            
            if valida:
                return True, tipo, msg
            else:
                return False, "SCADUTA", msg
                
        except Exception as e:
            return False, "ERRORE", f"Errore lettura licenza: {e}"
    
    def _salva_licenza(self, data):
        """Salva dati licenza su disco."""
        try:
            with open(self.license_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Errore salvataggio licenza: {e}")
    
    def _get_hardware_id(self):
        """Genera ID univoco hardware (per binding)."""
        try:
            # Usa MAC address come ID
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) 
                           for i in range(0, 48, 8)])
            return hashlib.md5(mac.encode()).hexdigest()[:16]
        except:
            return "unknown"
    
    def features_disponibili(self, tipo_licenza):
        """
        Ritorna features disponibili per tipo licenza.
        
        Returns:
            dict con feature: bool
        """
        features = {
            "FREE": {
                "comandi_base": True,
                "comandi_completi": False,
                "gui_classica": False,
                "visualizzatore_3d": False,
                "template_robotica": False,
                "cache": False,
                "multi_comando": False,
                "max_comandi_giorno": 50
            },
            "TRIAL": {
                "comandi_base": True,
                "comandi_completi": True,
                "gui_classica": True,
                "visualizzatore_3d": True,
                "template_robotica": True,
                "cache": True,
                "multi_comando": True,
                "max_comandi_giorno": 200
            },
            "PERSONALE": {
                "comandi_base": True,
                "comandi_completi": True,
                "gui_classica": True,
                "visualizzatore_3d": False,
                "template_robotica": False,
                "cache": True,
                "multi_comando": True,
                "max_comandi_giorno": -1  # illimitati
            },
            "PRO": {
                "comandi_base": True,
                "comandi_completi": True,
                "gui_classica": True,
                "visualizzatore_3d": True,
                "template_robotica": True,
                "cache": True,
                "multi_comando": True,
                "oggetti_3d": True,
                "max_comandi_giorno": -1
            },
            "ENTERPRISE": {
                "comandi_base": True,
                "comandi_completi": True,
                "gui_classica": True,
                "visualizzatore_3d": True,
                "template_robotica": True,
                "cache": True,
                "multi_comando": True,
                "oggetti_3d": True,
                "codice_sorgente": True,
                "supporto_prioritario": True,
                "max_comandi_giorno": -1
            }
        }
        
        return features.get(tipo_licenza, features["FREE"])


def mostra_schermata_attivazione():
    """Mostra schermata di attivazione licenza."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║               PYTHONITA IA v3.1 - ATTIVAZIONE                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

Inserisci la tua chiave di licenza per attivare Pythonita IA.

OPZIONI:
1. Inserisci chiave licenza acquistata
2. Attiva trial gratuito 14 giorni (TRIAL123)
3. Usa versione FREE limitata (FREE456)
4. Acquista licenza ora

""")
    
    scelta = input("Scelta (1-4): ").strip()
    
    manager = LicenseManager()
    
    if scelta == "1":
        chiave = input("\nInserisci chiave licenza: ").strip()
        success, msg = manager.attiva_licenza(chiave)
        print(f"\n{msg}\n")
        return success
        
    elif scelta == "2":
        success, msg = manager.attiva_licenza("TRIAL123")
        print(f"\n{msg}\n")
        return True
        
    elif scelta == "3":
        success, msg = manager.attiva_licenza("FREE456")
        print(f"\n{msg}\n")
        return True
        
    elif scelta == "4":
        print("""
Acquista Pythonita IA su:
https://gumroad.com/l/pythonita-ia

Prezzi:
- Personale: €49 (GUI + comandi completi)
- Pro: €149 (3D + robotica)
- Enterprise: €499 (codice sorgente + supporto)
""")
        return False
    
    return False


# Singleton instance
_license_manager = None

def get_license_manager():
    """Ottiene istanza singleton license manager."""
    global _license_manager
    if _license_manager is None:
        _license_manager = LicenseManager()
    return _license_manager


if __name__ == "__main__":
    # Test generazione licenze
    manager = LicenseManager()
    
    print("GENERAZIONE LICENZE DI TEST")
    print("="*70)
    
    # Genera licenze di test
    for tipo in ["PERSONALE", "PRO", "ENTERPRISE"]:
        key, info = manager.genera_chiave_licenza(tipo, f"test@{tipo.lower()}.com")
        print(f"\n{tipo}:")
        print(f"  Chiave: {key}")
        print(f"  Info: {info}")
    
    print("\n" + "="*70)
    print("\nTEST VALIDAZIONE:")
    
    # Test validazione
    test_keys = ["TRIAL123", "FREE456", "1234-5678-90AB-CDEF"]
    
    for key in test_keys:
        valida, msg, tipo = manager.valida_licenza(key)
        print(f"\n{key}: {'✅' if valida else '❌'} {msg} ({tipo})")

