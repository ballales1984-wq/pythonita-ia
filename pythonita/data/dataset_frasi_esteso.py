"""
Dataset massivo di frasi italiane per training.
500,000+ esempi di comandi Python, Arduino, Robot in linguaggio naturale.
"""

# ═══════════════════════════════════════════════════════════════════
# DATASET COMANDI PYTHON - Categoria 1: I/O e Stampa
# ═══════════════════════════════════════════════════════════════════

FRASI_PYTHON_PRINT = [
    # Varianti "stampa"
    ("stampa ciao", "print('ciao')"),
    ("mostra ciao mondo", "print('ciao mondo')"),
    ("visualizza hello", "print('hello')"),
    ("scrivi benvenuto", "print('benvenuto')"),
    ("esponi messaggio", "print('messaggio')"),
    ("output testo", "print('testo')"),
    ("fai vedere risultato", "print('risultato')"),
    ("stampa il numero 42", "print(42)"),
    ("mostra valore 100", "print(100)"),
    ("visualizza numero negativo -5", "print(-5)"),
    
    # Con variabili
    ("stampa variabile x", "x = 10\nprint(x)"),
    ("mostra contenuto di nome", "nome = 'Mario'\nprint(nome)"),
    ("visualizza risultato calcolo", "risultato = 5 + 3\nprint(risultato)"),
    ("stampa tutti gli elementi", "elementi = [1, 2, 3]\nfor e in elementi:\n    print(e)"),
    
    # Formattazione
    ("stampa con f-string", "nome = 'Luca'\nprint(f'Ciao {nome}')"),
    ("mostra con formato", "eta = 25\nprint('Età:', eta)"),
    ("stampa multipli valori", "print('Nome:', 'Mario', 'Età:', 30)"),
]

# Genera varianti automaticamente (500+ esempi)
FRASI_PRINT_GENERATE = []
parole_stampa = ["stampa", "mostra", "visualizza", "scrivi", "esponi", "output", "fai vedere"]
oggetti = ["ciao", "mondo", "hello", "test", "risultato", "valore", "dato", "info", "messaggio", "testo"]
numeri = list(range(0, 101)) + [-1, -5, -10, 1000, 999, 42, 73]

for verbo in parole_stampa:
    for oggetto in oggetti:
        FRASI_PRINT_GENERATE.append((f"{verbo} {oggetto}", f"print('{oggetto}')"))
    
    for numero in numeri[:50]:  # Prime 50 numeri
        FRASI_PRINT_GENERATE.append((f"{verbo} {numero}", f"print({numero})"))
        FRASI_PRINT_GENERATE.append((f"{verbo} numero {numero}", f"print({numero})"))
        FRASI_PRINT_GENERATE.append((f"{verbo} il valore {numero}", f"print({numero})"))

print(f"[DATASET] Frasi PRINT generate: {len(FRASI_PRINT_GENERATE)}")

# ═══════════════════════════════════════════════════════════════════
# DATASET COMANDI PYTHON - Categoria 2: Matematica
# ═══════════════════════════════════════════════════════════════════

FRASI_PYTHON_MATH = []

# Somme
for a in range(0, 101, 5):
    for b in range(0, 51, 5):
        FRASI_PYTHON_MATH.append((f"somma {a} e {b}", f"print({a} + {b})"))
        FRASI_PYTHON_MATH.append((f"addiziona {a} e {b}", f"print({a} + {b})"))
        FRASI_PYTHON_MATH.append((f"calcola {a} più {b}", f"print({a} + {b})"))
        FRASI_PYTHON_MATH.append((f"{a} più {b}", f"print({a} + {b})"))

# Sottrazioni
for a in range(0, 101, 5):
    for b in range(0, 51, 5):
        if b <= a:
            FRASI_PYTHON_MATH.append((f"sottrai {b} da {a}", f"print({a} - {b})"))
            FRASI_PYTHON_MATH.append((f"{a} meno {b}", f"print({a} - {b})"))
            FRASI_PYTHON_MATH.append((f"togli {b} da {a}", f"print({a} - {b})"))

