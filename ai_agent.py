"""
AI Agent v4 - SAFE + Vector Memory
Memoria semantica persistente con Chroma + sentence-transformers
"""

import json
import os
import logging
import re
import io
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MEMORY_FILE = "agent_memory_safe.json"
VECTOR_DB_PATH = "./vector_memory"
SAFE_WORKSPACE = "workspace_agent"
MAX_STEPS = 5
MAX_MEMORY_SIZE = 500

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


class VectorMemory:
    """Memoria vettoriale semantica con Chroma."""

    def __init__(self):
        self.client = None
        self.collection = None
        self._init_vector_db()

    def _init_vector_db(self):
        try:
            import chromadb
            from chromadb.utils import embedding_functions

            Path(VECTOR_DB_PATH).mkdir(exist_ok=True)
            self.client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
            self.embedding_fn = (
                embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
            )
            self.collection = self.client.get_or_create_collection(
                name="pythonita_agent_memory",
                embedding_function=self.embedding_fn,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info("✅ Vector memory attivata (Chroma + MiniLM)")
        except ImportError:
            logger.warning(
                "⚠️ Chroma non installato. Usa: pip install chromadb sentence-transformers"
            )
            self.client = None
        except Exception as e:
            logger.warning(f"⚠️ Vector DB non disponibile: {e}")
            self.client = None

    def add(self, text: str, metadata: dict = None, doc_id: str = None) -> bool:
        """Aggiunge testo con embedding semantico."""
        if not self.client or not self.collection:
            return False

        if not metadata:
            metadata = {}
        metadata["timestamp"] = datetime.now().isoformat()

        if not doc_id:
            doc_id = f"mem_{int(datetime.now().timestamp() * 1000)}"

        try:
            self.collection.add(
                documents=[text[:1000]], metadatas=[metadata], ids=[doc_id]
            )
            return True
        except Exception as e:
            logger.error(f"Errore aggiunta vector: {e}")
            return False

    def search(self, query: str, k: int = 5) -> List[dict]:
        """Ricerca semantica (RAG)."""
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
            ]
        except Exception as e:
            logger.error(f"Errore ricerca: {e}")
            return []


def safe_create_workspace():
    Path(SAFE_WORKSPACE).mkdir(exist_ok=True)


def load_structured_memory() -> dict:
    if not os.path.exists(MEMORY_FILE):
        return {"history": [], "stato": {}, "conoscenze": {}, "version": "v4_vector"}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"history": [], "stato": {}, "conoscenze": {}, "version": "v4_vector"}


def save_structured_memory(memory: dict):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


def safe_add_to_memory(memory: dict, ruolo: str, contenuto: str, azione: str = None):
    if len(str(contenuto)) > MAX_MEMORY_SIZE:
        contenuto = str(contenuto)[:MAX_MEMORY_SIZE]

    entry = {
        "ruolo": ruolo,
        "contenuto": contenuto,
        "timestamp": datetime.now().isoformat(),
    }
    if azione:
        entry["azione"] = azione

    memory["history"].append(entry)
    if len(memory["history"]) > 100:
        memory["history"] = memory["history"][-50:]

    save_structured_memory(memory)
    return memory


def memorizza(memory: dict, chiave: str, valore: Any):
    if len(str(valore)) > MAX_MEMORY_SIZE:
        valore = str(valore)[:MAX_MEMORY_SIZE]
    memory["conoscenze"][chiave] = {
        "valore": valore,
        "timestamp": datetime.now().isoformat(),
    }
    save_structured_memory(memory)


def recupera(memory: dict, chiave: str) -> Optional[Any]:
    if chiave in memory["conoscenze"]:
        return memory["conoscenze"][chiave]["valore"]
    return None


class SafeTool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def execute(self, memory: dict, **kwargs) -> str:
        raise NotImplementedError


