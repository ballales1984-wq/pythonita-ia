"""
AI Agent v7 - Self-Improving Research Agent
Complete architecture: Planner → Executor → Critic → Reflection → Memory
Inspired by Anthropic's research agent patterns
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

MEMORY_FILE = "agent_memory_research.json"
VECTOR_DB_PATH = "./vector_memory_research"
SAFE_WORKSPACE = "workspace_research"
MAX_STEPS = 10
MAX_REFLECTION_ITERATIONS = 3

ALLOWED_TOOLS = [
    "crea_file",
    "esegui_codice",
    "calcola",
    "memoria",
    "rispondi",
    "ricerca",
]

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


class AgentState:
    """Stato dell'agente che evolve nel tempo."""

    def __init__(self):
        self.strategy_level = 1
        self.success_rate = 0.5
        self.last_errors = []
        self.total_executions = 0
        self.successful_executions = 0
        self.improvement_history = []

    def to_dict(self) -> dict:
        return {
            "strategy_level": self.strategy_level,
            "success_rate": self.success_rate,
            "last_errors": self.last_errors[-5:],
            "total_executions": self.total_executions,
            "successful_executions": self.successful_executions,
            "improvement_history": self.improvement_history[-10:],
        }

    def load(self, data: dict):
        if data:
            self.strategy_level = data.get("strategy_level", 1)
            self.success_rate = data.get("success_rate", 0.5)
            self.last_errors = data.get("last_errors", [])[-5:]
            self.total_executions = data.get("total_executions", 0)
            self.successful_executions = data.get("successful_executions", 0)
            self.improvement_history = data.get("improvement_history", [])[-10:]


class VectorMemory:
    """Vector memory per RAG e storage semantico."""

    def __init__(self, persist_path: str = VECTOR_DB_PATH):
        self.client = None
        self.collection = None
        self._init(persist_path)

    def _init(self, persist_path: str):
        try:
            import chromadb
            from chromadb.utils import embedding_functions

            Path(persist_path).mkdir(exist_ok=True)
            self.client = chromadb.PersistentClient(path=persist_path)
            self.embedding_fn = (
                embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
            )
            self.collection = self.client.get_or_create_collection(
                name="research_agent_memory",
                embedding_function=self.embedding_fn,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info("OK Vector Memory attivata")
        except:
            logger.warning("⚠️ Vector DB non disponibile")
            self.client = None

    def add(self, text: str, metadata: dict = None) -> bool:
        if not self.client or not self.collection:
            return False
        try:
            doc_id = f"mem_{int(datetime.now().timestamp() * 1000)}"
            self.collection.add(
                documents=[text[:1000]], metadatas=[metadata or {}], ids=[doc_id]
            )
            return True
        except:
            return False

    def search(self, query: str, k: int = 5, threshold: float = 0.6) -> List[dict]:
        if not self.client or not self.collection:
            return []
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=k,
                include=["documents", "metadatas", "distances"],
            )
            if not results["documents"] or not results["documents"][0]:
                return []
            return [
                {"text": doc, "metadata": meta, "similarity": 1 - dist}
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                )
                if (1 - dist) > threshold
            ]
        except:
            return []


