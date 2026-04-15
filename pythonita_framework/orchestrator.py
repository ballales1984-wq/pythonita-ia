"""
Multi-Agent Orchestrator
Coordina agent specializzati per gestire diversi tipi di richieste
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, List, Dict
from enum import Enum

logger = logging.getLogger(__name__)


class AgentType(Enum):
    DIDATTICO = "didattico"
    ROBOTICA = "robotica"
    CODICE = "codice"
    GENERALE = "generale"


class BaseAgent:
    """Base class per tutti gli agent."""

    def __init__(self, agent_type: AgentType, name: str, description: str):
        self.type = agent_type
        self.name = name
        self.description = description

    def can_handle(self, query: str) -> float:
        return 0.0

    def process(self, query: str, context: dict) -> dict:
        raise NotImplementedError


class DidatticoAgent(BaseAgent):
    """Agent specializzato in didattica Python."""

    def __init__(self):
        super().__init__(
            AgentType.DIDATTICO, "Didattico", "Spiegazioni Python, lezioni, esercizi"
        )

    def can_handle(self, query: str) -> float:
        text = query.lower()
        keywords = [
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
        ]
        score = sum(1 for k in keywords if k in text)
        return min(score / 3, 1.0)

    def process(self, query: str, context: dict) -> dict:
        prompt = f"""Sei un insegnante di Python paziente e chiaro.
Spiega il concetto in modo semplice con esempi pratici.

DOMANDA: {query}

Rispondi in italiano in modo didattico."""

        return {
            "tipo": "didattico",
            "risposta": self._call_llm(prompt),
            "azione": "rispondi",
        }

    def _call_llm(self, prompt: str) -> str:
        try:
            import ollama

            risposta = ollama.chat(
                model="llama3.2", messages=[{"role": "user", "content": prompt}]
            )
            return risposta["message"]["content"].strip()
        except:
            return "Spiegazione non disponibile (LLM non connesso). Prova a formulare diversamente."


class RoboticaAgent(BaseAgent):
    """Agent specializzato in robotica e visualizzazione 3D."""

    def __init__(self):
        super().__init__(
            AgentType.ROBOTICA,
            "Robotica",
            "Robot 3D, Arduino, mani bioniche, animazioni",
        )

    def can_handle(self, query: str) -> float:
        text = query.lower()
        keywords = [
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
        ]
        score = sum(1 for k in keywords if k in text)
        return min(score / 3, 1.0)

    def process(self, query: str, context: dict) -> dict:
        prompt = f"""Sei un esperto di robotica e automazione.
Genera codice Python per robotica e animazioni 3D.

Richiesta: {query}

Se è richiesta un'animazione, genera codice Matplotlib.
Se è per Arduino, genera codice C++."""

        return {
            "tipo": "robotica",
            "risposta": self._call_llm(prompt),
            "azione": "rispondi",
        }

    def _call_llm(self, prompt: str) -> str:
        try:
            import ollama

            risposta = ollama.chat(
                model="llama3.2", messages=[{"role": "user", "content": prompt}]
            )
            return risposta["message"]["content"].strip()
        except:
            return "# Codice robotica non disponibile"


class CodiceAgent(BaseAgent):
    """Agent specializzato in generazione codice Python."""

    def __init__(self):
        super().__init__(
            AgentType.CODICE, "Codice", "Generazione codice, debugging, ottimizzazione"
        )

    def can_handle(self, query: str) -> float:
        text = query.lower()
        keywords = [
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
        ]
        score = sum(1 for k in keywords if k in text)
        return min(score / 3, 1.0)

    def process(self, query: str, context: dict) -> dict:
        prompt = f"""Genera SOLO codice Python pulito e funzionante per:
{query}

Regole:
- Solo codice, nessuna spiegazione
- Codice sicuro e idiomatico
- Output massimo 50 righe"""

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

    def _call_llm(self, prompt: str) -> str:
        try:
            import ollama

            risposta = ollama.chat(
                model="llama3.2", messages=[{"role": "user", "content": prompt}]
            )
            return risposta["message"]["content"].strip()
        except:
            return "# LLM non disponibile"


class MultiAgentOrchestrator:
    """Orchestratore multi-agent che coordina tutti gli agent."""

    def __init__(self):
        self.agents: List[BaseAgent] = [
            DidatticoAgent(),
            RoboticaAgent(),
            CodiceAgent(),
        ]
        self.memory = self._load_memory()
        self.vector_db = self._init_vector_db()
        self.llm_available = self._check_llm()

        logger.info(f"✅ Orchestrator attivato con {len(self.agents)} agent")

    def _load_memory(self) -> dict:
        if os.path.exists("agent_memory_multi.json"):
            try:
                with open("agent_memory_multi.json", "r") as f:
                    return json.load(f)
            except:
                pass
        return {"history": [], "conoscenze": {}}

    def _init_vector_db(self):
        try:
            import chromadb
            from chromadb.utils import embedding_functions

            Path("./vector_memory_multi").mkdir(exist_ok=True)
            client = chromadb.PersistentClient(path="./vector_memory_multi")
            embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
            collection = client.get_or_create_collection(
                name="multi_agent_memory", embedding_function=embedding_fn
            )
            logger.info("✅ Vector DB attivo")
            return {"client": client, "collection": collection}
        except:
            logger.warning("⚠️ Vector DB non disponibile")
            return None

    def _check_llm(self) -> bool:
        try:
            import ollama

            ollama.list()
            return True
        except:
            return False

    def add_agent(self, agent: BaseAgent):
        """Aggiunge un agent personalizzato."""
        self.agents.append(agent)
        logger.info(f"✅ Agent aggiunto: {agent.name}")

    def select_agent(self, query: str) -> tuple[BaseAgent, float]:
        """Seleziona l'agent migliore per la query."""
        best_agent = self.agents[-1]
        best_score = 0.0

        for agent in self.agents:
            score = agent.can_handle(query)
            if score > best_score:
                best_score = score
                best_agent = agent

        if best_score < 0.3:
            return self.agents[-1], 0.5

        return best_agent, best_score

    def process(self, query: str) -> dict:
        agent, score = self.select_agent(query)
        logger.info(f"🎯 Agent: {agent.name} (score: {score:.2f})")

        context = {"history": self.memory.get("history", [])[-3:]}
        result = agent.process(query, context)

        self._save_interaction(query, result)

        return result

    def _save_interaction(self, query: str, result: dict):
        self.memory["history"].append(
            {
                "query": query[:200],
                "agent": result.get("tipo", "sconosciuto"),
                "timestamp": datetime.now().isoformat(),
            }
        )
        if len(self.memory["history"]) > 50:
            self.memory["history"] = self.memory["history"][-25:]

        with open("agent_memory_multi.json", "w") as f:
            json.dump(self.memory, f, indent=2)

    def get_status(self) -> dict:
        return {
            "agents": [
                {"name": a.name, "type": a.type.value, "description": a.description}
                for a in self.agents
            ],
            "history_count": len(self.memory.get("history", [])),
            "llm_available": self.llm_available,
            "vector_db_active": self.vector_db is not None,
        }
