"""
Demo rapida di Pythonita IA v2.0
Mostra le capacità del nuovo sistema
"""

from core import genera_codice
import time

def stampa_separatore():
    print("\n" + "="*70 + "\n")

def demo():
    print("""
====================================================================
                                                                  
              DEMO PYTHONITA IA v2.0 - Italiano                   
                                                                  
             Architettura Ibrida Ottimizzata                      
                                                                  
====================================================================
""")
    
    esempi = [
        ("Esempio Base", "stampa ciao mondo"),
        ("Operazione Matematica", "moltiplica 8 per 9"),
        ("Struttura Dati", "crea una lista con i numeri 10 20 30"),
        ("Ciclo", "crea un ciclo da 1 a 3"),
        ("Condizione", "crea un if che controlla se x è maggiore di 5"),
        ("Richiesta Complessa", "crea una funzione che trova il numero più grande in una lista"),
    ]
    
    for titolo, frase in esempi:
        stampa_separatore()
        print(f"[{titolo}]")
        print(f"Frase: \"{frase}\"")
        print(f"\nGenerazione in corso...")
        
        start = time.time()
        codice = genera_codice(frase)
        elapsed = time.time() - start
        
        print(f"\nCodice generato in {elapsed:.2f} secondi:\n")
        print("-" * 70)
        print(codice)
        print("-" * 70)
        
        # Pausa per leggibilità
        time.sleep(1)
    
    stampa_separatore()
    print("""
*** Demo completata! ***

Caratteristiche mostrate:
   - AI locale (Llama3.2 via Ollama)
   - Output pulito senza riferimenti ai file
   - Gestione richieste semplici e complesse
   - Velocita' di generazione ottimale

Architettura Ibrida:
   - Livello 1: AI locale per richieste complesse
   - Livello 2: Sistema a regole per comandi base
   - Fallback automatico se AI non disponibile

Prova tu stesso:
   - CLI: python main.py
   - GUI: python gui_pythonita.py
""")

if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrotta")
    except Exception as e:
        print(f"\nERRORE: {e}")

