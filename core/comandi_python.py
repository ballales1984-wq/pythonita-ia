"""
Mappatura completa italiano → comandi Python.
Supporta 100+ comandi Python built-in e standard library.
"""

# Mappa completa comandi Python con sinonimi italiani
COMANDI_PYTHON = {
    # ==================== I/O ====================
    "print": ["stampa", "mostra", "visualizza", "scrivi", "esponi", "output"],
    "input": ["chiedi", "inserisci", "digita", "domanda", "ricevi", "leggi"],
    
    # ==================== STRUTTURE DI CONTROLLO ====================
    "if": ["se", "condizione", "verifica", "controlla", "valuta"],
    "elif": ["altrimenti se", "else if", "sennò se"],
    "else": ["altrimenti", "diversamente", "sennò"],
    "for": ["ciclo", "ripeti", "scorri", "itera", "ripassa", "per ogni"],
    "while": ["finché", "continua", "mentre", "ciclo mentre"],
    "break": ["interrompi", "esci", "fermati", "stoppa"],
    "continue": ["prosegui", "continua", "salta", "vai avanti"],
    "pass": ["non fare nulla", "passa", "vuoto", "placeholder"],
    
    # ==================== FUNZIONI ====================
    "def": ["funzione", "definisci", "crea funzione", "costruisci", "dichiara"],
    "return": ["restituisci", "torna", "rispondi", "dai", "ritorna"],
    "lambda": ["funzione anonima", "lambda", "funzione inline"],
    "yield": ["produci", "genera", "yield"],
    
    # ==================== STRUTTURE DATI ====================
    "list": ["lista", "array", "sequenza", "elenco", "metti"],
    "dict": ["dizionario", "mappa", "coppie", "chiavi valori", "hash"],
    "tuple": ["tupla", "coppia", "terna", "immutabile"],
    "set": ["insieme", "set", "unici", "collezione"],
    "frozenset": ["insieme immutabile", "frozenset"],
    
    # ==================== OPERAZIONI LISTE/DICT ====================
    "append": ["aggiungi", "metti", "inserisci", "unisci"],
    "extend": ["estendi", "aggiungi lista", "concatena"],
    "insert": ["inserisci in posizione", "metti in"],
    "remove": ["togli", "elimina", "cancella", "rimuovi"],
    "pop": ["rimuovi ultimo", "estrai", "pop"],
    "clear": ["pulisci", "svuota", "cancella tutto"],
    "copy": ["copia", "duplica", "clona"],
    "sort": ["ordina", "organizza", "sistema"],
    "reverse": ["inverti", "ribalta", "rovescia"],
    "index": ["trova indice", "posizione di", "cerca"],
    "count": ["conta", "numero di", "quanti"],
    "get": ["ottieni", "prendi", "recupera"],
    "keys": ["chiavi", "keys"],
    "values": ["valori", "values"],
    "items": ["elementi", "items", "coppie"],
    "update": ["aggiorna", "unisci dizionario"],
    
    # ==================== OPERAZIONI MATEMATICHE ====================
    "+": ["somma", "aggiungi", "più", "totale", "addiziona"],
    "-": ["sottrai", "togli", "meno", "differenza"],
    "*": ["moltiplica", "per", "prodotto"],
    "/": ["dividi", "fraziona", "separa", "diviso"],
    "//": ["divisione intera", "dividi intero"],
    "%": ["modulo", "resto", "resto divisione"],
    "**": ["potenza", "elevato", "alla"],
    "abs": ["valore assoluto", "assoluto", "abs"],
    "round": ["arrotonda", "round"],
    "pow": ["potenza", "elevamento"],
    "divmod": ["divisione e resto", "divmod"],
    
    # ==================== FUNZIONI AGGREGATE ====================
    "sum": ["somma", "totale", "aggiungi tutti"],
    "max": ["massimo", "più alto", "valore massimo", "maggiore"],
    "min": ["minimo", "più basso", "valore minimo", "minore"],
    "len": ["lunghezza", "conta", "dimensione", "misura", "numero elementi"],
    "all": ["tutti veri", "all"],
    "any": ["almeno uno", "any", "qualcuno vero"],
    "sorted": ["ordina", "organizza", "sistema", "metti in ordine"],
    "reversed": ["invertito", "reversed", "al contrario"],
    
    # ==================== CONVERSIONI TIPO ====================
    "int": ["intero", "converti intero", "numero intero"],
    "float": ["decimale", "float", "numero decimale"],
    "str": ["stringa", "testo", "converti stringa"],
    "bool": ["booleano", "vero falso", "bool"],
    "bytes": ["byte", "bytes"],
    "list": ["converti lista", "a lista"],
    "tuple": ["converti tupla", "a tupla"],
    "set": ["converti set", "a insieme"],
    "dict": ["converti dizionario", "a dizionario"],
    
    # ==================== FUNZIONI STRINGA ====================
    "upper": ["maiuscolo", "upper", "tutto maiuscolo"],
    "lower": ["minuscolo", "lower", "tutto minuscolo"],
    "capitalize": ["capitalizza", "prima lettera maiuscola"],
    "title": ["titolo", "title", "ogni parola maiuscola"],
    "strip": ["rimuovi spazi", "strip", "trim"],
    "lstrip": ["rimuovi spazi sinistra", "lstrip"],
    "rstrip": ["rimuovi spazi destra", "rstrip"],
    "split": ["dividi", "split", "separa"],
    "join": ["unisci", "join", "concatena con"],
    "replace": ["sostituisci", "replace", "rimpiazza"],
    "find": ["trova", "cerca", "find"],
    "startswith": ["inizia con", "comincia con"],
    "endswith": ["finisce con", "termina con"],
    
    # ==================== RANGE & ENUMERATE ====================
    "range": ["intervallo", "da a", "sequenza", "range"],
    "enumerate": ["enumera", "con indice", "enumerate"],
    "zip": ["accoppia", "zip", "combina"],
    "map": ["mappa", "applica funzione", "map"],
    "filter": ["filtra", "filter", "seleziona"],
    
    # ==================== FILE I/O ====================
    "open": ["apri", "apri file", "leggi file", "scrivi file"],
    "read": ["leggi", "read"],
    "write": ["scrivi", "write"],
    "close": ["chiudi", "close"],
    "readline": ["leggi riga", "readline"],
    "readlines": ["leggi righe", "readlines"],
    "writelines": ["scrivi righe", "writelines"],
    
    # ==================== IMPORT ====================
    "import": ["importa", "usa", "carica", "include"],
    "from": ["da", "from"],
    "as": ["come", "as", "rinomina"],
    
    # ==================== CLASSI & OOP ====================
    "class": ["classe", "class", "definisci classe"],
    "self": ["se stesso", "self"],
    "super": ["super", "genitore", "classe padre"],
    "__init__": ["costruttore", "inizializza", "init"],
    "property": ["proprietà", "property", "getter"],
    "@property": ["decoratore property", "getter"],
    "@staticmethod": ["metodo statico", "staticmethod"],
    "@classmethod": ["metodo classe", "classmethod"],
    
    # ==================== GESTIONE ERRORI ====================
    "try": ["prova", "tenta", "gestisci", "verifica"],
    "except": ["errore", "cattura", "proteggi", "gestione errore", "eccezione"],
    "finally": ["infine", "finally", "comunque"],
    "raise": ["lancia", "solleva", "raise", "genera errore"],
    "assert": ["asserisci", "verifica che", "assert"],
    
    # ==================== FUNZIONI BUILT-IN ====================
    "type": ["tipo", "classe", "typeof", "tipo di"],
    "isinstance": ["è istanza", "isinstance", "è di tipo"],
    "issubclass": ["è sottoclasse", "issubclass"],
    "id": ["id", "identificatore", "indirizzo"],
    "hash": ["hash", "hashcode"],
    "dir": ["directory", "attributi", "dir"],
    "help": ["aiuto", "help", "documentazione"],
    "vars": ["variabili", "vars"],
    "globals": ["globali", "globals"],
    "locals": ["locali", "locals"],
    
    # ==================== ITERATORI ====================
    "iter": ["iteratore", "iter"],
    "next": ["prossimo", "next", "successivo"],
    
    # ==================== VARIE ====================
    "del": ["elimina", "del", "cancella variabile"],
    "None": ["niente", "nulla", "vuoto", "null"],
    "True": ["vero", "true"],
    "False": ["falso", "false"],
    "and": ["e", "and"],
    "or": ["o", "or", "oppure"],
    "not": ["non", "not", "negazione"],
    "in": ["in", "dentro", "contenuto"],
    "is": ["è", "is", "identico"],
    "with": ["con", "with", "usando"],
    
    # ==================== COMPREHENSION ====================
    "list_comprehension": ["lista comprensione", "list comp"],
    "dict_comprehension": ["dict comprensione", "dict comp"],
    "set_comprehension": ["set comprensione", "set comp"],
    
    # ==================== MODULI STANDARD LIBRARY ====================
    "math": ["matematica", "math"],
    "random": ["casuale", "random", "aleatorio"],
    "datetime": ["data", "datetime", "tempo"],
    "time": ["tempo", "time", "ora"],
    "json": ["json", "javascript object"],
    "csv": ["csv", "comma separated"],
    "os": ["sistema operativo", "os", "file system"],
    "sys": ["sistema", "sys"],
    "re": ["regex", "espressione regolare", "pattern"],
    "pathlib": ["path", "percorso", "pathlib"],
    "collections": ["collezioni", "collections"],
    "itertools": ["strumenti iterazione", "itertools"],
    "functools": ["strumenti funzionali", "functools"],
    
    # ==================== AVANZATI ====================
    "async": ["asincrono", "async"],
    "await": ["attendi", "await"],
    "with": ["context manager", "with", "usando"],
    "decorator": ["decoratore", "decorator", "wrapper"],
    "generator": ["generatore", "generator"],
    "comprehension": ["comprensione", "comprehension"],
}


