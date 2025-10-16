"""
Test visualizzatore 3D con mela
Questo codice mostra la mano che afferra la mela in 3D
"""

from visualizzatore.viewer_3d import VisualizzatoreMano3D
from visualizzatore.modelli_3d import ManoRobotica
from visualizzatore.oggetti_3d import crea_oggetto

# Crea visualizzatore
vis = VisualizzatoreMano3D(titolo="Mano Afferra Mela")

# Crea mano
mano = ManoRobotica()

# Crea mela
mela = crea_oggetto("mela", posizione=(10, 15, 0))

print("=" * 60)
print("VISUALIZZATORE 3D - MANO AFFERRA MELA")
print("=" * 60)
print(f"Mano creata: {mano}")
print(f"Mela creata: {mela.nome}")
print(f"Posizione mela: {mela.posizione}")
print(f"Colore mela: {mela.colore}")
print("=" * 60)

# Apri mano
mano.apri()
vis.aggiungi_mano(mano)

# Aggiungi mela al visualizzatore
vis.aggiungi_oggetto(mela)

# Disegna stato iniziale
vis.disegna_mano()

# Animazione: muovi mano verso mela
print("Animazione: mano si muove verso la mela...")
for frame in range(30):
    # Chiudi gradualmente
    chiusura = frame / 30.0
    
    # Aggiorna posizioni dita
    for dito in mano.dita:
        for segmento in dito.segmenti:
            segmento.angolo = chiusura * 90  # Chiusura graduale
    
    # Aggiorna visualizzatore
    vis.disegna_mano()

print("✅ Animazione completata!")
print("Chiudi la finestra 3D per terminare.")

# Mantieni finestra aperta
vis.mostra()

