"""
Agent Base Classes e Agent Specializzati
Definisce la struttura base e gli agent predefiniti
"""

import logging
from typing import Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)

from .orchestrator import AgentType


class BaseAgent:
    """Base class per tutti gli agent."""

    def __init__(self, agent_type: AgentType, name: str, description: str):
        self.type = agent_type
        self.name = name
        self.description = description

    def can_handle(self, query: str) -> float:
        """Ritorna 0.0-1.0 score di quanto l'agent può gestire la query."""
        return 0.0

    def process(self, query: str, context: Dict) -> Dict:
        """Processa la query e ritorna un risultato."""
        raise NotImplementedError

    def _call_llm(self, prompt: str) -> str:
        """Chiama LLM per generare risposta."""
        try:
            import ollama

            risposta = ollama.chat(
                model="llama3.2", messages=[{"role": "user", "content": prompt}]
            )
            return risposta["message"]["content"].strip()
        except Exception as e:
            logger.warning(f"LLM non disponibile: {e}")
            return "Servizio non disponibile"


class DidatticoAgent(BaseAgent):
    """Agent specializzato in didattica Python."""

    def __init__(self):
        super().__init__(
            AgentType.DIDATTICO, "Didattico", "Spiegazioni Python, lezioni, esercizi"
        )
        self.keywords = [
            "spiega",
            "lezione",
            "come funziona",
            "cos'è",
            "esempio",
            "esercizio",
            "impara",
            "studente",
            "teoria",
            "concetto",
            "for",
            "while",
            "if",
            "list",
            "dizionario",
            "funzione",
            "classe",
            "python",
            "def",
            "return",
            "iterazione",
            "variabile",
            "ciclo",
            "condizione",
            "boolean",
            "stringa",
        ]

    def can_handle(self, query: str) -> float:
        text = query.lower()
        score = sum(1 for k in self.keywords if k in text)
        return min(score / 3, 1.0)

    def process(self, query: str, context: Dict) -> Dict:
        prompt = f"""Sei un insegnante di Python paziente e chiaro.
Spiega il concetto in modo semplice con esempi pratici in italiano.

DOMANDA: {query}

Rispondi con:
1. Spiegazione semplice (2-3 frasi)
2. Esempio di codice
3. Output atteso (se presente)"""

        risposta = self._call_llm(prompt)

        return {"tipo": "didattico", "risposta": risposta, "azione": "rispondi"}


class RoboticaAgent(BaseAgent):
    """Agent specializzato in robotica e visualizzazione 3D."""

    def __init__(self):
        super().__init__(
            AgentType.ROBOTICA, "Robotica", "Robot 3D, Arduino, mani bioniche"
        )
        self.keywords = [
            "robot",
            "mano",
            "braccio",
            "apri",
            "chiudi",
            "pugno",
            "dita",
            "arduino",
            "3d",
            "animazione",
            "motore",
            "servo",
            "afferra",
            "solleva",
            "muovi",
            "visualizzatore",
            "gripper",
            "pinza",
            "braccio",
            "gomito",
            "spalla",
            "angolo",
            "movimento",
            "simulazione",
        ]

    def can_handle(self, query: str) -> float:
        text = query.lower()
        score = sum(1 for k in self.keywords if k in text)
        return min(score / 3, 1.0)

    def process(self, query: str, context: Dict) -> Dict:
        prompt = f"""Sei un esperto di robotica e automazione.
Genera codice Python per robotica e animazioni 3D.

Richiesta: {query}

Se richiede animazione → codice Matplotlib.
Se Arduino → codice C++."""

        risposta = self._call_llm(prompt)

        return {"tipo": "robotica", "risposta": risposta, "azione": "rispondi"}


class CodiceAgent(BaseAgent):
    """Agent specializzato in generazione codice Python."""

    def __init__(self):
        super().__init__(AgentType.CODICE, "Codice", "Generazione codice Python")
        self.keywords = [
            "codice",
            "programma",
            "script",
            "crea",
            "genera",
            "scrivi",
            "funzione",
            "classe",
            "loop",
            "debug",
            "errore",
            "ottimizza",
            "python",
            "file",
            "salva",
            "esegui",
            "crea",
            "scrivi",
            "implementa",
            "algoritmo",
            "metodo",
            "property",
        ]

    def can_handle(self, query: str) -> float:
        text = query.lower()
        score = sum(1 for k in self.keywords if k in text)
        return min(score / 3, 1.0)

    def process(self, query: str, context: Dict) -> Dict:
        prompt = f"""Genera SOLO codice Python pulito e funzionante.
Non aggiungere spiegazioni, solo codice.

Richiesta: {query}

Regole:
- Codice idiomatico Python
- Max 30 righe
- Nessun import pericoloso"""

        codice = self._call_llm(prompt)

        if any(x in query.lower() for x in ["crea file", "salva", "scrivi su"]):
            return {
                "tipo": "codice",
                "risposta": codice,
                "azione": "crea_file",
                "percorso": "output.py",
                "contenuto": codice,
            }

        return {"tipo": "codice", "risposta": codice, "azione": "rispondi"}


class AgenteGenerale(BaseAgent):
    """Agent generale per query non specializzate."""

    def __init__(self):
        super().__init__(AgentType.GENERALE, "Generale", "Chat generica")

    def can_handle(self, query: str) -> float:
        return 0.5

    def process(self, query: str, context: Dict) -> Dict:
        prompt = f"""Sei Pythonita, assistente cordiale e utile.
Rispondi in italiano in modo conciso.

Richiesta: {query}"""

        risposta = self._call_llm(prompt)

        return {"tipo": "generale", "risposta": risposta, "azione": "rispondi"}
