"""
Plugin Loader - Carica plugin da file o directory.
"""

import os
import sys
import importlib.util
from pathlib import Path
from typing import List, Optional
import logging

from .plugin_api import Plugin

logger = logging.getLogger(__name__)


def load_plugin(plugin_path: Path) -> Optional[Plugin]:
    """
    Carica un plugin da file .py
    
    Args:
        plugin_path: Path al file plugin
        
    Returns:
        Istanza Plugin o None se errore
    """
    try:
        # Verifica file esista
        if not plugin_path.exists():
            logger.error(f"File plugin non trovato: {plugin_path}")
            return None
        
        # Carica modulo
        module_name = plugin_path.stem
        spec = importlib.util.spec_from_file_location(module_name, plugin_path)
        
        if spec is None or spec.loader is None:
            logger.error(f"Impossibile caricare spec per {plugin_path}")
            return None
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        # Cerca classe Plugin
        plugin_class = None
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, Plugin) and attr != Plugin:
                plugin_class = attr
                break
        
        if plugin_class is None:
            logger.error(f"Nessuna classe Plugin trovata in {plugin_path}")
            return None
        
        # Istanzia plugin
        plugin_instance = plugin_class()
        
        logger.info(f"Plugin caricato da {plugin_path}")
        return plugin_instance
        
    except Exception as e:
        logger.error(f"Errore caricamento plugin da {plugin_path}: {e}")
        return None


def discover_plugins(plugins_dir: Path) -> List[Plugin]:
    """
    Scopre e carica tutti i plugin in una directory.
    
    Args:
        plugins_dir: Directory contenente plugin (.py files)
        
    Returns:
        Lista di plugin caricati
    """
    plugins = []
    
    if not plugins_dir.exists():
        logger.warning(f"Directory plugin non trovata: {plugins_dir}")
        return plugins
    
    # Cerca file .py
    for plugin_file in plugins_dir.glob("*.py"):
        # Salta __init__.py
        if plugin_file.name.startswith("__"):
            continue
        
        plugin = load_plugin(plugin_file)
        if plugin:
            plugins.append(plugin)
    
    logger.info(f"Scoperti {len(plugins)} plugin in {plugins_dir}")
    return plugins


def get_default_plugins_directory() -> Path:
    """
    Ottiene directory default per plugin utente.
    
    Returns:
        Path a ~/.pythonita/plugins/
    """
    plugins_dir = Path.home() / ".pythonita" / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    return plugins_dir

