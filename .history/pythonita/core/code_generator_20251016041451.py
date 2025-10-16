"""
Code Generator - Genera codice Python da comandi parsati.
Design Pattern: Strategy + Template Method
"""

from abc import ABC, abstractmethod
from typing import Optional
import logging

from .nlp_parser import ParsedCommand, parse_italian

logger = logging.getLogger(__name__)


class GenerationStrategy(ABC):
    """Strategia astratta per generazione codice."""
    
    @abstractmethod
    def can_handle(self, command: ParsedCommand) -> bool:
        """Determina se questa strategia può gestire il comando."""
        pass
    
    @abstractmethod
    def generate(self, command: ParsedCommand) -> Optional[str]:
        """Genera codice per il comando."""
        pass
    
    @property
    @abstractmethod
    def priority(self) -> int:
        """Priorità strategia (1=alta, 10=bassa)."""
        pass


class AIGenerationStrategy(GenerationStrategy):
    """Strategia basata su AI locale (Ollama/Llama)."""
    
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.ai_available = False
        if enabled:
            self._check_ai_availability()
    
    def _check_ai_availability(self):
        """Verifica se AI è disponibile."""
        try:
            import requests
            r = requests.get("http://127.0.0.1:11434/api/tags", timeout=1)
            self.ai_available = r.status_code == 200
            if self.ai_available:
                logger.info("AI Engine disponibile")
        except:
            self.ai_available = False
            logger.info("AI Engine non disponibile, uso fallback")
    
    def can_handle(self, command: ParsedCommand) -> bool:
        return self.enabled and self.ai_available
    
    def generate(self, command: ParsedCommand) -> Optional[str]:
        """Genera codice usando AI."""
        if not self.ai_available:
            return None
        
        try:
            import requests
            prompt = self._build_prompt(command)
            
            response = requests.post("http://127.0.0.1:11434/api/chat",
                json={
                    "model": "llama3.2",
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False
                },
                timeout=10
            )
            
            if response.status_code == 200:
                code = response.json()['message']['content']
                return self._extract_code(code)
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
        
        return None
    
    def _build_prompt(self, command: ParsedCommand) -> str:
        """Costruisce prompt per AI."""
        return f"""Genera codice Python per questo comando italiano:
"{command.original_text}"

Intent: {command.intent}
Entities: {command.entities}

Regole:
- Solo codice Python, no spiegazioni
- Commenti in italiano
- Codice pulito e professionale
"""
    
    def _extract_code(self, response: str) -> str:
        """Estrae blocco codice da risposta AI."""
        # Rimuovi markdown code blocks
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            return response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            return response[start:end].strip()
        return response.strip()
    
    @property
    def priority(self) -> int:
        return 1  # Priorità alta


class RuleGenerationStrategy(GenerationStrategy):
    """Strategia basata su regole fisse (fallback garantito)."""
    
    def can_handle(self, command: ParsedCommand) -> bool:
        return command.intent != "unknown"
    
    def generate(self, command: ParsedCommand) -> Optional[str]:
        """Genera codice usando regole."""
        intent = command.intent
        entities = command.entities
        
        # Dispatch su intent
        generators = {
            "stampa": self._gen_print,
            "lista": self._gen_list,
            "somma": self._gen_sum,
            "robot_apri_mano": self._gen_robot_open_hand,
            "robot_chiudi_mano": self._gen_robot_close_hand,
            "robot_afferra": self._gen_robot_grasp,
        }
        
        generator_func = generators.get(intent)
        if generator_func:
            return generator_func(entities)
        
        return None
    
    def _gen_print(self, entities: Dict) -> str:
        """Genera codice print."""
        text = entities.get('text', 'ciao mondo')
        return f'print("{text}")'
    
    def _gen_list(self, entities: Dict) -> str:
        """Genera codice lista."""
        numbers = entities.get('numbers', [1, 2, 3])
        return f'lista = {numbers}\nprint(lista)'
    
    def _gen_sum(self, entities: Dict) -> str:
        """Genera codice somma."""
        nums = entities.get('numbers', [0, 0])
        if len(nums) >= 2:
            return f'''num1 = {nums[0]}
num2 = {nums[1]}
risultato = num1 + num2
print(f"{{num1}} + {{num2}} = {{risultato}}")'''
        return "# Errore: servono 2 numeri"
    
    def _gen_robot_open_hand(self, entities: Dict) -> str:
        """Genera codice apertura mano robot."""
        return '''# Apri mano robotica
from robot_api import RoboticHand

hand = RoboticHand()
hand.open(speed=1.0)
print("Mano aperta")'''
    
    def _gen_robot_close_hand(self, entities: Dict) -> str:
        """Genera codice chiusura mano."""
        return '''# Chiudi mano robotica
from robot_api import RoboticHand

hand = RoboticHand()
hand.close(force=0.7)
print("Mano chiusa")'''
    
    def _gen_robot_grasp(self, entities: Dict) -> str:
        """Genera codice afferra oggetto."""
        obj = entities.get('object', 'oggetto')
        return f'''# Afferra {obj}
from robot_api import RoboticHand

hand = RoboticHand()
hand.grasp(target="{obj}", force=0.5)
print("Oggetto afferrato")'''
    
    @property
    def priority(self) -> int:
        return 5  # Priorità media


