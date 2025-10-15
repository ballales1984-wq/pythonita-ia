"""
Parser unificato per l'analisi delle frasi in italiano.
Consolida la funzionalità di parsing da vari moduli.
"""

import spacy
from typing import Dict, List, Optional


class ParserItaliano:
    """Parser per frasi in italiano con supporto NLP."""
    
    def __init__(self, modello_spacy="it_core_news_sm"):
        """
        Inizializza il parser.
        
        Args:
            modello_spacy: nome del modello spaCy da caricare
        """
        try:
            self.nlp = spacy.load(modello_spacy)
        except OSError:
            print(f"⚠️  Modello spaCy '{modello_spacy}' non trovato.")
            print("   Installa con: python -m spacy download it_core_news_sm")
            self.nlp = None
    
    def analizza_completa(self, frase: str) -> Dict:
        """
        Analisi completa della frase con spaCy.
        
        Args:
            frase: frase da analizzare
            
        Returns:
            dizionario con tokens, lemmi, POS tags, ecc.
        """
        if not self.nlp:
            return self.analizza_semplice(frase)
        
        doc = self.nlp(frase)
        
        return {
            "testo": frase,
            "tokens": [token.text for token in doc],
            "lemmi": [token.lemma_ for token in doc],
            "pos_tags": [token.pos_ for token in doc],
            "parole_chiave": self._estrai_parole_chiave(doc),
            "verbi": [token.lemma_ for token in doc if token.pos_ == "VERB"],
            "sostantivi": [token.lemma_ for token in doc if token.pos_ == "NOUN"],
            "numeri": [token.text for token in doc if token.pos_ == "NUM" or token.like_num]
        }
    
    def analizza_semplice(self, frase: str) -> Dict:
        """
        Analisi semplice senza NLP (fallback).
        
        Args:
            frase: frase da analizzare
            
        Returns:
            dizionario base con parsing semplice
        """
        parole = frase.lower().strip().split()
        
        return {
            "testo": frase,
            "verbo": parole[0] if parole else "",
            "args": parole[1:] if len(parole) > 1 else [],
            "parole": parole,
            "numeri": [p for p in parole if p.replace(".", "").replace(",", "").isdigit()]
        }
    
    def estrai_parole_chiave(self, frase: str) -> List[str]:
        """
        Estrae parole chiave (verbi e sostantivi) dalla frase.
        
        Args:
            frase: frase da analizzare
            
        Returns:
            lista di parole chiave
        """
        if not self.nlp:
            # Fallback: prendi tutte le parole di lunghezza > 3
            return [p for p in frase.lower().split() if len(p) > 3]
        
        doc = self.nlp(frase)
        return self._estrai_parole_chiave(doc)
    
    def _estrai_parole_chiave(self, doc) -> List[str]:
        """Estrae parole chiave da un documento spaCy."""
        return [token.lemma_ for token in doc if token.pos_ in ["VERB", "NOUN"]]
    
    def estrai_numeri(self, frase: str) -> List[int]:
        """
        Estrae numeri dalla frase.
        
        Args:
            frase: frase da analizzare
            
        Returns:
            lista di numeri interi trovati
        """
        numeri = []
        for parola in frase.split():
            # Rimuovi caratteri non numerici
            parola_pulita = parola.strip(",.!?;:")
            if parola_pulita.isdigit():
                numeri.append(int(parola_pulita))
        
        return numeri


# Istanza singleton per uso rapido
_parser_globale: Optional[ParserItaliano] = None


def get_parser() -> ParserItaliano:
    """Ottieni l'istanza globale del parser."""
    global _parser_globale
    if _parser_globale is None:
        _parser_globale = ParserItaliano()
    return _parser_globale


def analizza_frase(frase: str) -> Dict:
    """
    Funzione helper per analisi rapida.
    
    Args:
        frase: frase da analizzare
        
    Returns:
        risultato dell'analisi
    """
    return get_parser().analizza_semplice(frase)

