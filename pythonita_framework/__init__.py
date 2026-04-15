"""
Pythonita AI Agent Framework v1.0
Framework multi-agent offline per applicazioni didattiche e automazione
https://github.com/ballales1984-wq/pythonita-ia
"""

__version__ = "1.0.0"
__author__ = "Pythonita IA Team"
__license__ = "MIT"

from .orchestrator import MultiAgentOrchestrator, AgentType
from .memory import VectorMemoryRAG, StructuredMemory
from .tools import SafeTool, SafeFileTool, SafePythonTool, SafeCalculatorTool
from .agent import BaseAgent, DidatticoAgent, RoboticaAgent, CodiceAgent

__all__ = [
    "MultiAgentOrchestrator",
    "AgentType",
    "VectorMemoryRAG",
    "StructuredMemory",
    "SafeTool",
    "SafeFileTool",
    "SafePythonTool",
    "SafeCalculatorTool",
    "BaseAgent",
    "DidatticoAgent",
    "RoboticaAgent",
    "CodiceAgent",
]

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🧠 PYTHONITA AI AGENT FRAMEWORK                                            ║
║                                                                              ║
║   Framework Python offline per costruire AI Agent con:                       ║
║   • Multi-agent system (didattico, robotica, codice)                        ║
║   • Vector memory (Chroma + sentence-transformers)                          ║
║   • Safe execution (sandbox, whitelist)                                     ║
║   • Tool system (file, codice, calcoli)                                     ║
║                                                                              ║
║   INSTALLAZIONE:                                                              ║
║   pip install -r requirements.txt                                           ║
║                                                                              ║
║   USO RAPIDO:                                                                ║
║   from pythonita_framework import MultiAgentOrchestrator                    ║
║   agent = MultiAgentOrchestrator()                                          ║
║   result = agent.process("spiegami i for loop")                             ║
║                                                                              ║
║   REQUISITI:                                                                  ║
║   - Python 3.8+                                                              ║
║   - Ollama con llama3.2 (opzionale, fallback integrato)                     ║
║   - chromadb, sentence-transformers (opzionali)                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

"""
📦 STRUTTURA PACKAGE

pythonita_framework/
├── __init__.py          # Questo file
├── orchestrator.py      # Multi-agent orchestrator
├── memory.py           # Vector + structured memory  
├── tools.py            # Safe tool system
├── agent.py            # Agent base class + specialisti
└── requirements.txt    # Dipendenze

📚 ESEMPI D'USO

1. Agentbase:
```python
from pythonita_framework import BaseAgent, AgentType

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.GENERALE, "MioAgent", "Descrizione")
    
    def can_handle(self, query):
        return 0.8 if "mio" in query.lower() else 0.0
    
    def process(self, query, context):
        return {"risposta": "Ciao!", "azione": "rispondi"}
```

2. Tool custom:
```python
from pythonita_framework import SafeTool

class MyTool(SafeTool):
    def __init__(self):
        super().__init__("mytool", "Il mio tool")
    
    def execute(self, memory, **kwargs):
        return "Risultato"
```

3. Orchestrator completo:
```python
from pythonita_framework import MultiAgentOrchestrator

orch = MultiAgentOrchestrator()
result = orch.process("crea una funzione somma")
print(result)
```

🔒 SICUREZZA

- Sandbox per exec() con whitelist funzioni
- Path traversal protection
- Max step limit (5 per richiesta)
- Memory size limit (500 char)

📄 LICENZA: MIT
🔗 Repo: https://github.com/ballales1984-wq/pythonita-ia
"""
