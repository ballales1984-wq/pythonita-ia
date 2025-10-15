# 🚀 Changelog v2.3.0 - Multi-Comando Intelligente

**Data Release**: 15 Ottobre 2025  
**Tipo**: Minor Release  
**Focus**: Combinazioni multi-comando

---

## ✨ Novità Principale: Multi-Comando! 🔗

**Ora puoi combinare più comandi in una frase!**

### Prima (v2.2):
```
"stampa ciao"  → print("ciao")
```

### Dopo (v2.3):
```
"chiedi nome e poi stampalo"  
→ nome = input("Inserisci il tuo nome: ")
  print(nome)
```

**Da comandi singoli a programmi completi!** 🎉

---

## 📦 Nuovi Moduli

### `core/multi_comando.py` (300 righe)
- **MultiComandoParser**: Identifica e separa più comandi
- **CombinatoreCodice**: Combina codici in modo intelligente
- **5 Template Pattern**: Per combinazioni comuni
- **Connettori**: poi, dopo, quindi, infine, e poi

**Features**:
- Pattern recognition automatico
- Template per combinazioni comuni
- Combinazione intelligente di codici
- Gestione variabili condivise

---

## 🎯 Pattern Supportati

### 1. Input → Print
```python
Frase: "chiedi nome e poi stampalo"

Codice:
nome = input("Inserisci il tuo nome: ")
print(nome)
```

### 2. Create → Iterate
```python
Frase: "crea lista con 1 2 3 poi stampa ogni elemento"

Codice:
lista = [1, 2, 3]
for elemento in lista:
    print(elemento)
```

### 3. Read → Process
```python
Frase: "leggi file dati.txt poi processa le righe"

Codice:
with open('dati.txt', 'r') as file:
    for riga in file:
        print(riga.strip())
```

### 4. Loop → Action
```python
Frase: "per ogni numero da 1 a 5 stampa il doppio"

Codice:
for i in range(1, 6):
    print(i * 2)
```

### 5. Conditional → Action
```python
Frase: "se x maggiore di 10 poi stampa risultato"

Codice:
x = 15
if x > 10:
    print(f"x ({x}) è maggiore di 10")
```

---

## 🔧 Modifiche ai File Esistenti

### `core/generatore.py`
- Aggiunto supporto multi-comando in `genera()`
- Nuovo metodo `_genera_multi_comando()`
- Strategia a 4 livelli:
  1. Cache
  2. AI (gestisce multi-comando complessi)
  3. Multi-comando con regole
  4. Fallback

### `core/__init__.py`
- Esportato `MultiComandoParser`
- Esportato `CombinatoreCodice`
- Esportato `combina_comandi`

---

## 🧪 Testing

### Nuovi Test
- **File**: `tests/unit/test_multi_comando.py`
- **Test**: 19 test
- **Risultati**: 19/19 PASSED ✅

**Totale Suite**: 112 test (93 + 19)

### Test Coverage
```
core/multi_comando.py: 89% coverage
Tutti i pattern testati
End-to-end test per ogni pattern
```

---

## 📚 Documentazione

### Nuovi Documenti
- **`MULTI_COMANDO.md`** (400 righe)
  - Guida completa multi-comando
  - 5 pattern con esempi
  - API programmatica
  - Best practices
  - Tips e limitazioni

### Esempi
- **`examples/esempio_multi_comando.py`**
  - 5 demo pratiche
  - Risultati visibili
  - Pattern comuni

---

## 📊 Esempi Reali Testati

Tutti questi esempi funzionano:

```python
# 1. Input e elaborazione
"chiedi due numeri poi sommali e stampa risultato"

# 2. Lista e filtraggio
"crea lista numeri poi filtra solo i pari e stampali"

# 3. File processing
"apri file testo.txt poi conta le righe e stampa totale"

# 4. Loop con calcolo
"per ogni numero da 1 a 10 calcola il quadrato poi stampalo"

# 5. Dizionario
"crea dizionario con nome età poi stampa le chiavi"
```

---

## 🎓 Casi d'Uso

### Didattica
- Mostra programmi completi agli studenti
- Genera esempi articolati
- Insegna il flusso logico

### Prototipazione
- Crea script rapidi con più azioni
- Test di logica multi-step
- POC (Proof of Concept) veloci

### Apprendimento
- Vedi come si combinano comandi
- Impara pattern comuni
- Comprendi il flusso di dati

---

## 📈 Statistiche

### Comandi
```
v2.2: 143 comandi singoli
v2.3: 143 comandi + infinite combinazioni!
```

### Pattern
```
Pattern riconosciuti: 5+
Connettori supportati: 7
Template disponibili: 5
```

### Test
```
v2.2: 93 test
v2.3: 112 test (+20%)
```

---

## 🚀 Performance

**Cache funziona anche con multi-comando!**

```
Query: "chiedi nome poi stampalo"
Prima volta: 4-5s (AI genera)
Seconda volta: 0.001s (cache hit!)
```

---

## ⬆️ Upgrade da v2.2

```bash
# Pull modifiche
git pull origin main

# Prova multi-comando
python main.py

>>> chiedi nome e poi stampalo
>>> crea lista poi itera
>>> leggi file poi processa
```

---

## 💡 Esempio Completo

**Input Utente**:
```
"chiedi età poi se maggiore di 18 stampa adulto altrimenti minorenne"
```

**Codice Generato**:
```python
età = int(input("Inserisci la tua età: "))

if età >= 18:
    print("Sei adulto")
else:
    print("Sei minorenne")
```

---

## 🎯 Breaking Changes

**Nessuno!** Tutto backward-compatible.

Comandi singoli funzionano esattamente come prima.

---

## 🔗 Link Utili

- **Guida Completa**: `MULTI_COMANDO.md`
- **Demo**: `examples/esempio_multi_comando.py`
- **Test**: `tests/unit/test_multi_comando.py`
- **Codice**: `core/multi_comando.py`

---

## 📋 Prossimi Passi (v2.4)

- [ ] Più template pattern
- [ ] Context sharing avanzato
- [ ] Supporto variabili tra comandi
- [ ] Ottimizzazione combinazioni
- [ ] GUI con preview multi-step

---

**Pythonita IA v2.3.0** - Dalla frase al programma! 🔗🚀

