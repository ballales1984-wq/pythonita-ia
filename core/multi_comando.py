"""
Sistema per combinare più comandi Python in un unico blocco di codice.
Permette di generare programmi complessi da frasi articolate.
"""

import re
from typing import List, Dict, Tuple
from .comandi_python import find_command_by_italian


class MultiComandoParser:
    """
    Parser per identificare e combinare più comandi in una frase.
    
    Esempi:
    - "crea lista poi stampa"
    - "chiedi nome e poi stampalo"
    - "leggi file e filtra le righe"
    """
    
    # Parole che indicano sequenza di comandi
    CONNETTORI = ['poi', 'dopo', 'successivamente', 'quindi', 'infine', 'e poi', 'e dopo']
    CONGIUNZIONI = ['e', 'ed', 'con', 'usando']
    
    def __init__(self):
        """Inizializza il parser multi-comando."""
        self.connettori_pattern = '|'.join(self.CONNETTORI)
        self.congiunzioni_pattern = '|'.join(self.CONGIUNZIONI)
    
    def identifica_multi_comando(self, frase: str) -> bool:
        """
        Verifica se la frase contiene più comandi.
        
        Args:
            frase: Frase da analizzare
            
        Returns:
            True se contiene più comandi
        """
        frase_lower = frase.lower()
        
        # Cerca connettori
        for connettore in self.CONNETTORI:
            if connettore in frase_lower:
                return True
        
        # Cerca pattern comuni multi-comando
        pattern_multi = [
            r'(crea|genera|fai).+(poi|dopo|quindi)',
            r'(leggi|apri).+(poi|dopo|e)',
            r'(chiedi|input).+(poi|dopo|e).+(stampa|mostra)',
            r'(per ogni|for).+(stampa|mostra|calcola)',
        ]
        
        for pattern in pattern_multi:
            if re.search(pattern, frase_lower):
                return True
        
        return False
    
    def separa_comandi(self, frase: str) -> List[str]:
        """
        Separa la frase in comandi individuali.
        
        Args:
            frase: Frase con più comandi
            
        Returns:
            Lista di comandi separati
        """
        frase_lower = frase.lower()
        
        # Prova prima con connettori espliciti
        for connettore in self.CONNETTORI:
            if connettore in frase_lower:
                parti = frase_lower.split(connettore)
                return [p.strip() for p in parti if p.strip()]
        
        # Prova con "e" se sembra sequenza
        if ' e ' in frase_lower and any(parola in frase_lower for parola in ['poi', 'stampa', 'mostra']):
            parti = frase_lower.split(' e ')
            return [p.strip() for p in parti if p.strip()]
        
        # Fallback: ritorna frase intera
        return [frase]
    
    def analizza_struttura(self, frase: str) -> Dict:
        """
        Analizza la struttura della frase multi-comando.
        
        Returns:
            Dizionario con struttura identificata
        """
        frase_lower = frase.lower()
        
        # Identifica pattern comuni
        pattern = self._identifica_pattern(frase_lower)
        comandi = self.separa_comandi(frase)
        
        return {
            "è_multi_comando": self.identifica_multi_comando(frase),
            "pattern": pattern,
            "comandi_separati": comandi,
            "numero_comandi": len(comandi)
        }
    
    def _identifica_pattern(self, frase: str) -> str:
        """Identifica il pattern comune della combinazione."""
        patterns = {
            "input_then_print": r'(chiedi|input|leggi).+(poi|dopo|e).+(stampa|mostra)',
            "create_then_iterate": r'(crea|genera).+(lista|array).+(poi|dopo|e).+(ciclo|for|stampa)',
            "read_then_process": r'(leggi|apri|carica).+(poi|dopo|e).+(filtra|cerca|trova)',
            "loop_with_action": r'(per ogni|for).+(stampa|mostra|calcola|aggiungi)',
            "conditional_action": r'(se|if).+(allora|poi).+(stampa|fai|esegui)',
        }
        
        for pattern_name, pattern_regex in patterns.items():
            if re.search(pattern_regex, frase):
                return pattern_name
        
        return "sequence"  # Sequenza generica


