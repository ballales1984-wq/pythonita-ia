"""
Pythonita IA v3.1 Professional Edition
Entry point principale - Usa nuova architettura modulare

Questo launcher usa la nuova struttura refactorata e integra
il codice esistente in modo backward-compatible.
"""

import sys
from pathlib import Path

# Assicura che pythonita package sia nel path
sys.path.insert(0, str(Path(__file__).parent))

print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║         PYTHONITA IA v3.1 PROFESSIONAL EDITION                   ║
║                                                                  ║
║    Nuova Architettura Refactorata - Production Grade             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

Versione: 3.1.0
Architettura: Modulare con Design Patterns
Licenza: Commerciale Proprietaria

Caricamento moduli...
""")

try:
    # Importa dalla nuova struttura
    from pythonita import __version__
    from pythonita.licensing import check_license, Tier
    from pythonita.core import CodeGenerator
    
    print(f"[OK] Pythonita v{__version__} caricato")
    print("[OK] Moduli core importati")
    
    # Check licenza
    print("\n[CHECK] Verifica licenza...")
    active, tier, msg = check_license()
    
    print(f"Status: {msg}")
    print(f"Tier: {tier}")
    
    if not active and tier == Tier.FREE:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  VERSIONE GRATUITA LIMITATA                                      ║
║                                                                  ║
║  Hai accesso a:                                                  ║
║  - 20 comandi base                                               ║
║  - CLI riga di comando                                           ║
║  - Max 50 comandi/giorno                                         ║
║                                                                  ║
║  Per sbloccare tutte le funzioni:                                ║
║  1. TRIAL 14 giorni: Inserisci TRIAL123                          ║
║  2. ACQUISTA: €49 Personal | €149 Pro | €499 Enterprise         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
        """)
        
        choice = input("\nVuoi attivare trial gratuito? (s/n): ").strip().lower()
        
        if choice == 's':
            from pythonita.licensing import activate_license
            success, msg = activate_license("TRIAL123", "trial@user.com")
            print(f"\n{msg}\n")
            if success:
                active, tier, _ = check_license()
    
    # Menu principale
    print("""
╔══════════════════════════════════════════════════════════════════╗
║  MENU PRINCIPALE                                                 ║
╚══════════════════════════════════════════════════════════════════╝

Scegli modalità:

1. CLI Interattiva (Riga di comando)
2. GUI Classica (Finestra semplice)
3. GUI 3D Visualizzatore (Richiede tier PRO)
4. Demo Codice (Test rapido)
5. Info Licenza
0. Esci

""")
    
    choice = input("Scelta (0-5): ").strip()
    
    if choice == "1":
        print("\n[AVVIO] CLI Interattiva...\n")
        # Usa modulo esistente
        from core import genera_codice
        
        print("Scrivi comandi in italiano (es: 'stampa ciao mondo')")
        print("Digita 'esci' per terminare\n")
        
        while True:
            try:
                cmd = input("➤ ").strip()
                if not cmd:
                    continue
                if cmd.lower() in ['esci', 'exit', 'quit']:
                    break
                
                code = genera_codice(cmd)
                print("\nCodice generato:")
                print("-" * 60)
                print(code)
                print("-" * 60)
                print()
            except (EOFError, KeyboardInterrupt):
                break
    
    elif choice == "3":
        # Check tier
        if tier not in [Tier.TRIAL, Tier.PRO, Tier.ENTERPRISE]:
            print("""
[ERRORE] Visualizzatore 3D richiede licenza PRO o superiore!

Upgrade a PRO (€149):
- Visualizzatore 3D completo
- 6 oggetti interattivi
- Template robotica
- 3 PC, aggiornamenti 2 anni

Acquista: https://gumroad.com/l/pythonita-ia-pro
""")
        else:
            print("\n[AVVIO] GUI 3D...")
            # Usa GUI esistente
            import gui_robot_3d
            gui_robot_3d.main()
    
    elif choice == "4":
        print("\n[DEMO] Test Generazione Codice\n")
        from pythonita.core import generate_code
        
        tests = [
            "stampa ciao mondo",
            "somma 5 e 10",
            "crea lista con 1 2 3"
        ]
        
        for i, cmd in enumerate(tests, 1):
            print(f"[{i}/{len(tests)}] Comando: \"{cmd}\"")
            code = generate_code(cmd)
            print("Codice:", code[:80] + "..." if len(code) > 80 else code)
            print()
    
    elif choice == "5":
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  INFORMAZIONI LICENZA                                            ║
╚══════════════════════════════════════════════════════════════════╝

Tier Corrente: {tier}
Status: {"✅ Attiva" if active else "❌ Non attiva"}

Features Disponibili:
""")
        from pythonita.licensing import FeatureGate, Feature
        features = FeatureGate.get_available_features(tier)
        for feat in features:
            print(f"  ✅ {feat.value}")
        
        print(f"\n Totale: {len(features)} features disponibili")
    
    else:
        print("\nArrivederci!")

except ImportError as e:
    print(f"""
[ERRORE] Modulo mancante: {e}

La nuova architettura richiede migrazione completa.
Per ora usa:
    python main.py           (CLI vecchia)
    python gui_robot_3d.py   (GUI vecchia)

Oppure completa ristrutturazione con:
    Leggi RISTRUTTURAZIONE.md
""")

except Exception as e:
    print(f"\n[ERRORE] {e}")
    import traceback
    traceback.print_exc()

print("\nGrazie per aver usato Pythonita IA!")

