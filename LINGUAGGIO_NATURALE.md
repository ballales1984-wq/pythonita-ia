"""# 🧠 Sistema Linguistico Avanzato - Pythonita IA v3.0

**Novità Rivoluzionaria**: Pythonita ora comprende strutture linguistiche complete e genera codice per robotica!

---

## 🎯 Cosa è Cambiato

### Prima (v2.x):
```
"stampa ciao"  →  print("ciao")
```

Semplice traduzione parola→comando.

### Ora (v3.0):
```
"il robot muove la mano destra quando rileva l'oggetto"

Pythonita capisce:
- Soggetto: "robot"
- Verbo: "muovere"
- Complemento: "mano"
- Interrogativo: "quando"
- Template: robot

Genera:
import robot_api
robot = robot_api.Robot()
if robot.sensore_oggetto.rileva():
    robot.mano_destra.muovi()
```

**Comprensione linguistica completa!** 🧠

---

## 📚 Componenti del Sistema

### 1. Parser Linguistico Avanzato
**File**: `core/linguaggio_naturale.py`

**Analizza**:
- ✅ **Soggetto** - Chi fa l'azione
- ✅ **Verbo** - L'azione
- ✅ **Complemento Oggetto** - Su cosa
- ✅ **Interrogativi** - chi, cosa, quando, dove, come, perché
- ✅ **Tempo Verbale** - presente, passato, futuro
- ✅ **Modalità** - imperativo, indicativo, condizionale

**Esempio**:
```python
from core.linguaggio_naturale import analizza_linguaggio

struttura = analizza_linguaggio("il robot afferra l'oggetto")

print(struttura.soggetto)    # → "robot"
print(struttura.verbo)       # → "afferrare"
print(struttura.complemento_oggetto)  # → "oggetto"
```

---

### 2. Sistema di Template
**File**: `core/template_domini.py`

**Template Disponibili**:

#### 🤖 Template Robot
Per robot umanoidi senza ruote:
- Bracci robotici
- Mani con dita
- Sensori
- Movimenti complessi

#### 🦾 Template Mano Bionica
Per mani bioniche/protesi:
- Controllo dita singole
- Prese: pugno, pinza, power grip
- Gesti: ok, thumbs up, point
- Forza e precisione

#### 💻 Template Generico
Codice Python normale (default)

---

## 🤖 Template Robot - Guida Completa

### Attivazione
```python
from core.generatore import GeneratoreCodice

# Crea generatore con template robot
gen = GeneratoreCodice(template='robot')

# Genera comandi
codice = gen.genera("muovi mano destra")
```

### Comandi Supportati

#### Movimento Mani
```
"muovi mano destra"
"sposta mano sinistra"
"ruota polso"
```

Genera:
```python
import robot_api
robot = robot_api.Robot()
robot.mano_destra.set_angolo(90)
robot.mano_destra.muovi()
```

#### Presa/Rilascio
```
"afferra oggetto con mano destra"
"prendi con mano sinistra"
"rilascia oggetto"
"apri mano"
```

Genera:
```python
robot = robot_api.Robot()
# Chiudi dita gradualmente
for i in range(0, 50, 5):
    robot.mano_destra.chiudi_dita(forza=i)
    robot.sleep(0.1)
```

#### Movimento Bracci
```
"alza braccio destro"
"abbassa braccio sinistro"
"estendi braccio"
"ritira braccio"
```

Genera:
```python
robot.braccio_destro.set_angolo_spalla(90)
robot.braccio_destro.muovi_fluido(velocita=30)
```

#### Sensori
```
"leggi sensore distanza"
"rileva oggetto"
"controlla distanza"
"misura temperatura"
```

Genera:
```python
valore = robot.sensore_distanza.leggi()
if valore < 20:
    print("Oggetto vicino!")
    robot.stop()
```

---

## 🦾 Template Mano Bionica - Guida Completa

### Attivazione
```python
gen = GeneratoreCodice(template='mano_bionica')
```

### Comandi Supportati

#### Prese
```
"chiudi pugno"          → Presa power (tutte le dita)
"fai pinza"             → Presa precision (pollice-indice)
"apri mano"             → Distendi tutte le dita
```

#### Gesti
```
"gesto ok"              → Cerchio pollice-indice
"pollice su"            → Thumbs up
"punta"                 → Indice esteso
```

#### Controllo Fine
```python
# Genera codice dettagliato
mano.chiudi_dito('pollice', forza=70)
mano.chiudi_dito('indice', forza=50)
# ...
```

---

## 🧠 Analisi Linguistica con Llama

### Come Funziona

**Step 1**: Parser linguistico analizza la frase
```
"il robot muove la mano quando rileva oggetto"

Analisi:
- Soggetto: robot
- Verbo: muovere
- Complemento: mano
- Interrogativo: quando (condizione temporale)
```

**Step 2**: Llama riceve contesto arricchito
```
Prompt per Llama:
"Genera codice Python per: [frase]

Analisi linguistica:
- Soggetto: robot
- Verbo: muovere
- Interrogativo: quando (condizione)

Template: robot
Libreria: robot_api
..."
```

**Step 3**: Llama genera codice contestualizzato
```python
import robot_api
robot = robot_api.Robot()

# Condizione: quando rileva oggetto
while True:
    if robot.sensore_oggetto.rileva():
        robot.mano_destra.muovi()
        break
```

**Risultato**: Codice più preciso e contestuale! 🎯

---

## 💡 Esempi Pratici

### Esempio 1: Sequenza Robot
```
Frase: "il robot afferra l'oggetto poi lo solleva poi lo rilascia"

Pythonita capisce:
- Multi-comando (3 azioni)
- Soggetto: robot
- Sequenza: afferra → solleva → rilascia

Genera:
import robot_api
robot = robot_api.Robot()

# Passo 1: Afferra
robot.mano_destra.chiudi_dita(forza=50)
robot.sleep(0.5)

# Passo 2: Solleva
robot.braccio_destro.solleva(altezza=100)
robot.sleep(0.5)

# Passo 3: Rilascia
robot.mano_destra.apri_dita()
```

### Esempio 2: Condizione con Interrogativo
```
Frase: "quando il sensore rileva distanza minore di 10cm, ferma il robot"

Analisi:
- Interrogativo: quando (condizione)
- Soggetto: sensore
- Verbo: rilevare
- Template: robot

Genera:
while True:
    distanza = robot.sensore_distanza.leggi()
    if distanza < 10:
        robot.stop()
        print("Oggetto vicino! Robot fermato")
        break
```

### Esempio 3: Mano Bionica Gesture
```
Frase: "la mano fa il gesto ok poi aspetta 2 secondi poi apre le dita"

Analisi:
- Multi-comando (3 azioni)
- Template: mano_bionica

Genera:
from mano_bionica import ManoBionica, Gesti
import time

mano = ManoBionica()
mano.connetti()

# Gesto OK
mano.esegui_gesto(Gesti.OK)

# Aspetta
time.sleep(2)

# Apri
mano.apri_dita()
```

---

## 🎓 Grammatica Supportata

### Strutture Riconosciute

**Soggetto-Verbo-Complemento**:
- "il robot muove la mano"
- "la mano afferra l'oggetto"
- "il sensore rileva la distanza"

**Imperativi**:
- "muovi la mano"
- "afferra l'oggetto"
- "alza il braccio"

**Con Interrogativi**:
- "quando muovi la mano"
- "come afferra l'oggetto"
- "dove si trova il sensore"
- "perché si chiude la mano"

**Multi-Comando**:
- "muovi poi stampa"
- "afferra e poi solleva"
- "leggi sensore quindi fermati"

---

## 🔧 API Programmativa

### Scegliere Template
```python
from core import get_sistema_template

sistema = get_sistema_template()

# Lista template
templates = sistema.lista_template()
for t in templates:
    print(f"{t.nome}: {t.descrizione}")

# Scegli template
sistema.scegli_template('robot')

# Verifica attivo
print(sistema.get_template_attivo())  # → 'robot'
```

### Analisi Linguistica
```python
from core.linguaggio_naturale import analizza_linguaggio

struttura = analizza_linguaggio("quando il robot muove la mano")

if struttura.interrogativo == 'tempo':
    print("Richiesta condizionale!")

if struttura.modalita == 'imperativo':
    print("Comando diretto!")
```

### Generazione Contestuale
```python
from core import genera_codice
from core.generatore import GeneratoreCodice

# Con template robot
gen_robot = GeneratoreCodice(template='robot')
codice = gen_robot.genera("afferra oggetto con mano destra")

# Con template mano bionica
gen_mano = GeneratoreCodice(template='mano_bionica')
codice = gen_mano.genera("chiudi pugno con forza massima")
```

---

## 📊 Confronto Versioni

| Feature | v2.x | v3.0 |
|---------|------|------|
| Comandi singoli | ✅ | ✅ |
| Multi-comando | ✅ (v2.3) | ✅ |
| Soggetto-Verbo-Complemento | ❌ | ✅ |
| Interrogativi | ❌ | ✅ |
| Template domini | ❌ | ✅ |
| Robotica | ❌ | ✅ |
| Analisi contesto | ❌ | ✅ |
| AI contestuale | ❌ | ✅ |

---

## 🚀 Casi d'Uso

### Robotica Educativa
```python
# Insegna programmazione robotica in italiano
gen = GeneratoreCodice(template='robot')

codice = gen.genera("il robot saluta muovendo la mano")
# Studenti vedono codice Python per robot reale!
```

### Protesi Bioniche
```python
# Controlla mano bionica
gen = GeneratoreCodice(template='mano_bionica')

codice = gen.genera("afferra delicatamente l'oggetto fragile")
# Genera codice con controllo forza appropriato
```

### Automazione
```python
# Sequenze automatizzate
gen = GeneratoreCodice(template='robot')

codice = gen.genera("""
il robot afferra l'oggetto quando il sensore rileva presenza,
poi lo solleva, lo sposta a sinistra, e infine lo rilascia
""")
# Genera intera sequenza automatica!
```

---

## 📋 Librerie Hardware Supportate

### Per Robot
- **robot_api** (generico)
- **ROS** (Robot Operating System)
- **PyBullet** (simulazione)
- **Arduino** (via serial)
- **Raspberry Pi GPIO**

### Per Mani Bioniche
- **mano_bionica** (generico)
- **Serial** (comunicazione seriale)
- **Arduino** (Servo control)
- **MyoWare** (EMG sensors)

---

## ⚙️ Configurazione Template

### File di Config (Futuro)
```python
# config_robot.py
ROBOT_CONFIG = {
    'tipo': 'umanoide',
    'bracci': 2,
    'mani': 2,
    'dita_per_mano': 5,
    'sensori': ['distanza', 'contatto', 'temperatura'],
    'libreria': 'robot_api',
    'porta': 'COM3' oppure '/dev/ttyUSB0'
}
```

---

## 🎓 Tutorial Completo

### Step 1: Scegli Template
```python
from core.generatore import GeneratoreCodice

# Per robot
gen = GeneratoreCodice(template='robot')
```

### Step 2: Scrivi Comando Naturale
```python
comando = "il robot afferra l'oggetto con la mano destra"
```

### Step 3: Genera Codice
```python
codice = gen.genera(comando)
print(codice)
```

### Step 4: Usa il Codice
```python
# Salva in file
with open("controllo_robot.py", "w") as f:
    f.write(codice)

# Oppure esegui direttamente (in ambiente sicuro!)
# exec(codice)
```

---

## 📖 Dizionario Comandi Robotica

### Mani
| Italiano | Azione | Parametri |
|----------|--------|-----------|
| muovi mano destra | Movimento servo | angolo, velocità |
| afferra oggetto | Chiusura dita | forza |
| rilascia | Apertura dita | - |
| ruota polso | Rotazione | gradi |

### Bracci
| Italiano | Azione | Parametri |
|----------|--------|-----------|
| alza braccio | Solleva | altezza |
| abbassa braccio | Abbassa | altezza |
| estendi braccio | Estensione | lunghezza |
| ritira braccio | Retrazione | - |

### Sensori
| Italiano | Tipo | Output |
|----------|------|--------|
| leggi sensore distanza | Ultrasuoni | cm |
| rileva contatto | Touch | bool |
| misura temperatura | Termometro | °C |
| controlla pressione | Barometro | Pa |

### Gesti (Mano Bionica)
| Italiano | Gesto | Codice |
|----------|-------|--------|
| gesto ok | OK sign | Gesti.OK |
| pollice su | Thumbs up | Gesti.THUMBS_UP |
| punta | Point | Gesti.POINT |
| pace | Peace sign | Gesti.PEACE |

---

## 🔬 Esempi Avanzati

### Esempio 1: Controllo Condizionale
```
Comando: "se il sensore rileva oggetto a meno di 15cm, 
          allora afferra con mano destra, 
          altrimenti continua a cercare"

Genera:
import robot_api

robot = robot_api.Robot()

while True:
    distanza = robot.sensore_distanza.leggi()
    
    if distanza < 15:
        # Oggetto rilevato
        print(f"Oggetto a {distanza}cm")
        robot.mano_destra.chiudi_dita(forza=50)
        if robot.mano_destra.sensore_contatto():
            print("Afferrato!")
            break
    else:
        # Continua ricerca
        robot.cerca_oggetto()
```

### Esempio 2: Sequenza Complessa
```
Comando: "il robot afferra l'oggetto, poi lo sposta 20cm a sinistra,
          poi lo solleva 10cm, poi lo rilascia delicatamente"

Genera:
import robot_api
import time

robot = robot_api.Robot()

# Passo 1: Afferra
robot.mano_destra.chiudi_dita(forza=60)
time.sleep(0.5)

# Passo 2: Sposta sinistra
robot.muovi_laterale(direzione='sinistra', distanza=20)
time.sleep(1)

# Passo 3: Solleva
robot.braccio_destro.solleva(altezza=10)
time.sleep(0.5)

# Passo 4: Rilascia delicatamente
for i in range(60, 0, -5):  # Apertura graduale
    robot.mano_destra.apri_dita(forza=i)
    time.sleep(0.05)

print("Sequenza completata!")
```

### Esempio 3: Loop con Sensore
```
Comando: "per ogni oggetto rilevato, afferra, conta, e rilascia"

Genera:
import robot_api

robot = robot_api.Robot()
contatore = 0

while contatore < 10:  # Max 10 oggetti
    # Rileva oggetto
    if robot.sensore_oggetto.rileva():
        print(f"Oggetto {contatore + 1} rilevato")
        
        # Afferra
        robot.mano_destra.chiudi_dita()
        contatore += 1
        robot.sleep(1)
        
        # Rilascia
        robot.mano_destra.apri_dita()
        robot.sleep(1)

print(f"Totale oggetti processati: {contatore}")
```

---

## 🎯 Vantaggi Sistema v3.0

### Per Robotica
✅ Codice hardware-specific pronto all'uso  
✅ API standardizzate (robot_api, mano_bionica)  
✅ Gestione sensori integrata  
✅ Sequenze sicure con sleep e controlli  
✅ Pattern robusti per evitare danni  

### Per Didattica
✅ Insegna robotica in italiano  
✅ Da linguaggio naturale a codice robot  
✅ Comprensione strutture linguistiche  
✅ Pattern di programmazione robotica  

### Per Sviluppo
✅ Prototipazione rapida  
✅ Template per vari hardware  
✅ Estendibile con nuovi template  
✅ AI comprende contesto dominio  

---

## 📐 Architettura v3.0

```
Frase in italiano
    ↓
[1] Parser Linguistico
    → Soggetto, Verbo, Complemento
    → Interrogativi
    ↓
[2] Sistema Template
    → robot / mano_bionica / generico
    ↓
[3] Generatore Contestuale
    ├─→ Template specifico → Codice hardware
    └─→ AI + Analisi → Codice avanzato
    ↓
Codice Python per Hardware
```

---

## 🔧 Estendere il Sistema

### Aggiungere Nuovo Template

```python
# In core/template_domini.py

class TemplateDrone:
    """Template per droni."""
    
    @staticmethod
    def genera_decollo(params):
        return '''
import drone_api
drone = drone_api.Drone()
drone.arma_motori()
drone.decolla(altezza=params.get('altezza', 2))
'''
    
    # ...

# Registra template
TEMPLATE_DISPONIBILI['drone'] = {
    'nome': 'Drone',
    'classe': TemplateDrone,
    # ...
}
```

### Aggiungere Nuovi Comandi Robot

```python
# In core/template_domini.py → TemplateRobot

COMANDI_ROBOT = {
    # ... esistenti ...
    "cammina": ["cammina", "vai avanti", "muoviti"],
    "fermati": ["fermati", "stop", "blocca"],
    # ...
}

@staticmethod
def genera_cammina(params):
    passi = params.get('passi', 10)
    return f'''
robot.inizializza_camminata()
for passo in range({passi}):
    robot.passo_avanti()
    robot.mantieni_equilibrio()
'''
```

---

## 📚 Riferimenti

### File Principali
- `core/linguaggio_naturale.py` - Parser linguistico
- `core/template_domini.py` - Sistema template
- `core/generatore.py` - Generatore integrato

### Esempi
- `examples/esempio_robot.py` - Demo robot
- `examples/esempio_linguaggio_naturale.py` - Demo analisi

### Documentazione
- `LINGUAGGIO_NATURALE.md` - Questo file
- `COMANDI_SUPPORTATI.md` - Elenco comandi

---

## 🎊 Conclusione

**Pythonita IA v3.0** porta la generazione di codice a un nuovo livello:

Da: "Traduttore parole → comandi"  
A: "Comprensione linguaggio naturale → programmi completi"

**Perfetto per**:
- 🤖 Robotica educativa
- 🦾 Controllo protesi
- 🏭 Automazione industriale
- 🎓 Insegnamento programmazione
- 🔬 Ricerca e prototipazione

---

**Pythonita IA v3.0** - Parla al tuo robot in italiano! 🤖🇮🇹

