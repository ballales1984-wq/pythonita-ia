"""
AI Agent - Versione 2
Memory persistente + Stato tra sessioni
Tool: code/file/calculator/memory
"""

import json
import os
import logging
import re
from typing import Any, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MEMORY_FILE = "agent_memory.json"


def load_memory() -> dict:
    """Carica memoria da file JSON."""
    if not os.path.exists(MEMORY_FILE):
        return {"history": [], "stato": {}, "conoscenze": {}}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"history": [], "stato": {}, "conoscenze": {}}


def save_memory(memory: dict):
    """Salva memoria su file JSON."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


def add_to_memory(
    memory: dict, ruolo: str, contenuto: str, azione: str = None, tool: str = None
):
    """Aggiunge elemento alla memoria."""
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


class Tool:
    """Base class per i tool."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def execute(self, memory: dict, **kwargs) -> str:
        raise NotImplementedError


class FileTool(Tool):
    """Tool per creare e gestire file."""

    def __init__(self):
        super().__init__("crea_file", "Crea un file con il contenuto specificato")

    def execute(self, memory: dict, percorso: str, contenuto: str) -> str:
        try:
            with open(percorso, "w", encoding="utf-8") as f:
                f.write(contenuto)
            add_to_memory(
                memory, "system", f"File creato: {percorso}", azione="crea_file"
            )
            return f"✅ File creato: {percorso}"
        except Exception as e:
            return f"❌ Errore: {e}"


class PythonTool(Tool):
    """Tool per eseguire codice Python."""

    def __init__(self):
        super().__init__("esegui_codice", "Esegua codice Python")

    def execute(self, memory: dict, codice: str) -> str:
        try:
            result = {}
            exec(codice, {}, result)
            output = str(result) if result else "✅ Codice eseguito"
            add_to_memory(
                memory,
                "system",
                f"Codice eseguito: {codice[:50]}...",
                azione="esegui_codice",
            )
            return f"✅ Risultato: {output}"
        except Exception as e:
            return f"❌ Errore: {e}"


class CalculatorTool(Tool):
    """Tool per calcoli matematici."""

    def __init__(self):
        super().__init__("calcola", "Esegue calcoli matematici")

    def execute(self, memory: dict, espressione: str) -> str:
        try:
            result = eval(espressione)
            add_to_memory(
                memory, "system", f"Calcolo: {espressione} = {result}", azione="calcola"
            )
            return f"✅ {espressione} = {result}"
        except Exception as e:
            return f"❌ Errore: {e}"


class MemoryTool(Tool):
    """Tool per memorizzare e recuperare informazioni."""

    def __init__(self):
        super().__init__("memoria", "Memorizza o recupera informazioni")

    def execute(
        self, memory: dict, azione: str = None, chiave: str = None, valore: str = None
    ) -> str:
        if azione == "salva" and chiave and valore:
            memory = memorizza(memory, chiave, valore)
            return f"🧠 Memorizzato: {chiave} = {valore}"

        if azione == "leggi" and chiave:
            result = recupera(memory, chiave)
            if result:
                return f"🧠 {chiave}: {result}"
            return f"🧠 Nessun dato per: {chiave}"

        if azione == "stato":
            return f"🧠 Memoria: {len(memory['history'])} eventi, {len(memory['conoscenze'])} conoscenze"

        return "🧠 Usa: memoria(salva, chiave, valore) o memoria(leggi, chiave)"


class Router:
    """Router che instrada le azioni ai tool."""

    def __init__(self):
        self.tools = {
            "crea_file": FileTool(),
            "esegui_codice": PythonTool(),
            "calcola": CalculatorTool(),
            "memoria": MemoryTool(),
        }

    def route(self, action: str, params: dict, memory: dict) -> str:
        """Instrada l'azione al tool appropriato."""

        if action == "rispondi":
            return params.get("testo", "Come posso aiutarti?")

        if action in self.tools:
            tool = self.tools[action]
            return tool.execute(memory, **params)

        return f"❌ Azione sconosciuta: {action}"


class Agent:
    """AI Agent con memoria persistente."""

    def __init__(self):
        self.memory = load_memory()
        self.router = Router()
        self.llm = None
        self._init_llm()

        logger.info(f"✅ Agent avviato. Memoria: {len(self.memory['history'])} eventi")

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
        """Decision layer: decide cosa fare."""

        contesto = ""
        if self.memory["history"]:
            recent = self.memory["history"][-3:]
            contesto = "\n".join([f"{c['ruolo']}: {c['contenuto']}" for c in recent])

        conoscenze = list(self.memory["conoscenze"].keys())
        if conoscenze:
            contesto += f"\nConoscenze: {conoscenze}"

        prompt = f"""Sei un AI Agent italiano. Analizza la richiesta e decidi cosa fare.

Contesto recente:
{contesto}

Se l'utente fornisce informazioni importanti (nome, preferenze, dati),
USA IL TOOL memoria PER SALVARLI.

Azioni disponibili:
- "rispondi" - per saluti e domande generali
- "crea_file" - per creare file (parametri: percorso, contenuto)
- "esegui_codice" - per eseguire Python (parametri: codice)
- "calcola" - per calcoli (parametri: espressione)
- "memoria" - per salvare/leggere (azione: salva|leggi, chiave, valore)

Richiesta: "{input_text}"

Rispondi SOLO con JSON:
{{"azione": "nome", "parametri": {{"chiave": "valore"}}}}

Esempi:
- "mi chiamo Marco" → {{"azione": "memoria", "parametri": {{"azione": "salva", "chiave": "nome_utente", "valore": "Marco"}}}}
- "come mi chiamo?" → {{"azione": "memoria", "parametri": {{"azione": "leggi", "chiave": "nome_utente"}}}}
- "crea lista 1-5" → {{"azione": "esegui_codice", "parametri": {{"codice": "print(list(range(1,6)))"}}}}
- "2+2" → {{"azione": "calcola", "parametri": {{"espressione": "2+2"}}}}
- "salva in dati.txt" → {{"azione": "crea_file", "parametri": {{"percorso": "dati.txt", "contenuto": "..."}}}}

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

        import re

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

        if any(x in text for x in ["codice", "lista", "python"]):
            return {
                "azione": "esegui_codice",
                "parametri": {"codice": "print('Ciao!')"},
            }

        return {"azione": "rispondi", "parametri": {}}

    def run(self, input_text: str) -> str:
        """Esegue ciclo completo dell'agent."""

        add_to_memory(self.memory, "utente", input_text)

        piano = self.plan_action(input_text)
        logger.info(f"📋 Piano: {piano}")

        risultato = self.router.route(
            piano.get("azione", "rispondi"), piano.get("parametri", {}), self.memory
        )

        add_to_memory(self.memory, "agent", risultato[:100])

        return risultato

    def get_stato(self) -> str:
        """Ritorna stato della memoria."""
        return f"📊 Memoria: {len(self.memory['history'])} eventi, {len(self.memory['conoscenze'])} conoscenze"


def main():
    """Demo AI Agent v2."""
    agent = Agent()

    print("\n🤖 AI Agent v2 - Memory Persistente")
    print("Comandi: 'stato' per vedere memoria, 'esci' per uscire\n")

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
