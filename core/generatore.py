"""
Generatore di codice Python con architettura ibrida:
- AI locale (Llama3.2 via Ollama) come metodo principale
- Sistema a regole come fallback
- Matching semantico per comandi semplici
"""

import json
import logging
from typing import Optional, Dict
from pathlib import Path


class GeneratoreCodice:
    """Generatore ibrido di codice Python da frasi italiane."""
    
    def __init__(self, use_ai=True, use_fallback=True, use_cache=True):
        """
        Inizializza il generatore.
        
        Args:
            use_ai: usa AI locale se disponibile
            use_fallback: usa sistema a regole come fallback
            use_cache: usa cache per query ripetute
        """
        self.use_ai = use_ai
        self.use_fallback = use_fallback
        self.use_cache = use_cache
        self.ai_disponibile = False
        self.mappa_comandi = self._carica_mappa_comandi()
        
        # Configura logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Inizializza cache se richiesto
        if use_cache:
            from .cache import get_cache
            self.cache = get_cache()
        else:
            self.cache = None
        
        # Inizializza AI se richiesto
        if use_ai:
            self._inizializza_ai()
    
    def _inizializza_ai(self):
        """Inizializza connessione a Ollama."""
        try:
            import ollama
            # Test di connessione
            ollama.list()
            self.ai_disponibile = True
            self.logger.info("✅ AI locale (Ollama) disponibile")
        except Exception as e:
            self.logger.warning(f"⚠️  AI locale non disponibile: {e}")
            self.ai_disponibile = False
    
    def _carica_mappa_comandi(self) -> Dict:
        """Carica la mappa dei comandi Python."""
        mappa_default = {
            "print": ["stampa", "mostra", "visualizza", "scrivi", "esponi"],
            "input": ["chiedi", "inserisci", "digita", "domanda", "ricevi"],
            "open": ["apri", "leggi", "scrivi", "salva", "carica", "esporta"],
            "def": ["funzione", "definisci", "crea", "costruisci", "dichiara"],
            "if": ["se", "condizione", "verifica", "controlla", "valuta"],
            "for": ["ciclo", "ripeti", "scorri", "itera", "ripassa"],
            "while": ["finché", "continua", "ripeti", "ciclo"],
            "list": ["lista", "metti", "raccogli", "elementi", "numeri"],
            "dict": ["dizionario", "mappa", "coppie", "chiavi", "valori"],
            "+": ["somma", "aggiungi", "più", "totale"],
            "-": ["sottrai", "togli", "meno", "differenza"],
            "*": ["moltiplica", "per", "prodotto"],
            "/": ["dividi", "fraziona", "separa"],
            "import": ["importa", "usa", "carica", "aggiungi"],
            "return": ["restituisci", "torna", "rispondi", "dai"],
            "len": ["lunghezza", "conta", "quantità", "misura"],
            "range": ["intervallo", "da a", "sequenza", "numeri"],
            "append": ["aggiungi", "metti", "inserisci", "unisci"],
            "remove": ["togli", "elimina", "cancella", "rimuovi"],
            "sum": ["somma", "totale", "aggiungi", "calcola"],
            "max": ["massimo", "più alto", "valore massimo"],
            "min": ["minimo", "più basso", "valore minimo"],
            "sorted": ["ordina", "organizza", "sistema", "metti in ordine"],
            "type": ["tipo", "classe", "categoria", "natura"],
            "try": ["prova", "tenta", "gestisci", "verifica"],
            "except": ["errore", "cattura", "proteggi", "gestione errore"]
        }
        
        return mappa_default
    
    def genera(self, frase: str) -> str:
        """
        Genera codice Python da una frase italiana.
        
        Strategia:
        0. Controlla cache (se abilitata)
        1. Prova con AI locale
        2. Se fallisce o non disponibile, usa sistema a regole
        3. Se anche quello fallisce, ritorna messaggio di errore
        
        Args:
            frase: frase in italiano
            
        Returns:
            codice Python generato
        """
        frase = frase.strip()
        
        if not frase:
            return "# Errore: frase vuota"
        
        # Strategia 0: Controlla cache
        if self.use_cache and self.cache:
            cached = self.cache.get(frase)
            if cached:
                self.logger.info("✅ Codice recuperato da cache")
                return cached
        
        # Strategia 1: AI locale
        if self.use_ai and self.ai_disponibile:
            codice = self._genera_con_ai(frase)
            if codice and not codice.startswith("# Errore"):
                self.logger.info("✅ Codice generato con AI")
                # Salva in cache
                if self.use_cache and self.cache:
                    self.cache.set(frase, codice)
                return codice
        
        # Strategia 2: Sistema a regole
        if self.use_fallback:
            codice = self._genera_con_regole(frase)
            if codice and not codice.startswith("# Comando non riconosciuto"):
                self.logger.info("✅ Codice generato con regole")
                # Salva in cache
                if self.use_cache and self.cache:
                    self.cache.set(frase, codice)
                return codice
        
        # Strategia 3: Fallback finale
        return self._genera_errore(frase)
    
    def _genera_con_ai(self, frase: str) -> Optional[str]:
        """Genera codice usando AI locale."""
        try:
            import ollama
            
            prompt = f"""Genera solo codice Python per questa richiesta in italiano: "{frase}"

Regole:
- Scrivi SOLO codice Python, senza spiegazioni
- Non aggiungere commenti tipo "# Codice generato..."
- Non usare markdown o ``` 
- Codice pulito e funzionante
- Se è una richiesta semplice, genera codice semplice

Codice Python:"""
            
            risposta = ollama.chat(
                model='llama3.2',
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            codice = risposta['message']['content'].strip()
            
            # Pulizia output AI
            codice = self._pulisci_output_ai(codice)
            
            return codice
            
        except Exception as e:
            self.logger.error(f"Errore AI: {e}")
            return None
    
    def _pulisci_output_ai(self, codice: str) -> str:
        """Pulisce l'output dell'AI rimuovendo markdown e commenti inutili."""
        # Rimuovi blocchi markdown
        if "```python" in codice:
            codice = codice.split("```python")[1].split("```")[0]
        elif "```" in codice:
            codice = codice.split("```")[1].split("```")[0]
        
        # Rimuovi commenti generati dall'AI all'inizio
        linee = codice.strip().split("\n")
        linee_pulite = []
        
        for linea in linee:
            # Salta commenti generici
            if linea.strip().startswith("# Codice generato"):
                continue
            if linea.strip().startswith("# Output:"):
                continue
            linee_pulite.append(linea)
        
        return "\n".join(linee_pulite).strip()
    
    def _genera_con_regole(self, frase: str) -> str:
        """Genera codice usando sistema a regole."""
        frase_lower = frase.lower()
        
        # Identifica il comando
        comando = self._identifica_comando(frase_lower)
        
        if not comando:
            return "# Comando non riconosciuto"
        
        # Genera codice basato sul comando
        return self._applica_regola(comando, frase)
    
    def _identifica_comando(self, frase: str) -> Optional[str]:
        """Identifica il comando Python dalla frase."""
        parole = frase.split()
        
        for comando, sinonimi in self.mappa_comandi.items():
            if any(parola in sinonimi or parola == comando for parola in parole):
                return comando
        
        return None
    
    def _applica_regola(self, comando: str, frase: str) -> str:
        """Applica la regola per generare codice."""
        frase = frase.lower().strip()
        
        # Import delle regole dal vecchio translator.py
        if comando == "print":
            contenuto = frase.split(" ", 1)[-1]
            return f'print("{contenuto}")'
        
        elif comando == "input":
            return 'risposta = input("Inserisci un valore: ")\nprint("Hai scritto:", risposta)'
        
        elif comando == "open":
            parole = frase.split()
            nome_file = next((p for p in parole if p.endswith((".txt", ".csv", ".json"))), "file.txt")
            if "scrivi" in frase or "salva" in frase:
                return f'with open("{nome_file}", "w", encoding="utf-8") as f:\n    f.write("Contenuto di esempio")'
            else:
                return f'with open("{nome_file}", "r", encoding="utf-8") as f:\n    contenuto = f.read()\n    print(contenuto)'
        
        elif comando == "def":
            return 'def saluto():\n    print("Ciao da Pythonita!")'
        
        elif comando == "if":
            return 'x = 10\nif x > 5:\n    print("x è maggiore di 5")'
        
        elif comando == "for":
            return 'for i in range(5):\n    print("Iterazione", i)'
        
        elif comando == "while":
            return 'x = 0\nwhile x < 5:\n    print("x =", x)\n    x += 1'
        
        elif comando == "list":
            numeri = [int(s) for s in frase.split() if s.isdigit()]
            return f'lista = {numeri}\nprint(lista)'
        
        elif comando == "dict":
            return 'dati = {"nome": "Alessio", "età": 30}\nprint(dati)'
        
        elif comando == "+":
            numeri = [int(s) for s in frase.split() if s.isdigit()]
            if len(numeri) >= 2:
                return f'print({numeri[0]} + {numeri[1]})'
            return "# Errore: servono almeno due numeri"
        
        elif comando == "-":
            numeri = [int(s) for s in frase.split() if s.isdigit()]
            if len(numeri) >= 2:
                return f'print({numeri[0]} - {numeri[1]})'
            return "# Errore: servono almeno due numeri"
        
        elif comando == "*":
            numeri = [int(s) for s in frase.split() if s.isdigit()]
            if len(numeri) >= 2:
                return f'print({numeri[0]} * {numeri[1]})'
            return "# Errore: servono almeno due numeri"
        
        elif comando == "/":
            numeri = [int(s) for s in frase.split() if s.isdigit()]
            if len(numeri) >= 2 and numeri[1] != 0:
                return f'print({numeri[0]} / {numeri[1]})'
            return "# Errore: divisione non valida"
        
        elif comando == "import":
            librerie = [s for s in frase.split() if s.isalpha() and s not in ["importa", "usa", "carica", "aggiungi"]]
            righe = [f'import {lib}' for lib in librerie]
            return "\n".join(righe) if righe else "# Nessuna libreria specificata"
        
        elif comando == "return":
            return 'def somma(a, b):\n    return a + b'
        
        elif comando == "len":
            return 'lista = [1, 2, 3, 4]\nprint("Lunghezza:", len(lista))'
        
        elif comando == "range":
            return 'for i in range(1, 6):\n    print(i)'
        
        elif comando == "append":
            return 'lista = []\nlista.append("elemento")\nprint(lista)'
        
        elif comando == "remove":
            return 'lista = ["a", "b", "c"]\nlista.remove("b")\nprint(lista)'
        
        elif comando == "sum":
            return 'numeri = [1, 2, 3]\nprint("Somma:", sum(numeri))'
        
        elif comando == "max":
            return 'valori = [10, 20, 5]\nprint("Massimo:", max(valori))'
        
        elif comando == "min":
            return 'valori = [10, 20, 5]\nprint("Minimo:", min(valori))'
        
        elif comando == "sorted":
            return 'lista = [3, 1, 2]\nprint("Ordinata:", sorted(lista))'
        
        elif comando == "type":
            return 'x = 42\nprint("Tipo:", type(x))'
        
        elif comando == "try":
            return 'try:\n    x = 1 / 0\nexcept ZeroDivisionError:\n    print("Errore: divisione per zero")'
        
        elif comando == "except":
            return 'try:\n    int("ciao")\nexcept ValueError:\n    print("Errore di conversione")'
        
        return "# Comando non riconosciuto"
    
    def _genera_errore(self, frase: str) -> str:
        """Genera messaggio di errore."""
        return f'''# ⚠️  Non sono riuscito a generare codice per: "{frase}"
# 
# Suggerimenti:
# - Prova a riformulare la frase in modo più semplice
# - Usa verbi come: stampa, crea, somma, apri, ecc.
# - Esempio: "stampa ciao mondo"
'''


# Istanza globale per uso rapido
_generatore: Optional[GeneratoreCodice] = None


def get_generatore() -> GeneratoreCodice:
    """Ottieni l'istanza globale del generatore."""
    global _generatore
    if _generatore is None:
        _generatore = GeneratoreCodice()
    return _generatore


def genera_codice(frase: str) -> str:
    """
    Funzione helper per generazione rapida.
    
    Args:
        frase: frase in italiano
        
    Returns:
        codice Python
    """
    return get_generatore().genera(frase)

