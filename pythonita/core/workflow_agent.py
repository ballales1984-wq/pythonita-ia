"""
Agente di coordinamento workflow Pythonita IA.

Controlla l'intero processo:
1. Input → Validazione
2. Generazione → Verifica codice
3. Esecuzione → Cattura output
4. Analisi → Decisione visualizzazione
5. Presentazione → Grafico appropriato

Con pause, controlli e feedback visivi.
"""

import time
import re
from typing import Dict, Optional, Callable
from enum import Enum


class WorkflowState(Enum):
    """Stati del workflow."""
    IDLE = "idle"
    VALIDATING_INPUT = "validating_input"
    GENERATING_CODE = "generating_code"
    VERIFYING_CODE = "verifying_code"
    EXECUTING_CODE = "executing_code"
    ANALYZING_OUTPUT = "analyzing_output"
    VISUALIZING = "visualizing"
    COMPLETED = "completed"
    ERROR = "error"


class WorkflowAgent:
    """Agente che coordina l'intero workflow."""
    
    def __init__(self, status_callback: Optional[Callable] = None):
        """
        Inizializza agente.
        
        Args:
            status_callback: Funzione per aggiornare status GUI
        """
        self.state = WorkflowState.IDLE
        self.status_callback = status_callback
        self.log = []
        
        # Configurazione pause (secondi)
        self.pause_dopo_validazione = 0.5
        self.pause_dopo_generazione = 0.3
        self.pause_dopo_verifica = 0.2
        self.pause_dopo_esecuzione = 0.5
        self.pause_dopo_analisi = 0.3
    
    def esegui_workflow(self, 
                       comando: str,
                       generatore: Callable,
                       esecutore: Callable,
                       visualizzatore: Callable) -> Dict:
        """
        Esegue workflow completo con coordinamento.
        
        Args:
            comando: Input utente
            generatore: Funzione generazione codice
            esecutore: Funzione esecuzione
            visualizzatore: Funzione visualizzazione
            
        Returns:
            Risultato workflow con tutti gli step
        """
        risultato = {
            "successo": False,
            "step_completati": [],
            "codice": "",
            "output": "",
            "visualizzazione": False,
            "errori": [],
            "tempo_totale": 0
        }
        
        start_time = time.time()
        
        try:
            # STEP 1: Validazione Input
            self._aggiorna_stato(WorkflowState.VALIDATING_INPUT, "🔍 Validazione input...")
            validato = self._valida_input(comando)
            if not validato["valido"]:
                raise ValueError(f"Input non valido: {validato['errore']}")
            risultato["step_completati"].append("validazione")
            self._log_step("✅ Input validato")
            time.sleep(self.pause_dopo_validazione)
            
            # STEP 2: Generazione Codice
            self._aggiorna_stato(WorkflowState.GENERATING_CODE, "🤖 AI sta generando codice...")
            codice = generatore(comando)
            if not codice or len(codice) < 10:
                raise ValueError("Codice generato vuoto o troppo corto")
            risultato["codice"] = codice
            risultato["step_completati"].append("generazione")
            self._log_step(f"✅ Codice generato ({len(codice)} char)")
            time.sleep(self.pause_dopo_generazione)
            
            # STEP 3: Verifica Codice
            self._aggiorna_stato(WorkflowState.VERIFYING_CODE, "🔬 Verifica codice...")
            verifica = self._verifica_codice(codice)
            if not verifica["valido"]:
                self._log_step(f"⚠️ Warning: {verifica['warning']}")
            risultato["step_completati"].append("verifica")
            self._log_step("✅ Codice verificato")
            time.sleep(self.pause_dopo_verifica)
            
            # STEP 4: Esecuzione
            self._aggiorna_stato(WorkflowState.EXECUTING_CODE, "⚡ Esecuzione codice...")
            exec_result = esecutore(codice)
            risultato["output"] = exec_result.get("output", "")
            if exec_result.get("errore"):
                risultato["errori"].append(exec_result["errore"])
            risultato["step_completati"].append("esecuzione")
            self._log_step(f"✅ Eseguito: {risultato['output'][:50]}...")
            time.sleep(self.pause_dopo_esecuzione)
            
            # STEP 5: Analisi Output
            self._aggiorna_stato(WorkflowState.ANALYZING_OUTPUT, "🧠 Analisi output...")
            analisi = self._analizza_output(comando, codice, risultato["output"])
            risultato["step_completati"].append("analisi")
            self._log_step(f"✅ Analisi: {analisi['tipo']}")
            time.sleep(self.pause_dopo_analisi)
            
            # STEP 6: Visualizzazione (se necessaria)
            if analisi["richiede_visualizzazione"]:
                self._aggiorna_stato(WorkflowState.VISUALIZING, "🎨 Generazione grafico...")
                try:
                    visualizzatore(comando, codice, risultato["output"])
                    risultato["visualizzazione"] = True
                    risultato["step_completati"].append("visualizzazione")
                    self._log_step("✅ Grafico visualizzato")
                except Exception as viz_err:
                    self._log_step(f"⚠️ Visualizzazione fallita: {viz_err}")
            
            # COMPLETATO
            self._aggiorna_stato(WorkflowState.COMPLETED, "✅ Workflow completato!")
            risultato["successo"] = True
            
        except Exception as e:
            self._aggiorna_stato(WorkflowState.ERROR, f"❌ Errore: {str(e)[:50]}")
            risultato["errori"].append(str(e))
            self._log_step(f"❌ ERRORE: {e}")
        
        risultato["tempo_totale"] = time.time() - start_time
        self._log_step(f"⏱️ Tempo totale: {risultato['tempo_totale']:.2f}s")
        
        return risultato
    
    def _valida_input(self, comando: str) -> Dict:
        """Valida input utente."""
        if not comando or len(comando.strip()) < 3:
            return {"valido": False, "errore": "Comando troppo corto"}
        
        if comando.strip().isdigit():
            return {"valido": False, "errore": "Solo numeri, specifica un comando"}
        
        # Controlli addizionali
        caratteri_strani = len(re.findall(r'[^a-zA-Z0-9\s\',\.àèéìòù]', comando))
        if caratteri_strani > 5:
            return {"valido": False, "errore": "Troppi caratteri speciali"}
        
        return {"valido": True}
    
    def _verifica_codice(self, codice: str) -> Dict:
        """Verifica sicurezza e correttezza codice."""
        warnings = []
        
        # Controlli sicurezza
        pericolosi = ['os.system', 'subprocess', 'eval(', '__import__', 'open(']
        for pericoloso in pericolosi:
            if pericoloso in codice:
                warnings.append(f"Uso di {pericoloso} - potenzialmente pericoloso")
        
        # Controlli sintassi base
        if codice.count('(') != codice.count(')'):
            warnings.append("Parentesi non bilanciate")
        
        if codice.count('[') != codice.count(']'):
            warnings.append("Bracket non bilanciati")
        
        return {
            "valido": True,
            "warning": "; ".join(warnings) if warnings else None
        }
    
    def _analizza_output(self, comando: str, codice: str, output: str) -> Dict:
        """
        Analizza output e decide se serve visualizzazione.
        
        Logica intelligente:
        - Geometria (cerchio, quadrato, ecc) → SÌ grafico
        - Funzioni matematiche → SÌ plot
        - Numeri semplici → NO grafico
        - Liste/array → Dipende dal contesto
        """
        comando_lower = comando.lower()
        
        # Keywords che richiedono visualizzazione
        viz_keywords = [
            'cerchio', 'quadrato', 'triangolo', 'rettangolo',
            'grafico', 'plot', 'funzione', 'seno', 'coseno',
            'fibonacci', 'lista', 'array', 'visualizza'
        ]
        
        richiede_viz = any(kw in comando_lower for kw in viz_keywords)
        
        # Determina tipo
        if 'cerchio' in comando_lower:
            tipo = "geometria_cerchio"
        elif 'quadrato' in comando_lower or 'rettangolo' in comando_lower:
            tipo = "geometria_quadrato"
        elif 'triangolo' in comando_lower:
            tipo = "geometria_triangolo"
        elif any(func in comando_lower for func in ['seno', 'coseno', 'funzione']):
            tipo = "funzione_matematica"
        elif 'fibonacci' in comando_lower:
            tipo = "sequenza"
        elif 'grafico' in comando_lower:
            tipo = "grafico_generico"
        else:
            tipo = "calcolo_semplice"
        
        return {
            "richiede_visualizzazione": richiede_viz,
            "tipo": tipo,
            "confidenza": 0.9 if richiede_viz else 0.1
        }
    
    def _aggiorna_stato(self, nuovo_stato: WorkflowState, messaggio: str):
        """Aggiorna stato e notifica GUI."""
        self.state = nuovo_stato
        if self.status_callback:
            self.status_callback(messaggio)
        print(f"[AGENT] {nuovo_stato.value}: {messaggio}")
    
    def _log_step(self, messaggio: str):
        """Registra step nel log."""
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {messaggio}"
        self.log.append(entry)
        print(f"[AGENT] {messaggio}")
    
    def get_log(self) -> str:
        """Restituisce log completo."""
        return "\n".join(self.log)
    
    def reset(self):
        """Reset agente per nuovo workflow."""
        self.state = WorkflowState.IDLE
        self.log = []


def get_workflow_agent(status_callback=None):
    """Restituisce istanza singleton agente."""
    if not hasattr(get_workflow_agent, '_instance'):
        get_workflow_agent._instance = WorkflowAgent(status_callback)
    return get_workflow_agent._instance

