"""
AI Agent - Versione 4 (SAFE + Vector Memory)
Sicuro + Memory vettoriale semantica
"""

import json
import os
import logging
import re
import io
import sys
from typing import Any, Optional, List
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MEMORY_FILE = "agent_memory.json"
SAFE_WORKSPACE = "workspace"
MAX_STEPS = 5
MAX_MEMORY_SIZE = 500
MAX_CODE_OUTPUT = 1000
ALLOWED_TOOLS = ["crea_file", "esegui_codice", "calcola", "memoria", "rispondi"]

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


def safe_create_workspace():
    """Crea la workspace sicura se non esiste."""
    Path(SAFE_WORKSPACE).mkdir(exist_ok=True)


def load_memory() -> dict:
    """Carica memoria da file JSON."""
    if not os.path.exists(MEMORY_FILE):
        return {"history": [], "stato": {}, "conoscenze": {}, "embeddings": []}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"history": [], "stato": {}, "conoscenze": {}, "embeddings": []}


def save_memory(memory: dict):
    """Salva memoria su file JSON."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


def safe_add_to_memory(
    memory: dict, ruolo: str, contenuto: str, azione: str = None, tool: str = None
):
    """Aggiunge elemento alla memoria con limiti di sicurezza."""
    if len(str(contenuto)) > MAX_MEMORY_SIZE:
        logger.warning("⚠️ Contenuto troppo grande, troncato")
        contenuto = str(contenuto)[:MAX_MEMORY_SIZE]

    entry = {
        "ruolo": ruolo,
        "contenuto": contenuto,
        "timestamp": datetime.now().isoformat(),
    }
    if azione:
        entry["azione"] = azione
    if tool:
        entry["tool"] = tool

    memory["history"].append(entry)

    if len(memory["history"]) > 100:
        memory["history"] = memory["history"][-50:]

    save_memory(memory)
    return memory


def memorizza(memory: dict, chiave: str, valore: Any) -> dict:
    """Memorizza informazione chiave-valore."""
    if len(str(valore)) > MAX_MEMORY_SIZE:
        valore = str(valore)[:MAX_MEMORY_SIZE]

    memory["conoscenze"][chiave] = {
        "valore": valore,
        "timestamp": datetime.now().isoformat(),
    }
    save_memory(memory)
    return memory


def recupera(memory: dict, chiave: str) -> Optional[Any]:
    """Recupera informazione dalla memoria."""
    if chiave in memory["conoscenze"]:
        return memory["conoscenze"][chiave]["valore"]
    return None


def search_semantic(memory: dict, query: str, top_k: int = 3) -> List[dict]:
    """Cerca nella memoria in modo semantico (keyword matching)."""
    if not memory.get("history"):
        return []

    query_lower = query.lower()
    query_words = set(query_lower.split())

    scored = []
    for entry in memory["history"]:
        content_lower = entry.get("contenuto", "").lower()

        matches = sum(1 for word in query_words if word in content_lower)
        score = matches / max(len(query_words), 1)

        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [entry for _, entry in scored[:top_k]]


def add_embedding(memory: dict, chiave: str, embedding: List[float]):
    """Aggiunge embedding vettoriale."""
    if "embeddings" not in memory:
        memory["embeddings"] = []

    memory["embeddings"].append(
        {
            "chiave": chiave,
            "vector": embedding[:128],
            "timestamp": datetime.now().isoformat(),
        }
    )

    if len(memory["embeddings"]) > 50:
        memory["embeddings"] = memory["embeddings"][-25:]

    save_memory(memory)


class SafeTool:
    """Base class per tool con validazione."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def validate_params(self, **kwargs) -> bool:
        return True

    def execute(self, memory: dict, **kwargs) -> str:
        raise NotImplementedError


class SafeFileTool(SafeTool):
    """Tool per creare file con sicurezza."""

    def __init__(self):
        super().__init__("crea_file", "Crea un file nella workspace sicura")

    def validate_params(self, **kwargs) -> bool:
        percorso = kwargs.get("percorso", "")
        if ".." in percorso or percorso.startswith("/") or ":" in percorso:
            return False
        return True

    def execute(self, memory: dict, percorso: str, contenuto: str) -> str:
        if not self.validate_params(percorso=percorso):
            return "❌ Percorso non consentito"

        safe_create_workspace()

        safe_path = os.path.join(SAFE_WORKSPACE, os.path.basename(percorso))

        try:
            with open(safe_path, "w", encoding="utf-8") as f:
                f.write(contenuto[:10000])
            safe_add_to_memory(
                memory, "system", f"File creato: {safe_path}", azione="crea_file"
            )
            return f"✅ File creato: {safe_path}"
        except Exception as e:
            return f"❌ Errore: {e}"


