"""
Controllore principale che gestisce la logica di generazione del codice.
Usa l'architettura ibrida (AI + regole).
"""

from core.generatore import get_generatore
import logging

# Configura logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def ciclo_di_controllo(frase):
    """
    Processa una frase in italiano e genera codice Python.
    
    Args:
        frase: frase in italiano da convertire
        
    Returns:
        codice Python generato
    """
    try:
        generatore = get_generatore()
        codice = generatore.genera(frase)
        return codice
    except Exception as e:
        logger.error(f"Errore nel ciclo di controllo: {e}")
        return f"# Errore: {str(e)}"