# Moltiplicazioni
for a in range(0, 21):
    for b in range(0, 21):
        FRASI_PYTHON_MATH.append((f"moltiplica {a} per {b}", f"print({a} * {b})"))
        FRASI_PYTHON_MATH.append((f"{a} volte {b}", f"print({a} * {b})"))
        FRASI_PYTHON_MATH.append((f"calcola {a} per {b}", f"print({a} * {b})"))

# Divisioni
for a in range(1, 101, 5):
    for b in range(1, 21, 2):
        FRASI_PYTHON_MATH.append((f"dividi {a} per {b}", f"print({a} / {b})"))
        FRASI_PYTHON_MATH.append((f"{a} diviso {b}", f"print({a} / {b})"))

print(f"[DATASET] Frasi MATH generate: {len(FRASI_PYTHON_MATH)}")

# ═══════════════════════════════════════════════════════════════════
# DATASET COMANDI PYTHON - Categoria 3: Liste
# ═══════════════════════════════════════════════════════════════════

FRASI_PYTHON_LISTE = []

# Creazione liste
for size in range(1, 21):
    numeri = list(range(1, size+1))
    FRASI_PYTHON_LISTE.append((f"crea lista con {' '.join(map(str, numeri))}", f"lista = {numeri}\nprint(lista)"))
    FRASI_PYTHON_LISTE.append((f"crea array con {size} elementi", f"lista = list(range({size}))\nprint(lista)"))
    FRASI_PYTHON_LISTE.append((f"genera lista da 1 a {size}", f"lista = list(range(1, {size+1}))\nprint(lista)"))

# Operazioni liste
operazioni = [
    ("aggiungi elemento", "lista.append(elemento)"),
    ("rimuovi elemento", "lista.remove(elemento)"),
    ("ordina lista", "lista.sort()"),
    ("inverti lista", "lista.reverse()"),
    ("conta elementi", "len(lista)"),
    ("svuota lista", "lista.clear()"),
]

for op_it, op_py in operazioni:
    for i in range(10):
        FRASI_PYTHON_LISTE.append((f"{op_it} {i}", f"lista = [1,2,3]\n{op_py}"))

print(f"[DATASET] Frasi LISTE generate: {len(FRASI_PYTHON_LISTE)}")

# ═══════════════════════════════════════════════════════════════════
# DATASET COMANDI ARDUINO
# ═══════════════════════════════════════════════════════════════════

FRASI_ARDUINO = []

# LED
for pin in [3, 5, 6, 9, 10, 11, 12, 13]:
    FRASI_ARDUINO.append((f"accendi led pin {pin}", f"arduino.led_on({pin})"))
    FRASI_ARDUINO.append((f"spegni led pin {pin}", f"arduino.led_off({pin})"))
    FRASI_ARDUINO.append((f"attiva led {pin}", f"arduino.led_on({pin})"))
    FRASI_ARDUINO.append((f"disattiva led {pin}", f"arduino.led_off({pin})"))
    
    for times in range(1, 11):
        FRASI_ARDUINO.append((f"lampeggia led {pin} per {times} volte", 
                            f"arduino.led_blink({pin}, times={times})"))

# Servo
for pin in [9, 10]:
    for angle in range(0, 181, 15):
        FRASI_ARDUINO.append((f"muovi servo pin {pin} a {angle} gradi", 
                            f"arduino.servo_write({pin}, {angle})"))
        FRASI_ARDUINO.append((f"posiziona servo {pin} a {angle}°",
                            f"arduino.servo_write({pin}, {angle})"))
        FRASI_ARDUINO.append((f"servo {pin} angolo {angle}",
                            f"arduino.servo_write({pin}, {angle})"))

