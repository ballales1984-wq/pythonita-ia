"""
Safe Tool System
Tool sicuri per eseguire azioni in sandbox
"""

import os
import io
import sys
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

SAFE_WORKSPACE = "workspace"
MAX_CODE_SIZE = 2000

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

ALLOWED_TOOLS = ["crea_file", "esegui_codice", "calcola", "memoria", "rispondi"]


def init_workspace():
    Path(SAFE_WORKSPACE).mkdir(exist_ok=True)


class SafeTool:
    """Base class per tool sicuri."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def execute(self, memory: dict = None, **kwargs) -> str:
        raise NotImplementedError


class SafeFileTool(SafeTool):
    """Tool per creare file in modo sicuro."""

    def __init__(self):
        super().__init__("crea_file", "Crea un file nella workspace sicura")
        init_workspace()

    def execute(
        self, memory: dict = None, percorso: str = "output.py", contenuto: str = ""
    ) -> str:
        if ".." in percorso or percorso.startswith("/") or ":" in percorso:
            return "❌ Percorso non consentito (path traversal blocked)"

        safe_path = os.path.join(SAFE_WORKSPACE, os.path.basename(percorso))

        try:
            with open(safe_path, "w", encoding="utf-8") as f:
                f.write(contenuto[:10000])
            logger.info(f"✅ File creato: {safe_path}")
            return f"✅ File creato: {safe_path}"
        except Exception as e:
            logger.error(f"Errore file: {e}")
            return f"❌ Errore: {e}"


class SafePythonTool(SafeTool):
    """Tool per eseguire codice Python in sandbox."""

    def __init__(self):
        super().__init__("esegui_codice", "Esegua codice Python in sandbox sicuro")

    def _is_safe_code(self, codice: str) -> bool:
        codice_lower = codice.lower()
        dangerous = [
            "import os",
            "import sys",
            "import subprocess",
            "import socket",
            "import requests",
            "__import__",
            "eval(",
            "exec(",
            "open(",
            "os.",
            "subprocess.",
            "sys.exit",
        ]
        return not any(d in codice_lower for d in dangerous)

    def execute(self, memory: dict = None, codice: str = "") -> str:
        if len(codice) > MAX_CODE_SIZE:
            return f"❌ Codice troppo lungo (max {MAX_CODE_SIZE} char)"

        if not self._is_safe_code(codice):
            return "❌ Codice non sicuro - import/operazioni pericolose bloccate"

        old_stdout = sys.stdout
        sys.stdout = captured = io.StringIO()

        try:
            result = {}
            exec(codice, SAFE_GLOBALS, result)
            sys.stdout = old_stdout

            output = captured.getvalue()
            if not output:
                output = (
                    str(result)[:500] if result else "✅ Codice eseguito senza output"
                )

            logger.info(f"✅ Codice eseguito")
            return f"✅ {output}"
        except Exception as e:
            sys.stdout = old_stdout
            logger.error(f"Errore exec: {e}")
            return f"❌ Errore: {e}"


class SafeCalculatorTool(SafeTool):
    """Tool per calcoli matematici sicuri."""

    def __init__(self):
        super().__init__("calcola", "Esegue calcoli matematici")

    def execute(self, memory: dict = None, espressione: str = "") -> str:
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in espressione):
            return "❌ Caratteri non permessi nell'espressione"

        try:
            result = eval(espressione)
            logger.info(f"✅ Calcolo: {espressione} = {result}")
            return f"✅ {espressione} = {result}"
        except Exception as e:
            return f"❌ Errore calcolo: {e}"


class SafeMemoryTool(SafeTool):
    """Tool per gestire la memoria."""

    def __init__(self):
        super().__init__("memoria", "Gestisce la memoria strutturata")

    def execute(
        self,
        memory: dict = None,
        azione: str = "",
        chiave: str = "",
        valore: str = "",
        cerca: str = "",
    ) -> str:
        from .memory import StructuredMemory, VectorMemoryRAG

        struct = StructuredMemory()
        vector = VectorMemoryRAG()

        if azione == "salva" and chiave and valore:
            struct.memorize(chiave, valore)
            vector.add(f"{chiave}: {valore}", {"tipo": "conoscenza", "chiave": chiave})
            return f"🧠 Memorizzato: {chiave}"

        if azione == "leggi" and chiave:
            result = struct.recall(chiave)
            if result:
                return f"🧠 {chiave}: {result}"
            return f"🧠 Nessun dato per: {chiave}"

        if azione == "cerca" and cerca:
            results = vector.search(cerca, k=3)
            if results:
                return "🧠 Risultati:\n" + "\n".join(
                    [f"- {r['text'][:80]}... (sim: {r['similarity']})" for r in results]
                )
            return "🧠 Nessun risultato"

        if azione == "stato":
            return struct.status()

        return "🧠 Usa: memoria(salva|leggi|cerca|stato)"


class SafeRouter:
    """Router che instrada le azioni ai tool appropriati."""

    def __init__(self):
        self.tools = {
            "crea_file": SafeFileTool(),
            "esegui_codice": SafePythonTool(),
            "calcola": SafeCalculatorTool(),
            "memoria": SafeMemoryTool(),
        }
        self.execution_count = 0
        self.max_steps = 5

    def route(self, action: str, params: dict, memory: dict = None) -> str:
        if self.execution_count >= self.max_steps:
            return "❌ Limite esecuzioni raggiunto"

        if action not in ALLOWED_TOOLS:
            return f"❌ Tool non permesso: {action}"

        if action == "rispondi":
            return params.get("risposta", params.get("testo", "Come posso aiutarti?"))

        if action in self.tools:
            self.execution_count += 1
            return self.tools[action].execute(memory, **params)

        return f"❌ Azione sconosciuta: {action}"

    def reset(self):
        self.execution_count = 0