# Funzioni Python built-in complete (69 funzioni)
BUILTIN_FUNCTIONS = {
    # A-C
    "abs": "valore assoluto",
    "all": "tutti veri",
    "any": "almeno uno vero",
    "ascii": "rappresentazione ASCII",
    "bin": "binario",
    "bool": "booleano",
    "bytearray": "array di byte",
    "bytes": "byte",
    "callable": "è chiamabile",
    "chr": "carattere da codice",
    "classmethod": "metodo di classe",
    "compile": "compila codice",
    "complex": "numero complesso",
    
    # D-H
    "delattr": "elimina attributo",
    "dict": "dizionario",
    "dir": "directory attributi",
    "divmod": "divisione e modulo",
    "enumerate": "enumera",
    "eval": "valuta espressione",
    "exec": "esegui codice",
    "filter": "filtra",
    "float": "decimale",
    "format": "formatta",
    "frozenset": "insieme immutabile",
    "getattr": "ottieni attributo",
    "globals": "variabili globali",
    "hasattr": "ha attributo",
    "hash": "hash",
    "help": "aiuto",
    "hex": "esadecimale",
    
    # I-O
    "id": "identificatore",
    "input": "input utente",
    "int": "intero",
    "isinstance": "è istanza",
    "issubclass": "è sottoclasse",
    "iter": "iteratore",
    "len": "lunghezza",
    "list": "lista",
    "locals": "variabili locali",
    "map": "mappa",
    "max": "massimo",
    "memoryview": "vista memoria",
    "min": "minimo",
    "next": "prossimo",
    "object": "oggetto",
    "oct": "ottale",
    "open": "apri file",
    "ord": "codice carattere",
    
    # P-S
    "pow": "potenza",
    "print": "stampa",
    "property": "proprietà",
    "range": "intervallo",
    "repr": "rappresentazione",
    "reversed": "invertito",
    "round": "arrotonda",
    "set": "insieme",
    "setattr": "imposta attributo",
    "slice": "fetta",
    "sorted": "ordinato",
    "staticmethod": "metodo statico",
    "str": "stringa",
    "sum": "somma",
    "super": "super",
    
    # T-Z
    "tuple": "tupla",
    "type": "tipo",
    "vars": "variabili",
    "zip": "zip",
}


