# Changelog - Pythonita IA

Tutti i cambiamenti notevoli al progetto sono documentati in questo file.

## [2.0.0] - 2025-10-15

### 🎉 Ottimizzazione Completa dell'Architettura

#### ✨ Aggiunte

**Nuovi Moduli Core:**
- `core/parser.py` - Parser NLP unificato con classe `ParserItaliano`
- `core/generatore.py` - Generatore ibrido intelligente (AI + regole)
- `core/__init__.py` - API pubblica del modulo core
- `config.py` - Configurazione centralizzata dell'applicazione
- `README.md` - Documentazione completa e migliorata
- `ARCHITETTURA.md` - Documentazione tecnica dell'architettura
- `CHANGELOG.md` - Questo file

**Funzionalità:**
- Architettura ibrida a due livelli (AI locale + sistema a regole)
- Fallback automatico se AI non disponibile
- Pulizia automatica dell'output AI (rimozione markdown)
- Logging integrato in tutti i moduli
- Gestione errori migliorata a più livelli
- GUI migliorata con debouncing, status bar e bottoni
- CLI migliorata con banner, help interattivo e gestione comandi
- Supporto comando `gui` dalla CLI per aprire interfaccia grafica

#### 🔧 Modifiche

**File Aggiornati:**
- `main.py` - Completamente riscritto con:
  - Banner ASCII art
  - Sistema di help interattivo
  - Gestione comandi speciali (help, gui, esci)
  - Migliore gestione errori e KeyboardInterrupt
  - Messaggi utente più chiari

- `gui_pythonita.py` - Trasformato in classe `PythonitaGUI` con:
  - Layout migliorato e responsive
  - Debouncing (300ms) per performance
  - Status bar per feedback utente
  - Bottoni per salvare e pulire
  - ScrolledText per contenuti lunghi
  - Gestione errori con messagebox

- `controllore.py` - Semplificato:
  - Usa nuova architettura `core.generatore`
  - Logging integrato
  - Gestione errori robusta

- `interprete_ai.py` - Pulito da duplicazioni:
  - Rimossi 3 duplicati della stessa funzione
  - Documentazione aggiunta
  - Due funzioni ben separate: `addestra_modello_classificazione` e `addestra_modello_generico`

- `requirements.txt` - Aggiornato:
  - Aggiunto `ollama` mancante
  - Commenti e organizzazione migliorata
  - Istruzioni per spaCy model

#### 🗑️ Deprecati

I seguenti file sono considerati deprecati e possono essere rimossi:

**File Sostituiti:**
- `copilot_local.py` → `core/generatore.py`
- `traduttore_semantico.py` → `core/parser.py`
- `translator.py` → `core/generatore.py` (regole integrate)
- `mappa_comandi.py` → `core/generatore.py` (dati integrati)
- `saver.py` → Logica in `main.py` e `gui_pythonita.py`

**Directory Obsolete:**
- `librerie/` → `core/`
- `linguaggio/` → `core/`

> **Nota**: I file deprecati sono ancora presenti per retrocompatibilità
> ma non sono più utilizzati dal codice principale.

#### 🎨 Miglioramenti

**Parser:**
- Consolidamento di 3 parser diversi in uno unico
- Supporto completo spaCy con fallback
- Estrazione intelligente di numeri
- API pulita e documentata

**Generatore:**
- Strategia a 3 livelli: AI → Regole → Errore
- 28+ comandi Python supportati
- Pulizia automatica output (rimozione riferimenti tipo `- file.py:123`)
- Singleton pattern per performance
- Logging dettagliato delle operazioni

**Configurazione:**
- Gestione centralizzata di tutte le configurazioni
- Path management con `pathlib`
- Creazione automatica directory necessarie
- Helper per configurazione AI e NLP

**Gestione Errori:**
- Try-catch a più livelli
- Logging strutturato
- Messaggi utente chiari e utili
- Suggerimenti contestuali

**Documentazione:**
- README completo con esempi e quick start
- ARCHITETTURA.md con dettagli tecnici
- Docstring in tutti i moduli
- Type hints dove appropriato

#### 🐛 Bug Fixes

- ✅ Rimossi riferimenti tipo `- translator.py:41` dall'output
- ✅ Eliminato codice duplicato in `interprete_ai.py`
- ✅ Corretto bug di sottrazione in `translator.py` (era `{numeri[0]}  {numeri[1]}` invece di `{numeri[0]} - {numeri[1]}`)
- ✅ Aggiunto `ollama` in requirements.txt
- ✅ Migliorata gestione KeyboardInterrupt in CLI

#### 📊 Statistiche

**Righe di codice:**
- `core/parser.py`: ~150 righe (nuovo)
- `core/generatore.py`: ~350 righe (nuovo)
- `main.py`: Da 27 → 156 righe (+480%)
- `gui_pythonita.py`: Da 43 → 203 righe (+370%)
- `controllore.py`: Da 4 → 30 righe (+650%)
- `interprete_ai.py`: Da 79 → 93 righe (pulito da duplicati)

**File rimossi/deprecati:** 7 file + 2 directory

**Documentazione aggiunta:**
- README.md: ~350 righe
- ARCHITETTURA.md: ~500 righe
- CHANGELOG.md: Questo file

---

## [1.0.0] - 2025-10-14 (Baseline)

### Versione Iniziale

- Interfaccia CLI base (`main.py`)
- Interfaccia GUI base (`gui_pythonita.py`)
- Integrazione Ollama/Llama3.2 (`copilot_local.py`)
- Sistema a regole (`translator.py`)
- Parser spaCy (`traduttore_semantico.py`)
- Dataset base (`frasi.csv`, `sinonimi.json`)
- Build eseguibile con PyInstaller

**Problemi noti:**
- Codice duplicato in `interprete_ai.py`
- Parser frammentato in 3 file diversi
- Manca gestione errori robusta
- Output con riferimenti ai file sorgente
- Manca `ollama` in requirements
- Architettura poco chiara

---

## 📋 Prossimi Passi (Roadmap)

### v2.1.0 - Pulizia e Testing
- [ ] Rimuovere file deprecati
- [ ] Aggiungere unit tests per `core/`
- [ ] Test integrazione AI + regole
- [ ] CI/CD con GitHub Actions

### v2.2.0 - Miglioramenti Dataset
- [ ] Espandere `frasi.csv` (50+ esempi)
- [ ] Aggiungere sinonimi in `sinonimi.json`
- [ ] Sistema di feedback utente
- [ ] Logging delle query per miglioramento

### v2.3.0 - Performance
- [ ] Cache risultati frequenti
- [ ] Lazy loading di modelli
- [ ] Ottimizzazione prompt AI
- [ ] Benchmark e profiling

### v3.0.0 - Nuove Features
- [ ] Interfaccia web (Flask/FastAPI)
- [ ] API REST
- [ ] Multi-utente
- [ ] Fine-tuning modello custom

---

## 🔗 Collegamenti

- Repository: https://github.com/ballales1984-wq/pythonita-ia
- Issue: https://github.com/ballales1984-wq/pythonita-ia/issues
- Documentazione: [README.md](README.md)
- Architettura: [ARCHITETTURA.md](ARCHITETTURA.md)

---

**Formato**: Questo changelog segue [Keep a Changelog](https://keepachangelog.com/it/1.0.0/)  
**Versionamento**: [Semantic Versioning](https://semver.org/lang/it/)