class SafePythonTool(SafeTool):
    """Tool per eseguire codice Python in sandbox."""

    def __init__(self):
        super().__init__("esegui_codice", "Esegua codice Python in sandbox")

    def execute(self, memory: dict, codice: str) -> str:
        if len(codice) > 2000:
            return "❌ Codice troppo lungo (max 2000 char)"

        codice = codice.strip()
        if any(
            d in codice.lower()
            for d in [
                "import os",
                "import sys",
                "import subprocess",
                "open(",
                "__import__",
            ]
        ):
            return "❌ Import non consentiti in sandbox"

        old_stdout = sys.stdout
        sys.stdout = captured = io.StringIO()

        try:
            result = {}
            exec(codice, SAFE_GLOBALS, result)
            sys.stdout = old_stdout

            output = captured.getvalue()
            if not output and result:
                output = str(result)[:MAX_CODE_OUTPUT]
            elif output:
                output = output[:MAX_CODE_OUTPUT]
            else:
                output = "✅ Codice eseguito"

            safe_add_to_memory(
                memory, "system", f"Eseguito: {codice[:50]}...", azione="esegui_codice"
            )
            return f"✅ {output}"
        except Exception as e:
            sys.stdout = old_stdout
            return f"❌ Errore: {e}"


class SafeCalculatorTool(SafeTool):
    """Tool per calcoli con validazione."""

    def __init__(self):
        super().__init__("calcola", "Esegue calcoli matematici sicuri")

    def validate_params(self, **kwargs) -> bool:
        expr = kwargs.get("espressione", "")
        allowed_chars = set("0123456789+-*/.() ")
        return all(c in allowed_chars for c in expr)

    def execute(self, memory: dict, espressione: str) -> str:
        if not self.validate_params(espressione=espressione):
            return "❌ Espressione non valida"

        try:
            result = eval(espressione)
            safe_add_to_memory(
                memory, "system", f"Calcolo: {espressione} = {result}", azione="calcola"
            )
            return f"✅ {espressione} = {result}"
        except Exception as e:
            return f"❌ Errore: {e}"


class SafeMemoryTool(SafeTool):
    """Tool per memoria con limiti."""

    def __init__(self):
        super().__init__("memoria", "Memorizza o recupera informazioni")

    def execute(
        self, memory: dict, azione: str = None, chiave: str = None, valore: str = None
    ) -> str:
        if azione == "salva" and chiave and valore:
            memory = memorizza(memory, chiave, valore[:500])
            return f"🧠 Memorizzato: {chiave}"

        if azione == "leggi" and chiave:
            result = recupera(memory, chiave)
            if result:
                return f"🧠 {chiave}: {result}"
            return f"🧠 Nessun dato per: {chiave}"

        if azione == "cerca" and chiave:
            results = search_semantic(memory, chiave)
            if results:
                return f"🧠 Risultati per '{chiave}':\n" + "\n".join(
                    [f"- {r['contenuto'][:100]}" for r in results]
                )
            return f"🧠 Nessun risultato per: {chiave}"

        if azione == "stato":
            return f"🧠 Memoria: {len(memory['history'])} eventi, {len(memory['conoscenze'])} conoscenze"

        return "🧠 Usa: memoria(salva|leggi|cerca, chiave, valore)"


class SafeRouter:
    """Router con whitelist e limiti."""

    def __init__(self):
        self.tools = {
            "crea_file": SafeFileTool(),
            "esegui_codice": SafePythonTool(),
            "calcola": SafeCalculatorTool(),
            "memoria": SafeMemoryTool(),
        }
        self.execution_count = 0

    def route(self, action: str, params: dict, memory: dict) -> str:
        """Instrada con validazione."""

        if self.execution_count >= MAX_STEPS:
            return "❌ Limite esecuzioni raggiunto"

        if action not in ALLOWED_TOOLS:
            return f"❌ Tool non permesso: {action}"

        if action == "rispondi":
            return params.get("testo", "Come posso aiutarti?")

        if action in self.tools:
            self.execution_count += 1
            tool = self.tools[action]
            return tool.execute(memory, **params)

        return f"❌ Azione sconosciuta: {action}"

    def reset_count(self):
        self.execution_count = 0


