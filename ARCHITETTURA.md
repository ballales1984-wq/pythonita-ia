# 🏗️ Architettura di Pythonita IA

Documento tecnico che descrive l'architettura del progetto dopo l'ottimizzazione.

## 📋 Indice

1. [Panoramica](#panoramica)
2. [Struttura dei Moduli](#struttura-dei-moduli)
3. [Flusso di Esecuzione](#flusso-di-esecuzione)
4. [Componenti Principali](#componenti-principali)
5. [Sistema Ibrido](#sistema-ibrido)
6. [Gestione Errori](#gestione-errori)
7. [Configurazione](#configurazione)
8. [File Deprecati](#file-deprecati)

---

## 📊 Panoramica

Pythonita IA usa un'**architettura ibrida a due livelli**:

1. **AI Locale** (primario) - Llama3.2 via Ollama
2. **Sistema a Regole** (fallback) - Pattern matching su comandi noti

Questa architettura garantisce:
- ✅ Flessibilità (AI gestisce richieste complesse)
- ✅ Affidabilità (fallback sempre disponibile)
- ✅ Offline (nessuna connessione internet necessaria)
- ✅ Velocità (regole per comandi semplici)

---

## 🗂️ Struttura dei Moduli

### Moduli Core (Nuova Architettura)

```
core/
├── __init__.py           # Esporta API pubblica
├── parser.py             # Parser NLP unificato con spaCy
└── generatore.py         # Generatore ibrido AI + regole
```

**`core/parser.py`**
- Classe `ParserItaliano`: parser NLP con spaCy
- Analisi completa: tokens, lemmi, POS tags
- Estrazione parole chiave (verbi, sostantivi)
- Fallback senza NLP per situazioni semplici

**`core/generatore.py`**
- Classe `GeneratoreCodice`: generatore ibrido
- Strategia AI → Regole → Errore
- 28+ comandi Python supportati
- Pulizia automatica output AI
- Logging integrato

### Moduli di Supporto

```
├── controllore.py        # Orchestrazione principale
├── config.py             # Configurazione centralizzata
├── interprete_ai.py      # [OPZIONALE] Training modelli TF
├── main.py               # CLI entry point
└── gui_pythonita.py      # GUI entry point
```

### File Deprecati (Da Rimuovere)

```
├── librerie/             # [DEPRECATO] Vecchi moduli
├── linguaggio/           # [DEPRECATO] Vecchi moduli
├── copilot_local.py      # [DEPRECATO] Sostituito da generatore.py
├── traduttore_semantico.py  # [DEPRECATO] Sostituito da parser.py
├── translator.py         # [DEPRECATO] Regole integrate in generatore.py
├── mappa_comandi.py      # [DEPRECATO] Integrato in generatore.py
└── saver.py              # [DEPRECATO] Logica in main.py/gui
```

---

## 🔄 Flusso di Esecuzione

### CLI Flow

```
1. Avvio: main.py
   ↓
2. Banner e istruzioni
   ↓
3. Input utente
   ↓
4. controllore.ciclo_di_controllo()
   ↓
5. core.generatore.get_generatore().genera()
   ↓
6. Strategia ibrida:
   ├─→ AI disponibile? → Ollama → Pulizia
   └─→ Fallback → Regole → Codice
   ↓
7. Output codice
   ↓
8. Salvataggio opzionale in output.py
```

### GUI Flow

```
1. Avvio: gui_pythonita.py
   ↓
2. Inizializzazione Tkinter
   ↓
3. Setup layout (2 text box + bottoni)
   ↓
4. Binding KeyRelease con debouncing (300ms)
   ↓
5. Ad ogni modifica:
   ├─→ controllore.ciclo_di_controllo()
   ├─→ Generazione codice
   └─→ Aggiornamento real-time output
   ↓
6. Salvataggio manuale con bottone
```

---

## 🔧 Componenti Principali

### 1. Parser (`core/parser.py`)

**Responsabilità:**
- Analisi linguistica della frase italiana
- Estrazione features (verbi, sostantivi, numeri)
- Supporto NLP con spaCy o fallback semplice

**API Pubblica:**

```python
from core import ParserItaliano, get_parser, analizza_frase

# Uso base
parser = get_parser()
risultato = parser.analizza_completa("stampa ciao mondo")
# → {"testo": "...", "tokens": [...], "lemmi": [...], ...}

# Uso semplice (fallback)
risultato = analizza_frase("stampa ciao")
# → {"verbo": "stampa", "args": ["ciao"], ...}
```

**Features:**
- Singleton pattern (`get_parser()`)
- Lazy loading di spaCy
- Estrazione numeri intelligente
- Gestione errori graceful

### 2. Generatore (`core/generatore.py`)

**Responsabilità:**
- Generazione codice Python
- Gestione AI + fallback
- Pulizia output
- Logging operazioni

**API Pubblica:**

```python
from core import GeneratoreCodice, get_generatore, genera_codice

# Uso base
generatore = get_generatore()
codice = generatore.genera("stampa ciao mondo")
# → 'print("ciao mondo")'

# Uso rapido
codice = genera_codice("somma 5 e 3")
# → 'print(5 + 3)'
```

**Strategia di Generazione:**

```python
def genera(self, frase: str) -> str:
    # 1. Prova con AI
    if self.ai_disponibile:
        codice = self._genera_con_ai(frase)
        if codice and non_errore(codice):
            return codice
    
    # 2. Fallback a regole
    if self.use_fallback:
        codice = self._genera_con_regole(frase)
        if codice and non_errore(codice):
            return codice
    
    # 3. Messaggio di errore
    return self._genera_errore(frase)
```

**Pulizia Output AI:**

```python
def _pulisci_output_ai(self, codice: str) -> str:
    # Rimuove markdown ```python``` e ```
    # Rimuove commenti generici dell'AI
    # Ritorna codice pulito
```

### 3. Controllore (`controllore.py`)

**Responsabilità:**
- Orchestrazione principale
- Gestione errori di alto livello
- Logging

```python
def ciclo_di_controllo(frase: str) -> str:
    try:
        generatore = get_generatore()
        return generatore.genera(frase)
    except Exception as e:
        logger.error(f"Errore: {e}")
        return f"# Errore: {str(e)}"
```

### 4. Configurazione (`config.py`)

**Responsabilità:**
- Configurazione centralizzata
- Path management
- Creazione directory automatica

```python
from config import Config

# Accesso configurazione
Config.AI_ENABLED           # True/False
Config.AI_MODEL             # "llama3.2"
Config.SPACY_MODEL          # "it_core_news_sm"
Config.OUTPUT_FILE          # Path("output.py")

# Helper
Config.assicura_directories()
Config.get_ai_config()
```

---

## 🤖 Sistema Ibrido

### Livello 1: AI Locale (Ollama + Llama3.2)

**Vantaggi:**
- ✅ Gestisce richieste complesse
- ✅ Comprensione naturale del linguaggio
- ✅ Adattabile a variazioni

**Svantaggi:**
- ⚠️ Richiede Ollama installato
- ⚠️ Più lento (1-3 secondi)
- ⚠️ Output può contenere markdown

**Prompt Engineering:**

```python
prompt = f"""Genera solo codice Python per questa richiesta in italiano: "{frase}"

Regole:
- Scrivi SOLO codice Python, senza spiegazioni
- Non aggiungere commenti tipo "# Codice generato..."
- Non usare markdown o ``` 
- Codice pulito e funzionante

Codice Python:"""
```

### Livello 2: Sistema a Regole

**Vantaggi:**
- ✅ Veloce (< 10ms)
- ✅ Deterministico
- ✅ Sempre disponibile
- ✅ Output pulito

**Svantaggi:**
- ⚠️ Limitato a comandi predefiniti
- ⚠️ Meno flessibile

**Pattern Matching:**

```python
mappa_comandi = {
    "print": ["stampa", "mostra", "visualizza", "scrivi"],
    "if": ["se", "condizione", "verifica"],
    # ... 28+ comandi
}

def _identifica_comando(frase: str) -> str:
    for comando, sinonimi in mappa_comandi.items():
        if any(parola in sinonimi for parola in frase.split()):
            return comando
```

---

## ⚠️ Gestione Errori

### Livelli di Gestione

1. **Generatore** - Cattura errori AI/regole
2. **Controllore** - Cattura errori di orchestrazione
3. **Main/GUI** - Cattura errori di interfaccia

### Logging

```python
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

logger.info("✅ Operazione completata")
logger.warning("⚠️  Attenzione")
logger.error("❌ Errore")
```

### Messaggi Utente

```python
# Errore generico
"# ⚠️  Non sono riuscito a generare codice per: '{frase}'"

# Con suggerimenti
"""
# ⚠️  Non sono riuscito a generare codice
# 
# Suggerimenti:
# - Prova a riformulare in modo più semplice
# - Usa verbi come: stampa, crea, somma
"""
```

---

## ⚙️ Configurazione

### File di Configurazione

**`config.py`** - Configurazione runtime

```python
class Config:
    # Paths
    BASE_DIR = Path(__file__).parent
    OUTPUT_FILE = BASE_DIR / "output.py"
    
    # AI
    AI_ENABLED = True
    AI_MODEL = "llama3.2"
    
    # NLP
    SPACY_MODEL = "it_core_news_sm"
```

**`requirements.txt`** - Dipendenze

```txt
spacy==3.7.2
tensorflow==2.15.0
pandas==2.1.1
scikit-learn==1.3.2
ollama
```

**`frasi.csv`** - Dataset training

```csv
frase,etichetta
stampa ciao,stampa
somma 3 piu 5,somma
```

**`sinonimi.json`** - Sinonimi per matching

```json
{
  "stampa": ["mostra", "visualizza", "scrivi"],
  "somma": ["aggiungi", "calcola"]
}
```

---

## 🗑️ File Deprecati

Questi file possono essere rimossi in future versioni:

### Da Rimuovere

| File | Motivo | Sostituito da |
|------|--------|---------------|
| `copilot_local.py` | Logica integrata | `core/generatore.py` |
| `traduttore_semantico.py` | Parser duplicato | `core/parser.py` |
| `translator.py` | Regole duplicate | `core/generatore.py` |
| `mappa_comandi.py` | Dati integrati | `core/generatore.py` |
| `saver.py` | Logica semplice | `main.py`, `gui_pythonita.py` |
| `librerie/` | Moduli vecchi | `core/` |
| `linguaggio/` | Moduli vecchi | `core/` |

### Pulizia Consigliata

```bash
# Backup (opzionale)
mkdir _old
mv copilot_local.py traduttore_semantico.py translator.py _old/
mv mappa_comandi.py saver.py _old/
mv librerie/ linguaggio/ _old/

# O eliminazione diretta
rm -rf librerie/ linguaggio/
rm copilot_local.py traduttore_semantico.py translator.py
rm mappa_comandi.py saver.py
```

---

## 🚀 Miglioramenti Futuri

### Breve Termine

1. ✅ Rimuovere file deprecati
2. ✅ Aggiungere unit tests
3. ✅ Espandere dataset `frasi.csv`
4. ✅ Documentare API completa

### Medio Termine

1. 🔄 Fine-tuning di Llama3.2 su dataset italiano
2. 🔄 Cache dei risultati per velocità
3. 🔄 Interfaccia web (Flask/FastAPI)
4. 🔄 Plugin per editor (VSCode)

### Lungo Termine

1. 📅 Supporto multi-lingua
2. 📅 Generazione di progetti completi
3. 📅 Debug automatico del codice
4. 📅 Suggerimenti intelligenti

---

## 📚 Riferimenti

- **spaCy**: https://spacy.io/
- **Ollama**: https://ollama.ai/
- **Llama 3.2**: https://ai.meta.com/llama/
- **Python Tkinter**: https://docs.python.org/3/library/tkinter.html

---

**Ultimo aggiornamento**: 2025-10-15  
**Versione architettura**: 2.0

