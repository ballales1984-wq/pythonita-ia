# 🚀 COME AVVIARE PYTHONITA IA

**3 Modi Garantiti per Avviare il Programma**

---

## ⭐ METODO 1: LAUNCHER UNIFICATO (CONSIGLIATO!)

### Il modo più facile:

```bash
python avvia_pythonita.py
```

**Vedrai un menu**:
```
1. CLI Interattiva
2. GUI Classica  
3. GUI 3D (con visualizzatore)
4. Demo Mano 3D
5. Test Rapido
0. Esci
```

Scegli la modalità che preferisci!

**Vantaggi**:
- ✅ Menu intuitivo
- ✅ Gestisce errori automaticamente
- ✅ Mostra cosa manca se errori
- ✅ Funziona sempre

---

## 💻 METODO 2: AVVIO DIRETTO

### CLI Interattiva (Più semplice)
```bash
python main.py
```

Poi scrivi comandi:
```
➤ stampa ciao mondo
➤ somma 5 e 10
➤ crea lista con 1 2 3
```

### GUI con Visualizzatore 3D (Più bello)
```bash
python gui_robot_3d.py
```

### Demo Mano 3D (Impressionante)
```bash
python demo_semplice.py
```

---

## 📦 METODO 3: FILE .EXE (Windows)

Se hai creato l'exe:

```bash
dist\PythonitaIA.exe
```

Oppure **doppio click** su `dist\PythonitaIA.exe`

**Vantaggi**:
- ✅ No Python richiesto
- ✅ Doppio click e parte
- ✅ Distribuibile

---

## 🐛 SE NON PARTE

### Errore: "No module named..."

```bash
# Installa dipendenze
pip install -r requirements.txt
python -m spacy download it_core_news_sm
```

### Errore: "matplotlib not found"

```bash
pip install matplotlib numpy
```

### Errore: "tkinter not found"

Tkinter dovrebbe essere già incluso con Python.
Se manca:
- Windows: Reinstalla Python con opzione "tcl/tk"
- Linux: `sudo apt-get install python3-tk`
- Mac: Dovrebbe essere già incluso

### Il programma si chiude subito

Usa il **launcher unificato**:
```bash
python avvia_pythonita.py
```

Gestisce tutti gli errori e mostra messaggi chiari.

---

## 📊 CONFRONTO MODALITÀ

| Modalità | File | Complessità | Dipendenze | Grafica |
|----------|------|-------------|------------|---------|
| **Launcher** | avvia_pythonita.py | Facile | Base | Menu |
| **CLI** | main.py | Facile | Base | No |
| **GUI Classic** | gui_pythonita.py | Media | + tkinter | Finestra |
| **GUI 3D** | gui_robot_3d.py | Media | + matplotlib | 3D! |
| **Demo 3D** | demo_semplice.py | Facile | + matplotlib | 3D! |
| **EXE** | dist/PythonitaIA.exe | Facilissimo | Nessuna | 3D! |

---

## 🎯 SCELTA RAPIDA

### Vuoi solo provare?
```bash
python avvia_pythonita.py
→ Scegli "5" (Test Rapido)
```

### Vuoi vedere il 3D?
```bash
python demo_semplice.py
```

### Vuoi usarlo interattivamente?
```bash
python avvia_pythonita.py
→ Scegli "1" (CLI)
```

### Vuoi la GUI completa?
```bash
python gui_robot_3d.py
```

### Vuoi distribuire?
```bash
dist\PythonitaIA.exe
```

---

## ✅ CHECKLIST PRIMA DI AVVIARE

- [ ] Python 3.7+ installato (`python --version`)
- [ ] Dipendenze installate (`pip list | findstr numpy`)
- [ ] Nella cartella pythonita-ia (`cd pythonita-ia`)
- [ ] File presente (`dir avvia_pythonita.py`)

Se tutto ✅, esegui:
```bash
python avvia_pythonita.py
```

---

## 🎓 ESEMPI COMANDI

### In CLI o Launcher (Modalità 1):
```
stampa ciao mondo
somma 10 e 20
crea lista con 1 2 3 4 5
ciclo for da 1 a 10
apri file test.txt
```

### In GUI 3D:
```
apri mano
chiudi pugno
fai pinza
afferra oggetto
alza braccio destro
```

---

## 🚨 ERRORI COMUNI

### 1. "python: command not found"
**Problema**: Python non installato  
**Soluzione**: Installa Python da python.org

### 2. "No module named 'core'"
**Problema**: Non sei nella cartella giusta  
**Soluzione**: `cd pythonita-ia`

### 3. "ModuleNotFoundError: matplotlib"
**Problema**: Dipendenze mancanti  
**Soluzione**: `pip install -r requirements.txt`

### 4. Finestra 3D non si apre
**Problema**: Backend matplotlib  
**Soluzione**: Usa `python avvia_pythonita.py` e scegli modalità 1

### 5. "Permission denied"
**Problema**: File non eseguibile (Linux/Mac)  
**Soluzione**: `chmod +x avvia_pythonita.py`

---

## 💡 TIPS

### Avvio Veloce
Crea shortcut:
```bash
# Windows: Crea file avvia.bat
@echo off
python avvia_pythonita.py
pause
```

Doppio click su `avvia.bat` per lanciare!

### Aggiungi al PATH
```bash
# Aggiungi cartella pythonita-ia al PATH
# Poi da ovunque:
pythonita
```

---

## 📞 AIUTO

Se nulla funziona:

1. **Verifica installazione**:
   ```bash
   python --version
   pip --version
   ```

2. **Reinstalla dipendenze**:
   ```bash
   pip uninstall -y numpy matplotlib tkinter
   pip install -r requirements.txt
   ```

3. **Usa launcher** (gestisce errori):
   ```bash
   python avvia_pythonita.py
   ```

4. **Leggi errore** mostrato e cerca online o chiedi aiuto

---

**INIZIA ORA**:
```bash
python avvia_pythonita.py
```

🎨 Buon divertimento con Pythonita IA! 🤖✨