class Planner:
    """PLANNER: trasforma richiesta in step eseguibili."""

    def __init__(self, llm_available: bool):
        self.llm_available = llm_available

    def plan(self, user_input: str, state: AgentState, context: str = "") -> List[dict]:
        """Genera piano di azioni basato sullo stato dell'agente."""

        prompt = f"""Sei un planner di azioni per un AI Agent.
Analizza la richiesta e crea una lista di step da eseguire.

Stato agente: strategy_level={state.strategy_level}, success_rate={state.success_rate:.2f}

Contesto dalla memoria:
{context}

Richiesta: "{user_input}"

Scegli gli step necessari:
- "rispondi" - risposta generale
- "calcola" - calcoli matematici
- "esegui_codice" - eseguire codice Python
- "crea_file" - creare file
- "ricerca" - cercare informazioni nella memoria
- "riflessione" - riflettere sul risultato

Rispondi SOLO con JSON array di step:
[{{"tool": "nome_tool", "params": {{"chiave": "valore"}}}}]

Esempio: "crea lista 1-5 e salvala" →
[{{"tool": "esegui_codice", "params": {{"codice": "lista = list(range(1,6))\\nprint(lista)"}}}},
 {{"tool": "crea_file", "params": {{"percorso": "lista.txt", "contenuto": "1,2,3,4,5"}}}}]

JSON:"""

        if self.llm_available:
            try:
                import ollama

                try:
                    risposta = ollama.chat(
                        model="gemma3:1b",
                        messages=[{"role": "user", "content": prompt}],
                    )
                except:
                    risposta = ollama.chat(
                        model="deepseek-coder:latest",
                        messages=[{"role": "user", "content": prompt}],
                    )

                content = (
                    risposta["message"]["content"]
                    .encode("utf-8", errors="replace")
                    .decode("utf-8")
                )

                if "[" in content and "]" in content:
                    json_str = content[content.find("[") : content.rfind("]") + 1]
                    steps = json.loads(json_str)

                    if state.strategy_level > 1:
                        steps.append({"tool": "riflessione", "params": {}})

                    return steps
            except Exception as e:
                logger.error(f"Planning error: {e}")

        return self._fallback_plan(user_input)

    def _fallback_plan(self, user_input: str) -> List[dict]:
        text = user_input.lower()

        if any(x in text for x in ["calcola", "quanto fa", "somma"]) and re.search(
            r"\d+", text
        ):
            expr = re.sub(r"[^\d+\-*/().]", "", text)
            return [{"tool": "calcola", "params": {"espressione": expr}}]

        if any(x in text for x in ["salva", "crea file", "scrivi"]):
            return [
                {
                    "tool": "crea_file",
                    "params": {"percorso": "output.txt", "contenuto": user_input},
                }
            ]

        return [{"tool": "rispondi", "params": {"testo": "Come posso aiutarti?"}}]


class Executor:
    """EXECUTOR: esegue gli step del piano."""

    def __init__(self):
        Path(SAFE_WORKSPACE).mkdir(exist_ok=True)
        self.execution_count = 0

    def execute(self, step: dict, memory) -> tuple[str, bool]:
        """Esegue uno step e ritorna (output, success)."""

        if self.execution_count >= MAX_STEPS:
            return "FAIL Limite esecuzioni raggiunto", False

        tool = step.get("tool", "")
        params = step.get("params", {})

        try:
            if tool == "rispondi":
                return params.get("testo", "Risposta vuota"), True

            elif tool == "calcola":
                return self._execute_calculator(params)

            elif tool == "esegui_codice":
                return self._execute_code(params)

            elif tool == "crea_file":
                return self._execute_file(params)

            elif tool == "ricerca":
                return self._execute_search(params, memory)

            elif tool == "riflessione":
                return "🔍 Riflessione completata", True

            return f"FAIL Tool sconosciuto: {tool}", False

        except Exception as e:
            self.execution_count += 1
            return f"FAIL Errore: {e}", False

    def _execute_calculator(self, params: dict) -> tuple[str, bool]:
        expr = params.get("espressione", "")
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expr):
            return "FAIL Espressione non valida", False
        try:
            result = eval(expr)
            return f"OK {expr} = {result}", True
        except:
            return "FAIL Calcolo errato", False

    def _execute_code(self, params: dict) -> tuple[str, bool]:
        codice = params.get("codice", "")
        if len(codice) > 2000:
            return "FAIL Codice troppo lungo", False
        if any(
            d in codice.lower()
            for d in ["import os", "import sys", "subprocess", "__import__"]
        ):
            return "FAIL Import non consentiti", False

        old_stdout = sys.stdout
        sys.stdout = captured = io.StringIO()
        try:
            exec(codice, SAFE_GLOBALS, {})
            sys.stdout = old_stdout
            output = captured.getvalue() or "OK Eseguito"
            return f"OK {output}", True
        except Exception as e:
            sys.stdout = old_stdout
            return f"FAIL {e}", False

    def _execute_file(self, params: dict) -> tuple[str, bool]:
        percorso = params.get("percorso", "output.txt")
        if ".." in percorso or percorso.startswith("/"):
            return "FAIL Percorso non consentito", False

        safe_path = os.path.join(SAFE_WORKSPACE, os.path.basename(percorso))
        try:
            with open(safe_path, "w") as f:
                f.write(params.get("contenuto", "")[:10000])
            return f"OK File: {safe_path}", True
        except Exception as e:
            return f"FAIL {e}", False

    def _execute_search(self, params: dict, memory) -> tuple[str, bool]:
        query = params.get("query", "")
        results = memory.vector.search(query, k=3)
        if results:
            return "📚 Risultati:\n" + "\n".join(
                [f"- {r['text'][:80]}" for r in results]
            ), True
        return "📚 Nessun risultato", True

    def reset(self):
        self.execution_count = 0