# Moduli standard library più comuni
STANDARD_LIBRARY = {
    # Matematica e numeri
    "math": ["matematica", "math", "calcoli"],
    "random": ["casuale", "random", "aleatorio", "randomico"],
    "decimal": ["decimale", "decimal", "precisione"],
    "fractions": ["frazioni", "fractions"],
    "statistics": ["statistiche", "statistics", "stats"],
    
    # Data e tempo
    "datetime": ["data tempo", "datetime", "data e ora"],
    "time": ["tempo", "time", "cronometro"],
    "calendar": ["calendario", "calendar"],
    
    # File e path
    "os": ["sistema", "os", "file system", "cartelle"],
    "os.path": ["percorso", "path", "os.path"],
    "pathlib": ["path moderno", "pathlib"],
    "shutil": ["utilità file", "shutil", "copia file"],
    "glob": ["glob", "pattern file"],
    "tempfile": ["file temporaneo", "tempfile"],
    
    # Dati e serializzazione
    "json": ["json", "javascript object"],
    "csv": ["csv", "comma separated"],
    "pickle": ["pickle", "serializza oggetto"],
    "xml": ["xml"],
    "configparser": ["config", "configurazione"],
    
    # Testo e pattern
    "re": ["regex", "espressione regolare", "pattern"],
    "string": ["stringhe", "string", "testo"],
    "textwrap": ["formatta testo", "textwrap"],
    "difflib": ["differenze", "diff"],
    
    # Collezioni
    "collections": ["collezioni", "collections"],
    "array": ["array", "vettore"],
    "heapq": ["heap", "coda priorità"],
    "bisect": ["bisect", "ricerca binaria"],
    
    # Iterazione
    "itertools": ["strumenti iterazione", "itertools"],
    "functools": ["strumenti funzionali", "functools"],
    "operator": ["operatori", "operator"],
    
    # Sistema
    "sys": ["sistema", "sys", "interprete"],
    "platform": ["piattaforma", "platform", "sistema operativo"],
    "subprocess": ["subprocess", "processo", "comando"],
    
    # Rete e internet
    "urllib": ["urllib", "url", "web"],
    "http": ["http", "client server"],
    "socket": ["socket", "rete"],
    "email": ["email", "posta"],
    
    # Compressione
    "zipfile": ["zip", "archivio zip"],
    "tarfile": ["tar", "archivio tar"],
    "gzip": ["gzip", "compressione"],
    
    # Testing
    "unittest": ["unittest", "test unitari"],
    "doctest": ["doctest", "test documentazione"],
    
    # Logging
    "logging": ["logging", "log", "registrazione"],
    
    # Argparse
    "argparse": ["argparse", "argomenti", "parametri riga comando"],
    
    # Copy
    "copy": ["copia", "deepcopy", "copia profonda"],
}


