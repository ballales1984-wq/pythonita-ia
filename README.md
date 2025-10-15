# 🧠 Pythonita IA 🇮🇹

**Assistente didattico in italiano con AI locale**  
Genera codice Python da frasi in linguaggio naturale italiano.

## 🌟 Caratteristiche

- ✅ **Interfaccia CLI e GUI** - Scegli quella che preferisci
- 🤖 **AI Locale** - Usa Llama3.2 tramite Ollama (nessuna connessione internet necessaria)
- 🔄 **Fallback Intelligente** - Sistema a regole se l'AI non è disponibile
- 🇮🇹 **Completamente in Italiano** - Parser NLP ottimizzato per l'italiano
- 📚 **Didattico** - Perfetto per imparare Python

## 🚀 Quick Start

### Installazione

```bash
# 1. Clona il repository
git clone https://github.com/ballales1984-wq/pythonita-ia.git
cd pythonita

# 2. Installa le dipendenze
pip install -r requirements.txt

# 3. Installa il modello spaCy italiano
python -m spacy download it_core_news_sm

# 4. Installa Ollama (per l'AI locale)
# Scarica da: https://ollama.ai
# Poi esegui: ollama pull llama3.2
```

### Uso

**Interfaccia CLI:**
```bash
python main.py
```

**Interfaccia GUI:**
```bash
python gui_pythonita.py
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
pythonita/
├── core/                      # Moduli principali
│   ├── __init__.py
│   ├── parser.py             # Parser NLP unificato
│   └── generatore.py         # Generatore ibrido (AI + regole)
├── data/                      # Dati e configurazioni
│   ├── funzioni_salvate/     # Funzioni generate salvate
├── librerie/                  # [DEPRECATO] Vecchi moduli
├── linguaggio/                # [DEPRECATO] Vecchi moduli
├── main.py                    # Entry point CLI
├── gui_pythonita.py          # Entry point GUI
├── controllore.py            # Controllore principale
├── config.py                 # Configurazione centralizzata
├── interprete_ai.py          # Modelli di machine learning
├── requirements.txt          # Dipendenze Python
├── frasi.csv                 # Dataset di training
├── sinonimi.json             # Sinonimi per matching
└── output.py                 # Output del codice generato
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

Il sistema a regole supporta 28+ comandi Python:

**Base:**
- `print`, `input`, `if`, `for`, `while`
- `def` (funzioni), `try/except` (gestione errori)

**Strutture dati:**
- `list` (liste), `dict` (dizionari)
- `append`, `remove`, `len`, `sorted`

**Operazioni:**
- `+`, `-`, `*`, `/` (aritmetica)
- `sum`, `max`, `min` (aggregazione)

**File:**
- `open` (lettura/scrittura file)
- `import` (importazione librerie)

**Altro:**
- `range`, `return`, `type`

Vedi `core/generatore.py` per l'elenco completo.

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

MIT License - vedi `LICENSE`

## 🙏 Riconoscimenti

- **spaCy** - NLP per l'italiano
- **Ollama** - Runtime per AI locale
- **Llama3.2** - Modello linguistico di Meta
- **TensorFlow** - Machine learning

## 📞 Supporto

Per domande o problemi:
- Apri un'Issue su GitHub
- Email: [il-tuo-email]

---

**Pythonita IA** - Impara Python in italiano! 🚀🇮🇹

