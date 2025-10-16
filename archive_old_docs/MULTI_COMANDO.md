# 🔗 Combinazioni Multi-Comando - Pythonita IA v2.3

**Novità**: Pythonita ora può combinare più comandi in un unico programma!

---

## 🎯 Cos'è Multi-Comando?

Prima potevi dire:
```
"stampa ciao"  → print("ciao")
```

Ora puoi dire:
```
"chiedi nome e poi stampalo"  
→ nome = input("Inserisci il tuo nome: ")
  print(nome)
```

**Più comandi = Programmi completi!** 🚀

---

## 💡 Pattern Supportati

### 1. Input → Print
**Frase**: "chiedi nome e poi stampalo"

**Codice Generato**:
```python
nome = input("Inserisci il tuo nome: ")
print(nome)
```

---

### 2. Crea → Itera
**Frase**: "crea lista con 1 2 3 poi stampa ogni elemento"

**Codice Generato**:
```python
lista = [1, 2, 3]
for elemento in lista:
    print(elemento)
```

---

### 3. Leggi File → Processa
**Frase**: "leggi file dati.txt poi processa le righe"

**Codice Generato**:
```python
with open('dati.txt', 'r') as file:
    for riga in file:
        print(riga.strip())
```

---

### 4. Loop → Azione
**Frase**: "per ogni numero da 1 a 5 stampa il doppio"

**Codice Generato**:
```python
for i in range(1, 6):
    print(i * 2)
```

---

### 5. Condizione → Azione
**Frase**: "se x maggiore di 10 poi stampa risultato"

**Codice Generato**:
```python
x = 15
if x > 10:
    print(f"x ({x}) è maggiore di 10")
    risultato = x * 2
    print(f"Risultato: {risultato}")
```

---

## 🔑 Parole Chiave per Combinazioni

### Connettori Sequenza:
- **poi** - "crea lista poi stampa"
- **dopo** - "leggi file dopo processa"
- **quindi** - "chiedi input quindi calcola"
- **infine** - "crea poi ordina infine stampa"
- **e poi** - "apri file e poi leggi"
- **e dopo** - "genera numeri e dopo sommali"

### Congiunzioni:
- **e** - "chiedi nome e stampalo"
- **con** - "crea lista con 5 elementi"
- **usando** - "apri file usando with"

---

## 📚 Esempi Pratici

### Esempio 1: Calculator
```
Frase: "chiedi due numeri poi sommali e stampa risultato"

Codice:
a = int(input("Primo numero: "))
b = int(input("Secondo numero: "))
risultato = a + b
print(f"Risultato: {risultato}")
```

### Esempio 2: Lista Filtrata
```
Frase: "crea lista numeri poi filtra solo i pari e stampali"

Codice:
numeri = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
pari = [n for n in numeri if n % 2 == 0]
print(pari)
```

### Esempio 3: File Processing
```
Frase: "apri file testo.txt poi conta le righe e stampa totale"

Codice:
with open('testo.txt', 'r') as f:
    righe = f.readlines()
    totale = len(righe)
    print(f"Totale righe: {totale}")
```

### Esempio 4: Loop Complesso
```
Frase: "per ogni numero da 1 a 10 calcola il quadrato poi stampalo"

Codice:
for numero in range(1, 11):
    quadrato = numero ** 2
    print(f"{numero}^2 = {quadrato}")
```

### Esempio 5: Dizionario
```
Frase: "crea dizionario con nome eta poi stampa le chiavi"

Codice:
dati = {"nome": "Mario", "età": 30}
print("Chiavi:", dati.keys())
```

---

## 🎨 Pattern Riconosciuti Automaticamente

Il sistema riconosce questi pattern comuni:

| Pattern | Esempio | Template |
|---------|---------|----------|
| `input_then_print` | "chiedi X poi stampa" | Input → Print |
| `create_then_iterate` | "crea lista poi ciclo" | Lista → For loop |
| `read_then_process` | "leggi file poi processa" | Open → Process |
| `loop_with_action` | "per ogni X fai Y" | For → Action |
| `conditional_action` | "se X poi Y" | If → Then |
| `sequence` | Sequenza generica | Combina codici |

---

## 🚀 Come Funziona

### 1. Parsing Intelligente
```python
Frase: "chiedi nome poi stampalo"

Parser identifica:
- Multi-comando: Sì
- Pattern: input_then_print
- Comandi: ["chiedi nome", "stampalo"]
```

