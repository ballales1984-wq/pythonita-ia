"""
Command Registry - Database centralizzato di tutti i comandi Python supportati.
Design Pattern: Registry + Factory
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Callable


@dataclass
class CommandDefinition:
    """Definizione di un comando Python."""
    name: str                          # Nome interno (es: "print")
    italian_names: List[str]           # Sinonimi italiani
    category: str                      # Categoria (builtin, stdlib, ops)
    description: str                   # Descrizione
    example_italian: str               # Esempio italiano
    example_code: str                  # Esempio codice
    tier_required: str = "FREE"        # Tier minimo richiesto


class CommandRegistry:
    """
    Registry centralizzato di tutti i comandi supportati.
    Singleton pattern.
    """
    
    _instance: Optional['CommandRegistry'] = None
    
    def __init__(self):
        """Inizializza registry."""
        self.commands: Dict[str, CommandDefinition] = {}
        self._load_commands()
    
    @classmethod
    def get_instance(cls) -> 'CommandRegistry':
        """Ottiene istanza singleton."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _load_commands(self):
        """Carica tutti i comandi supportati."""
        # Built-in functions
        self._register_builtins()
        
        # Standard library
        self._register_stdlib()
        
        # Operazioni comuni
        self._register_common_ops()
        
        # Comandi robotica (PRO tier)
        self._register_robotics()
    
    def _register_builtins(self):
        """Registra built-in functions."""
        builtins = [
            CommandDefinition(
                name="print",
                italian_names=["stampa", "print", "scrivi", "mostra", "visualizza"],
                category="builtin",
                description="Stampa output",
                example_italian="stampa ciao mondo",
                example_code='print("ciao mondo")',
                tier_required="FREE"
            ),
            CommandDefinition(
                name="len",
                italian_names=["lunghezza", "len", "dimensione", "conta"],
                category="builtin",
                description="Lunghezza oggetto",
                example_italian="lunghezza della lista",
                example_code="len(lista)",
                tier_required="FREE"
            ),
            CommandDefinition(
                name="range",
                italian_names=["intervallo", "range", "sequenza"],
                category="builtin",
                description="Genera sequenza numeri",
                example_italian="intervallo da 1 a 10",
                example_code="list(range(1, 11))",
                tier_required="FREE"
            ),
            # ... (altri 60+ builtins)
        ]
        
        for cmd in builtins:
            self.register(cmd)
    
    def _register_stdlib(self):
        """Registra standard library modules."""
        stdlib = [
            CommandDefinition(
                name="datetime",
                italian_names=["data", "ora", "datetime", "tempo"],
                category="stdlib",
                description="Gestione date e ore",
                example_italian="mostra data di oggi",
                example_code="from datetime import datetime\nprint(datetime.now())",
                tier_required="PERSONAL"
            ),
            # ... (altri 50+ moduli)
        ]
        
        for cmd in stdlib:
            self.register(cmd)
    
    def _register_common_ops(self):
        """Registra operazioni comuni."""
        ops = [
            CommandDefinition(
                name="create_list",
                italian_names=["crea lista", "lista", "elenco", "array"],
                category="operation",
                description="Crea lista",
                example_italian="crea lista con 1 2 3",
                example_code="lista = [1, 2, 3]",
                tier_required="FREE"
            ),
            # ... (altri 30+ ops)
        ]
        
        for cmd in ops:
            self.register(cmd)
    
    def _register_robotics(self):
        """Registra comandi robotica (tier PRO)."""
        robotics = [
            CommandDefinition(
                name="robot_open_hand",
                italian_names=["apri mano", "apri la mano"],
                category="robotics",
                description="Apri mano robotica",
                example_italian="apri mano destra",
                example_code="hand.open()",
                tier_required="PRO"
            ),
            CommandDefinition(
                name="robot_grasp",
                italian_names=["afferra", "prendi", "solleva"],
                category="robotics",
                description="Afferra oggetto",
                example_italian="afferra la mela",
                example_code='hand.grasp("apple")',
                tier_required="PRO"
            ),
            # ... (altri comandi robot)
        ]
        
        for cmd in robotics:
            self.register(cmd)
    
    def register(self, command: CommandDefinition):
        """Registra un comando."""
        self.commands[command.name] = command
    
    def find_by_italian(self, text: str) -> Optional[CommandDefinition]:
        """Trova comando da sinonimo italiano."""
        text_lower = text.lower()
        
        for cmd in self.commands.values():
            if any(italian in text_lower for italian in cmd.italian_names):
                return cmd
        
        return None
    
    def get(self, name: str) -> Optional[CommandDefinition]:
        """Ottiene comando per nome."""
        return self.commands.get(name)
    
    def get_all_for_tier(self, tier: str) -> List[CommandDefinition]:
        """Ottiene tutti i comandi disponibili per un tier."""
        tier_priority = {"FREE": 0, "TRIAL": 4, "PERSONAL": 1, "PRO": 2, "ENTERPRISE": 3}
        user_level = tier_priority.get(tier, 0)
        
        return [
            cmd for cmd in self.commands.values()
            if tier_priority.get(cmd.tier_required, 0) <= user_level
        ]


# Singleton getter
def get_registry() -> CommandRegistry:
    """Ottiene istanza singleton del registry."""
    return CommandRegistry.get_instance()


def get_command(name: str) -> Optional[CommandDefinition]:
    """Helper per ottenere comando."""
    return get_registry().get(name)

