"""
Telemetry System - Traccia errori e usage (anonimo, privacy-first).
NON invia dati a server esterni senza consenso utente.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
import sys
import traceback as tb

logger = logging.getLogger(__name__)


class TelemetryManager:
    """
    Gestore telemetria locale.
    
    Privacy-first:
    - Tutti i dati salvati LOCALMENTE
    - Nessun invio automatico a server esterni
    - Anonimizzazione completa
    - Opt-in esplicito per condivisione
    """
    
    def __init__(self, app_name="pythonita"):
        """Inizializza telemetry manager."""
        self.app_name = app_name
        self.data_dir = Path.home() / f".{app_name}" / "telemetry"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.crash_file = self.data_dir / "crashes.json"
        self.usage_file = self.data_dir / "usage.json"
        self.session_file = self.data_dir / "sessions.json"
        
        self.current_session = {
            'start_time': datetime.now().isoformat(),
            'commands_executed': 0,
            'errors_count': 0,
            'features_used': set()
        }
        
        # Privacy settings
        self.telemetry_enabled = self._load_telemetry_consent()
        
        logger.info(f"Telemetry initialized. Enabled: {self.telemetry_enabled}")
    
    def _load_telemetry_consent(self) -> bool:
        """Carica consenso telemetria da file."""
        consent_file = self.data_dir / "consent.json"
        
        if consent_file.exists():
            try:
                with open(consent_file, 'r') as f:
                    data = json.load(f)
                    return data.get('enabled', False)
            except:
                return False
        
        # Default: telemetria locale abilitata, condivisione disabilitata
        return True
    
    def set_telemetry_consent(self, enabled: bool):
        """Imposta consenso telemetria."""
        self.telemetry_enabled = enabled
        
        consent_file = self.data_dir / "consent.json"
        with open(consent_file, 'w') as f:
            json.dump({
                'enabled': enabled,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        logger.info(f"Telemetry consent set to: {enabled}")
    
    def log_crash(self, exception: Exception, context: Optional[Dict] = None):
        """
        Registra crash dell'applicazione.
        
        Args:
            exception: Eccezione verificatasi
            context: Contesto aggiuntivo (comando, stato, ecc)
        """
        if not self.telemetry_enabled:
            return
        
        crash_data = {
            'timestamp': datetime.now().isoformat(),
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
            'traceback': tb.format_exc(),
            'context': context or {},
            'python_version': sys.version,
            'platform': sys.platform
        }
        
        # Anonimizza dati sensibili
        crash_data = self._anonymize_data(crash_data)
        
        # Carica crashes esistenti
        crashes = self._load_json(self.crash_file, default=[])
        
        # Aggiungi nuovo crash
        crashes.append(crash_data)
        
        # Mantieni solo ultimi 100 crashes
        if len(crashes) > 100:
            crashes = crashes[-100:]
        
        # Salva
        self._save_json(self.crash_file, crashes)
        
        logger.error(f"Crash logged: {crash_data['exception_type']}")
    
    def log_command(self, command: str, success: bool, execution_time: float = 0):
        """
        Registra esecuzione comando.
        
        Args:
            command: Comando eseguito (anonimizzato)
            success: Successo esecuzione
            execution_time: Tempo esecuzione in secondi
        """
        if not self.telemetry_enabled:
            return
        
        self.current_session['commands_executed'] += 1
        
        if not success:
            self.current_session['errors_count'] += 1
        
        usage_data = {
            'timestamp': datetime.now().isoformat(),
            'command_hash': hash(command) % 10000,  # Hash anonimizzato
            'command_length': len(command),
            'success': success,
            'execution_time': execution_time
        }
        
        # Carica usage esistente
        usage = self._load_json(self.usage_file, default=[])
        
        # Aggiungi nuovo record
        usage.append(usage_data)
        
        # Mantieni solo ultimi 1000 comandi
        if len(usage) > 1000:
            usage = usage[-1000:]
        
        # Salva
        self._save_json(self.usage_file, usage)
    
    def log_feature_usage(self, feature_name: str):
        """
        Registra uso feature.
        
        Args:
            feature_name: Nome feature (es: "gui_3d", "cache", "ai_generation")
        """
        if not self.telemetry_enabled:
            return
        
        self.current_session['features_used'].add(feature_name)
        
        logger.debug(f"Feature used: {feature_name}")
    
    def end_session(self):
        """Termina sessione corrente e salva statistiche."""
        if not self.telemetry_enabled:
            return
        
        self.current_session['end_time'] = datetime.now().isoformat()
        self.current_session['features_used'] = list(self.current_session['features_used'])
        
        # Carica sessioni esistenti
        sessions = self._load_json(self.session_file, default=[])
        
        # Aggiungi sessione corrente
        sessions.append(self.current_session)
        
        # Mantieni solo ultime 50 sessioni
        if len(sessions) > 50:
            sessions = sessions[-50:]
        
        # Salva
        self._save_json(self.session_file, sessions)
        
        logger.info(f"Session ended. Commands: {self.current_session['commands_executed']}")
    
    def get_statistics(self) -> Dict:
        """
        Ottieni statistiche usage aggregate.
        
        Returns:
            Dict con statistiche
        """
        crashes = self._load_json(self.crash_file, default=[])
        usage = self._load_json(self.usage_file, default=[])
        sessions = self._load_json(self.session_file, default=[])
        
        # Calcola statistiche
        total_commands = len(usage)
        total_crashes = len(crashes)
        total_sessions = len(sessions)
        
        successful_commands = sum(1 for u in usage if u.get('success', False))
        success_rate = (successful_commands / total_commands * 100) if total_commands > 0 else 0
        
        avg_execution_time = (sum(u.get('execution_time', 0) for u in usage) / total_commands) if total_commands > 0 else 0
        
        # Features più usate
        all_features = []
        for session in sessions:
            all_features.extend(session.get('features_used', []))
        
        from collections import Counter
        feature_counts = Counter(all_features)
        
        # Errori più comuni
        error_types = Counter(c.get('exception_type', 'Unknown') for c in crashes)
        
        return {
            'total_commands': total_commands,
            'total_crashes': total_crashes,
            'total_sessions': total_sessions,
            'success_rate': success_rate,
            'avg_execution_time': avg_execution_time,
            'most_used_features': feature_counts.most_common(5),
            'most_common_errors': error_types.most_common(5),
            'current_session': self.current_session
        }
    
    def print_statistics(self):
        """Stampa statistiche formattate."""
        stats = self.get_statistics()
        
        print("\n" + "="*70)
        print("STATISTICHE TELEMETRIA")
        print("="*70)
        print(f"\nComandi Eseguiti:   {stats['total_commands']}")
        print(f"Sessioni Totali:    {stats['total_sessions']}")
        print(f"Crash Registrati:   {stats['total_crashes']}")
        print(f"Success Rate:       {stats['success_rate']:.1f}%")
        print(f"Tempo Medio Exec:   {stats['avg_execution_time']*1000:.2f}ms")
        
        print(f"\nFeatures Più Usate:")
        for feature, count in stats['most_used_features']:
            print(f"  - {feature}: {count} volte")
        
        if stats['most_common_errors']:
            print(f"\nErrori Più Comuni:")
            for error, count in stats['most_common_errors']:
                print(f"  - {error}: {count} occorrenze")
        
        print(f"\nSessione Corrente:")
        print(f"  Comandi: {stats['current_session']['commands_executed']}")
        print(f"  Errori:  {stats['current_session']['errors_count']}")
        
        print("="*70 + "\n")
    
    def export_for_sharing(self) -> Dict:
        """
        Esporta dati anonimizzati per condivisione (opt-in).
        
        Returns:
            Dict con dati completamente anonimizzati
        """
        stats = self.get_statistics()
        
        # Rimuovi tutti i dati identificativi
        export_data = {
            'app_version': '3.1.0',
            'total_commands': stats['total_commands'],
            'success_rate': stats['success_rate'],
            'avg_execution_time': stats['avg_execution_time'],
            'most_used_features': dict(stats['most_used_features']),
            'most_common_errors': dict(stats['most_common_errors']),
            'timestamp': datetime.now().isoformat()
        }
        
        return export_data
    
    def _anonymize_data(self, data: Dict) -> Dict:
        """Rimuove dati sensibili."""
        # Rimuovi path assoluti
        if 'traceback' in data:
            traceback_lines = data['traceback'].split('\n')
            # Sostituisci path con placeholder
            anonymized_lines = []
            for line in traceback_lines:
                # Rimuovi path utente
                if 'Users' in line or 'home' in line:
                    line = line.split('/', 3)[-1] if '/' in line else line
                anonymized_lines.append(line)
            data['traceback'] = '\n'.join(anonymized_lines)
        
        # Rimuovi informazioni utente da context
        if 'context' in data and isinstance(data['context'], dict):
            if 'user' in data['context']:
                del data['context']['user']
            if 'email' in data['context']:
                del data['context']['email']
        
        return data
    
    def _load_json(self, file_path: Path, default=None):
        """Carica JSON da file."""
        if not file_path.exists():
            return default if default is not None else {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return default if default is not None else {}
    
    def _save_json(self, file_path: Path, data):
        """Salva JSON su file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving {file_path}: {e}")


