"""
Estrattore di oggetti 3D dalle frasi in italiano.
Riconosce i 18 oggetti disponibili nel visualizzatore.
"""

import re
from typing import Optional, List

# Mapping oggetti 3D disponibili con sinonimi
OGGETTI_3D = {
    # Frutta
    'mela': ['mela', 'mele'],
    'banana': ['banana', 'banane'],
    'arancia': ['arancia', 'arance', 'agrume'],
    'palla': ['palla', 'palle', 'sfera', 'pallone'],
    
    # Strumenti
    'martello': ['martello', 'mazzuolo'],
    'cacciavite': ['cacciavite', 'giravite'],
    'chiave': ['chiave', 'chiave inglese', 'chiave_inglese'],
    'pinza': ['pinza', 'pinze', 'tenaglia'],
    
    # Cibo
    'panino': ['panino', 'sandwich', 'tramezzino'],
    
    # Elettronica
    'mouse': ['mouse', 'topo'],
    'tastiera': ['tastiera', 'keyboard'],
    'smartphone': ['smartphone', 'telefono', 'cellulare'],
    
    # Quotidiano
    'libro': ['libro', 'testo', 'volume'],
    'penna': ['penna', 'biro', 'penna a sfera'],
    'orologio': ['orologio', 'watch'],
    'tazza': ['tazza', 'coppa', 'bicchiere'],
    'bottiglia': ['bottiglia', 'flacone'],
    'cubo': ['cubo', 'quadrato', 'parallelepipedo'],
}


def estrai_oggetto(frase: str) -> Optional[str]:
    """
    Estrae il nome dell'oggetto 3D dalla frase.
    
    Args:
        frase: Frase in italiano
        
    Returns:
        Nome oggetto se trovato, None altrimenti
        
    Examples:
        >>> estrai_oggetto("la mano afferra la mela")
        'mela'
        >>> estrai_oggetto("prendi il martello")
        'martello'
        >>> estrai_oggetto("afferra smartphone")
        'smartphone'
    """
    frase_lower = frase.lower().strip()
    
    # Rimuovi articoli comuni
    frase_clean = re.sub(r'\b(il|lo|la|i|gli|le|un|uno|una|del|della|dei|degli|delle)\b', '', frase_lower)
    
    # Cerca ogni oggetto
    for oggetto, sinonimi in OGGETTI_3D.items():
        for sinonimo in sinonimi:
            # Match parola intera
            pattern = r'\b' + re.escape(sinonimo) + r'\b'
            if re.search(pattern, frase_clean):
                return oggetto
    
    return None


def ha_oggetto(frase: str) -> bool:
    """
    Verifica se la frase contiene un oggetto 3D.
    
    Args:
        frase: Frase in italiano
        
    Returns:
        True se contiene un oggetto
    """
    return estrai_oggetto(frase) is not None


def lista_oggetti_disponibili() -> List[str]:
    """
    Ritorna lista di tutti gli oggetti disponibili.
    
    Returns:
        Lista nomi oggetti
    """
    return list(OGGETTI_3D.keys())


def get_sinonimi_oggetto(oggetto: str) -> List[str]:
    """
    Ottiene i sinonimi di un oggetto.
    
    Args:
        oggetto: Nome oggetto
        
    Returns:
        Lista sinonimi o lista vuota
    """
    return OGGETTI_3D.get(oggetto, [])


if __name__ == "__main__":
    # Test
    test_frasi = [
        "la mano afferra la mela",
        "prendi il martello",
        "afferra smartphone",
        "la mano si chiude sulla palla",
        "porta il cacciavite",
        "alza la bottiglia",
        "apri mano",  # Nessun oggetto
        "chiudi pugno",  # Nessun oggetto
    ]
    
    print("Test estrattore oggetti:\n")
    for frase in test_frasi:
        oggetto = estrai_oggetto(frase)
        print(f"'{frase}' -> {oggetto if oggetto else 'Nessun oggetto'}")