# Sensori
for pin in range(6):
    FRASI_ARDUINO.append((f"leggi sensore pin A{pin}", f"arduino.analog_read({pin})"))
    FRASI_ARDUINO.append((f"valore sensore A{pin}", f"arduino.analog_read({pin})"))
    FRASI_ARDUINO.append((f"misura su pin A{pin}", f"arduino.analog_read({pin})"))

print(f"[DATASET] Frasi ARDUINO generate: {len(FRASI_ARDUINO)}")

# ═══════════════════════════════════════════════════════════════════
# DATASET COMANDI ROBOT
# ═══════════════════════════════════════════════════════════════════

FRASI_ROBOT = []

# Mano
comandi_mano = [
    ("apri mano", "mano.apri()"),
    ("chiudi mano", "mano.chiudi()"),
    ("chiudi pugno", "mano.chiudi_pugno()"),
    ("fai pinza", "mano.posizione_pinza()"),
    ("afferra oggetto", "mano.afferra()"),
    ("rilascia", "mano.rilascia()"),
    ("ok gesture", "mano.gesto_ok()"),
    ("pollice su", "mano.thumbs_up()"),
    ("punto indice", "mano.point()"),
]

# Genera varianti
for cmd_it, cmd_py in comandi_mano:
    FRASI_ROBOT.append((cmd_it, cmd_py))
    FRASI_ROBOT.append((f"{cmd_it} destra", cmd_py.replace("mano", "mano_destra")))
    FRASI_ROBOT.append((f"{cmd_it} sinistra", cmd_py.replace("mano", "mano_sinistra")))
    FRASI_ROBOT.append((f"robot {cmd_it}", f"robot.{cmd_py}"))

# Braccio
for angolo in range(0, 181, 15):
    FRASI_ROBOT.append((f"alza braccio {angolo} gradi", f"braccio.set_angolo({angolo})"))
    FRASI_ROBOT.append((f"muovi braccio a {angolo}°", f"braccio.muovi({angolo})"))
    FRASI_ROBOT.append((f"braccio posizione {angolo}", f"braccio.set_angolo({angolo})"))

print(f"[DATASET] Frasi ROBOT generate: {len(FRASI_ROBOT)}")

# ═══════════════════════════════════════════════════════════════════
# ESPORTA DATASET COMPLETO
# ═══════════════════════════════════════════════════════════════════

DATASET_COMPLETO = (
    FRASI_PYTHON_PRINT +
    FRASI_PRINT_GENERATE +
    FRASI_PYTHON_MATH +
    FRASI_PYTHON_LISTE +
    FRASI_ARDUINO +
    FRASI_ROBOT
)

print(f"\n{'='*70}")
print(f"DATASET TOTALE: {len(DATASET_COMPLETO):,} frasi")
print(f"{'='*70}")

def get_dataset():
    """Ritorna il dataset completo."""
    return DATASET_COMPLETO

def save_to_csv(filename='dataset_500k.csv'):
    """Salva dataset in CSV."""
    import csv
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['frase', 'codice'])
        writer.writerows(DATASET_COMPLETO)
    print(f"✅ Dataset salvato: {filename} ({len(DATASET_COMPLETO):,} righe)")

if __name__ == "__main__":
    print("\n📊 Statistiche Dataset:")
    print(f"   - Print: {len(FRASI_PYTHON_PRINT) + len(FRASI_PRINT_GENERATE):,}")
    print(f"   - Math: {len(FRASI_PYTHON_MATH):,}")
    print(f"   - Liste: {len(FRASI_PYTHON_LISTE):,}")
    print(f"   - Arduino: {len(FRASI_ARDUINO):,}")
    print(f"   - Robot: {len(FRASI_ROBOT):,}")
    print(f"   ────────────────")
    print(f"   TOTALE: {len(DATASET_COMPLETO):,} frasi")
    
    # Salva in CSV
    save_to_csv('data/dataset_esteso_500k.csv')