class SafeFileTool(SafeTool):
    def __init__(self):
        super().__init__("crea_file", "Crea file nella workspace sicura")

    def execute(self, memory: dict, percorso: str, contenuto: str) -> str:
        if ".." in percorso or percorso.startswith("/") or ":" in percorso:
            return "❌ Percorso non consentito"

        safe_create_workspace()
        safe_path = os.path.join(SAFE_WORKSPACE, os.path.basename(percorso))

        try:
            with open(safe_path, "w", encoding="utf-8") as f:
                f.write(contenuto[:10000])
            safe_add_to_memory(
                memory, "system", f"File: {safe_path}", azione="crea_file"
            )
            return f"✅ File: {safe_path}"
        except Exception as e:
            return f"❌ Errore: {e}"


class SafePythonTool(SafeTool):
    def __init__(self):
        super().__init__("esegui_codice", "Esegua Python in sandbox")

    def execute(self, memory: dict, codice: str) -> str:
        if len(codice) > 2000:
            return "❌ Codice troppo lungo"

        if any(
            d in codice.lower()
            for d in ["import os", "import sys", "import subprocess", "__import__"]
        ):
            return "❌ Import non consentiti"

        old_stdout = sys.stdout
        sys.stdout = captured = io.StringIO()

        try:
            result = {}
            exec(codice, SAFE_GLOBALS, result)
            sys.stdout = old_stdout
            output = captured.getvalue() or str(result)[:1000] or "✅ Eseguito"
            safe_add_to_memory(
                memory, "system", f"Code: {codice[:50]}...", azione="esegui_codice"
            )
            return f"✅ {output}"
        except Exception as e:
            sys.stdout = old_stdout
            return f"❌ Errore: {e}"


class SafeCalculatorTool(SafeTool):
    def __init__(self):
        super().__init__("calcola", "Calcoli matematici")

    def execute(self, memory: dict, espressione: str) -> str:
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in espressione):
            return "❌ Espressione non valida"
        try:
            result = eval(espressione)
            return f"✅ {espressione} = {result}"
        except:
            return f"❌ Errore calcolo"


class SafeMemoryTool(SafeTool):
    def __init__(self):
        super().__init__("memoria", "Memoria strutturata e semantica")

    def execute(
        self,
        memory: dict,
        azione: str = None,
        chiave: str = None,
        valore: str = None,
        cerca: str = None,
        vector_memory: VectorMemory = None,
    ) -> str:
        if azione == "salva" and chiave and valore:
            memorizza(memory, chiave, valore[:500])
            if vector_memory:
                vector_memory.add(
                    f"{chiave}: {valore}", {"tipo": "conoscenza", "chiave": chiave}
                )
            return f"🧠 Memorizzato: {chiave}"

        if azione == "leggi" and chiave:
            result = recupera(memory, chiave)
            if result:
                return f"🧠 {chiave}: {result}"
            return f"🧠 Nessun dato: {chiave}"

        if azione == "cerca" and cerca and vector_memory:
            results = vector_memory.search(cerca, k=3)
            if results:
                return "🧠 Risultati semantici:\n" + "\n".join(
                    [
                        f"- {r['text'][:100]} (sim: {r['similarity']:.2f})"
                        for r in results
                    ]
                )
            return "🧠 Nessun risultato"

        if azione == "stato":
            return f"🧠 Storia: {len(memory['history'])}, Conoscenze: {len(memory['conoscenze'])}"

        return "🧠 Usa: memoria(salva|leggi|cerca|stato)"


class SafeRouter:
    def __init__(self, vector_memory: VectorMemory = None):
        self.vector_memory = vector_memory
        self.tools = {
            "crea_file": SafeFileTool(),
            "esegui_codice": SafePythonTool(),
            "calcola": SafeCalculatorTool(),
            "memoria": SafeMemoryTool(),
        }
        self.execution_count = 0

    def route(self, action: str, params: dict, memory: dict) -> str:
        if self.execution_count >= MAX_STEPS:
            return "❌ Limite raggiunto"

        if action not in ALLOWED_TOOLS:
            return f"❌ Tool non permesso: {action}"

        if action == "rispondi":
            return params.get("testo", "Come posso aiutarti?")

        if action in self.tools:
            self.execution_count += 1
            params["vector_memory"] = self.vector_memory
            return self.tools[action].execute(memory, **params)

        return f"❌ Azione sconosciuta: {action}"

    def reset(self):
        self.execution_count = 0


