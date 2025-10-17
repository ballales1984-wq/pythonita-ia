"""
Sistema di logging errori per Pythonita IA.

Registra tutti gli errori in file di log accessibili.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
import traceback
import json


class ErrorLogger:
    """Logger centralizzato per errori e eventi."""
    
    def __init__(self):
        """Inizializza logger."""
        # Directory log
        self.log_dir = Path.home() / "pythonita_logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # File log
        oggi = datetime.now().strftime("%Y%m%d")
        self.log_file = self.log_dir / f"pythonita_{oggi}.log"
        self.error_file = self.log_dir / f"errors_{oggi}.log"
        self.session_file = self.log_dir / f"session_{oggi}.json"
        
        # Configura logging
        self._setup_logging()
        
        # Statistiche sessione
        self.session_stats = {
            "start_time": datetime.now().isoformat(),
            "comandi_eseguiti": 0,
            "errori_totali": 0,
            "codice_generato": 0,
            "esecuzioni_successo": 0,
            "esecuzioni_fallite": 0,
        }
    
    def _setup_logging(self):
        """Configura sistema logging."""
        # Logger principale
        self.logger = logging.getLogger('pythonita')
        self.logger.setLevel(logging.DEBUG)
        
        # Handler file generale
        fh_general = logging.FileHandler(self.log_file, encoding='utf-8')
        fh_general.setLevel(logging.DEBUG)
        
        # Handler file solo errori
        fh_errors = logging.FileHandler(self.error_file, encoding='utf-8')
        fh_errors.setLevel(logging.ERROR)
        
        # Formato log
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        fh_general.setFormatter(formatter)
        fh_errors.setFormatter(formatter)
        
        self.logger.addHandler(fh_general)
        self.logger.addHandler(fh_errors)
    
    def log_info(self, messaggio: str):
        """Registra info."""
        self.logger.info(messaggio)
    
    def log_warning(self, messaggio: str):
        """Registra warning."""
        self.logger.warning(messaggio)
    
    def log_error(self, messaggio: str, exception: Exception = None):
        """
        Registra errore con traceback completo.
        
        Args:
            messaggio: Descrizione errore
            exception: Eccezione catturata
        """
        self.session_stats["errori_totali"] += 1
        
        error_msg = f"{messaggio}"
        if exception:
            error_msg += f"\nTipo: {type(exception).__name__}"
            error_msg += f"\nDettagli: {str(exception)}"
            error_msg += f"\nTraceback:\n{traceback.format_exc()}"
        
        self.logger.error(error_msg)
        
        # Salva anche in formato JSON per analisi
        self._save_error_json(messaggio, exception)
    
    def _save_error_json(self, messaggio: str, exception: Exception = None):
        """Salva errore in formato JSON."""
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "messaggio": messaggio,
            "tipo": type(exception).__name__ if exception else "Unknown",
            "dettagli": str(exception) if exception else "",
            "traceback": traceback.format_exc() if exception else ""
        }
        
        errors_json = self.log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Leggi errori esistenti
        if errors_json.exists():
            with open(errors_json, 'r', encoding='utf-8') as f:
                errors = json.load(f)
        else:
            errors = []
        
        errors.append(error_data)
        
        # Salva
        with open(errors_json, 'w', encoding='utf-8') as f:
            json.dump(errors, f, indent=2, ensure_ascii=False)
    
    def log_comando(self, comando: str, successo: bool = True):
        """Registra comando eseguito."""
        self.session_stats["comandi_eseguiti"] += 1
        if successo:
            self.logger.info(f"Comando eseguito: '{comando}'")
        else:
            self.logger.warning(f"Comando fallito: '{comando}'")
    
    def log_generazione(self, frase: str, codice_generato: str, tempo_ms: int):
        """Registra generazione codice."""
        self.session_stats["codice_generato"] += 1
        self.logger.info(f"Codice generato per '{frase}' in {tempo_ms}ms ({len(codice_generato)} char)")
    
    def log_esecuzione(self, successo: bool, output: str = "", errore: str = ""):
        """Registra esecuzione codice."""
        if successo:
            self.session_stats["esecuzioni_successo"] += 1
            self.logger.info(f"Esecuzione OK: {output[:100]}...")
        else:
            self.session_stats["esecuzioni_fallite"] += 1
            self.logger.error(f"Esecuzione FALLITA: {errore}")
    
    def apri_cartella_log(self):
        """Apre cartella log in Esplora Risorse."""
        import subprocess
        import platform
        
        if platform.system() == 'Windows':
            os.startfile(self.log_dir)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', self.log_dir])
        else:  # Linux
            subprocess.run(['xdg-open', self.log_dir])
        
        self.logger.info("Cartella log aperta")
    
    def genera_report_sessione(self) -> str:
        """Genera report completo sessione."""
        self.session_stats["end_time"] = datetime.now().isoformat()
        
        # Calcola durata
        start = datetime.fromisoformat(self.session_stats["start_time"])
        end = datetime.now()
        durata = (end - start).total_seconds()
        
        self.session_stats["durata_secondi"] = int(durata)
        
        # Salva report
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_stats, f, indent=2, ensure_ascii=False)
        
        # Genera report testuale
        report = f"""
╔════════════════════════════════════════════════════════════╗
║           REPORT SESSIONE PYTHONITA IA                     ║
╚════════════════════════════════════════════════════════════╝

Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Durata: {durata:.0f} secondi ({durata/60:.1f} minuti)

STATISTICHE:
  • Comandi eseguiti:       {self.session_stats['comandi_eseguiti']}
  • Codice generato:        {self.session_stats['codice_generato']}
  • Esecuzioni successo:    {self.session_stats['esecuzioni_successo']}
  • Esecuzioni fallite:     {self.session_stats['esecuzioni_fallite']}
  • Errori totali:          {self.session_stats['errori_totali']}

SUCCESSO RATE:
  • Generazione: {100 if self.session_stats['codice_generato'] > 0 else 0}%
  • Esecuzione: {int(self.session_stats['esecuzioni_successo'] / max(1, self.session_stats['esecuzioni_successo'] + self.session_stats['esecuzioni_fallite']) * 100)}%

FILE LOG:
  • Log generale:  {self.log_file}
  • Solo errori:   {self.error_file}
  • Report JSON:   {self.session_file}

╚════════════════════════════════════════════════════════════╝
"""
        return report
    
    def __del__(self):
        """Cleanup: salva report finale."""
        try:
            report = self.genera_report_sessione()
            print(report)
        except:
            pass


# Singleton instance
_error_logger = None

def get_error_logger() -> ErrorLogger:
    """Restituisce istanza singleton del logger."""
    global _error_logger
    if _error_logger is None:
        _error_logger = ErrorLogger()
    return _error_logger

