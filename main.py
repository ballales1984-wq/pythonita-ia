"""
Pythonita IA - Assistente didattico italiano con AI locale
Entry point principale per l'interfaccia CLI.

Uso:
    python main.py              # Avvia interfaccia CLI
    python gui_pythonita.py     # Avvia interfaccia GUI
"""

from controllore import ciclo_di_controllo
from config import Config
import logging
import sys

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def stampa_banner():
    """Stampa il banner di benvenuto."""
    banner = """
╔══════════════════════════════════════════════════════╗
║                                                      ║
║           🧠 Pythonita IA 🇮🇹                        ║
║                                                      ║
║   Assistente didattico per generare codice Python   ║
║   da frasi in italiano con AI locale                ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

💡 Comandi disponibili:
   - Scrivi una frase in italiano per generare codice
   - 'esci' o 'quit' per uscire
   - 'help' per vedere esempi
   - 'gui' per aprire l'interfaccia grafica

"""
    print(banner)


def stampa_help():
    """Stampa esempi di utilizzo."""
    help_text = """
📚 Esempi di frasi:

   Semplici:
   - "stampa ciao mondo"
   - "somma 5 e 3"
   - "crea una lista con 1 2 3"
   
   Intermedi:
   - "apri il file dati.txt"
   - "crea un ciclo da 1 a 10"
   - "crea una funzione saluto"
   
   Avanzati:
   - "crea un dizionario con nome e età"
   - "gestisci errori di divisione per zero"
   - "importa pandas e numpy"

💡 Suggerimento: Sii specifico e usa verbi chiari!
"""
    print(help_text)


def salva_codice(codice: str) -> bool:
    """
    Salva il codice generato in output.py.
    
    Args:
        codice: codice da salvare
        
    Returns:
        True se salvato con successo, False altrimenti
    """
    try:
        with open(Config.OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(codice)
        print(f"✅ Codice salvato in {Config.OUTPUT_FILE}")
        return True
    except Exception as e:
        logger.error(f"Errore salvataggio: {e}")
        print(f"❌ Impossibile salvare: {e}")
        return False


def main():
    """Entry point principale della CLI."""
    stampa_banner()
    
    try:
        while True:
            try:
                # Input utente
                print("\n" + "="*60)
                frase = input("➤ Frase in italiano: ").strip()
                
                # Gestisci comandi speciali
                if frase.lower() in ["esci", "exit", "quit", "q"]:
                    print("\n👋 Arrivederci da Pythonita!")
                    break
                
                if frase.lower() in ["help", "aiuto", "h", "?"]:
                    stampa_help()
                    continue
                
                if frase.lower() == "gui":
                    print("\n🖥️  Avvio interfaccia grafica...")
                    try:
                        import gui_pythonita
                        gui_pythonita.main()
                    except Exception as e:
                        print(f"❌ Errore nell'avvio della GUI: {e}")
                    continue
                
                if not frase:
                    print("⚠️  Scrivi una frase valida o 'help' per esempi")
                    continue
                
                # Genera codice
                print("\n🔄 Generazione codice in corso...")
                codice = ciclo_di_controllo(frase)
                
                # Mostra risultato
                print("\n🧾 Codice generato:")
                print("-" * 60)
                print(codice)
                print("-" * 60)
                
                # Chiedi se salvare
                if not codice.startswith("# Errore") and not codice.startswith("# ⚠️"):
                    risposta = input("\n💾 Salvare in output.py? (s/n): ").lower()
                    if risposta in ["s", "si", "sì", "y", "yes"]:
                        salva_codice(codice)
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Interruzione rilevata. Digita 'esci' per uscire.")
                continue
            
            except Exception as e:
                logger.error(f"Errore durante l'elaborazione: {e}")
                print(f"\n❌ Errore: {e}")
                print("💡 Prova a riformulare la frase o digita 'help' per esempi")
    
    except KeyboardInterrupt:
        print("\n\n👋 Arrivederci da Pythonita!")
        sys.exit(0)


if __name__ == "__main__":
    main()