# Keywords Python
PYTHON_KEYWORDS = [
    "False", "None", "True", "and", "as", "assert", "async", "await",
    "break", "class", "continue", "def", "del", "elif", "else", "except",
    "finally", "for", "from", "global", "if", "import", "in", "is",
    "lambda", "nonlocal", "not", "or", "pass", "raise", "return",
    "try", "while", "with", "yield"
]


def get_all_commands():
    """Ritorna lista di tutti i comandi supportati."""
    return list(COMANDI_PYTHON.keys())


def get_all_builtins():
    """Ritorna lista di tutte le funzioni built-in."""
    return list(BUILTIN_FUNCTIONS.keys())


def get_all_modules():
    """Ritorna lista di tutti i moduli standard library."""
    return list(STANDARD_LIBRARY.keys())


def find_command_by_italian(parola_italiana: str) -> str:
    """
    Trova comando Python da parola italiana.
    
    Args:
        parola_italiana: Parola in italiano
        
    Returns:
        Comando Python o None se non trovato
    """
    parola = parola_italiana.lower().strip()
    
    # Cerca nei comandi
    for cmd, sinonimi in COMANDI_PYTHON.items():
        if parola in sinonimi or parola == cmd:
            return cmd
    
    # Cerca nei moduli
    for module, sinonimi in STANDARD_LIBRARY.items():
        if parola in sinonimi or parola == module:
            return module
    
    return None


def get_command_info(comando: str) -> dict:
    """
    Ottiene informazioni su un comando.
    
    Args:
        comando: Nome comando Python
        
    Returns:
        Dizionario con info sul comando
    """
    info = {
        "comando": comando,
        "sinonimi": COMANDI_PYTHON.get(comando, []),
        "categoria": _categorizza_comando(comando),
        "builtin": comando in BUILTIN_FUNCTIONS,
        "module": comando in STANDARD_LIBRARY,
    }
    
    return info


def _categorizza_comando(comando: str) -> str:
    """Categorizza il comando."""
    categorie = {
        "I/O": ["print", "input", "open", "read", "write"],
        "Controllo": ["if", "elif", "else", "for", "while", "break", "continue"],
        "Funzioni": ["def", "return", "lambda", "yield"],
        "Strutture Dati": ["list", "dict", "tuple", "set"],
        "Matematica": ["+", "-", "*", "/", "abs", "round", "sum", "max", "min"],
        "Stringhe": ["upper", "lower", "split", "join", "replace"],
        "Iterazione": ["range", "enumerate", "zip", "map", "filter"],
        "Tipo": ["int", "float", "str", "bool", "type"],
        "Gestione Errori": ["try", "except", "finally", "raise"],
    }
    
    for cat, comandi in categorie.items():
        if comando in comandi:
            return cat
    
    return "Altro"

