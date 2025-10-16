"""
Generatore dataset massivo - 500K+ frasi italiane.
Espande il programma con training data pesante.
"""

import random
import csv
from pathlib import Path

print("=" * 70)
print("📦 GENERATORE DATASET MASSIVO - Target: 500K+ frasi")
print("=" * 70)

dataset = []

# ═══════════════════════════════════════════════════════════════════
# 1. COMANDI PRINT - Target: 100K frasi
# ═══════════════════════════════════════════════════════════════════

print("\n[1/7] Generando frasi PRINT...")

verbi_stampa = ["stampa", "mostra", "visualizza", "scrivi", "esponi", "output", "fai vedere", "display"]
sostantivi = ["ciao", "mondo", "hello", "test", "risultato", "valore", "dato", "info", "messaggio", 
              "testo", "output", "risposta", "contenuto", "elemento", "oggetto", "variabile",
              "nome", "cognome", "città", "paese", "indirizzo", "telefono", "email", "codice"]
aggettivi = ["bello", "grande", "piccolo", "nuovo", "vecchio", "importante", "utile", "finale"]

for verbo in verbi_stampa:
    for sost in sostantivi:
        dataset.append((f"{verbo} {sost}", f"print('{sost}')"))
        dataset.append((f"{verbo} il {sost}", f"print('{sost}')"))
        dataset.append((f"{verbo} questo {sost}", f"print('{sost}')"))
        
        for agg in aggettivi:
            dataset.append((f"{verbo} {sost} {agg}", f"print('{sost} {agg}')"))

# Numeri
for verbo in verbi_stampa:
    for n in range(0, 1001, 1):  # 0-1000
        dataset.append((f"{verbo} {n}", f"print({n})"))
        if n % 10 == 0:
            dataset.append((f"{verbo} numero {n}", f"print({n})"))
            dataset.append((f"{verbo} il valore {n}", f"print({n})"))

print(f"   Frasi PRINT: {len([d for d in dataset if 'print' in d[1]]):,}")

# ═══════════════════════════════════════════════════════════════════
# 2. MATEMATICA - Target: 150K frasi
# ═══════════════════════════════════════════════════════════════════

print("[2/7] Generando frasi MATEMATICA...")

# Somme complete
for a in range(0, 201):
    for b in range(0, 201):
        dataset.append((f"somma {a} e {b}", f"print({a} + {b})"))
        if (a + b) % 10 == 0:
            dataset.append((f"quanto fa {a} più {b}", f"print({a} + {b})"))
            dataset.append((f"calcola {a} più {b}", f"print({a} + {b})"))

# Sottrazioni
for a in range(0, 201):
    for b in range(0, min(a+1, 101)):
        dataset.append((f"{a} meno {b}", f"print({a} - {b})"))
        if a % 10 == 0:
            dataset.append((f"sottrai {b} da {a}", f"print({a} - {b})"))

# Moltiplicazioni
for a in range(0, 101):
    for b in range(0, 101):
        dataset.append((f"{a} per {b}", f"print({a} * {b})"))
        if b % 5 == 0:
            dataset.append((f"moltiplica {a} per {b}", f"print({a} * {b})"))

# Divisioni
for a in range(1, 201):
    for b in range(1, 51):
        dataset.append((f"{a} diviso {b}", f"print({a} / {b})"))

print(f"   Frasi MATH: {len([d for d in dataset if '+' in d[1] or '-' in d[1] or '*' in d[1] or '/' in d[1]]):,}")

# ═══════════════════════════════════════════════════════════════════
# 3. LISTE E STRUTTURE DATI - Target: 50K
# ═══════════════════════════════════════════════════════════════════

print("[3/7] Generando frasi LISTE...")

for size in range(1, 101):
    dataset.append((f"crea lista da 1 a {size}", f"lista = list(range(1, {size+1}))\nprint(lista)"))
    dataset.append((f"genera array di {size} elementi", f"lista = list(range({size}))\nprint(lista)"))
    dataset.append((f"lista con {size} numeri", f"lista = list(range({size}))\nprint(lista)"))

# Operazioni su liste
for i in range(1, 501):
    dataset.append((f"aggiungi {i} alla lista", f"lista.append({i})"))
    dataset.append((f"rimuovi {i} dalla lista", f"lista.remove({i})"))

print(f"   Frasi LISTE: {len([d for d in dataset if 'list' in d[1] or 'append' in d[1]]):,}")

# ═══════════════════════════════════════════════════════════════════
# 4. CICLI E CONTROLLO - Target: 50K
# ═══════════════════════════════════════════════════════════════════

print("[4/7] Generando frasi CICLI...")

for start in range(0, 51):
    for end in range(start+1, start+51):
        dataset.append((f"ciclo da {start} a {end}", f"for i in range({start}, {end+1}):\n    print(i)"))
        dataset.append((f"ripeti da {start} a {end}", f"for i in range({start}, {end+1}):\n    print(i)"))
        dataset.append((f"itera da {start} a {end}", f"for i in range({start}, {end+1}):\n    print(i)"))

for times in range(1, 101):
    dataset.append((f"ripeti {times} volte", f"for i in range({times}):\n    print(i)"))
    dataset.append((f"esegui {times} iterazioni", f"for i in range({times}):\n    print(i)"))

print(f"   Frasi CICLI: {len([d for d in dataset if 'for' in d[1] or 'while' in d[1]]):,}")