class Critic:
    """CRITIC: valuta la qualità dei risultati."""

    def __init__(self):
        pass

    def critique(
        self, outputs: List[tuple[str, bool]], plan: List[dict]
    ) -> Dict[str, Any]:
        """Valuta outputs e ritorna punteggio + feedback."""

        if not outputs:
            return {
                "score": 0.0,
                "status": "FAIL",
                "reason": "Nessun output",
                "suggestion": "Riprova con più step",
            }

        success_count = sum(1 for _, success in outputs if success)
        total = len(outputs)

        score = success_count / max(1, total)

        if score == 0:
            return {
                "score": 0.0,
                "status": "FAIL",
                "reason": "Tutti gli step falliti",
                "suggestion": "Ricomposta il piano",
            }

        if score < 0.5:
            return {
                "score": score,
                "status": "WEAK",
                "reason": "Alcuni step falliti",
                "suggestion": "Migliora la pianificazione",
            }

        if score < 1.0:
            return {
                "score": score,
                "status": "PARTIAL",
                "reason": "Quasi tutto ok",
                "suggestion": "Rifletti sul risultato",
            }

        return {
            "score": score,
            "status": "OK",
            "reason": "Tutto eseguito con successo",
            "suggestion": "Ottimo lavoro!",
        }


class ReflectionLoop:
    """REFLECTION LOOP: migliora la strategia dell'agente."""

    def __init__(self):
        pass

    def reflect(
        self,
        state: AgentState,
        critique: Dict[str, Any],
        outputs: List[tuple[str, bool]],
    ) -> AgentState:
        """Aggiorna lo stato dell'agente basandosi sulla valutazione."""

        score = critique["score"]
        status = critique["status"]

        state.total_executions += 1
        if status == "OK" or status == "PARTIAL":
            state.successful_executions += 1

        new_success_rate = state.successful_executions / max(1, state.total_executions)

        if status == "FAIL":
            state.strategy_level = min(5, state.strategy_level + 1)
            state.last_errors.append(critique["reason"])
            state.improvement_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "action": "level_up",
                    "reason": critique["reason"],
                }
            )

        elif status == "OK" and new_success_rate > 0.8:
            state.strategy_level = max(1, state.strategy_level - 1)
            state.improvement_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "action": "level_down",
                    "reason": "alta riuscita",
                }
            )

        state.success_rate = new_success_rate

        return state


