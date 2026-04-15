# 🧠 Pythonita IA 🇮🇹

**Assistente didattico in italiano con AI locale**  
Genera codice Python da frasi in linguaggio naturale italiano.

## 🌟 Caratteristiche

- ✅ **Interfaccia CLI e GUI** - Scegli quella che preferisci
- 🤖 **AI Locale** - Usa Llama3.2 tramite Ollama (nessuna connessione internet necessaria)
- 🔄 **Fallback Intelligente** - Sistema a regole se l'AI non è disponibile
- 🇮🇹 **Completamente in Italiano** - Parser NLP ottimizzato per l'italiano
- 📚 **Didattico** - Perfetto per imparare Python
- 🚀 **Cache Intelligente** - Query ripetute 24,000x più veloci! (v2.1+)
- 🛡️ **Input Validation** - Protezione da DoS e code injection (v2.1+)
- 🧪 **112 Test Automatici** - Coverage 74% per massima affidabilità (v2.1+)
- 🐍 **143+ Comandi Python** - Supporto completo linguaggio Python (v2.2+)
- 🔗 **Multi-Comando** - Combina più azioni in un unico programma! (v2.3+)
- 🗣️ **Linguaggio Naturale Avanzato** - Analisi SVC e interrogativi (v3.0+)
- 🤖 **Template Robotica** - Genera codice per robot e mani bioniche (v3.0+)
- 🎨 **Visualizzatore 3D** - Vedi i comandi animati in 3D con misure reali! (v3.1+)
- 🍎 **Oggetti 3D** - Afferra mela, palla, cubo con grafica realistica! (v3.1+)
- 🧠 **AI Agent v7** - Self-Improving Agent con Planner, Executor, Critic, Reflection, Memory (v7+)

## 🧠 NOVITÀ v7: AI Agent Self-Improving

**Il cuore intelligente del sistema** - Un agent AI che pensa, esegue, valuta e migliora!

```python
python ai_agent.py
```

### Architettura

```
INPUT → PLANNER → EXECUTOR → CRITIC → REFLECTION → MEMORY
```

### Componenti

| Componente | Funzione |
|------------|----------|
| **Planner** | Genera piano azioni da input |
| **Executor** | Esegue tool in sandbox sicuro |
| **Critic** | Valuta risultati (score 0-1) |
| **Reflection** | Auto-migliora strategy_level |
| **Memory** | Vector DB (Chroma) per memoria semantica |

### Tool Disponibili

- `calcola` - Operazioni matematiche
- `crea_file` - Scrive file in workspace
- `esegui_codice` - Esegue Python in sandbox
- `rispondi` - Risposte testuali

### Esempi

```bash
➤ calcola 100*2
  Output: OK 100*2 = 200

➤ salva hello in test.txt
  Output: OK File: workspace/test.txt
```

### Self-Improving

L'agente impara dalle sue performance:
- Fallimenti → strategy_level +1 (più attento)
- Successi frequenti → strategy_level -1 (più veloce)

### Dipendenze

```bash
pip install chromadb sentence-transformers ollama
```

**Documentazione**: [AI_AGENT_V7.md](AI_AGENT_V7.md)

**Vedi i tuoi comandi robot prendere vita in 3D!**

```bash
python gui_robot_3d.py
```

### Cosa Fa?

1. Scrivi un comando in italiano: **"apri mano"**
2. Vedi il codice Python generato automaticamente
3. Premi "Esegui Animazione 3D"
4. **Guarda la mano 3D aprirsi con misure reali!**

### Animazioni Disponibili:
- 🖐️ **Apri/Chiudi Mano** - Tutte le 5 dita si muovono
- ✊ **Chiudi Pugno** - Formazione pugno completo
- 🤏 **Posizione Pinza** - Pollice + Indice
- 🤖 **Afferra Oggetto** - Chiusura graduale
- 💪 **Alza Braccio** - Movimento spalla/gomito

### Misure Reali Implementate:
```
Palmo: 10cm x 8.5cm
Pollice: 8.3cm    Indice: 9.2cm    Medio: 10.2cm
Anulare: 9.5cm    Mignolo: 7.8cm
Braccio: 55cm totale (30cm + 25cm)
Angoli: 0-90° (dita), 0-150° (gomito)
```

**Documentazione completa**: [VISUALIZZATORE_3D.md](VISUALIZZATORE_3D.md)

### 🍎 NOVITÀ: Oggetti 3D Interattivi!

**Prendi oggetti reali nella scena 3D!**

```python
"prendi mela"        → Mano afferra mela rossa 3D
"afferra palla"      → Mano prende palla arancione
"solleva cubo"       → Mano afferra cubo blu
"rilascia oggetto"   → Mano apre e rilascia
```

**Oggetti disponibili**: Mela, Palla, Cubo, Bottiglia, Smartphone, Tazza

**Demo**:
```bash
python demo_oggetti_3d.py
```

**Documentazione**: [OGGETTI_3D_E_GRAFICA.md](OGGETTI_3D_E_GRAFICA.md)

## 💰 ACQUISTA / PROVA GRATIS

