"""
Parser linguistico avanzato per Pythonita IA.
Analizza strutture linguistiche complete: soggetto-verbo-complemento.
Riconosce interrogativi: chi, quando, come, dove, perché.
"""

import spacy
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class StrutturaLinguistica:
    """Rappresenta la struttura linguistica di una frase."""
    testo_originale: str
    soggetto: Optional[str] = None
    verbo: Optional[str] = None
    complemento_oggetto: Optional[str] = None
    complementi: List[str] = None
    interrogativo: Optional[str] = None  # chi, quando, come, dove, perché
    tempo_verbale: Optional[str] = None  # presente, passato, futuro
    modalita: Optional[str] = None  # indicativo, condizionale, imperativo
    
    def __post_init__(self):
        if self.complementi is None:
            self.complementi = []


class ParserLinguisticoAvanzato:
    """
    Parser che analizza strutture linguistiche complete.
    
    Riconosce:
    - Soggetto-Verbo-Complemento
    - Interrogativi (chi, quando, come, dove, perché, cosa)
    - Tempo verbale
    - Modalità (imperativo, indicativo, ecc.)
    """
    
    # Interrogativi italiani
    INTERROGATIVI = {
        'chi': 'persona',
        'cosa': 'oggetto',
        'quando': 'tempo',
        'dove': 'luogo',
        'come': 'modo',
        'perché': 'causa',
        'perche': 'causa',
        'quanto': 'quantità',
        'quale': 'scelta',
        'quali': 'scelta_plurale'
    }
    
    def __init__(self, usa_spacy=True):
        """
        Inizializza il parser linguistico.
        
        Args:
            usa_spacy: Usa spaCy se disponibile per analisi avanzata
        """
        self.nlp = None
        self.usa_spacy = usa_spacy
        
        if usa_spacy:
            try:
                self.nlp = spacy.load("it_core_news_sm")
            except:
                print("⚠️  spaCy non disponibile, uso parsing semplice")
                self.nlp = None
    
    def analizza(self, frase: str) -> StrutturaLinguistica:
        """
        Analizza completamente una frase italiana.
        
        Args:
            frase: Frase da analizzare
            
        Returns:
            Struttura linguistica completa
        """
        if self.nlp and self.usa_spacy:
            return self._analizza_con_spacy(frase)
        else:
            return self._analizza_semplice(frase)
    
    def _analizza_con_spacy(self, frase: str) -> StrutturaLinguistica:
        """Analisi completa con spaCy."""
        doc = self.nlp(frase)
        
        # Estrai componenti
        soggetto = self._estrai_soggetto(doc)
        verbo = self._estrai_verbo(doc)
        complemento = self._estrai_complemento_oggetto(doc)
        complementi = self._estrai_complementi(doc)
        interrogativo = self._identifica_interrogativo(frase)
        tempo = self._identifica_tempo_verbale(doc)
        modalita = self._identifica_modalita(doc)
        
        return StrutturaLinguistica(
            testo_originale=frase,
            soggetto=soggetto,
            verbo=verbo,
            complemento_oggetto=complemento,
            complementi=complementi,
            interrogativo=interrogativo,
            tempo_verbale=tempo,
            modalita=modalita
        )
    
    def _analizza_semplice(self, frase: str) -> StrutturaLinguistica:
        """Analisi semplificata senza spaCy."""
        parole = frase.lower().split()
        
        # Identifica interrogativo
        interrogativo = None
        for parola in parole:
            if parola in self.INTERROGATIVI:
                interrogativo = self.INTERROGATIVI[parola]
                break
        
        # Estrai verbo (euristica: seconda parola o prima)
        verbo = parole[1] if len(parole) > 1 else (parole[0] if parole else None)
        
        # Soggetto (euristica: prima parola se non interrogativo)
        soggetto = parole[0] if parole and parole[0] not in self.INTERROGATIVI else None
        
        # Complemento (resto della frase)
        complemento = ' '.join(parole[2:]) if len(parole) > 2 else None
        
        return StrutturaLinguistica(
            testo_originale=frase,
            soggetto=soggetto,
            verbo=verbo,
            complemento_oggetto=complemento,
            complementi=parole[2:] if len(parole) > 2 else [],
            interrogativo=interrogativo,
            tempo_verbale='presente',  # Default
            modalita='imperativo' if verbo and verbo.endswith(('a', 'i', 'ate')) else 'indicativo'
        )
    
    def _estrai_soggetto(self, doc) -> Optional[str]:
        """Estrae il soggetto dalla frase."""
        for token in doc:
            if token.dep_ in ['nsubj', 'nsubj:pass']:  # Soggetto
                return token.text
        return None
    
    def _estrai_verbo(self, doc) -> Optional[str]:
        """Estrae il verbo principale."""
        for token in doc:
            if token.pos_ == 'VERB' and token.dep_ == 'ROOT':
                return token.lemma_
        
        # Fallback: primo verbo
        for token in doc:
            if token.pos_ == 'VERB':
                return token.lemma_
        
        return None
    
    def _estrai_complemento_oggetto(self, doc) -> Optional[str]:
        """Estrae il complemento oggetto."""
        for token in doc:
            if token.dep_ == 'obj':  # Oggetto diretto
                return token.text
        return None
    
    def _estrai_complementi(self, doc) -> List[str]:
        """Estrae tutti i complementi."""
        complementi = []
        for token in doc:
            if token.dep_ in ['obl', 'iobj', 'obl:arg']:  # Complementi vari
                complementi.append(token.text)
        return complementi
    
    def _identifica_interrogativo(self, frase: str) -> Optional[str]:
        """Identifica se c'è un interrogativo."""
        parole = frase.lower().split()
        for parola in parole:
            if parola in self.INTERROGATIVI:
                return self.INTERROGATIVI[parola]
        return None
    
    def _identifica_tempo_verbale(self, doc) -> str:
        """Identifica il tempo verbale."""
        for token in doc:
            if token.pos_ == 'VERB':
                if 'Past' in token.morph.get('Tense'):
                    return 'passato'
                elif 'Fut' in token.morph.get('Tense'):
                    return 'futuro'
        return 'presente'
    
    def _identifica_modalita(self, doc) -> str:
        """Identifica la modalità del verbo."""
        for token in doc:
            if token.pos_ == 'VERB':
                mood = token.morph.get('Mood')
                if 'Imp' in mood:
                    return 'imperativo'
                elif 'Cnd' in mood:
                    return 'condizionale'
        return 'indicativo'


# Singleton
_parser_linguistico: Optional[ParserLinguisticoAvanzato] = None


def get_parser_linguistico() -> ParserLinguisticoAvanzato:
    """Ottiene istanza singleton del parser linguistico."""
    global _parser_linguistico
    if _parser_linguistico is None:
        _parser_linguistico = ParserLinguisticoAvanzato()
    return _parser_linguistico


def analizza_linguaggio(frase: str) -> StrutturaLinguistica:
    """
    Helper per analisi rapida.
    
    Args:
        frase: Frase da analizzare
        
    Returns:
        Struttura linguistica
    """
    return get_parser_linguistico().analizza(frase)

