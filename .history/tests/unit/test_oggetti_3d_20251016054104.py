"""
Test suite per oggetti 3D del visualizzatore.
"""

import pytest
import numpy as np
from visualizzatore.oggetti_3d import (
    Mela, Palla, Cubo, Bottiglia, Smartphone, Tazza,
    crea_oggetto
)


class TestOggetti3DBase:
    """Test funzionalità base comuni a tutti gli oggetti."""
    
    def test_mela_creazione(self):
        """Test creazione mela."""
        mela = Mela()
        assert mela.nome == "mela"
        assert mela.colore == (1.0, 0.0, 0.0)  # Rosso
        assert mela.dimensione > 0
    
    def test_palla_creazione(self):
        """Test creazione palla."""
        palla = Palla()
        assert palla.nome == "palla"
        assert palla.dimensione > 0
    
    def test_cubo_creazione(self):
        """Test creazione cubo."""
        cubo = Cubo()
        assert cubo.nome == "cubo"
        assert cubo.dimensione > 0
    
    def test_bottiglia_creazione(self):
        """Test creazione bottiglia."""
        bottiglia = Bottiglia()
        assert bottiglia.nome == "bottiglia"
        assert bottiglia.altezza > 0
    
    def test_smartphone_creazione(self):
        """Test creazione smartphone."""
        smartphone = Smartphone()
        assert smartphone.nome == "smartphone"
        assert hasattr(smartphone, 'larghezza')
    
    def test_tazza_creazione(self):
        """Test creazione tazza."""
        tazza = Tazza()
        assert tazza.nome == "tazza"
        assert hasattr(tazza, 'capacita')


class TestGetOggetto:
    """Test funzione factory get_oggetto."""
    
    def test_get_mela(self):
        """Test recupero mela."""
        obj = get_oggetto("mela")
        assert obj is not None
        assert obj.nome == "mela"
    
    def test_get_palla(self):
        """Test recupero palla."""
        obj = get_oggetto("palla")
        assert obj is not None
        assert obj.nome == "palla"
    
    def test_get_cubo(self):
        """Test recupero cubo."""
        obj = get_oggetto("cubo")
        assert obj is not None
        assert obj.nome == "cubo"
    
    def test_get_oggetto_inesistente(self):
        """Test oggetto non esistente."""
        obj = get_oggetto("oggetto_inesistente")
        assert obj is None
    
    def test_get_oggetto_case_insensitive(self):
        """Test case insensitive."""
        obj1 = get_oggetto("MELA")
        obj2 = get_oggetto("mela")
        obj3 = get_oggetto("MeLa")
        
        assert obj1 is not None
        assert obj2 is not None
        assert obj3 is not None
        assert obj1.nome == obj2.nome == obj3.nome


class TestOggettiGeometria:
    """Test geometria e mesh degli oggetti."""
    
    def test_mela_ha_vertices(self):
        """Test che mela abbia vertici."""
        mela = Mela()
        vertices = mela.get_vertices()
        assert vertices is not None
        assert len(vertices) > 0
    
    def test_palla_ha_faces(self):
        """Test che palla abbia facce."""
        palla = Palla()
        faces = palla.get_faces()
        assert faces is not None
        assert len(faces) > 0
    
    def test_cubo_ha_dimensioni_corrette(self):
        """Test dimensioni cubo."""
        cubo = Cubo()
        vertices = cubo.get_vertices()
        
        # Un cubo deve avere 8 vertici
        assert len(vertices) >= 8
    
    def test_oggetti_hanno_colore(self):
        """Test che tutti gli oggetti abbiano colore."""
        oggetti = [Mela(), Palla(), Cubo(), Bottiglia(), Smartphone(), Tazza()]
        
        for obj in oggetti:
            assert hasattr(obj, 'colore')
            assert len(obj.colore) == 3  # RGB
            
            # Valori RGB validi (0-1)
            for val in obj.colore:
                assert 0.0 <= val <= 1.0


class TestOggettiPosizione:
    """Test posizionamento e trasformazioni oggetti."""
    
    def test_mela_posizione_default(self):
        """Test posizione default mela."""
        mela = Mela()
        pos = mela.get_posizione()
        assert pos is not None
        assert len(pos) == 3  # x, y, z
    
    def test_set_posizione(self):
        """Test impostazione posizione."""
        mela = Mela()
        nuova_pos = (10, 20, 30)
        mela.set_posizione(nuova_pos)
        
        pos = mela.get_posizione()
        assert pos[0] == 10
        assert pos[1] == 20
        assert pos[2] == 30
    
    def test_rotazione(self):
        """Test rotazione oggetto."""
        cubo = Cubo()
        
        # Ruota 90 gradi
        cubo.ruota(90, asse='z')
        
        rotazione = cubo.get_rotazione()
        assert rotazione is not None


