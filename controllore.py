"""
Controllore principale che gestisce la logica di generazione del codice.
Usa l'architettura ibrida (AI + regole) con validazione input e cache.
"""

from core.generatore import get_generatore
from core.validator import validate_input
import logging

# Configura logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def ciclo_di_controllo(frase):
    """
    Processa una frase in italiano e genera codice Python.
    
    Steps:
    1. Valida e sanitizza input
    2. Genera codice (usa cache se disponibile)
    3. Gestisce errori
    
    Args:
        frase: frase in italiano da convertire
        
    Returns:
        codice Python generato
    """
    try:
        # 1. Valida input
        result = validate_input(frase)
        
        if not result.is_valid:
            logger.warning(f"Input invalido: {result.message}")
            return f"# Errore di validazione: {result.message}"
        
        # 2. Usa input sanitizzato
        frase_pulita = result.sanitized_input
        logger.debug(f"Input sanitizzato: '{frase_pulita}'")
        
        # 3. Genera codice
        generatore = get_generatore()
        codice = generatore.genera(frase_pulita)
        return codice
        
    except Exception as e:
        logger.error(f"Errore nel ciclo di controllo: {e}")
        return f"# Errore: {str(e)}"