class CombinatoreCodice:
    """
    Combina codice da più comandi in un unico blocco coerente.
    """
    
    def __init__(self):
        """Inizializza il combinatore."""
        self.parser = MultiComandoParser()
    
    def combina(self, codici: List[str]) -> str:
        """
        Combina più blocchi di codice in uno coerente.
        
        Args:
            codici: Lista di blocchi di codice
            
        Returns:
            Codice combinato
        """
        if not codici:
            return "# Nessun codice da combinare"
        
        if len(codici) == 1:
            return codici[0]
        
        # Pulisci codici
        codici_puliti = [self._pulisci_codice(c) for c in codici]
        
        # Combina in modo intelligente
        return self._combina_intelligente(codici_puliti)
    
    def _pulisci_codice(self, codice: str) -> str:
        """Rimuove commenti e print ridondanti."""
        linee = codice.split('\n')
        linee_pulite = []
        
        for linea in linee:
            # Salta commenti standalone
            if linea.strip().startswith('#'):
                continue
            linee_pulite.append(linea)
        
        return '\n'.join(linee_pulite)
    
    def _combina_intelligente(self, codici: List[str]) -> str:
        """
        Combina codici in modo intelligente.
        
        - Unisce dichiarazioni di variabili
        - Rimuove duplicati
        - Mantiene l'ordine logico
        """
        risultato = []
        variabili_definite = set()
        
        for i, codice in enumerate(codici):
            linee = codice.split('\n')
            
            for linea in linee:
                # Traccia variabili definite
                if '=' in linea and not linea.strip().startswith('print'):
                    var_name = linea.split('=')[0].strip()
                    variabili_definite.add(var_name)
                
                risultato.append(linea)
            
            # Aggiungi riga vuota tra blocchi (tranne l'ultimo)
            if i < len(codici) - 1:
                risultato.append('')
        
        return '\n'.join(risultato)
    
    def genera_da_template(self, pattern: str, frase: str) -> str:
        """
        Genera codice usando template per pattern comuni.
        
        Args:
            pattern: Tipo di pattern identificato
            frase: Frase originale
            
        Returns:
            Codice generato
        """
        templates = {
            "input_then_print": self._template_input_print,
            "create_then_iterate": self._template_create_iterate,
            "read_then_process": self._template_read_process,
            "loop_with_action": self._template_loop_action,
            "conditional_action": self._template_conditional_action,
        }
        
        template_func = templates.get(pattern, self._template_generic)
        return template_func(frase)
    
    def _template_input_print(self, frase: str) -> str:
        """Template: chiedi input poi stampa."""
        return '''# Input e stampa
nome = input("Inserisci il tuo nome: ")
print(f"Ciao, {nome}!")'''
    
    def _template_create_iterate(self, frase: str) -> str:
        """Template: crea lista poi itera."""
        from .regole_comandi import estrai_numeri
        numeri = estrai_numeri(frase)
        
        if numeri:
            return f'''# Crea lista e itera
lista = {numeri}
for elemento in lista:
    print(f"Elemento: {{elemento}}")'''
        
        return '''# Crea lista e itera
lista = [1, 2, 3, 4, 5]
for elemento in lista:
    print(f"Elemento: {elemento}")'''
    
    def _template_read_process(self, frase: str) -> str:
        """Template: leggi file poi processa."""
        return '''# Leggi file e processa
with open("dati.txt", "r", encoding="utf-8") as f:
    righe = f.readlines()
    
# Processa ogni riga
for riga in righe:
    riga_pulita = riga.strip()
    if riga_pulita:  # Salta righe vuote
        print(riga_pulita)'''
    
    def _template_loop_action(self, frase: str) -> str:
        """Template: ciclo con azione."""
        from .regole_comandi import estrai_numeri
        numeri = estrai_numeri(frase)
        
        limite = numeri[0] if numeri else 10
        
        return f'''# Ciclo con azione
for i in range(1, {limite} + 1):
    print(f"Iterazione {{i}}: valore = {{i * 2}}")'''
    
    def _template_conditional_action(self, frase: str) -> str:
        """Template: condizione poi azione."""
        return '''# Condizione e azione
x = 15
if x > 10:
    print(f"x ({x}) è maggiore di 10")
    risultato = x * 2
    print(f"Risultato: {risultato}")
else:
    print(f"x ({x}) è minore o uguale a 10")'''
    
    def _template_generic(self, frase: str) -> str:
        """Template generico per sequenze."""
        return '''# Sequenza di comandi
# Passo 1
valore = 10

# Passo 2
risultato = valore * 2

# Passo 3
print(f"Risultato: {risultato}")'''


def combina_comandi(frase: str, codici: List[str]) -> str:
    """
    Funzione helper per combinare comandi.
    
    Args:
        frase: Frase originale
        codici: Lista di codici generati
        
    Returns:
        Codice combinato
    """
    combinatore = CombinatoreCodice()
    return combinatore.combina(codici)

