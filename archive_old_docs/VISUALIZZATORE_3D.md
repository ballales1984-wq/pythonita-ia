# 🎨 Visualizzatore 3D Robot - Pythonita IA v3.1

**NOVITÀ RIVOLUZIONARIA**: Vedi i tuoi comandi robot animati in 3D con misure reali!

---

## 🎯 Cosa Hai Appena Ottenuto

### GUI Completa a 3 Colonne:

```
┌─────────────────────────────────────────────────────────────┐
│  Pythonita IA v3.1 - Visualizzatore 3D Robot                │
├──────────────┬───────────────┬──────────────────────────────┤
│              │               │                              │
│   COMANDO    │    CODICE     │      PREVIEW 3D              │
│   ITALIANO   │    PYTHON     │    (Animazione)              │
│              │               │                              │
│  "apri mano" │  import...    │    [Mano 3D che]             │
│              │  mano.apri()  │    [si apre!]                │
│              │  ...          │                              │
│              │               │                              │
│ [Esempi]     │               │   Misure Reali:              │
│ - Apri Mano  │               │   Palmo: 10cm x 8.5cm       │
│ - Chiudi     │               │   Dita: lunghezze reali      │
│ - Pinza      │               │   Angoli: 0-90°              │
│ - Afferra    │               │                              │
└──────────────┴───────────────┴──────────────────────────────┘
```

---

## ✨ Funzionalità

### 1. **Comando in Italiano** (Colonna Sinistra)
Scrivi comandi naturali:
- "apri mano"
- "chiudi pugno"
- "fai pinza"
- "afferra oggetto"
- "alza braccio destro"

### 2. **Codice Python Generato** (Colonna Centro)
Vedi il codice generato in tempo reale:
```python
from mano_bionica import ManoBionica
mano = ManoBionica()
mano.apri_dita()
```

### 3. **Preview 3D Animata** (Colonna Destra)
Visualizzazione 3D che si anima con misure reali!

---

## 🎮 Come Usare

### Avvio
```bash
python gui_robot_3d.py
```

### Passo 1: Scrivi Comando
Nella box sinistra, scrivi ad esempio:
```
apri mano
```

### Passo 2: Vedi Codice
Al centro appare automaticamente il codice Python

### Passo 3: Esegui Animazione
Premi "**Esegui Animazione 3D**"

### Passo 4: Guarda!
La mano 3D a destra **si anima veramente**!
- Si apre gradualmente
- Mostra le misure reali
- Angoli e percentuali

---

## 🤖 Comandi Supportati

### Mano Robotica

| Comando | Animazione 3D | Misure |
|---------|---------------|--------|
| "apri mano" | Dita si aprono | 0° → Estese |
| "chiudi pugno" | Dita si chiudono | 0° → 90° |
| "fai pinza" | Pollice+Indice | Apertura 20mm |
| "afferra oggetto" | Chiusura graduale | Forza 50% |

### Braccio Robotico

| Comando | Animazione 3D | Angoli |
|---------|---------------|--------|
| "alza braccio" | Spalla ruota | 0° → 90° |
| "piega gomito" | Gomito si piega | 0° → 90° |
| "estendi braccio" | Estensione completa | Max estensione |

---

## 📐 Misure Reali Implementate

### Mano (Misure Medie Adulto)
```
Palmo: 10cm x 8.5cm
Pollice: 3.8cm + 2.5cm + 2.0cm = 8.3cm
Indice:  4.5cm + 2.7cm + 2.0cm = 9.2cm
Medio:   5.0cm + 3.0cm + 2.2cm = 10.2cm
Anulare: 4.6cm + 2.8cm + 2.1cm = 9.5cm
Mignolo: 3.8cm + 2.2cm + 1.8cm = 7.8cm
```

### Braccio
```
Braccio superiore (omero): 30cm
Avambraccio (ulna/radio): 25cm
Totale: 55cm
```

### Angoli Massimi
```
Dita:   0° - 90°
Polso:  0° - 180°
Gomito: 0° - 150°
Spalla: 0° - 180°
```

---

## 🎨 Animazioni Disponibili

### 1. Apertura Mano
```
Comando: "apri mano"
Animazione: 20 frame, 1 secondo
Effetto: Tutte le 5 dita si aprono gradualmente
```

### 2. Chiusura Pugno
```
Comando: "chiudi pugno"
Animazione: 20 frame, 1 secondo
Effetto: Tutte le dita si chiudono formando pugno
```

### 3. Posizione Pinza
```
Comando: "fai pinza"
Animazione: 15 frame
Effetto:
  - Medio, anulare, mignolo si aprono
  - Pollice e indice si posizionano a pinza
  - Apertura 20mm
```

### 4. Afferra Oggetto
```
Comando: "afferra oggetto"
Animazione: Chiusura graduale con controllo forza
Percentuale: 0% → 50% (presa delicata)
```

### 5. Alza Braccio
```
Comando: "alza braccio"
Animazione: 30 frame, movimento fluido
Angolo spalla: 0° → 90°
```