class Agent:
    """AI Agent sicuro con memory vettoriale."""

    def __init__(self):
        self.memory = load_memory()
        self.router = SafeRouter()
        self.llm = None
        self._init_llm()

        logger.info(
            f"✅ Agent v4 avviato. Memoria: {len(self.memory['history'])} eventi"
        )

    def _init_llm(self):
        """Inizializza LLM."""
        try:
            import ollama

            ollama.list()
            self.llm = "ollama"
            logger.info("✅ LLM connesso (Ollama)")
        except:
            self.llm = None
            logger.warning("⚠️ LLM non disponibile")

    def plan_action(self, input_text: str) -> dict:
        """Decision layer con contesto memoria."""

        contesto = ""
        if self.memory["history"]:
            recent = self.memory["history"][-3:]
            contesto = "\n".join([f"{c['ruolo']}: {c['contenuto']}" for c in recent])

        conoscenze = list(self.memory["conoscenze"].keys())
        if conoscenze:
            contesto += f"\nConoscenze: {conoscenze}"

        prompt = f"""Sei un AI Agent italiano SICURO. Analizza la richiesta e decidi cosa fare.

Contesto recente:
{contesto}

Regole di sicurezza:
- NON usare import os, sys, subprocess
- File salvati solo nella cartella 'workspace'
- Max 5 azioni per richiesta

Azioni disponibili (SOLO queste):
- "rispondi" - per saluti e domande
- "crea_file" - per creare file (percorso, contenuto)
- "esegui_codice" - per Python (codice) - NO import pericolosi
- "calcola" - per calcoli (espressione)
- "memoria" - per salvare/leggere/cercare (azione: salva|leggi|cerca, chiave, valore)

Richiesta: "{input_text}"

Rispondi SOLO con JSON:
{{"azione": "nome", "parametri": {{"chiave": "valore"}}}}

JSON:"""

        if self.llm:
            return self._plan_with_llm(prompt)
        return self._plan_fallback(input_text)

    def _plan_with_llm(self, prompt: str) -> dict:
        try:
            import ollama

            risposta = ollama.chat(
                model="llama3.2", messages=[{"role": "user", "content": prompt}]
            )
            content = risposta["message"]["content"].strip()

            if "{" in content:
                json_str = content[content.find("{") : content.rfind("}") + 1]
                return json.loads(json_str)
        except Exception as e:
            logger.error(f"Errore LLM: {e}")

        return {"azione": "rispondi", "parametri": {}}

    def _plan_fallback(self, input_text: str) -> dict:
        text = input_text.lower()

        if any(x in text for x in ["calcola", "quanto fa"]) and re.search(r"\d+", text):
            expr = re.sub(r"[^\d+\-*/().]", "", text)
            return {"azione": "calcola", "parametri": {"espressione": expr}}

        if any(x in text for x in ["salva", "crea file"]):
            return {
                "azione": "crea_file",
                "parametri": {"percorso": "output.txt", "contenuto": input_text},
            }

        if any(x in text for x in ["chiama", "nome"]):
            nome = re.search(r"mi chiamo (\w+)", text)
            if nome:
                return {
                    "azione": "memoria",
                    "parametri": {
                        "azione": "salva",
                        "chiave": "nome_utente",
                        "valore": nome.group(1),
                    },
                }

        return {"azione": "rispondi", "parametri": {}}

    def run(self, input_text: str) -> str:
        """Esegue ciclo completo dell'agent."""

        safe_add_to_memory(self.memory, "utente", input_text)

        piano = self.plan_action(input_text)
        logger.info(f"📋 Piano: {piano}")

        risultato = self.router.route(
            piano.get("azione", "rispondi"), piano.get("parametri", {}), self.memory
        )

        safe_add_to_memory(self.memory, "agent", str(risultato)[:100])
        self.router.reset_count()

        return risultato

    def get_stato(self) -> str:
        return f"📊 Memoria: {len(self.memory['history'])} eventi, {len(self.memory['conoscenze'])} conoscenze"


def main():
    """Demo AI Agent v4."""
    safe_create_workspace()
    agent = Agent()

    print("\n🤖 AI Agent v4 - SAFE + Vector Memory")
    print("Workspace: ./workspace | Max steps: 5 | 'esci' per uscire\n")

    while True:
        user_input = input("➤ ").strip()

        if user_input.lower() in ["esci", "exit"]:
            print("👋 Ciao!")
            break

        if user_input.lower() == "stato":
            print(f"\n{agent.get_stato()}\n")
            continue

        if not user_input:
            continue

        result = agent.run(user_input)
        print(f"\n{result}\n")


if __name__ == "__main__":
    main()