class TestOggettiInterazione:
    """Test interazioni con oggetti (es: afferrare)."""
    
    def test_mela_is_afferrabile(self):
        """Test che mela sia afferrabile."""
        mela = Mela()
        assert hasattr(mela, 'afferrabile')
        assert mela.afferrabile is True
    
    def test_bottiglia_is_afferrabile(self):
        """Test che bottiglia sia afferrabile."""
        bottiglia = Bottiglia()
        assert bottiglia.afferrabile is True
    
    def test_oggetti_hanno_peso(self):
        """Test che oggetti abbiano peso (per fisica)."""
        mela = Mela()
        assert hasattr(mela, 'peso')
        assert mela.peso > 0
        
        # Mela dovrebbe pesare circa 100-200g
        assert 50 < mela.peso < 300


class TestOggettiRendering:
    """Test parametri di rendering."""
    
    def test_mela_ha_alpha(self):
        """Test trasparenza mela."""
        mela = Mela()
        assert hasattr(mela, 'alpha')
        assert 0.0 <= mela.alpha <= 1.0
    
    def test_oggetti_hanno_material(self):
        """Test proprietà material."""
        oggetti = [Mela(), Palla(), Cubo()]
        
        for obj in oggetti:
            # Deve avere proprietà materiale
            assert hasattr(obj, 'colore')
            assert hasattr(obj, 'alpha')
    
    def test_rendering_wireframe_vs_solid(self):
        """Test modalità rendering."""
        mela = Mela()
        
        # Default dovrebbe essere solid
        assert mela.get_render_mode() == 'solid'
        
        # Cambia a wireframe
        mela.set_render_mode('wireframe')
        assert mela.get_render_mode() == 'wireframe'


class TestOggettiValidazione:
    """Test validazione dati oggetti."""
    
    def test_dimensioni_positive(self):
        """Test che dimensioni siano positive."""
        oggetti = [Mela(), Palla(), Cubo(), Bottiglia(), Tazza()]
        
        for obj in oggetti:
            dim = obj.dimensione if hasattr(obj, 'dimensione') else obj.altezza
            assert dim > 0, f"{obj.nome} ha dimensione negativa/zero"
    
    def test_colori_validi(self):
        """Test che colori siano nel range valido."""
        oggetti = [Mela(), Palla(), Cubo(), Bottiglia(), Smartphone(), Tazza()]
        
        for obj in oggetti:
            r, g, b = obj.colore
            assert 0.0 <= r <= 1.0
            assert 0.0 <= g <= 1.0
            assert 0.0 <= b <= 1.0
    
    def test_nomi_univoci(self):
        """Test che ogni oggetto abbia nome univoco."""
        oggetti = [Mela(), Palla(), Cubo(), Bottiglia(), Smartphone(), Tazza()]
        nomi = [obj.nome for obj in oggetti]
        
        # Nessun duplicato
        assert len(nomi) == len(set(nomi))


class TestOggettiPerformance:
    """Test performance rendering oggetti."""
    
    def test_vertices_count_ragionevole(self):
        """Test che numero vertici sia ragionevole."""
        mela = Mela()
        vertices = mela.get_vertices()
        
        # Non troppi vertici (performance)
        # Oggetto semplice: < 10000 vertici
        assert len(vertices) < 10000
    
    def test_creazione_veloce(self):
        """Test che creazione oggetto sia veloce."""
        import time
        
        start = time.time()
        
        # Crea 100 mele
        for _ in range(100):
            _ = Mela()
        
        elapsed = time.time() - start
        
        # Deve creare 100 oggetti in < 1 secondo
        assert elapsed < 1.0, f"Creazione troppo lenta: {elapsed}s"


# Test di integrazione
class TestOggettiIntegrazione:
    """Test integrazione oggetti con visualizzatore."""
    
    def test_tutti_oggetti_disponibili(self):
        """Test che tutti gli oggetti siano accessibili."""
        nomi_attesi = ["mela", "palla", "cubo", "bottiglia", "smartphone", "tazza"]
        
        for nome in nomi_attesi:
            obj = get_oggetto(nome)
            assert obj is not None, f"Oggetto {nome} non disponibile"
    
    def test_oggetti_compatibili_con_numpy(self):
        """Test che oggetti siano compatibili con numpy."""
        mela = Mela()
        vertices = mela.get_vertices()
        
        # Converti a numpy array
        arr = np.array(vertices)
        assert arr.shape[1] == 3  # x, y, z


if __name__ == "__main__":
    # Esegui test
    pytest.main([__file__, "-v", "--tb=short"])

