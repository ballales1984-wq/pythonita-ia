"""
Demo Semplice Pythonita IA v3.1
Versione garantita funzionante - Visualizzatore 3D Mano
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("""
==================================================================
      PYTHONITA IA v3.1 - DEMO VISUALIZZATORE 3D
==================================================================

Questa demo mostra:
- Mano robotica 3D con misure reali
- Animazioni fluide (apri, chiudi, pinza)
- Grafica avanzata con colori realistici

La finestra 3D si aprira' automaticamente...
==================================================================
""")

try:
    from visualizzatore import VisualizzatoreMano3D
    import matplotlib.pyplot as plt
    
    print("\n[1/5] Inizializzazione visualizzatore...")
    viz = VisualizzatoreMano3D("Pythonita v3.1 - Demo Mano 3D")
    
    # Mano aperta
    print("[2/5] Mostra mano aperta...")
    viz.mano.apri_mano()
    viz.disegna_mano()
    plt.pause(1)
    
    # Animazione chiusura
    print("[3/5] Animazione: Chiusura pugno...")
    viz.anima_chiusura(steps=15)
    plt.pause(0.5)
    
    # Animazione apertura
    print("[4/5] Animazione: Riapertura mano...")
    viz.anima_apertura(steps=15)
    plt.pause(0.5)
    
    # Posizione pinza
    print("[5/5] Animazione: Posizione pinza...")
    viz.anima_pinza(steps=10)
    
    print("\n" + "="*70)
    print("DEMO COMPLETATA CON SUCCESSO!")
    print("="*70)
    print("\nChiudi la finestra per terminare.")
    print("Oppure premi CTRL+C per interrompere.")
    
    # Mostra finestra
    viz.mostra()
    
except ImportError as e:
    print(f"\n[ERRORE] Modulo mancante: {e}")
    print("\nInstalla dipendenze:")
    print("  pip install -r requirements.txt")
    print("  python -m spacy download it_core_news_sm")
    
except Exception as e:
    print(f"\n[ERRORE] {e}")
    import traceback
    traceback.print_exc()
    
print("\nDemo terminata.")