# Singleton instance
_telemetry_manager: Optional[TelemetryManager] = None


def get_telemetry_manager() -> TelemetryManager:
    """Ottiene istanza singleton telemetry manager."""
    global _telemetry_manager
    if _telemetry_manager is None:
        _telemetry_manager = TelemetryManager()
    return _telemetry_manager


# Convenience functions
def log_crash(exception: Exception, context: Optional[Dict] = None):
    """Log crash."""
    get_telemetry_manager().log_crash(exception, context)


def log_command(command: str, success: bool, execution_time: float = 0):
    """Log command execution."""
    get_telemetry_manager().log_command(command, success, execution_time)


def log_feature(feature_name: str):
    """Log feature usage."""
    get_telemetry_manager().log_feature_usage(feature_name)


if __name__ == "__main__":
    # Test telemetry
    print("Telemetry System - Test")
    
    tm = TelemetryManager("pythonita-test")
    
    # Simula usage
    tm.log_command("stampa ciao", True, 0.05)
    tm.log_command("crea lista", True, 0.03)
    tm.log_command("comando invalido", False, 0.01)
    
    # Simula feature usage
    tm.log_feature("gui_3d")
    tm.log_feature("cache")
    tm.log_feature("ai_generation")
    
    # Simula crash
    try:
        raise ValueError("Test error")
    except Exception as e:
        tm.log_crash(e, {'command': 'test', 'state': 'testing'})
    
    # Stats
    tm.print_statistics()
    
    # Export
    export = tm.export_for_sharing()
    print("\nExport Data:")
    print(json.dumps(export, indent=2))
    
    print("\n[OK] Telemetry tested!")

