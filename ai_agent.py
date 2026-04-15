"""
AI Agent v6 - Multi-Agent System
Collaborazione tra agent specializzati: Didattico, Robotica, Codice
"""

import json
import os
import logging
import re
import io
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, List, Dict
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MEMORY_FILE = "agent_memory_multi.json"
VECTOR_DB_PATH = "./vector_memory_multi"
SAFE_WORKSPACE = "workspace_agent"
MAX_STEPS = 5
SIMILARITY_THRESHOLD = 0.65

SAFE_GLOBALS = {
    "__builtins__": {
        "print": print,
        "range": range,
        "len": len,
        "list": list,
        "dict": dict,
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "abs": abs,
        "max": max,
        "min": min,
        "sum": sum,
        "sorted": sorted,
        "enumerate": enumerate,
        "zip": zip,
        "map": map,
        "filter": filter,
        "round": round,
    }
}


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
        """Ritorna 0-1 score di quanto l'agent può gestire la query."""
        return 0.0

    def process(self, query: str, context: dict) -> dict:
        """Processa la query e ritorna risultato."""
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
            return "Spiegazione non disponibile (LLM non connesso)"


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
        ]
        score = sum(1 for k in keywords if k in text)
        return min(score / 3, 1.0)

    def process(self, query: str, context: dict) -> dict:
        prompt = f"""Sei un esperto di robotica e automazione.
Genera codice Python per robotica e animazioni 3D.

 Richiesta: {query}

Se è richiesta un'animazione, genera codice Matplotlib/Visualization.
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
            return "Codice robotica non disponibile"


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
        ]
        score = sum(1 for k in keywords if k in text)
        return min(score / 3, 1.0)

    def process(self, query: str, context: dict) -> dict:
        prompt = f"""Genera SOLO codice Python pulito e funzionante per:
{query}

Regole:
- Solo codice, nessuna spiegazione
- Codice sicuro e idiomatico
- Se richiede file, usa la workspace './workspace_agent/'"""

        codice = self._call_llm(prompt)

        if "crea_file" in query.lower() or "salva" in query.lower():
            return {
                "tipo": "codice",
                "risposta": codice,
                "azione": "crea_file",
                "percorso": "output.py",
                "contenuto": codice,
            }

        return {
            "tipo": "codice",
            "risposta": codice,
            "azione": "esegui_codice",
            "codice": codice,
        }

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

        logger.info(
            f"✅ Multi-Agent Orchestrator attivato con {len(self.agents)} agent"
        )

    def _load_memory(self) -> dict:
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    return json.load(f)
            except:
                pass
        return {"history": [], "conoscenze": {}}

    def _init_vector_db(self):
        try:
            import chromadb
            from chromadb.utils import embedding_functions

            Path(VECTOR_DB_PATH).mkdir(exist_ok=True)
            client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
            embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
            collection = client.get_or_create_collection(
                name="multi_agent_memory", embedding_function=embedding_fn
            )
            logger.info("✅ Vector DB attivo")
            return {
                "client": client,
                "collection": collection,
                "embedding_fn": embedding_fn,
            }
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

    def select_agent(self, query: str) -> tuple[BaseAgent, float]:
        """Seleziona l'agent migliore per la query."""
        best_agent = None
        best_score = 0.0

        for agent in self.agents:
            score = agent.can_handle(query)
            if score > best_score:
                best_score = score
                best_agent = agent

        if best_score < 0.3:
            return self.agents[2], 0.5  # Default a codice

        return best_agent, best_score

    def get_context(self, query: str) -> str:
        if not self.vector_db:
            return ""

        try:
            results = self.vector_db["collection"].query(
                query_texts=[query], n_results=3, include=["documents", "metadatas"]
            )
            if results["documents"] and results["documents"][0]:
                ctx = "\n📚 Contesto:\n"
                for doc in results["documents"][0]:
                    ctx += f"- {doc[:100]}...\n"
                return ctx
        except:
            pass
        return ""

    def process(self, query: str) -> dict:
        agent, score = self.select_agent(query)
        logger.info(f"🎯 Agent selezionato: {agent.name} (score: {score:.2f})")

        context = self.get_context(query)
        context_dict = {
            "context": context,
            "history": self.memory.get("history", [])[-3:],
        }

        result = agent.process(query, context_dict)

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

        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)

        if self.vector_db and result.get("risposta"):
            try:
                self.vector_db["collection"].add(
                    documents=[result["risposta"][:500]],
                    metadatas=[
                        {"agent": result.get("tipo", "generic"), "query": query[:100]}
                    ],
                    ids=[f"mem_{int(datetime.now().timestamp() * 1000)}"],
                )
            except:
                pass


class Router:
    """Router per eseguire le azioni degli agent."""

    def __init__(self):
        Path(SAFE_WORKSPACE).mkdir(exist_ok=True)

    def execute(self, azione: str, params: dict) -> str:
        if azione == "rispondi":
            return params.get("risposta", "Come posso aiutarti?")

        if azione == "esegui_codice":
            codice = params.get("codice", "")
            if len(codice) > 2000:
                return "❌ Codice troppo lungo"
            if any(
                d in codice.lower() for d in ["import os", "import sys", "subprocess"]
            ):
                return "❌ Import non consentiti"

            old_stdout = sys.stdout
            sys.stdout = captured = io.StringIO()
            try:
                exec(codice, SAFE_GLOBALS, {})
                sys.stdout = old_stdout
                return f"✅ {captured.getvalue() or 'Eseguito'}"
            except Exception as e:
                sys.stdout = old_stdout
                return f"❌ {e}"

        if azione == "crea_file":
            percorso = params.get("percorso", "output.py")
            percorso = os.path.join(SAFE_WORKSPACE, os.path.basename(percorso))
            try:
                with open(percorso, "w") as f:
                    f.write(params.get("contenuto", "")[:10000])
                return f"✅ File creato: {percorso}"
            except Exception as e:
                return f"❌ {e}"

        return f"❌ Azione sconosciuta: {azione}"


def main():
    orchestrator = MultiAgentOrchestrator()
    router = Router()

    print("\n🤖 Multi-Agent System v6")
    print("Agent: Didattico | Robotica | Codice")
    print("Digita 'esci' per uscire, 'stato' per info\n")

    while True:
        user_input = input("➤ ").strip()

        if user_input.lower() in ["esci", "exit"]:
            print("👋 Ciao!")
            break

        if user_input.lower() == "stato":
            print(f"📊 Interazioni: {len(orchestrator.memory['history'])}")
            print(
                "Agent disponibili:", ", ".join([a.name for a in orchestrator.agents])
            )
            continue

        if not user_input:
            continue

        result = orchestrator.process(user_input)
        output = router.execute(result.get("azione", "rispondi"), result)
        print(f"\n🎯 [{result.get('tipo', '?')}] {output}\n")


if __name__ == "__main__":
    main()