class SelfImprovingAgent:
    """Self-Improving Research Agent completo."""

    def __init__(self):
        self.state = self._load_state()
        self.vector_memory = VectorMemory()
        self.planner = Planner(self._check_llm())
        self.executor = Executor()
        self.critic = Critic()
        self.reflection = ReflectionLoop()

        logger.info(
            f"OK Self-Improving Agent avviato. Strategy: {self.state.strategy_level}, Success: {self.state.success_rate:.2f}"
        )

    def _check_llm(self) -> bool:
        try:
            import ollama

            ollama.list()
            return True
        except:
            return False

    def _load_state(self) -> AgentState:
        state = AgentState()
        if os.path.exists("agent_state.json"):
            try:
                with open("agent_state.json", "r") as f:
                    state.load(json.load(f))
            except:
                pass
        return state

    def _save_state(self):
        with open("agent_state.json", "w") as f:
            json.dump(self.state.to_dict(), f, indent=2)

    def _get_context(self, query: str) -> str:
        results = self.vector_memory.search(query, k=3)
        if results:
            return "\n".join([r["text"][:100] for r in results])
        return ""

    def run(
        self, user_input: str, max_iterations: int = MAX_REFLECTION_ITERATIONS
    ) -> Dict[str, Any]:
        """Esegue il loop completo: plan → execute → critique → reflect → memory."""

        self.executor.reset()

        context = self._get_context(user_input)

        for iteration in range(max_iterations):
            logger.info(f"📋 Iterazione {iteration + 1}/{max_iterations}")

            plan = self.planner.plan(user_input, self.state, context)
            logger.info(f"   Piano: {len(plan)} step")

            outputs = []
            for step in plan:
                output, success = self.executor.execute(step, self.vector_memory)
                outputs.append((output, success))
                logger.info(
                    f"   Step: {step.get('tool')} → {'OK' if success else 'FAIL'}"
                )

            critique = self.critic.critique(outputs, plan)
            logger.info(
                f"   Critic: {critique['status']} (score: {critique['score']:.2f})"
            )

            self.state = self.reflection.reflect(self.state, critique, outputs)
            self._save_state()

            if critique["status"] == "OK":
                break

            if critique["status"] == "FAIL" and iteration < max_iterations - 1:
                logger.info(
                    f"   🔄 Retry con strategia livello {self.state.strategy_level}"
                )
                context += (
                    f"\n[Iterazione {iteration + 1} fallita: {critique['reason']}]"
                )

        final_output = "\n".join([out for out, _ in outputs])

        self.vector_memory.add(
            user_input,
            {
                "output": final_output[:200],
                "status": critique["status"],
                "score": critique["score"],
                "strategy_level": self.state.strategy_level,
                "success_rate": self.state.success_rate,
            },
        )

        self._save_memory(user_input, final_output, critique)

        return {
            "output": final_output,
            "critique": critique,
            "state": self.state.to_dict(),
            "iterations": iteration + 1,
        }

    def _save_memory(self, input_text: str, output: str, critique: Dict):
        memory_data = {"history": [], "conoscenze": {}}

        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    memory_data = json.load(f)
            except:
                pass

        memory_data["history"].append(
            {
                "input": input_text[:200],
                "output": output[:200],
                "status": critique["status"],
                "score": critique["score"],
                "timestamp": datetime.now().isoformat(),
            }
        )

        if len(memory_data["history"]) > 100:
            memory_data["history"] = memory_data["history"][-50:]

        with open(MEMORY_FILE, "w") as f:
            json.dump(memory_data, f, indent=2)

    def get_status(self) -> str:
        return f"""[*] Agent Status:
  Strategy Level: {self.state.strategy_level}
  Success Rate: {self.state.success_rate:.2%}
  Total Executions: {self.state.total_executions}
  Successful: {self.state.successful_executions}
  Errors: {len(self.state.last_errors)}"""


def main():
    """Demo Self-Improving Agent."""
    agent = SelfImprovingAgent()

    print("\n[*] Self-Improving Research Agent v7")
    print("Architecture: Planner -> Executor -> Critic -> Reflection -> Memory")
    print("Digita 'esci' per uscire, 'stato' per info")

    while True:
        user_input = input(">> ").strip()

        if user_input.lower() in ["esci", "exit"]:
            print("Ciao!")
            break

        if user_input.lower() == "stato":
            print(f"\n{agent.get_status()}\n")
            continue

        if not user_input:
            continue

        result = agent.run(user_input)

        print(f"\n-- Output:")
        print(result["output"])
        print(
            f"\n-- Valutazione: {result['critique']['status']} | Score: {result['critique']['score']:.2f}"
        )
        print(f"-- Iterazioni: {result['iterations']}")
        print(f"-- Suggerimento: {result['critique']['suggestion']}\n")


if __name__ == "__main__":
    main()
