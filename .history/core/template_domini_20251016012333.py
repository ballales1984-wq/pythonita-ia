"""
Template per domini specifici: Robotica, Hardware, IoT.
Permette di scegliere un template e generare codice specializzato.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class TemplateInfo:
    """Informazioni su un template."""
    nome: str
    descrizione: str
    tipo: str  # robot, hardware, iot, generico
    comandi_supportati: List[str]
    esempi: List[str]


class TemplateRobot:
    """
    Template per robot senza ruote (umanoidi, bracci robotici).
    Genera codice Python per controllare servomotori, sensori, ecc.
    """
    
    COMANDI_ROBOT = {
        # Movimento mani/bracci
        "muovi_mano": ["muovi mano", "sposta mano", "mano si muove"],
        "afferra": ["afferra", "prendi", "chiudi mano", "grip"],
        "rilascia": ["rilascia", "apri mano", "lascia", "release"],
        "ruota_polso": ["ruota polso", "gira polso", "torci polso"],
        
        # Movimento braccia
        "alza_braccio": ["alza braccio", "solleva braccio", "braccio su"],
        "abbassa_braccio": ["abbassa braccio", "braccio giù"],
        "estendi_braccio": ["estendi braccio", "allunga braccio", "braccio avanti"],
        "ritira_braccio": ["ritira braccio", "braccio indietro"],
        
        # Movimento corpo (umanoide)
        "inclina": ["inclina", "piega", "tilt"],
        "ruota": ["ruota", "gira", "rotate"],
        "equilibrio": ["mantieni equilibrio", "bilancia", "balance"],
        
        # Sensori
        "leggi_sensore": ["leggi sensore", "rileva", "misura"],
        "controlla_distanza": ["controlla distanza", "quanto dista"],
        "rileva_oggetto": ["rileva oggetto", "c'è qualcosa", "detect"],
        
        # Sequenze
        "sequenza": ["sequenza", "routine", "esegui passi"],
        "loop": ["ripeti", "continua", "loop"],
        "attendi": ["aspetta", "attendi", "pausa", "wait"],
    }
    
    @staticmethod
    def genera_muovi_mano(params: Dict) -> str:
        """Genera codice per muovere mano."""
        direzione = params.get('direzione', 'sinistra')
        angolo = params.get('angolo', 90)
        
        return f'''# Muovi mano {direzione}
import robot_api  # Libreria robot (es: ROS, PyBullet, ecc.)

# Imposta angolo servo mano
robot = robot_api.Robot()
robot.mano_{direzione}.set_angolo({angolo})
robot.mano_{direzione}.muovi()

print(f"Mano {direzione} mossa a {{angolo}}°")'''
    
    @staticmethod
    def genera_afferra(params: Dict) -> str:
        """Genera codice per afferrare oggetto."""
        mano = params.get('mano', 'destra')
        forza = params.get('forza', 50)
        
        return f'''# Afferra oggetto con mano {mano}
import robot_api

robot = robot_api.Robot()

# Chiudi dita gradualmente
for i in range(0, {forza}, 5):
    robot.mano_{mano}.chiudi_dita(forza=i)
    robot.sleep(0.1)

# Verifica presa
if robot.mano_{mano}.sensore_contatto():
    print("Oggetto afferrato con successo!")
else:
    print("Nessun oggetto rilevato")'''
    
    @staticmethod
    def genera_rilascia(params: Dict) -> str:
        """Genera codice per rilasciare oggetto."""
        mano = params.get('mano', 'destra')
        
        return f'''# Rilascia oggetto
import robot_api

robot = robot_api.Robot()

# Apri dita
robot.mano_{mano}.apri_dita()
robot.sleep(0.5)

print("Oggetto rilasciato")'''
    
    @staticmethod
    def genera_alza_braccio(params: Dict) -> str:
        """Genera codice per alzare braccio."""
        braccio = params.get('braccio', 'destro')
        altezza = params.get('altezza', 90)
        
        return f'''# Alza braccio {braccio}
import robot_api

robot = robot_api.Robot()

# Movimento fluido braccio
robot.braccio_{braccio}.set_angolo_spalla({altezza})
robot.braccio_{braccio}.muovi_fluido(velocita=30)

print(f"Braccio {braccio} alzato a {{altezza}}°")'''
    
    @staticmethod
    def genera_leggi_sensore(params: Dict) -> str:
        """Genera codice per leggere sensore."""
        tipo_sensore = params.get('tipo', 'distanza')
        
        return f'''# Leggi sensore {tipo_sensore}
import robot_api

robot = robot_api.Robot()

# Leggi valore sensore
valore = robot.sensore_{tipo_sensore}.leggi()
print(f"Sensore {tipo_sensore}: {{valore}}")

# Logica basata su valore
if valore < 20:  # es: distanza < 20cm
    print("Oggetto vicino!")
    robot.stop()
else:
    print("Nessun ostacolo")'''
    
    @staticmethod
    def genera_sequenza_complessa(azioni: List[str]) -> str:
        """Genera sequenza complessa di azioni."""
        return f'''# Sequenza robotica complessa
import robot_api
import time

robot = robot_api.Robot()

print("Inizio sequenza...")

# Sequenza azioni
{chr(10).join(f"# Passo {i+1}: {azione}" for i, azione in enumerate(azioni))}

# Passo 1: Posizione iniziale
robot.reset_posizione()
time.sleep(1)

# Passo 2: Estendi braccio
robot.braccio_destro.estendi(angolo=90)
time.sleep(0.5)

# Passo 3: Afferra oggetto
robot.mano_destra.chiudi_dita(forza=50)
time.sleep(0.5)

# Passo 4: Solleva
robot.braccio_destro.solleva(altezza=100)
time.sleep(0.5)

# Passo 5: Rilascia
robot.mano_destra.apri_dita()

print("Sequenza completata!")'''


class TemplateManiBioniche:
    """Template specifico per mani bioniche/protesi."""
    
    COMANDI_MANO = {
        "chiudi_pugno": ["chiudi pugno", "pugno", "stretta"],
        "apri_mano": ["apri mano", "distendi dita", "mano aperta"],
        "pinza": ["pinza", "pollice indice", "precision grip"],
        "ok": ["segno ok", "gesto ok"],
        "pollice_su": ["pollice su", "thumbs up", "like"],
        "punta": ["punta", "indica", "point"],
        "gesto": ["gesto", "gesture"],
    }
    
    @staticmethod
    def genera_chiudi_pugno(params: Dict) -> str:
        """Genera codice per chiudere pugno."""
        forza = params.get('forza', 70)
        
        return f'''# Chiudi pugno mano bionica
from mano_bionica import ManoBionica

mano = ManoBionica(porta="COM3")  # o altra porta seriale
mano.connetti()

# Chiudi tutte le dita progressivamente
dita = ['pollice', 'indice', 'medio', 'anulare', 'mignolo']
for dito in dita:
    mano.chiudi_dito(dito, forza={forza})
    mano.sleep(0.1)

print("Pugno chiuso")
mano.disconnetti()'''
    
    @staticmethod
    def genera_pinza(params: Dict) -> str:
        """Genera codice per presa di precisione."""
        apertura = params.get('apertura', 20)  # mm
        
        return f'''# Presa a pinza (pollice-indice)
from mano_bionica import ManoBionica

mano = ManoBionica()
mano.connetti()

# Apri altre dita
mano.apri_dito('medio')
mano.apri_dito('anulare')
mano.apri_dito('mignolo')

# Posiziona pollice e indice
mano.posizione_pinza(apertura={apertura})  # {apertura}mm

print(f"Pinza pronta (apertura {{apertura}}mm)")

# Afferra
mano.chiudi_pinza()
print("Oggetto afferrato in presa di precisione")'''
    
    @staticmethod
    def genera_gesto(params: Dict) -> str:
        """Genera codice per gesto specifico."""
        gesto = params.get('tipo', 'ok')
        
        return f'''# Esegui gesto: {gesto}
from mano_bionica import ManoBionica, Gesti

mano = ManoBionica()
mano.connetti()

# Esegui gesto predefinito
mano.esegui_gesto(Gesti.{gesto.upper()})

print(f"Gesto '{gesto}' eseguito")
mano.sleep(2)
mano.reset()'''


class SistemaTemplate:
    """
    Sistema di gestione template per vari domini.
    """
    
    TEMPLATE_DISPONIBILI = {
        'robot': {
            'nome': 'Robot Umanoide',
            'descrizione': 'Robot senza ruote con bracci e mani',
            'classe': TemplateRobot,
            'esempi': [
                'robot muovi mano destra',
                'robot afferra oggetto',
                'robot alza braccio sinistro'
            ]
        },
        'mano_bionica': {
            'nome': 'Mano Bionica/Protesi',
            'descrizione': 'Mano bionica controllabile',
            'classe': TemplateManiBioniche,
            'esempi': [
                'mano chiudi pugno',
                'mano fai pinza',
                'mano gesto ok'
            ]
        },
        'generico': {
            'nome': 'Generico Python',
            'descrizione': 'Codice Python generico',
            'classe': None,  # Usa generatore normale
            'esempi': [
                'stampa ciao',
                'crea lista',
                'leggi file'
            ]
        }
    }
    
    def __init__(self, template_default='generico'):
        """
        Inizializza sistema template.
        
        Args:
            template_default: Template da usare di default
        """
        self.template_attivo = template_default
        self.templates = self.TEMPLATE_DISPONIBILI
    
    def scegli_template(self, nome_template: str) -> bool:
        """
        Seleziona un template specifico.
        
        Args:
            nome_template: Nome del template (robot, mano_bionica, generico)
            
        Returns:
            True se trovato e attivato
        """
        if nome_template in self.templates:
            self.template_attivo = nome_template
            return True
        return False
    
    def get_template_attivo(self) -> str:
        """Ritorna il nome del template attualmente attivo."""
        return self.template_attivo
    
    def get_info_template(self, nome: Optional[str] = None) -> Dict:
        """Ottiene info su un template."""
        nome = nome or self.template_attivo
        return self.templates.get(nome, {})
    
    def lista_template(self) -> List[TemplateInfo]:
        """Lista tutti i template disponibili."""
        infos = []
        for nome, data in self.templates.items():
            info = TemplateInfo(
                nome=nome,
                descrizione=data.get('descrizione', ''),
                tipo=data.get('nome', ''),
                comandi_supportati=[],  # TODO: estrarre da classe
                esempi=data.get('esempi', [])
            )
            infos.append(info)
        return infos
    
    def genera_con_template(self, frase: str, parametri: Optional[Dict] = None) -> str:
        """
        Genera codice usando il template attivo.
        
        Args:
            frase: Comando in italiano
            parametri: Parametri extra
            
        Returns:
            Codice Python specifico per il dominio
        """
        params = parametri or {}
        
        # Identifica comando nel template
        template_info = self.templates[self.template_attivo]
        template_class = template_info['classe']
        
        if template_class is None:
            return None  # Usa generatore generico
        
        # Prova a matchare comando
        if self.template_attivo == 'robot':
            return self._genera_comando_robot(frase, params, template_class)
        elif self.template_attivo == 'mano_bionica':
            return self._genera_comando_mano(frase, params, template_class)
        
        return None
    
    def _genera_comando_robot(self, frase: str, params: Dict, template_class) -> Optional[str]:
        """Genera comando robot."""
        frase_lower = frase.lower()
        
        # Match comandi
        if any(kw in frase_lower for kw in ["muovi mano", "sposta mano"]):
            # Estrai parametri dalla frase
            if "destra" in frase_lower:
                params['direzione'] = 'destra'
            elif "sinistra" in frase_lower:
                params['direzione'] = 'sinistra'
            
            return template_class.genera_muovi_mano(params)
        
        elif any(kw in frase_lower for kw in ["afferra", "prendi", "chiudi mano"]):
            if "destra" in frase_lower:
                params['mano'] = 'destra'
            elif "sinistra" in frase_lower:
                params['mano'] = 'sinistra'
            
            return template_class.genera_afferra(params)
        
        elif any(kw in frase_lower for kw in ["rilascia", "apri mano", "lascia"]):
            if "destra" in frase_lower:
                params['mano'] = 'destra'
            elif "sinistra" in frase_lower:
                params['mano'] = 'sinistra'
            
            return template_class.genera_rilascia(params)
        
        elif any(kw in frase_lower for kw in ["alza braccio", "solleva braccio"]):
            if "destro" in frase_lower or "destra" in frase_lower:
                params['braccio'] = 'destro'
            elif "sinistro" in frase_lower or "sinistra" in frase_lower:
                params['braccio'] = 'sinistro'
            
            return template_class.genera_alza_braccio(params)
        
        elif any(kw in frase_lower for kw in ["leggi sensore", "rileva", "misura"]):
            # Identifica tipo sensore
            if "distanza" in frase_lower:
                params['tipo'] = 'distanza'
            elif "temperatura" in frase_lower:
                params['tipo'] = 'temperatura'
            elif "pressione" in frase_lower:
                params['tipo'] = 'pressione'
            
            return template_class.genera_leggi_sensore(params)
        
        return None
    
    def _genera_comando_mano(self, frase: str, params: Dict, template_class) -> Optional[str]:
        """Genera comando mano bionica."""
        frase_lower = frase.lower()
        
        if any(kw in frase_lower for kw in ["chiudi pugno", "pugno", "stretta"]):
            return template_class.genera_chiudi_pugno(params)
        
        elif any(kw in frase_lower for kw in ["pinza", "pollice indice"]):
            return template_class.genera_pinza(params)
        
        elif any(kw in frase_lower for kw in ["gesto", "gesture"]):
            # Identifica tipo gesto
            if "ok" in frase_lower:
                params['tipo'] = 'ok'
            elif "pollice su" in frase_lower or "like" in frase_lower:
                params['tipo'] = 'thumbs_up'
            elif "punta" in frase_lower:
                params['tipo'] = 'point'
            
            return template_class.genera_gesto(params)
        
        return None


# Singleton
_sistema_template: Optional[SistemaTemplate] = None


def get_sistema_template() -> SistemaTemplate:
    """Ottiene istanza singleton sistema template."""
    global _sistema_template
    if _sistema_template is None:
        _sistema_template = SistemaTemplate()
    return _sistema_template


def scegli_template(nome: str) -> bool:
    """
    Helper per scegliere template.
    
    Args:
        nome: Nome template (robot, mano_bionica, generico)
        
    Returns:
        True se attivato
    """
    return get_sistema_template().scegli_template(nome)


def genera_con_template(frase: str, parametri: Optional[Dict] = None) -> Optional[str]:
    """
    Helper per generare con template attivo.
    
    Args:
        frase: Comando in italiano
        parametri: Parametri opzionali
        
    Returns:
        Codice generato o None
    """
    return get_sistema_template().genera_con_template(frase, parametri)