class Agent:
    """AI Agent sicuro con memoria vettoriale."""

    def __init__(self):
        self.structured_memory = load_structured_memory()
        self.vector_memory = VectorMemory()
        self.router = SafeRouter(self.vector_memory)
        self.llm = None
        self._init_llm()

        logger.info(
            f"✅ Agent v4 Vector. Storia: {len(self.structured_memory['history'])}"
        )

    def _init_llm(self):
        try:
            import ollama

            ollama.list()
            self.llm = "ollama"
            logger.info("✅ LLM connesso")
        except:
            self.llm = None

    def get_relevant_context(self, query: str) -> str:
        results = self.vector_memory.search(query, k=4)
        if not results:
            return ""

        ctx = "\n📚 Contesto dalla memoria:\n"
        for r in results:
            ctx += f"- {r['text'][:120]}...\n"
        return ctx

    def plan_action(self, input_text: str) -> dict:
        contesto_vett = self.get_relevant_context(input_text)

        recent = (
            self.structured_memory["history"][-3:]
            if self.structured_memory["history"]
            else []
        )
        contesto_stru = "\n".join([f"{c['ruolo']}: {c['contenuto']}" for c in recent])

        prompt = f"""Sei Pythonita IA, assistente didattico sicuro.
{contesto_vett}
{contesto_stru}

Richiesta: "{input_text}"

Azioni: rispondi, calcola, esegui_codice, crea_file, memoria(salva|leggi|cerca|stato)

Rispondi SOLO JSON:
{{"azione": "...", "parametri": {{...}}}}

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
            logger.error(f"LLM: {e}")

        return {"azione": "rispondi", "parametri": {}}

    def _plan_fallback(self, input_text: str) -> dict:
        text = input_text.lower()

        if any(x in text for x in ["calcola", "quanto fa"]) and re.search(r"\d+", text):
            expr = re.sub(r"[^\d+\-*/().]", "", text)
            return {"azione": "calcola", "parametri": {"espressione": expr}}

        if any(x in text for x in ["salva", "ricorda"]):
            return {
                "azione": "memoria",
                "parametri": {
                    "azione": "salva",
                    "chiave": "info",
                    "valore": input_text,
                },
            }

        if "cerca" in text:
            return {
                "azione": "memoria",
                "parametri": {"azione": "cerca", "cerca": input_text},
            }

        return {"azione": "rispondi", "parametri": {}}

    def run(self, input_text: str) -> str:
        self.vector_memory.add(input_text, {"ruolo": "utente", "tipo": "input"})

        piano = self.plan_action(input_text)
        risultato = self.router.route(
            piano.get("azione"), piano.get("parametri", {}), self.structured_memory
        )

        safe_add_to_memory(self.structured_memory, "utente", input_text)
        safe_add_to_memory(self.structured_memory, "agent", str(risultato)[:100])
        self.vector_memory.add(risultato, {"ruolo": "agent", "tipo": "output"})

        self.router.reset()
        return risultato


def main():
    safe_create_workspace()
    agent = Agent()

    print("\n🤖 Pythonita IA - SAFE Agent v4 + Vector Memory")
    print("Digita 'esci' per uscire, 'stato' per info\n")

    while True:
        user_input = input("➤ ").strip()

        if user_input.lower() in ["esci", "exit"]:
            print("👋 Ciao!")
            break

        if user_input.lower() == "stato":
            print(f"📊 Memoria: {len(agent.structured_memory['history'])} eventi")
            continue

        if not user_input:
            continue

        result = agent.run(user_input)
        print(f"\n{result}\n")


if __name__ == "__main__":
    main()
