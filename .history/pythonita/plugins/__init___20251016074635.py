"""
Plugin System - Sistema di plugin per estendere Pythonita.
Permette a sviluppatori di terze parti di aggiungere funzionalità.
"""

from .plugin_api import Plugin, PluginManager, PluginInfo
from .plugin_loader import load_plugin, discover_plugins

__all__ = [
    'Plugin',
    'PluginManager',
    'PluginInfo',
    'load_plugin',
    'discover_plugins',
]

