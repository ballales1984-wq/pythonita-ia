"""
Regole per generare codice Python da comandi italiani.
Supporta 100+ comandi Python.
"""

from typing import List


def estrai_numeri(frase: str) -> List[int]:
    """Estrae numeri dalla frase."""
    return [int(s) for s in frase.split() if s.replace('.', '').replace('-', '').isdigit()]


def estrai_stringhe(frase: str) -> List[str]:
    """Estrae parole (escludendo keyword comuni)."""
    skip = ['stampa', 'mostra', 'crea', 'usa', 'importa', 'con', 'per', 'da', 'a', 'e', 'il', 'la', 'di', 'un', 'una']
    return [p for p in frase.split() if p.lower() not in skip and not p.isdigit()]


class RegoleComandi:
    """Regole per generare codice da comandi italiani."""
    
    @staticmethod
    def genera_print(frase: str) -> str:
        """Regola per print."""
        contenuto = frase.split(" ", 1)[-1]
        return f'print("{contenuto}")'
    
    @staticmethod
    def genera_input(frase: str) -> str:
        """Regola per input."""
        return 'risposta = input("Inserisci un valore: ")\nprint("Hai scritto:", risposta)'
    
    @staticmethod
    def genera_somma(frase: str) -> str:
        """Regola per somma."""
        numeri = estrai_numeri(frase)
        if len(numeri) >= 2:
            return f'print({numeri[0]} + {numeri[1]})'
        return f'# Somma di numeri\nrisultato = sum([{", ".join(map(str, numeri))}])\nprint(risultato)'
    
    @staticmethod
    def genera_sottrazione(frase: str) -> str:
        """Regola per sottrazione."""
        numeri = estrai_numeri(frase)
        if len(numeri) >= 2:
            return f'print({numeri[0]} - {numeri[1]})'
        return "# Errore: servono almeno due numeri"
    
    @staticmethod
    def genera_moltiplicazione(frase: str) -> str:
        """Regola per moltiplicazione."""
        numeri = estrai_numeri(frase)
        if len(numeri) >= 2:
            return f'print({numeri[0]} * {numeri[1]})'
        return "# Errore: servono almeno due numeri"
    
    @staticmethod
    def genera_divisione(frase: str) -> str:
        """Regola per divisione."""
        numeri = estrai_numeri(frase)
        if len(numeri) >= 2 and numeri[1] != 0:
            return f'print({numeri[0]} / {numeri[1]})'
        return "# Errore: divisione non valida"
    
    @staticmethod
    def genera_if(frase: str) -> str:
        """Regola per if."""
        return 'x = 10\nif x > 5:\n    print("x è maggiore di 5")'
    
    @staticmethod
    def genera_for(frase: str) -> str:
        """Regola per ciclo for."""
        numeri = estrai_numeri(frase)
        if len(numeri) >= 2:
            return f'for i in range({numeri[0]}, {numeri[1]} + 1):\n    print(i)'
        return 'for i in range(5):\n    print("Iterazione", i)'
    
    @staticmethod
    def genera_while(frase: str) -> str:
        """Regola per while."""
        return 'x = 0\nwhile x < 5:\n    print("x =", x)\n    x += 1'
    
    @staticmethod
    def genera_lista(frase: str) -> str:
        """Regola per lista."""
        numeri = estrai_numeri(frase)
        if numeri:
            return f'lista = {numeri}\nprint(lista)'
        return 'lista = []\nprint(lista)'
    
    @staticmethod
    def genera_dizionario(frase: str) -> str:
        """Regola per dizionario."""
        return 'dati = {"nome": "Mario", "età": 30}\nprint(dati)'
    
    @staticmethod
    def genera_def(frase: str) -> str:
        """Regola per definizione funzione."""
        return 'def saluto():\n    print("Ciao da Pythonita!")\n    return "Hello"'
    
    @staticmethod
    def genera_return(frase: str) -> str:
        """Regola per return."""
        return 'def somma(a, b):\n    return a + b\n\nrisultato = somma(5, 3)\nprint(risultato)'
    
    @staticmethod
    def genera_import(frase: str) -> str:
        """Regola per import."""
        parole = estrai_stringhe(frase)
        if parole:
            righe = [f'import {lib}' for lib in parole if lib.isalpha()]
            return "\n".join(righe) if righe else "import math"
        return "import math"
    
    @staticmethod
    def genera_open(frase: str) -> str:
        """Regola per open file."""
        parole = frase.split()
        nome_file = next((p for p in parole if p.endswith((".txt", ".csv", ".json", ".py"))), "file.txt")
        
        if "scrivi" in frase or "salva" in frase:
            return f'with open("{nome_file}", "w", encoding="utf-8") as f:\n    f.write("Contenuto di esempio")\nprint("File salvato!")'
        else:
            return f'with open("{nome_file}", "r", encoding="utf-8") as f:\n    contenuto = f.read()\n    print(contenuto)'
    
    @staticmethod
    def genera_len(frase: str) -> str:
        """Regola per len."""
        return 'lista = [1, 2, 3, 4, 5]\nprint("Lunghezza:", len(lista))'
    
    @staticmethod
    def genera_range(frase: str) -> str:
        """Regola per range."""
        numeri = estrai_numeri(frase)
        if len(numeri) >= 2:
            return f'for i in range({numeri[0]}, {numeri[1]} + 1):\n    print(i)'
        return 'for i in range(1, 11):\n    print(i)'
    
    @staticmethod
    def genera_append(frase: str) -> str:
        """Regola per append."""
        return 'lista = [1, 2, 3]\nlista.append(4)\nprint(lista)'
    
    @staticmethod
    def genera_remove(frase: str) -> str:
        """Regola per remove."""
        return 'lista = ["a", "b", "c"]\nlista.remove("b")\nprint(lista)'
    
    @staticmethod
    def genera_sum(frase: str) -> str:
        """Regola per sum."""
        numeri = estrai_numeri(frase)
        if numeri:
            return f'numeri = {numeri}\nprint("Somma:", sum(numeri))'
        return 'numeri = [1, 2, 3, 4, 5]\nprint("Somma:", sum(numeri))'
    
    @staticmethod
    def genera_max(frase: str) -> str:
        """Regola per max."""
        numeri = estrai_numeri(frase)
        if numeri:
            return f'valori = {numeri}\nprint("Massimo:", max(valori))'
        return 'valori = [10, 20, 5, 15]\nprint("Massimo:", max(valori))'
    
    @staticmethod
    def genera_min(frase: str) -> str:
        """Regola per min."""
        numeri = estrai_numeri(frase)
        if numeri:
            return f'valori = {numeri}\nprint("Minimo:", min(valori))'
        return 'valori = [10, 20, 5, 15]\nprint("Minimo:", min(valori))'
    
    @staticmethod
    def genera_sorted(frase: str) -> str:
        """Regola per sorted."""
        return 'lista = [3, 1, 4, 1, 5, 9, 2]\nprint("Ordinata:", sorted(lista))'
    
    @staticmethod
    def genera_type(frase: str) -> str:
        """Regola per type."""
        return 'x = 42\nprint("Tipo di x:", type(x))'
    
    @staticmethod
    def genera_try(frase: str) -> str:
        """Regola per try-except."""
        return 'try:\n    x = 1 / 0\nexcept ZeroDivisionError:\n    print("Errore: divisione per zero")'
    
    # ==================== NUOVI COMANDI ====================
    
    @staticmethod
    def genera_enumerate(frase: str) -> str:
        """Regola per enumerate."""
        return 'lista = ["a", "b", "c"]\nfor indice, valore in enumerate(lista):\n    print(f"{indice}: {valore}")'
    
    @staticmethod
    def genera_zip(frase: str) -> str:
        """Regola per zip."""
        return 'nomi = ["Mario", "Luigi", "Peach"]\netà = [25, 27, 24]\nfor nome, età in zip(nomi, età):\n    print(f"{nome}: {età} anni")'
    
    @staticmethod
    def genera_map(frase: str) -> str:
        """Regola per map."""
        return 'numeri = [1, 2, 3, 4, 5]\nquadrati = list(map(lambda x: x**2, numeri))\nprint(quadrati)'
    
    @staticmethod
    def genera_filter(frase: str) -> str:
        """Regola per filter."""
        return 'numeri = [1, 2, 3, 4, 5, 6]\npari = list(filter(lambda x: x % 2 == 0, numeri))\nprint("Numeri pari:", pari)'
    
    @staticmethod
    def genera_lambda(frase: str) -> str:
        """Regola per lambda."""
        return 'quadrato = lambda x: x**2\nprint(quadrato(5))'
    
    @staticmethod
    def genera_class(frase: str) -> str:
        """Regola per class."""
        return 'class Persona:\n    def __init__(self, nome):\n        self.nome = nome\n    \n    def saluta(self):\n        print(f"Ciao, sono {self.nome}")\n\np = Persona("Mario")\np.saluta()'
    
    @staticmethod
    def genera_upper(frase: str) -> str:
        """Regola per upper."""
        return 'testo = "ciao mondo"\nprint(testo.upper())'
    
    @staticmethod
    def genera_lower(frase: str) -> str:
        """Regola per lower."""
        return 'testo = "CIAO MONDO"\nprint(testo.lower())'
    
    @staticmethod
    def genera_split(frase: str) -> str:
        """Regola per split."""
        return 'testo = "uno,due,tre"\nparole = testo.split(",")\nprint(parole)'
    
    @staticmethod
    def genera_join(frase: str) -> str:
        """Regola per join."""
        return 'parole = ["Ciao", "mondo", "Python"]\nfrase = " ".join(parole)\nprint(frase)'
    
    @staticmethod
    def genera_replace(frase: str) -> str:
        """Regola per replace."""
        return 'testo = "Ciao mondo"\nnuovo = testo.replace("mondo", "Python")\nprint(nuovo)'
    
    @staticmethod
    def genera_tuple(frase: str) -> str:
        """Regola per tuple."""
        numeri = estrai_numeri(frase)
        if numeri:
            return f'tupla = ({", ".join(map(str, numeri))})\nprint(tupla)'
        return 'tupla = (1, 2, 3)\nprint(tupla)'
    
    @staticmethod
    def genera_set(frase: str) -> str:
        """Regola per set."""
        numeri = estrai_numeri(frase)
        if numeri:
            return f'insieme = {{{", ".join(map(str, numeri))}}}\nprint(insieme)'
        return 'insieme = {1, 2, 3, 2, 1}  # Rimuove duplicati\nprint(insieme)'
    
    @staticmethod
    def genera_abs(frase: str) -> str:
        """Regola per abs."""
        numeri = estrai_numeri(frase)
        num = numeri[0] if numeri else -10
        return f'valore = {num}\nprint("Valore assoluto:", abs(valore))'
    
    @staticmethod
    def genera_round(frase: str) -> str:
        """Regola per round."""
        return 'numero = 3.14159\nprint("Arrotondato:", round(numero, 2))'
    
    @staticmethod
    def genera_reversed(frase: str) -> str:
        """Regola per reversed."""
        return 'lista = [1, 2, 3, 4, 5]\ninvertita = list(reversed(lista))\nprint(invertita)'
    
    @staticmethod
    def genera_all(frase: str) -> str:
        """Regola per all."""
        return 'valori = [True, True, False]\nprint("Tutti veri?", all(valori))'
    
    @staticmethod
    def genera_any(frase: str) -> str:
        """Regola per any."""
        return 'valori = [False, False, True]\nprint("Almeno uno vero?", any(valori))'
    
    @staticmethod
    def genera_isinstance(frase: str) -> str:
        """Regola per isinstance."""
        return 'x = 42\nprint("È un intero?", isinstance(x, int))'
    
    @staticmethod
    def genera_break(frase: str) -> str:
        """Regola per break."""
        return 'for i in range(10):\n    if i == 5:\n        break\n    print(i)'
    
    @staticmethod
    def genera_continue(frase: str) -> str:
        """Regola per continue."""
        return 'for i in range(10):\n    if i % 2 == 0:\n        continue\n    print(i)  # Solo dispari'
    
    @staticmethod
    def genera_elif(frase: str) -> str:
        """Regola per elif."""
        return 'x = 10\nif x < 5:\n    print("Minore di 5")\nelif x < 15:\n    print("Tra 5 e 15")\nelse:\n    print("Maggiore di 15")'
    
    @staticmethod
    def genera_with(frase: str) -> str:
        """Regola per with."""
        return 'with open("file.txt", "r") as f:\n    contenuto = f.read()\n    print(contenuto)'
    
    @staticmethod
    def genera_raise(frase: str) -> str:
        """Regola per raise."""
        return 'def controlla_età(età):\n    if età < 0:\n        raise ValueError("Età non può essere negativa")\n    return età'
    
    @staticmethod
    def genera_assert(frase: str) -> str:
        """Regola per assert."""
        return 'x = 5\nassert x > 0, "x deve essere positivo"\nprint("OK")'
    
    @staticmethod
    def genera_comprehension(frase: str) -> str:
        """Regola per list comprehension."""
        if "quadrati" in frase:
            return 'quadrati = [x**2 for x in range(10)]\nprint(quadrati)'
        elif "pari" in frase:
            return 'pari = [x for x in range(20) if x % 2 == 0]\nprint(pari)'
        return 'lista = [x * 2 for x in range(5)]\nprint(lista)'
    
    @staticmethod
    def genera_dict_comprehension(frase: str) -> str:
        """Regola per dict comprehension."""
        return 'quadrati = {x: x**2 for x in range(5)}\nprint(quadrati)'
    
    # ==================== MODULI STANDARD LIBRARY ====================
    
    @staticmethod
    def genera_import_math(frase: str) -> str:
        """Regola per import math."""
        if "radice" in frase or "sqrt" in frase:
            return 'import math\nrisultato = math.sqrt(16)\nprint("Radice quadrata:", risultato)'
        elif "pi" in frase or "pigreco" in frase:
            return 'import math\nprint("Pi greco:", math.pi)'
        return 'import math\nprint("Seno di 90°:", math.sin(math.radians(90)))'
    
    @staticmethod
    def genera_import_random(frase: str) -> str:
        """Regola per import random."""
        if "scelta" in frase or "choice" in frase:
            return 'import random\nlista = ["rosso", "verde", "blu"]\nscelta = random.choice(lista)\nprint("Scelto:", scelta)'
        elif "shuffle" in frase or "mescola" in frase:
            return 'import random\nlista = [1, 2, 3, 4, 5]\nrandom.shuffle(lista)\nprint("Mescolata:", lista)'
        return 'import random\nnumero = random.randint(1, 100)\nprint("Numero casuale:", numero)'
    
    @staticmethod
    def genera_import_datetime(frase: str) -> str:
        """Regola per import datetime."""
        return 'from datetime import datetime\noggi = datetime.now()\nprint("Data e ora:", oggi.strftime("%d/%m/%Y %H:%M:%S"))'
    
    @staticmethod
    def genera_import_json(frase: str) -> str:
        """Regola per import json."""
        if "carica" in frase or "leggi" in frase:
            return 'import json\nwith open("dati.json", "r") as f:\n    dati = json.load(f)\n    print(dati)'
        return 'import json\ndati = {"nome": "Mario", "età": 30}\njson_str = json.dumps(dati, indent=2)\nprint(json_str)'
    
    @staticmethod
    def genera_import_csv(frase: str) -> str:
        """Regola per import csv."""
        return 'import csv\nwith open("dati.csv", "r") as f:\n    reader = csv.reader(f)\n    for riga in reader:\n        print(riga)'
    
    @staticmethod
    def genera_import_os(frase: str) -> str:
        """Regola per import os."""
        if "lista" in frase or "directory" in frase:
            return 'import os\nfile = os.listdir(".")\nprint("File:", file)'
        return 'import os\nprint("Directory corrente:", os.getcwd())'
    
    @staticmethod
    def genera_import_sys(frase: str) -> str:
        """Regola per import sys."""
        return 'import sys\nprint("Versione Python:", sys.version)\nprint("Argomenti:", sys.argv)'
    
    @staticmethod
    def genera_import_re(frase: str) -> str:
        """Regola per import re (regex)."""
        return 'import re\ntesto = "Il mio numero è 12345"\nnumeri = re.findall(r"\\d+", testo)\nprint("Numeri trovati:", numeri)'


# Mappa comando → funzione generatrice
REGOLE_GENERAZIONE = {
    "print": RegoleComandi.genera_print,
    "input": RegoleComandi.genera_input,
    "+": RegoleComandi.genera_somma,
    "-": RegoleComandi.genera_sottrazione,
    "*": RegoleComandi.genera_moltiplicazione,
    "/": RegoleComandi.genera_divisione,
    "if": RegoleComandi.genera_if,
    "for": RegoleComandi.genera_for,
    "while": RegoleComandi.genera_while,
    "list": RegoleComandi.genera_lista,
    "dict": RegoleComandi.genera_dizionario,
    "def": RegoleComandi.genera_def,
    "return": RegoleComandi.genera_return,
    "import": RegoleComandi.genera_import,
    "open": RegoleComandi.genera_open,
    "len": RegoleComandi.genera_len,
    "range": RegoleComandi.genera_range,
    "append": RegoleComandi.genera_append,
    "remove": RegoleComandi.genera_remove,
    "sum": RegoleComandi.genera_sum,
    "max": RegoleComandi.genera_max,
    "min": RegoleComandi.genera_min,
    "sorted": RegoleComandi.genera_sorted,
    "type": RegoleComandi.genera_type,
    "try": RegoleComandi.genera_try,
    "enumerate": RegoleComandi.genera_enumerate,
    "zip": RegoleComandi.genera_zip,
    "map": RegoleComandi.genera_map,
    "filter": RegoleComandi.genera_filter,
    "lambda": RegoleComandi.genera_lambda,
    "class": RegoleComandi.genera_class,
    "upper": RegoleComandi.genera_upper,
    "lower": RegoleComandi.genera_lower,
    "split": RegoleComandi.genera_split,
    "join": RegoleComandi.genera_join,
    "replace": RegoleComandi.genera_replace,
    "tuple": RegoleComandi.genera_tuple,
    "set": RegoleComandi.genera_set,
    "abs": RegoleComandi.genera_abs,
    "round": RegoleComandi.genera_round,
    "reversed": RegoleComandi.genera_reversed,
    "all": RegoleComandi.genera_all,
    "any": RegoleComandi.genera_any,
    "isinstance": RegoleComandi.genera_isinstance,
    "break": RegoleComandi.genera_break,
    "continue": RegoleComandi.genera_continue,
    "elif": RegoleComandi.genera_elif,
    "with": RegoleComandi.genera_with,
    "raise": RegoleComandi.genera_raise,
    "assert": RegoleComandi.genera_assert,
    "comprehension": RegoleComandi.genera_comprehension,
    "dict_comprehension": RegoleComandi.genera_dict_comprehension,
    
    # Moduli
    "math": RegoleComandi.genera_import_math,
    "random": RegoleComandi.genera_import_random,
    "datetime": RegoleComandi.genera_import_datetime,
    "json": RegoleComandi.genera_import_json,
    "csv": RegoleComandi.genera_import_csv,
    "os": RegoleComandi.genera_import_os,
    "sys": RegoleComandi.genera_import_sys,
    "re": RegoleComandi.genera_import_re,
}

