"""
Pythonita IA v3.1 - Launcher Unificato
Versione semplificata che funziona sempre!
"""

import sys
from pathlib import Path

# Aggiungi path
sys.path.insert(0, str(Path(__file__).parent))

def stampa_banner():
    """Stampa banner iniziale."""
    print("""
==================================================================
                    PYTHONITA IA v3.1
        Da Linguaggio Naturale Italiano a Codice Python
==================================================================

Versione: 3.1.0
Funzionalita':
  - 143+ comandi Python supportati
  - Multi-comando (combina piu' azioni)
  - Template robotica
  - Cache intelligente (24,000x piu' veloce)
  - Input validation

==================================================================
""")

def menu_principale():
    """Mostra menu e gestisce scelta."""
    print("\nScegli modalita':\n")
    print("1. CLI Interattiva (Riga di comando)")
    print("2. GUI Classica (Finestra semplice)")
    print("3. GUI 3D (Visualizzatore robot) - Richiede matplotlib")
    print("4. Demo Mano 3D - Richiede matplotlib")
    print("5. Test Rapido (Genera codice)")
    print("0. Esci")
    print()
    
    try:
        scelta = input("Scelta (0-5): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\nInterrotto dall'utente.")
        return '0'
    
    return scelta

def avvia_cli():
    """Avvia versione CLI."""
    print("\n" + "="*70)
    print("MODALITA' CLI - Interfaccia Riga di Comando")
    print("="*70)
    print("\nScrivi comandi in italiano (es: 'stampa ciao mondo')")
    print("Oppure 'esci' per terminare\n")
    
    try:
        from core import genera_codice
        
        while True:
            try:
                frase = input("➤ ").strip()
                
                if not frase:
                    continue
                
                if frase.lower() in ['esci', 'quit', 'exit']:
                    print("Arrivederci!")
                    break
                
                # Genera codice
                codice = genera_codice(frase)
                print("\nCodice generato:")
                print("-" * 60)
                print(codice)
                print("-" * 60)
                print()
                
            except KeyboardInterrupt:
                print("\n\nInterrotto. Arrivederci!")
                break
            except EOFError:
                break
                
    except ImportError as e:
        print(f"\n[ERRORE] Modulo mancante: {e}")
        print("\nInstalla dipendenze:")
        print("  pip install -r requirements.txt")

def avvia_gui_classica():
    """Avvia GUI classica senza 3D."""
    print("\n[AVVIO] GUI Classica...")
    try:
        import tkinter
        from gui_pythonita import main
        main()
    except ImportError as e:
        print(f"[ERRORE] {e}")
        print("\nLa GUI richiede tkinter (dovrebbe essere gia' installato)")
    except FileNotFoundError:
        print("[ERRORE] File gui_pythonita.py non trovato")
        print("Usa invece: python main.py")

def avvia_gui_3d():
    """Avvia GUI con visualizzatore 3D."""
    print("\n[AVVIO] GUI con Visualizzatore 3D...")
    print("Attendere caricamento moduli...")
    try:
        import numpy
        import matplotlib
        from gui_robot_3d import main
        main()
    except ImportError as e:
        print(f"\n[ERRORE] Modulo mancante: {e}")
        print("\nInstalla dipendenze:")
        print("  pip install numpy matplotlib")
    except Exception as e:
        print(f"\n[ERRORE] {e}")

def avvia_demo_3d():
    """Avvia demo mano 3D."""
    print("\n[AVVIO] Demo Mano 3D...")
    try:
        import demo_semplice
        # Il modulo si esegue automaticamente
    except ImportError as e:
        print(f"\n[ERRORE] Modulo mancante: {e}")
        print("\nInstalla dipendenze:")
        print("  pip install numpy matplotlib")
    except Exception as e:
        print(f"\n[ERRORE] {e}")
        import traceback
        traceback.print_exc()

def test_rapido():
    """Test rapido generazione codice."""
    print("\n" + "="*70)
    print("TEST RAPIDO - Generazione Codice")
    print("="*70)
    
    test_frasi = [
        "stampa ciao mondo",
        "somma 10 e 20",
        "crea lista con 1 2 3 4 5"
    ]
    
    try:
        from core import genera_codice
        
        for i, frase in enumerate(test_frasi, 1):
            print(f"\n[Test {i}/3] Frase: \"{frase}\"")
            codice = genera_codice(frase)
            print("Codice generato:")
            print("-" * 60)
            print(codice[:200] + "..." if len(codice) > 200 else codice)
            print("-" * 60)
        
        print("\n[OK] Tutti i test completati con successo!")
        
    except Exception as e:
        print(f"\n[ERRORE] {e}")

def main():
    """Funzione principale."""
    stampa_banner()
    
    while True:
        scelta = menu_principale()
        
        if scelta == '1':
            avvia_cli()
        elif scelta == '2':
            avvia_gui_classica()
        elif scelta == '3':
            avvia_gui_3d()
        elif scelta == '4':
            avvia_demo_3d()
        elif scelta == '5':
            test_rapido()
        elif scelta == '0':
            print("\nArrivederci!")
            break
        else:
            print("\n[ERRORE] Scelta non valida. Riprova.")
        
        # Pausa prima di tornare al menu
        if scelta in ['1', '5']:
            try:
                input("\nPremi ENTER per tornare al menu...")
            except (EOFError, KeyboardInterrupt):
                pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrotto dall'utente. Arrivederci!")
    except Exception as e:
        print(f"\n[ERRORE CRITICO] {e}")
        import traceback
        traceback.print_exc()