---

## 🎓 Esempio Completo d'Uso

### Scenario: Programma Robot per Afferrare

**Step 1**: Avvia GUI
```bash
python gui_robot_3d.py
```

**Step 2**: Scrivi comando
```
il robot afferra l'oggetto con la mano destra
```

**Step 3**: Vedi codice generato
```python
import robot_api
robot = robot_api.Robot()

for i in range(0, 50, 5):
    robot.mano_destra.chiudi_dita(forza=i)
    robot.sleep(0.1)

if robot.mano_destra.sensore_contatto():
    print("Oggetto afferrato!")
```

**Step 4**: Premi "Esegui Animazione 3D"

**Step 5**: Guarda!
La mano 3D si chiude gradualmente come programmato!

**Step 6**: Salva codice
Premi "Salva Codice" → `output_robot.py`

**Step 7**: Usa su robot reale!
Adatta il codice alla tua libreria hardware.

---

## 🔧 Bottoni Disponibili

### "Esegui Animazione 3D"
- Analizza il comando
- Esegue animazione corrispondente
- Mostra misure in tempo reale

### "Reset Posizione"
- Riporta robot a posizione iniziale
- Mano aperta
- Braccio abbassato

### "Salva Codice"
- Salva codice generato in `output_robot.py`
- Pronto per essere usato

---

## 📊 Tecnologie Utilizzate

- **Tkinter**: Interfaccia GUI
- **Matplotlib**: Rendering 3D
- **NumPy**: Calcoli geometrici
- **Threading**: Animazioni fluide
- **spaCy**: Analisi linguistica (opzionale)

---

## 🎯 Template Disponibili

### Robot (Default)
```
Comandi: mano, braccio, sensori
Visualizzazione: Braccio + Mano 3D
Libreria: robot_api
```

### Mano Bionica
```
Comandi: dita, prese, gesti
Visualizzazione: Mano 3D dettagliata
Libreria: mano_bionica
```

### Generico
```
Comandi: Python normale
Visualizzazione: Nessuna (codice solo)
```

---

## 💡 Tips per Usare il Visualizzatore

### 1. Sii Specifico
✅ "apri mano destra"  
✅ "chiudi pugno con forza 80%"  
✅ "alza braccio a 45 gradi"  

### 2. Usa Animazioni
- Ogni comando ha animazione associata
- Premi "Esegui Animazione" per vederla
- Le animazioni mostrano movimento reale

### 3. Combina con Multi-Comando
```
"apri mano poi chiudi poi riapri"
→ Sequenza di 3 animazioni!
```

### 4. Verifica Codice
Il codice generato è **esattamente** quello che fa l'animazione!

---

## 🔬 Precisione e Realismo

### Cinematica
- ✅ Angoli reali delle giunture
- ✅ Lunghezze segmenti realistiche
- ✅ Limiti fisici rispettati (max 90°, 150°, ecc.)

### Fisica
- ✅ Movimento fluido (non istantaneo)
- ✅ Velocità configurabile
- ✅ Pause tra movimenti

### Feedback
- ✅ Percentuale chiusura in tempo reale
- ✅ Angoli mostrati
- ✅ Status bar aggiornato

---

## 🚀 Esempi Rapidi

Prova questi nella GUI:

```
1. apri mano
   → Vedi mano che si apre

2. chiudi pugno
   → Vedi mano che si chiude a pugno

3. fai pinza
   → Vedi pollice e indice formare pinza

4. afferra oggetto
   → Chiusura graduale con controllo

5. alza braccio destro
   → Braccio si solleva a 90°
```

---

## 📚 File del Sistema

```
visualizzatore/
├── __init__.py
├── modelli_3d.py          # Modelli geometrici con misure reali
└── viewer_3d.py           # Visualizzatore matplotlib 3D

gui_robot_3d.py            # GUI completa integrata

examples/
├── esempio_robot.py       # Demo template
└── esempio_linguaggio_naturale.py  # Demo analisi
```

---

## 🎓 Didattica con 3D

### Per Insegnanti
- Mostra VISIVAMENTE cosa fa il codice
- Studenti capiscono cinematica robotica
- Da teoria a pratica visiva

### Per Studenti
- Vedi l'effetto immediato
- Comprendi angoli e movimenti
- Impari geometria 3D

### Per Sviluppatori
- Prototiping visuale
- Debug movimenti
- Test prima di hardware reale

---

## ⚠️ Note Tecniche

### Performance
- Animazioni: 20-30 FPS
- Rendering: Real-time
- CPU: Basso impatto

### Requisiti
- Python 3.7+
- matplotlib
- numpy
- tkinter (incluso)

### Limitazioni Attuali
- Modello semplificato (wire-frame)
- 2.5D (non full 3D mesh)
- Collisioni non implementate

### Futuri Miglioramenti
- Mesh 3D realistici
- Texture e materiali
- Fisica avanzata
- Export animazioni

---

**Pythonita IA v3.1** - Vedi il tuo codice prendere vita! 🎨🤖✨

