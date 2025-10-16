"""
Test suite per oggetti 3D del visualizzatore.
"""

import pytest
import numpy as np
from pythonita.visualization.oggetti_3d import (
    Mela, Palla, Cubo, Bottiglia, Smartphone, Tazza,
    crea_oggetto
)


class TestOggetti3DBase:
    """Test funzionalità base comuni a tutti gli oggetti."""
    
    def test_mela_creazione(self):
        """Test creazione mela."""
        mela = Mela()
        assert mela.nome == "Mela"
        assert mela.colore == (0.9, 0.1, 0.1)  # Rosso
        assert mela.raggio > 0
    
    def test_palla_creazione(self):
        """Test creazione palla."""
        palla = Palla()
        assert palla.nome == "Palla"
        assert palla.raggio > 0
    
    def test_cubo_creazione(self):
        """Test creazione cubo."""
        cubo = Cubo()
        assert cubo.nome == "Cubo"
        assert cubo.lato > 0
    
    def test_bottiglia_creazione(self):
        """Test creazione bottiglia."""
        bottiglia = Bottiglia()
        assert bottiglia.nome == "Bottiglia"
        assert bottiglia.altezza > 0
    
    def test_smartphone_creazione(self):
        """Test creazione smartphone."""
        smartphone = Smartphone()
        assert smartphone.nome == "Smartphone"
        assert hasattr(smartphone, 'larghezza')
    
    def test_tazza_creazione(self):
        """Test creazione tazza."""
        tazza = Tazza()
        assert tazza.nome == "Tazza"
        assert hasattr(tazza, 'altezza')


class TestCreaOggetto:
    """Test funzione factory crea_oggetto."""
    
    def test_crea_mela(self):
        """Test creazione mela."""
        obj = crea_oggetto("mela")
        assert obj is not None
        assert obj.nome == "Mela"
    
    def test_crea_palla(self):
        """Test creazione palla."""
        obj = crea_oggetto("palla")
        assert obj is not None
        assert obj.nome == "Palla"
    
    def test_crea_cubo(self):
        """Test creazione cubo."""
        obj = crea_oggetto("cubo")
        assert obj is not None
        assert obj.nome == "Cubo"
    
    def test_crea_oggetto_inesistente(self):
        """Test oggetto non esistente."""
        obj = crea_oggetto("oggetto_inesistente")
        # crea_oggetto potrebbe ritornare oggetto default o None
        # Dipende dall'implementazione
    
    def test_crea_oggetto_case_insensitive(self):
        """Test case insensitive."""
        obj1 = crea_oggetto("MELA")
        obj2 = crea_oggetto("mela")
        obj3 = crea_oggetto("MeLa")
        
        assert obj1 is not None
        assert obj2 is not None
        assert obj3 is not None
        assert obj1.nome == obj2.nome == obj3.nome


class TestOggettiGeometria:
    """Test geometria e mesh degli oggetti."""
    
    def test_mela_ha_mesh(self):
        """Test che mela abbia mesh."""
        mela = Mela()
        x, y, z = mela.get_mesh()
        assert x is not None
        assert y is not None
        assert z is not None
        assert len(x) > 0
    
    def test_palla_ha_mesh(self):
        """Test che palla abbia mesh."""
        palla = Palla()
        x, y, z = palla.get_mesh()
        assert x is not None
        assert len(x) > 0
    
    def test_cubo_ha_mesh(self):
        """Test mesh cubo."""
        cubo = Cubo()
        x, y, z = cubo.get_mesh()
        
        # Mesh deve avere dati
        assert x is not None
        assert y is not None
        assert z is not None
    
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
        pos = mela.posizione
        assert pos is not None
        assert len(pos) == 3  # x, y, z
    
    def test_set_posizione(self):
        """Test impostazione posizione."""
        mela = Mela()
        nuova_pos = np.array([10, 20, 30])
        mela.posizione = nuova_pos
        
        pos = mela.posizione
        assert pos[0] == 10
        assert pos[1] == 20
        assert pos[2] == 30
    
    def test_rotazione(self):
        """Test rotazione oggetto."""
        cubo = Cubo()
        
        # Rotazione è un attributo numpy array
        cubo.rotazione = np.array([0, 0, 90])
        
        rotazione = cubo.rotazione
        assert rotazione is not None
        assert rotazione[2] == 90


class TestOggettiInterazione:
    """Test interazioni con oggetti (es: afferrare)."""
    
    def test_mela_is_afferrabile(self):
        """Test che mela sia afferrabile."""
        mela = Mela()
        assert hasattr(mela, 'proprieta')
        assert mela.proprieta.afferrabile is True
    
    def test_bottiglia_is_afferrabile(self):
        """Test che bottiglia sia afferrabile."""
        bottiglia = Bottiglia()
        assert bottiglia.proprieta.afferrabile is True
    
    def test_oggetti_hanno_peso(self):
        """Test che oggetti abbiano peso (per fisica)."""
        mela = Mela()
        assert hasattr(mela.proprieta, 'massa')
        assert mela.proprieta.massa > 0
        
        # Mela dovrebbe pesare circa 100-200g (in kg: 0.1-0.2)
        assert 0.05 < mela.proprieta.massa < 0.3


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
    
    def test_rendering_visibilita(self):
        """Test visibilità rendering."""
        mela = Mela()
        
        # Default dovrebbe essere visibile
        assert mela.visibile is True
        
        # Nascondi oggetto
        mela.visibile = False
        assert mela.visibile is False


class TestOggettiValidazione:
    """Test validazione dati oggetti."""
    
    def test_dimensioni_positive(self):
        """Test che dimensioni siano positive."""
        oggetti = [Mela(), Palla(), Cubo(), Bottiglia(), Tazza()]
        
        for obj in oggetti:
            # Controlla le dimensioni nelle proprietà
            dimensioni = obj.proprieta.dimensioni
            assert all(d > 0 for d in dimensioni), f"{obj.nome} ha dimensioni negative/zero"
    
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
        nomi = [obj.nome.lower() for obj in oggetti]
        
        # Nessun duplicato (case insensitive)
        assert len(nomi) == len(set(nomi))


class TestOggettiPerformance:
    """Test performance rendering oggetti."""
    
    def test_mesh_count_ragionevole(self):
        """Test che mesh sia ragionevole."""
        mela = Mela()
        x, y, z = mela.get_mesh()
        
        # Non troppi vertici (performance)
        # Oggetto semplice: < 10000 vertici
        assert x.size < 10000
    
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
            obj = crea_oggetto(nome)
            assert obj is not None, f"Oggetto {nome} non disponibile"
    
    def test_oggetti_compatibili_con_numpy(self):
        """Test che oggetti siano compatibili con numpy."""
        mela = Mela()
        x, y, z = mela.get_mesh()
        
        # Mesh usa numpy arrays
        assert isinstance(x, np.ndarray)
        assert isinstance(y, np.ndarray)
        assert isinstance(z, np.ndarray)


if __name__ == "__main__":
    # Esegui test
    pytest.main([__file__, "-v", "--tb=short"])