### Opzioni Licenza

- **🆓 TRIAL**: 14 giorni gratis, tutte le funzioni
- **👤 PERSONALE**: €49 - Uso personale, GUI classica, 143 comandi
- **⭐ PRO**: €149 - Visualizzatore 3D, oggetti, template robotica
- **🏢 ENTERPRISE**: €499 - Codice sorgente, supporto dedicato

**[Prova Gratis 14 Giorni](#)** | **[Acquista Ora](#)**

### Download Trial

1. **Scarica**: [PythonitaIA.exe](#) (113 MB)
2. **Doppio click** sul file
3. **Seleziona**: "Attiva Trial 14 giorni"
4. **Usa tutte le features!**

**No installazione Python richiesta** - Funziona subito!

---

## 🚀 Quick Start (Per Sviluppatori)

Se hai il codice sorgente:

```bash
# 1. Clona
git clone https://github.com/ballales1984-wq/pythonita-ia.git
cd pythonita-ia

# 2. Installa dipendenze
pip install -r requirements.txt

# 3. Modello spaCy
python -m spacy download it_core_news_sm

# 4. Avvia
python AVVIA.bat
```

### Uso

**Interfaccia CLI:**
```bash
python main.py
```

**Interfaccia GUI Classica:**
```bash
python gui_pythonita.py
```

**Interfaccia GUI con Visualizzatore 3D (NUOVO!):**
```bash
python gui_robot_3d.py
```

## 💡 Esempi

```
➤ Frase in italiano: stampa ciao mondo

🧾 Codice generato:
print("ciao mondo")
```

```
➤ Frase in italiano: somma 5 e 3

🧾 Codice generato:
print(5 + 3)
```

```
➤ Frase in italiano: crea un ciclo da 1 a 10

🧾 Codice generato:
for i in range(1, 11):
    print(i)
```

## 📁 Struttura del Progetto

```
pythonita-ia/
├── ai_agent.py                   # AI Agent v7 (Self-Improving)
├── pythonita_framework/          # Framework modulare AI Agent
│   ├── __init__.py
│   ├── orchestrator.py          # Multi-agent orchestrator
│   ├── agent.py                 # Agent base classes
│   ├── tools.py                 # Safe tool system
│   ├── memory.py                # Vector + structured memory
│   └── setup.py
├── pythonita/                    # Package principale
│   ├── core/                    # Parser, generatore, validatore
│   ├── visualization/            # Visualizzatore 3D, robot
│   ├── hardware/                # Arduino, CircuitPython
│   ├── gui/                     # Interfacce utente
│   ├── plugins/                 # Plugin system
│   └── utils/                   # Cache, config, export
├── tests/                        # 112 test automatici
├── examples/                     # Esempi d'uso
├── traduttore_semantico.py      # Parser NLP italiano
├── sinonimi.json                # Mappa comandi
└── requirements.txt              # Dipendenze
```

## 🏗️ Architettura

### Architettura Ibrida Intelligente

Pythonita usa un sistema a **due livelli**:

1. **Livello AI (Primario)**
   - Usa Llama3.2 via Ollama
   - Genera codice complesso e naturale
   - Si adatta a richieste variegate

2. **Livello Regole (Fallback)**
   - Sistema basato su pattern matching
   - 28+ comandi Python supportati
   - Attivato se AI non disponibile

### Flusso di Generazione

```
Frase italiana
    ↓
Controllore
    ↓
Generatore (AI disponibile?)
    ├─→ SÌ → Ollama/Llama3.2 → Pulizia output → Codice Python
    └─→ NO → Sistema a regole → Codice Python
```

## 🛠️ Configurazione

Modifica `config.py` per personalizzare:

```python
class Config:
    # Configurazione AI
    AI_ENABLED = True              # Abilita/disabilita AI
    AI_MODEL = "llama3.2"          # Modello Ollama da usare
    AI_FALLBACK_TO_RULES = True    # Fallback a regole
    
    # Configurazione NLP
    SPACY_MODEL = "it_core_news_sm"  # Modello spaCy italiano
```

## 📚 Comandi Supportati

Pythonita IA supporta **143+ comandi Python** con sinonimi italiani! 🚀

### Categorie Principali:

**I/O & Controllo** (11):
- `print`, `input`, `if`, `elif`, `else`, `for`, `while`
- `break`, `continue`, `pass`, `with`

**Strutture Dati** (17):
- Liste: `list`, `append`, `extend`, `insert`, `remove`, `pop`, `clear`, `sort`, `reverse`
- Dizionari: `dict`, `keys`, `values`, `items`, `update`, `get`
- Altro: `tuple`, `set`, `frozenset`

**Matematica** (15):
- Operatori: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- Funzioni: `sum`, `max`, `min`, `abs`, `round`, `pow`, `divmod`

**Stringhe** (11):
- `upper`, `lower`, `split`, `join`, `replace`, `strip`
- `capitalize`, `title`, `find`, `startswith`, `endswith`

**Iterazione** (5):
- `range`, `enumerate`, `zip`, `map`, `filter`

**Conversioni** (9):
- `int`, `float`, `str`, `bool`, `bytes`, `list()`, `tuple()`, `set()`, `dict()`

**File I/O** (7):
- `open`, `read`, `write`, `close`, `readline`, `readlines`, `writelines`

**Gestione Errori** (5):
- `try`, `except`, `finally`, `raise`, `assert`

**OOP** (8):
- `class`, `self`, `super`, `__init__`, `property`, `@staticmethod`, `@classmethod`

**Funzioni** (4):
- `def`, `return`, `lambda`, `yield`

**Moduli Standard Library** (40+):
- Matematica: `math`, `random`, `decimal`, `statistics`
- Data/Tempo: `datetime`, `time`, `calendar`
- File System: `os`, `pathlib`, `shutil`, `glob`
- Serializzazione: `json`, `csv`, `pickle`
- Testo: `re`, `string`, `textwrap`
- Collezioni: `collections`, `array`, `itertools`, `functools`
- Sistema: `sys`, `platform`, `subprocess`
- E molti altri...

**📖 Vedi `COMANDI_SUPPORTATI.md` per l'elenco completo con tabelle ed esempi!**

## 🎓 Modalità d'Uso Didattico

Pythonita è perfetto per:

1. **Insegnanti** - Dimostra velocemente concetti Python
2. **Studenti** - Impara vedendo esempi di codice
3. **Principianti** - Sperimenta senza paura di errori
4. **Prototipazione** - Genera rapidamente snippet di codice

## 🔧 Comandi CLI

Nell'interfaccia CLI puoi usare:

- `help` / `aiuto` - Mostra esempi
- `gui` - Apri l'interfaccia grafica
- `esci` / `quit` - Esci dal programma

## 🧪 Testing

Per testare il sistema:

```bash
# Test CLI
python main.py
>>> stampa ciao mondo

# Test GUI
python gui_pythonita.py
```

## 📊 Dataset

Il file `frasi.csv` contiene esempi per l'addestramento:

```csv
frase,etichetta
stampa ciao,stampa
somma 3 piu 5,somma
crea lista con 1 2 3,lista
```

Puoi espandere questo dataset per migliorare le prestazioni.

## 🤝 Contribuire

Contributi benvenuti! Apri una Pull Request o un'Issue per:

- Aggiungere nuovi comandi
- Migliorare il parser italiano
- Espandere il dataset
- Correggere bug

## 📄 Licenza

**SOFTWARE COMMERCIALE PROPRIETARIO** - Copyright © 2025

Questo software è protetto da copyright e richiede una licenza valida per l'uso.

**Opzioni licenza**:
- 🆓 **TRIAL**: 14 giorni gratuiti (tutte le funzioni)
- 👤 **PERSONALE**: €49 - 1 PC, aggiornamenti 1 anno
- ⭐ **PRO**: €149 - 3 PC, visualizzatore 3D, aggiornamenti 2 anni
- 🏢 **ENTERPRISE**: €499 - Illimitato, codice sorgente, supporto 24/7

**Garanzia**: 30 giorni soddisfatti o rimborsati  
Vedi [LICENSE](LICENSE) per termini completi.

## 💳 Dove Acquistare

- **Gumroad**: https://[link-gumroad]
- **Sito ufficiale**: https://pythonita.com (coming soon)
- **Email**: vendite@pythonita.com

## 🙏 Riconoscimenti

- **spaCy** - NLP per l'italiano
- **Ollama** - Runtime per AI locale
- **Matplotlib** - Visualizzazione 3D
- **NumPy** - Calcoli scientifici

## 📞 Supporto

**Clienti paganti**:
- Email: support@pythonita.com
- Risposta entro 24h (Pro: 12h, Enterprise: 1h)

**Pre-vendita**:
- Email: vendite@pythonita.com
- FAQ: https://pythonita.com/faq

**Community** (free users):
- GitHub Issues (solo bug, no supporto)
- Forum: https://pythonita.com/forum

## 🧠 AI Agent v7 - Guida Rapida

### Installazione

```bash
pip install -r requirements.txt
pip install chromadb sentence-transformers ollama
```

### Uso

```python
from ai_agent import SelfImprovingAgent

agent = SelfImprovingAgent()
result = agent.run("calcola 10+5")
print(result['output'])
```

### Test

```bash
python ai_agent.py
```

### Componenti Core

```python
# Planner - genera piano azioni
plan = planner.plan(input, state, context)

# Executor - esegue in sandbox
output, success = executor.execute(step, memory)

# Critic - valuta risultati
critique = critic.critique(outputs, plan)

# Reflection - auto-migliora
state = reflection.reflect(state, critique, outputs)
```

### File Importanti

| File | Descrizione |
|------|-------------|
| `ai_agent.py` | Self-Improving Agent principale |
| `traduttore_semantico.py` | Parser NLP italiano |
| `sinonimi.json` | Mappa comandi italiani |
| `pythonita_framework/` | Framework modulare |

---

**Pythonita IA v7** - AI Agent + Didattica + Robotica 3D! 🤖💻

