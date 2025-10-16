"""
Demo Oggetti 3D + Interazione
Mostra mano che afferra oggetti con grafica migliorata!
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from visualizzatore import VisualizzatoreMano3D


def stampa_banner():
    print("""
==================================================================
      PYTHONITA IA v3.1 - OGGETTI 3D + INTERAZIONE
==================================================================

Demo completa con:
- Oggetti 3D (mela, palla, cubo, bottiglia, tazza)
- Grafica migliorata (mesh 3D, colori, shading)
- Interazioni (afferra, rilascia)
- Rendering avanzato

==================================================================
""")


def demo_oggetti():
    """Demo oggetti 3D e interazioni."""
    
    stampa_banner()
    
    print("[1] Creando visualizzatore con rendering avanzato...")
    viz = VisualizzatoreMano3D("Pythonita v3.1 - Demo Oggetti 3D")
    
    # Mano aperta iniziale
    viz.mano.apri_mano()
    viz.disegna_mano()
    print("    [OK] Visualizzatore creato!")
    print("\nAttendi 2 secondi...")
    import matplotlib.pyplot as plt
    plt.pause(2)
    
    # PARTE 1: Aggiungi vari oggetti alla scena
    print("\n[2] Aggiungendo oggetti alla scena...")
    print("    - Mela (rossa)")
    mela = viz.aggiungi_oggetto("mela", (0, 15, 0))
    
    print("    - Palla (arancione)")
    palla = viz.aggiungi_oggetto("palla", (10, 15, 0))
    
    print("    - Cubo (blu)")
    cubo = viz.aggiungi_oggetto("cubo", (-10, 15, 0))
    
    print("    - Bottiglia (verde trasparente)")
    bottiglia = viz.aggiungi_oggetto("bottiglia", (5, 15, 5))
    
    viz.disegna_mano()
    print("    [OK] Oggetti aggiunti!")
    print("\nAttendi 2 secondi...")
    plt.pause(2)
    
    # PARTE 2: Afferra mela
    print("\n[3] Animazione: Afferra mela!")
    print("    - Apri mano")
    print("    - Avvicina alla mela")
    print("    - Chiudi dita sulla mela")
    print("    - Mela nella mano!")
    
    viz.anima_afferra_oggetto("mela", steps=20)
    
    print("    [OK] Mela afferrata!")
    print("\nAttendi 2 secondi...")
    plt.pause(2)
    
    # PARTE 3: Rilascia mela
    print("\n[4] Animazione: Rilascia mela!")
    print("    - Apri dita gradualmente")
    print("    - Mela cade")
    
    viz.anima_rilascia_oggetto(steps=15)
    
    print("    [OK] Mela rilasciata!")
    print("\nAttendi 2 secondi...")
    plt.pause(2)
    
    # PARTE 4: Afferra palla
    print("\n[5] Animazione: Afferra palla grande!")
    # Rimuovi mela e sposta palla al centro
    viz.gestore_oggetti.rimuovi_oggetto(mela)
    palla.posizione = [0, 15, 0]
    
    viz.anima_afferra_oggetto("palla", steps=20)
    
    print("    [OK] Palla afferrata!")
    print("\n[PREMI ENTER per continuare]")
    input()
    
    # PARTE 5: Mostra rendering avanzato
    print("\n[6] RENDERING AVANZATO ATTIVO!")
    print("    - Mesh 3D solide (no wireframe)")
    print("    - Colori realistici")
    print("    - Shading e sfumature")
    print("    - Trasparenze (bottiglia)")
    print("    - Etichette oggetti")
    
    print("\n[OK] Demo completata!")
    print("\nChiudi la finestra per terminare.")
    viz.mostra()


def demo_tutti_oggetti():
    """Mostra tutti i tipi di oggetti disponibili."""
    print("\n" + "="*70)
    print("BONUS: CATALOGO OGGETTI 3D")
    print("="*70)
    
    viz = VisualizzatoreMano3D("Catalogo Oggetti 3D")
    
    # Griglia di oggetti
    oggetti = [
        ("mela", (-8, 15, -5)),
        ("palla", (0, 15, -5)),
        ("cubo", (8, 15, -5)),
        ("bottiglia", (-8, 15, 5)),
        ("smartphone", (0, 15, 5)),
        ("tazza", (8, 15, 5)),
    ]
    
    print("\nCatalogo oggetti:")
    for nome, pos in oggetti:
        print(f"  - {nome.capitalize()}: posizione {pos}")
        viz.aggiungi_oggetto(nome, pos)
    
    viz.mano.apri_mano()
    viz.disegna_mano()
    
    print("\n[OK] Catalogo completo!")
    print("Chiudi la finestra per terminare.")
    viz.mostra()


if __name__ == "__main__":
    try:
        demo_oggetti()
        
        # Opzionale: mostra catalogo
        risposta = input("\nVuoi vedere il catalogo completo oggetti? (s/n): ")
        if risposta.lower() == 's':
            demo_tutti_oggetti()
            
    except KeyboardInterrupt:
        print("\n\n[INTERROTTO] Demo fermata.")
    except Exception as e:
        print(f"\n[ERRORE] {e}")
        import traceback
        traceback.print_exc()