# ═══════════════════════════════════════════════════════════════════
# 5. ARDUINO - Target: 80K
# ═══════════════════════════════════════════════════════════════════

print("[5/7] Generando frasi ARDUINO...")

# LED su tutti i pin
for pin in range(2, 14):
    for state in ['accendi', 'spegni', 'attiva', 'disattiva', 'acceso', 'spento']:
        dataset.append((f"{state} led pin {pin}", f"arduino.led_{('on' if state in ['accendi','attiva','acceso'] else 'off')}({pin})"))
    
    for times in range(1, 51):
        dataset.append((f"lampeggia led {pin} {times} volte", f"arduino.led_blink({pin}, times={times})"))
        dataset.append((f"led {pin} lampeggia {times}", f"arduino.led_blink({pin}, times={times})"))

# Servo completo
for pin in [3, 5, 6, 9, 10, 11]:
    for angle in range(0, 181):
        dataset.append((f"servo pin {pin} angolo {angle}", f"arduino.servo_write({pin}, {angle})"))
        if angle % 5 == 0:
            dataset.append((f"muovi servo {pin} a {angle} gradi", f"arduino.servo_write({pin}, {angle})"))

print(f"   Frasi ARDUINO: {len([d for d in dataset if 'arduino' in d[1]]):,}")

# ═══════════════════════════════════════════════════════════════════
# 6. ROBOT - Target: 30K
# ═══════════════════════════════════════════════════════════════════

print("[6/7] Generando frasi ROBOT...")

comandi_base = ["apri", "chiudi", "muovi", "ruota", "alza", "abbassa", "piega", "estendi"]
parti = ["mano", "dita", "pollice", "indice", "medio", "anulare", "mignolo", "pugno", "braccio", "gomito", "spalla"]
lati = ["destra", "sinistra", ""]

for comando in comandi_base:
    for parte in parti:
        for lato in lati:
            frase = f"{comando} {parte} {lato}".strip()
            codice = f"robot.{comando}_{parte}()" if not lato else f"robot.{comando}_{parte}_{lato}()"
            dataset.append((frase, codice))
            
            # Varianti
            dataset.append((f"robot {frase}", codice))
            dataset.append((f"fai {frase}", codice))

# Angoli specifici
for angolo in range(0, 181, 5):
    for parte in ["braccio", "gomito", "polso"]:
        dataset.append((f"{parte} a {angolo} gradi", f"robot.{parte}.set_angolo({angolo})"))
        dataset.append((f"muovi {parte} {angolo}°", f"robot.{parte}.muovi({angolo})"))

print(f"   Frasi ROBOT: {len([d for d in dataset if 'robot' in d[1]]):,}")

# ═══════════════════════════════════════════════════════════════════
# 7. COMANDI COMPLESSI - Target: 40K
# ═══════════════════════════════════════════════════════════════════

print("[7/7] Generando frasi COMPLESSE...")

# Funzioni
nomi_funzioni = ["calcola", "somma", "moltiplica", "elabora", "processa", "analizza", "verifica"]
for nome in nomi_funzioni:
    for i in range(100):
        dataset.append((f"crea funzione {nome}", f"def {nome}():\n    pass"))
        dataset.append((f"definisci {nome}", f"def {nome}():\n    return None"))

# Classi
nomi_classi = ["Robot", "Sensore", "Motore", "LED", "Servo", "Controller", "Manager", "Handler"]
for nome in nomi_classi:
    for i in range(50):
        dataset.append((f"crea classe {nome}", f"class {nome}:\n    def __init__(self):\n        pass"))

# Gestione errori
for i in range(200):
    dataset.append((f"gestisci errore divisione", "try:\n    x = 1/0\nexcept ZeroDivisionError:\n    print('Errore')"))
    dataset.append((f"cattura eccezione", "try:\n    pass\nexcept Exception as e:\n    print(e)"))

# File I/O
estensioni = ['txt', 'csv', 'json', 'xml', 'log']
for ext in estensioni:
    for i in range(100):
        dataset.append((f"leggi file {ext}", f"with open('file.{ext}', 'r') as f:\n    content = f.read()"))
        dataset.append((f"scrivi file {ext}", f"with open('file.{ext}', 'w') as f:\n    f.write('data')"))

print(f"   Frasi COMPLESSE: {len(dataset) - (len([d for d in dataset if 'arduino' in d[1]]) + len([d for d in dataset if 'robot' in d[1] and 'arduino' not in d[1]]) + len([d for d in dataset if any(op in d[1] for op in ['+','-','*','/']) and 'arduino' not in d[1]]) + len([d for d in dataset if 'print' in d[1] and all(op not in d[1] for op in ['+','-','*','/'])])):,}")

# ═══════════════════════════════════════════════════════════════════
# SALVA DATASET
# ═══════════════════════════════════════════════════════════════════

print(f"\n{'='*70}")
print(f"📊 DATASET TOTALE: {len(dataset):,} frasi")
print(f"{'='*70}")

# Crea directory se non esiste
Path('data').mkdir(exist_ok=True)

# Salva CSV
filename = 'data/dataset_massivo_500k.csv'
with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['frase_italiana', 'codice_python'])
    writer.writerows(dataset)

# Calcola dimensione
size_mb = Path(filename).stat().st_size / (1024 * 1024)

print(f"\n✅ Dataset salvato!")
print(f"   File: {filename}")
print(f"   Righe: {len(dataset):,}")
print(f"   Dimensione: {size_mb:.2f} MB")
print(f"{'='*70}")