class TemplateGenerationStrategy(GenerationStrategy):
    """Strategia basata su template pre-definiti."""
    
    def __init__(self, template_name="generic"):
        self.template_name = template_name
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Carica template disponibili."""
        return {
            "generic": {},
            "robot": {
                "muovi_mano": "hand.move(angle={angle})",
                "afferra": "hand.grasp(force=0.7)",
            },
            "mano_bionica": {
                "chiudi_pugno": "bionic_hand.close_fist()",
                "pinza": "bionic_hand.pinch(aperture={aperture})",
            }
        }
    
    def can_handle(self, command: ParsedCommand) -> bool:
        return command.intent.startswith("robot_") and self.template_name != "generic"
    
    def generate(self, command: ParsedCommand) -> Optional[str]:
        """Genera da template."""
        # Template-based generation
        template = self.templates.get(self.template_name, {})
        # TODO: Implementa template matching
        return None
    
    @property
    def priority(self) -> int:
        return 3  # Priorità alta per template specifici


class CodeGenerator:
    """
    Generatore principale di codice.
    Usa strategia composita con fallback multipli.
    """
    
    def __init__(self, use_ai=True, use_cache=True, template="generic"):
        """
        Inizializza generatore.
        
        Args:
            use_ai: Abilita AI generation
            use_cache: Usa cache per speedup
            template: Template dominio (generic, robot, mano_bionica)
        """
        self.use_cache = use_cache
        self.cache = None
        
        # Strategieordinate per priorità
        self.strategies: List[GenerationStrategy] = []
        
        if use_ai:
            self.strategies.append(AIGenerationStrategy(enabled=True))
        
        if template != "generic":
            self.strategies.append(TemplateGenerationStrategy(template))
        
        self.strategies.append(RuleGenerationStrategy())
        
        # Ordina per priorità
        self.strategies.sort(key=lambda s: s.priority)
        
        logger.info(f"Generator inizializzato con {len(self.strategies)} strategie")
    
    def generate(self, text: str) -> str:
        """
        Genera codice Python da testo italiano.
        
        Args:
            text: Comando in italiano
            
        Returns:
            Codice Python generato
        """
        # 0. Verifica cache
        if self.use_cache and self.cache:
            cached = self.cache.get(text)
            if cached:
                logger.info("Cache hit")
                return cached
        
        # 1. Parse comando
        command = parse_italian(text)
        logger.debug(f"Parsed: {command.intent}")
        
        # 2. Prova strategie in ordine di priorità
        for strategy in self.strategies:
            if strategy.can_handle(command):
                code = strategy.generate(command)
                if code:
                    logger.info(f"Generato con {strategy.__class__.__name__}")
                    
                    # Salva in cache
                    if self.use_cache and self.cache:
                        self.cache.set(text, code)
                    
                    return code
        
        # 3. Fallback: errore
        return f"# Comando non riconosciuto: {text}"


# Helper function
def generate_code(text: str, **kwargs) -> str:
    """
    Helper rapido per generazione codice.
    
    Args:
        text: Comando italiano
        **kwargs: Parametri per CodeGenerator
        
    Returns:
        Codice Python
    """
    generator = CodeGenerator(**kwargs)
    return generator.generate(text)

