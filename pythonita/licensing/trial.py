"""Gestione trial 14 giorni."""

from datetime import datetime, timedelta
from pathlib import Path
import json

class TrialManager:
    """Gestisce periodo trial."""
    
    TRIAL_DAYS = 14
    
    @staticmethod
    def is_trial_active() -> Tuple[bool, int]:
        """
        Verifica se trial è attivo.
        
        Returns:
            (attivo, giorni_rimasti)
        """
        trial_file = Path.home() / ".pythonita" / "trial.json"
        
        if not trial_file.exists():
            # Primo avvio - inizia trial
            TrialManager._start_trial()
            return True, TrialManager.TRIAL_DAYS
        
        try:
            with open(trial_file, 'r') as f:
                data = json.load(f)
            
            start = datetime.fromisoformat(data['started_at'])
            elapsed = (datetime.now() - start).days
            remaining = TrialManager.TRIAL_DAYS - elapsed
            
            if remaining > 0:
                return True, remaining
            else:
                return False, 0
                
        except:
            return False, 0
    
    @staticmethod
    def _start_trial():
        """Inizia periodo trial."""
        trial_file = Path.home() / ".pythonita" / "trial.json"
        trial_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "started_at": datetime.now().isoformat(),
            "version": "3.1.0"
        }
        
        with open(trial_file, 'w') as f:
            json.dump(data, f)


def is_trial_active() -> bool:
    """Helper: verifica se trial è attivo."""
    active, _ = TrialManager.is_trial_active()
    return active

