"""
Parser NLP Italiano - Estrae intent e entities da frasi italiane.
Design Pattern: Strategy + Template Method
"""

import spacy
from typing import Optional, List, Dict
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# Carica modello spaCy (lazy loading)
_nlp_model = None

def _get_nlp():
    """Lazy loading modello spaCy."""
    global _nlp_model
    if _nlp_model is None:
        try:
            _nlp_model = spacy.load("it_core_news_sm")
            logger.info("Modello spaCy caricato")
        except OSError:
            logger.warning("spaCy model non trovato. Funzionalità limitate.")
            _nlp_model = None
    return _nlp_model


@dataclass
class ParsedCommand:
    """Comando parsato con intent ed entities."""
    original_text: str
    intent: str                    # es: "create_list", "print", "robot_grasp"
    entities: Dict[str, any]       # es: {"numbers": [1,2,3], "object": "apple"}
    subject: Optional[str] = None
    verb: Optional[str] = None
    object: Optional[str] = None
    interrogative: Optional[str] = None
    confidence: float = 1.0


class ItalianNLPParser:
    """
    Parser avanzato per linguaggio naturale italiano.
    Estrae intent, entities e struttura grammaticale.
    """
    
    def __init__(self):
        """Inizializza parser."""
        self.logger = logging.getLogger(__name__)
        self.nlp = _get_nlp()
        
    def parse(self, text: str) -> ParsedCommand:
        """
        Parsa frase italiana ed estrae informazioni strutturate.
        
        Args:
            text: Frase in italiano
            
        Returns:
            ParsedCommand con intent ed entities
        """
        text = text.strip().lower()
        
        # Estrai intent da keywords
        intent = self._extract_intent(text)
        
        # Estrai entities specifiche
        entities = self._extract_entities(text, intent)
        
        # Analisi grammaticale (se spaCy disponibile)
        grammar = self._analyze_grammar(text) if self.nlp else {}
        
        return ParsedCommand(
            original_text=text,
            intent=intent,
            entities=entities,
            subject=grammar.get('subject'),
            verb=grammar.get('verb'),
            object=grammar.get('object'),
            interrogative=grammar.get('interrogative'),
            confidence=grammar.get('confidence', 0.8)
        )
    
    def _extract_intent(self, text: str) -> str:
        """Estrae intent principale."""
        # Intent mapping (estendibile)
        intents = {
            "stampa": ["stampa", "print", "scrivi", "mostra"],
            "lista": ["lista", "elenco", "array"],
            "somma": ["somma", "addizione", "aggiungi", "più"],
            "robot_apri_mano": ["apri mano", "apri la mano"],
            "robot_chiudi_mano": ["chiudi mano", "chiudi pugno"],
            "robot_afferra": ["afferra", "prendi", "solleva"],
        }
        
        for intent, keywords in intents.items():
            if any(kw in text for kw in keywords):
                return intent
        
        return "unknown"
    
    def _extract_entities(self, text: str, intent: str) -> Dict:
        """Estrae entities basate su intent."""
        entities = {}
        
        # Estrai numeri
        import re
        numbers = re.findall(r'\b\d+\b', text)
        if numbers:
            entities['numbers'] = [int(n) for n in numbers]
        
        # Estrai oggetti (per comandi robot)
        objects = {
            "mela": ["mela", "apple"],
            "palla": ["palla", "ball"],
            "cubo": ["cubo", "cube"],
        }
        
        for obj, keywords in objects.items():
            if any(kw in text for kw in keywords):
                entities['object'] = obj
                break
        
        return entities
    
    def _analyze_grammar(self, text: str) -> Dict:
        """Analizza struttura grammaticale con spaCy."""
        if not self.nlp:
            return {}
        
        doc = self.nlp(text)
        grammar = {}
        
        for token in doc:
            if "subj" in token.dep_:
                grammar['subject'] = token.lemma_
            if token.pos_ == "VERB":
                grammar['verb'] = token.lemma_
            if "obj" in token.dep_:
                grammar['object'] = token.lemma_
        
        return grammar


# Singleton instance
_parser_instance: Optional[ItalianNLPParser] = None

def get_parser() -> ItalianNLPParser:
    """Ottiene istanza singleton del parser."""
    global _parser_instance
    if _parser_instance is None:
        _parser_instance = ItalianNLPParser()
    return _parser_instance

def parse_italian(text: str) -> ParsedCommand:
    """Helper function per parsing rapido."""
    return get_parser().parse(text)