### 2. Generazione Template
```python
Se pattern riconosciuto:
    → Usa template specifico
Altrimenti:
    → Genera ogni comando singolarmente
    → Combina in modo intelligente
```

### 3. Combinazione Intelligente
```python
- Rimuove duplicati
- Unisce variabili
- Mantiene ordine logico
- Aggiunge commenti chiarificatori
```

---

## 💻 API Programmatica

### Verifica se Frase è Multi-Comando
```python
from core.multi_comando import MultiComandoParser

parser = MultiComandoParser()
is_multi = parser.identifica_multi_comando("crea lista poi stampa")
# → True
```

### Analizza Struttura
```python
analisi = parser.analizza_struttura("chiedi nome poi stampalo")

print(analisi)
# {
#     'è_multi_comando': True,
#     'pattern': 'input_then_print',
#     'comandi_separati': ['chiedi nome', 'stampalo'],
#     'numero_comandi': 2
# }
```

### Combina Codici Manualmente
```python
from core.multi_comando import combina_comandi

codici = [
    'x = 10',
    'y = 20',
    'print(x + y)'
]

combinato = combina_comandi("test", codici)
# → x = 10
#   y = 20
#   print(x + y)
```

---

## 🎓 Tips per Usare Multi-Comando

### 1. Usa Connettori Chiari
✅ "crea lista **poi** itera"  
✅ "leggi file **dopo** processa"  
✅ "chiedi input **quindi** stampa"  

### 2. Sii Specifico
✅ "crea lista con 1 2 3 poi stampa ogni elemento"  
❌ "fai qualcosa poi altra cosa"  

### 3. Ordine Logico
✅ "prima chiedi nome poi stampalo"  
✅ "apri file poi leggi poi chiudi"  

### 4. L'AI Gestisce Complessità
Per frasi molto complesse, l'AI locale (Llama3.2) è migliore:
```
"crea una funzione che legge un file CSV, filtra le righe dove 
l'età è maggiore di 18, e stampa i nomi in ordine alfabetico"

→ L'AI genera tutto il codice necessario!
```

---

## 📊 Confronto

### Prima (v2.2)
```
Query: "crea lista poi stampa"
→ Genera solo: lista = [1, 2, 3]
   (ignora "poi stampa")
```

### Dopo (v2.3)
```
Query: "crea lista poi stampa"
→ Genera:
   lista = [1, 2, 3]
   print(lista)
   
(Combina entrambi i comandi!)
```

---

## 🧪 Test

**Test Suite**: 19 test per multi-comando  
**Risultati**: 19/19 PASSATI ✅  

Test coprono:
- Identificazione multi-comando
- Separazione comandi
- Pattern recognition
- Template generation
- Combinazione codici
- End-to-end

---

## 📝 Limitazioni Attuali

1. **Max 5 comandi** combinati (poi usa AI)
2. **Pattern predefiniti** limitati (ma espandibili)
3. **Contesto semplice** (variabili condivise base)

**Soluzione**: Per frasi molto complesse, l'AI gestisce tutto automaticamente!

---

## 🔮 Esempi Avanzati

### Con AI (Gestisce Complessità)
```
"crea funzione che filtra lista numeri pari poi li eleva al quadrato 
poi li somma e stampa risultato"

→ L'AI genera:
def filtra_e_calcola(numeri):
    pari = [n for n in numeri if n % 2 == 0]
    quadrati = [n**2 for n in pari]
    somma = sum(quadrati)
    print(f"Somma quadrati pari: {somma}")

numeri = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
filtra_e_calcola(numeri)
```

### Con Regole (Pattern Semplici)
```
"crea lista poi ordina poi stampa"

→ Regole generano:
lista = [3, 1, 4, 1, 5]
lista_ordinata = sorted(lista)
print(lista_ordinata)
```

---

## 🎯 Best Practices

### DO ✅
- Usa connettori chiari ("poi", "dopo", "e poi")
- Mantieni frasi logiche e sequenziali
- Specifica i dettagli importanti
- Usa pattern comuni (quelli nell'elenco sopra)

### DON'T ❌
- Non mescolare troppe azioni diverse
- Non usare frasi ambigue
- Non omettere i connettori
- Non chiedere più di 5 comandi insieme con regole

---

## 📖 Riferimenti

- **Modulo**: `core/multi_comando.py`
- **Test**: `tests/unit/test_multi_comando.py`
- **Demo**: `examples/esempio_multi_comando.py`

---

**Pythonita IA v2.3** - Combina comandi come un vero programmatore! 🔗🚀

