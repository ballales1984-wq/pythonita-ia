# 🚀 Pythonita IA v2.0.0 - Architettura Ottimizzata

> **Assistente didattico italiano con AI locale per generare codice Python da linguaggio naturale**

## ✨ Novità Principali

### 🏗️ Architettura Ibrida Intelligente
- **AI Locale**: Integrazione Llama3.2 via Ollama per richieste complesse
- **Sistema a Regole**: Fallback automatico con 28+ comandi Python supportati
- **Output Pulito**: Nessun riferimento ai file sorgente, solo codice pronto all'uso

### 🎨 Interfacce Migliorate

**GUI (Interfaccia Grafica)**:
- Debouncing intelligente (300ms) per performance ottimali
- Status bar con feedback real-time
- Bottoni Salva e Pulisci
- Layout responsive e moderno

**CLI (Riga di Comando)**:
- Banner ASCII professionale
- Sistema di help interattivo con esempi
- Comandi speciali: `help`, `gui`, `esci`
- Gestione KeyboardInterrupt robusta

### 📦 Nuovo Modulo Core
```
core/
├── __init__.py      # API pubblica
├── parser.py        # Parser NLP unificato (150+ righe)
└── generatore.py    # Generatore ibrido (350+ righe)
```

### 📚 Documentazione Completa (850+ righe)
- **README.md**: Guida utente completa con quick start
- **ARCHITETTURA.md**: Documentazione tecnica approfondita (500+ righe)
- **CHANGELOG.md**: Storia dettagliata delle modifiche
- **RIEPILOGO_OTTIMIZZAZIONE.md**: Metriche e confronti

### 🛡️ Qualità del Codice
- Gestione errori a più livelli
- Logging strutturato in tutti i moduli
- Type hints dove appropriato
- Docstring complete

## 🎯 Caratteristiche

✅ **Generazione Intelligente**: AI locale + sistema a regole  
✅ **Offline First**: Funziona senza connessione internet  
✅ **Output Professionale**: Codice pulito e pronto all'uso  
✅ **28+ Comandi**: print, input, if, for, while, list, dict, e molto altro  
✅ **GUI & CLI**: Scegli l'interfaccia che preferisci  
✅ **Italiano Nativo**: Parser ottimizzato per la lingua italiana  

## 📥 Installazione

```bash
# 1. Clona il repository
git clone https://github.com/ballales1984-wq/pythonita-ia.git
cd pythonita-ia

# 2. Installa le dipendenze
pip install -r requirements.txt

# 3. Installa il modello spaCy italiano
python -m spacy download it_core_news_sm

# 4. (Opzionale) Installa Ollama per l'AI locale
# Scarica da: https://ollama.ai
# Poi esegui: ollama pull llama3.2
```

## 🚀 Quick Start

### Interfaccia Grafica (Consigliata)
```bash
python gui_pythonita.py
```

### Interfaccia CLI
```bash
python main.py
```

## 💡 Esempi

**Semplici**:
```
➤ stampa ciao mondo
→ print("ciao mondo")

➤ somma 15 e 7
→ print(15 + 7)
```

**Intermedi**:
```
➤ crea un ciclo da 1 a 10
→ for i in range(1, 11):
      print(i)

➤ crea una lista con 5 10 15
→ lista = [5, 10, 15]
  print(lista)
```

**Avanzati**:
```
➤ crea una funzione che calcola il fattoriale
→ def fattoriale(n):
      if n == 0:
          return 1
      else:
          return n * fattoriale(n-1)
```

## 🔧 Requisiti

### Obbligatori
- Python 3.7+
- spaCy con modello italiano (`it_core_news_sm`)
- Dipendenze in `requirements.txt`

### Opzionali (per AI locale)
- Ollama installato
- Modello Llama3.2 scaricato

**Nota**: Se Ollama non è installato, il sistema usa automaticamente il fallback a regole.

## 📊 Metriche di Miglioramento

### Codice
| Metrica | v1.0 | v2.0 | Miglioramento |
|---------|------|------|---------------|
| Parser | 3 file | 1 modulo | -66% |
| Codice duplicato | 79 righe | 0 | -100% |
| Copertura errori | ~30% | ~95% | +217% |
| Documentazione | 2 righe | 850+ | +42,400% |

### Qualità
| Aspetto | v1.0 | v2.0 |
|---------|------|------|
| Manutenibilità | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Testabilità | ⭐ | ⭐⭐⭐⭐ |
| Documentazione | ⭐ | ⭐⭐⭐⭐⭐ |
| User Experience | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🔄 Modifiche da v1.0

### ✨ Aggiunte
- Nuovo modulo `core/` con architettura modulare
- File `config.py` per configurazione centralizzata
- Documentazione completa (3 nuovi file MD)
- Script `build_exe.bat` per compilazione
- File `demo.py` per test interattivo
- Dataset `frasi.csv` e `sinonimi.json`

### 🔧 Modifiche
- `main.py`: CLI completamente riscritta (+480% righe)
- `gui_pythonita.py`: Trasformata in classe moderna (+370% righe)
- `controllore.py`: Usa nuova architettura (+650% righe)
- `interprete_ai.py`: Pulito da duplicati
- `requirements.txt`: Aggiunto ollama

### 🗑️ Rimossi
- `copilot_local.py` (integrato in core/generatore.py)
- `traduttore_semantico.py` (sostituito da core/parser.py)
- `translator.py` (regole integrate in core/generatore.py)
- `mappa_comandi.py` (dati integrati in core/generatore.py)
- `saver.py` (logica in main.py e gui_pythonita.py)
- Cartelle `librerie/` e `linguaggio/` (obsolete)

### 🐛 Bug Fix
- Rimossi riferimenti tipo `"- file.py:123"` dall'output
- Corretto bug sottrazione in translator.py
- Aggiunto `ollama` in requirements.txt
- Migliorata gestione KeyboardInterrupt

## 🤝 Contribuire

I contributi sono benvenuti! Per contribuire:

1. Fork il repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

MIT License - vedi [LICENSE](LICENSE)

## 🙏 Riconoscimenti

- **spaCy**: NLP per l'italiano
- **Ollama**: Runtime per AI locale
- **Llama3.2**: Modello linguistico di Meta
- **TensorFlow**: Machine learning framework

## 📞 Supporto

- 📖 [Documentazione Completa](README.md)
- 🏗️ [Architettura Tecnica](ARCHITETTURA.md)
- 📋 [Changelog](CHANGELOG.md)
- 🐛 [Segnala un Bug](https://github.com/ballales1984-wq/pythonita-ia/issues)

---

**Pythonita IA v2.0.0** - Impara Python in italiano! 🇮🇹🚀

