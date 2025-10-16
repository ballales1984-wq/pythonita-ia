"""
Plugin API - API base per creare plugin per Pythonita.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable, Any
from pathlib import Path
import logging
import importlib.util

logger = logging.getLogger(__name__)


@dataclass
class PluginInfo:
    """Informazioni su un plugin."""
    name: str
    version: str
    author: str
    description: str
    homepage: Optional[str] = None
    license: str = "Unknown"
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class Plugin(ABC):
    """
    Classe base per plugin Pythonita.
    
    Tutti i plugin devono ereditare da questa classe e implementare
    i metodi astratti.
    
    Example:
        ```python
        class MyPlugin(Plugin):
            def get_info(self):
                return PluginInfo(
                    name="MyPlugin",
                    version="1.0.0",
                    author="Your Name",
                    description="My custom plugin"
                )
            
            def initialize(self, context):
                print("Plugin initialized!")
                
            def shutdown(self):
                print("Plugin shutdown!")
        ```
    """
    
    @abstractmethod
    def get_info(self) -> PluginInfo:
        """
        Ritorna informazioni sul plugin.
        
        Returns:
            PluginInfo con nome, versione, autore, ecc.
        """
        pass
    
    @abstractmethod
    def initialize(self, context: Dict[str, Any]):
        """
        Inizializza il plugin.
        
        Args:
            context: Contesto applicazione con riferimenti utili:
                - code_generator: Generatore codice
                - command_registry: Registro comandi
                - license_manager: Gestore licenze
                - etc.
        """
        pass
    
    @abstractmethod
    def shutdown(self):
        """
        Chiude il plugin e libera risorse.
        """
        pass
    
    def on_command_parsed(self, command: str, parsed_data: Dict) -> Optional[Dict]:
        """
        Hook chiamato dopo parsing comando.
        
        Args:
            command: Comando originale
            parsed_data: Dati parsati
            
        Returns:
            Dati modificati o None
        """
        return None
    
    def on_code_generated(self, code: str, metadata: Dict) -> Optional[str]:
        """
        Hook chiamato dopo generazione codice.
        
        Args:
            code: Codice generato
            metadata: Metadata generazione
            
        Returns:
            Codice modificato o None
        """
        return None
    
    def register_commands(self) -> Dict[str, Callable]:
        """
        Registra nuovi comandi custom.
        
        Returns:
            Dict[comando_nome, handler_function]
        """
        return {}
    
    def register_3d_objects(self) -> Dict[str, type]:
        """
        Registra nuovi oggetti 3D custom.
        
        Returns:
            Dict[oggetto_nome, classe_oggetto]
        """
        return {}
    
    def register_templates(self) -> Dict[str, str]:
        """
        Registra nuovi template custom.
        
        Returns:
            Dict[template_nome, template_string]
        """
        return {}


class PluginManager:
    """
    Gestisce il ciclo di vita dei plugin.
    
    Responsabile di:
    - Caricamento/scaricamento plugin
    - Chiamata hooks
    - Registrazione comandi/oggetti custom
    """
    
    def __init__(self):
        """Inizializza plugin manager."""
        self.plugins: Dict[str, Plugin] = {}
        self.context: Dict[str, Any] = {}
        self.hooks_enabled = True
        
        logger.info("PluginManager initialized")
    
    def set_context(self, context: Dict[str, Any]):
        """
        Imposta contesto applicazione.
        
        Args:
            context: Contesto con riferimenti a code_generator, etc.
        """
        self.context = context
        logger.info(f"Context set with {len(context)} keys")
    
    def load_plugin(self, plugin: Plugin) -> bool:
        """
        Carica e inizializza un plugin.
        
        Args:
            plugin: Istanza plugin da caricare
            
        Returns:
            True se caricato con successo
        """
        try:
            info = plugin.get_info()
            
            if info.name in self.plugins:
                logger.warning(f"Plugin {info.name} già caricato")
                return False
            
            # Inizializza plugin
            plugin.initialize(self.context)
            
            # Registra plugin
            self.plugins[info.name] = plugin
            
            logger.info(f"Plugin caricato: {info.name} v{info.version}")
            return True
            
        except Exception as e:
            logger.error(f"Errore caricamento plugin: {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Scarica un plugin.
        
        Args:
            plugin_name: Nome plugin da scaricare
            
        Returns:
            True se scaricato con successo
        """
        if plugin_name not in self.plugins:
            logger.warning(f"Plugin {plugin_name} non trovato")
            return False
        
        try:
            plugin = self.plugins[plugin_name]
            plugin.shutdown()
            
            del self.plugins[plugin_name]
            
            logger.info(f"Plugin scaricato: {plugin_name}")
            return True
            
        except Exception as e:
            logger.error(f"Errore scaricamento plugin {plugin_name}: {e}")
            return False
    
    def get_loaded_plugins(self) -> List[PluginInfo]:
        """
        Ottiene lista plugin caricati.
        
        Returns:
            Lista di PluginInfo
        """
        return [plugin.get_info() for plugin in self.plugins.values()]
    
    def call_hook_command_parsed(self, command: str, parsed_data: Dict) -> Dict:
        """
        Chiama hook on_command_parsed su tutti i plugin.
        
        Args:
            command: Comando originale
            parsed_data: Dati parsati
            
        Returns:
            Dati parsati (possibilmente modificati)
        """
        if not self.hooks_enabled:
            return parsed_data
        
        result = parsed_data
        
        for plugin in self.plugins.values():
            try:
                modified = plugin.on_command_parsed(command, result)
                if modified is not None:
                    result = modified
            except Exception as e:
                logger.error(f"Errore hook command_parsed in {plugin.get_info().name}: {e}")
        
        return result
    
    def call_hook_code_generated(self, code: str, metadata: Dict) -> str:
        """
        Chiama hook on_code_generated su tutti i plugin.
        
        Args:
            code: Codice generato
            metadata: Metadata generazione
            
        Returns:
            Codice (possibilmente modificato)
        """
        if not self.hooks_enabled:
            return code
        
        result = code
        
        for plugin in self.plugins.values():
            try:
                modified = plugin.on_code_generated(result, metadata)
                if modified is not None:
                    result = modified
            except Exception as e:
                logger.error(f"Errore hook code_generated in {plugin.get_info().name}: {e}")
        
        return result
    
    def get_custom_commands(self) -> Dict[str, Callable]:
        """
        Raccoglie tutti i comandi custom dai plugin.
        
        Returns:
            Dict[comando_nome, handler_function]
        """
        commands = {}
        
        for plugin in self.plugins.values():
            try:
                plugin_commands = plugin.register_commands()
                commands.update(plugin_commands)
            except Exception as e:
                logger.error(f"Errore registrazione comandi da {plugin.get_info().name}: {e}")
        
        return commands
    
    def get_custom_3d_objects(self) -> Dict[str, type]:
        """
        Raccoglie tutti gli oggetti 3D custom dai plugin.
        
        Returns:
            Dict[oggetto_nome, classe_oggetto]
        """
        objects = {}
        
        for plugin in self.plugins.values():
            try:
                plugin_objects = plugin.register_3d_objects()
                objects.update(plugin_objects)
            except Exception as e:
                logger.error(f"Errore registrazione oggetti 3D da {plugin.get_info().name}: {e}")
        
        return objects
    
    def get_custom_templates(self) -> Dict[str, str]:
        """
        Raccoglie tutti i template custom dai plugin.
        
        Returns:
            Dict[template_nome, template_string]
        """
        templates = {}
        
        for plugin in self.plugins.values():
            try:
                plugin_templates = plugin.register_templates()
                templates.update(plugin_templates)
            except Exception as e:
                logger.error(f"Errore registrazione template da {plugin.get_info().name}: {e}")
        
        return templates
    
    def enable_hooks(self):
        """Abilita chiamata hooks."""
        self.hooks_enabled = True
        logger.info("Hooks abilitati")
    
    def disable_hooks(self):
        """Disabilita chiamata hooks."""
        self.hooks_enabled = False
        logger.info("Hooks disabilitati")


# Singleton instance
_plugin_manager = None


def get_plugin_manager() -> PluginManager:
    """Ottiene istanza singleton plugin manager."""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager

