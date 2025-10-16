"""
Example Plugin - Esempio di plugin per Pythonita.

Questo plugin dimostra come:
- Creare un plugin custom
- Registrare comandi personalizzati
- Aggiungere oggetti 3D custom
- Usare hooks per modificare comportamento

Per usarlo:
1. Copia questo file in ~/.pythonita/plugins/
2. Riavvia Pythonita
3. Il plugin verrà caricato automaticamente
"""

from pythonita.plugins import Plugin, PluginInfo
import numpy as np


class ExamplePlugin(Plugin):
    """Plugin di esempio che aggiunge comandi e oggetti custom."""
    
    def get_info(self) -> PluginInfo:
        """Informazioni plugin."""
        return PluginInfo(
            name="ExamplePlugin",
            version="1.0.0",
            author="Pythonita Team",
            description="Plugin di esempio che dimostra le funzionalità dell'API",
            homepage="https://github.com/pythonita-ia/example-plugin",
            license="MIT",
            dependencies=["numpy"]
        )
    
    def initialize(self, context):
        """Inizializzazione plugin."""
        print(f"[{self.get_info().name}] Plugin inizializzato!")
        self.context = context
        self.counter = 0
    
    def shutdown(self):
        """Chiusura plugin."""
        print(f"[{self.get_info().name}] Plugin chiuso. Comandi eseguiti: {self.counter}")
    
    def on_command_parsed(self, command: str, parsed_data: dict):
        """
        Hook chiamato dopo parsing comando.
        Aggiunge metadata custom.
        """
        if parsed_data:
            parsed_data['plugin_processed'] = True
            parsed_data['processed_by'] = self.get_info().name
        return parsed_data
    
    def on_code_generated(self, code: str, metadata: dict):
        """
        Hook chiamato dopo generazione codice.
        Aggiunge commento header.
        """
        header = f"# Generated with {self.get_info().name} v{self.get_info().version}\n"
        return header + code
    
    def register_commands(self):
        """
        Registra comandi custom.
        
        Returns:
            Dict[comando_nome, handler_function]
        """
        return {
            'saluta': self._comando_saluta,
            'conta': self._comando_conta,
            'calcola_fibonacci': self._comando_fibonacci,
        }
    
    def register_3d_objects(self):
        """
        Registra oggetti 3D custom.
        
        Returns:
            Dict[oggetto_nome, classe_oggetto]
        """
        return {
            'piramide': PiramideCustom,
            'stella': StellaCustom,
        }
    
    def register_templates(self):
        """
        Registra template custom.
        
        Returns:
            Dict[template_nome, template_string]
        """
        return {
            'saluto_custom': 'print("Ciao dal plugin custom!")',
            'loop_custom': 'for i in range({n}):\n    print(f"Iterazione {{i}}")',
        }
    
    # ═══════════════════════════════════════════════════════════
    # COMANDI CUSTOM
    # ═══════════════════════════════════════════════════════════
    
    def _comando_saluta(self, *args, **kwargs):
        """Comando custom: saluta."""
        self.counter += 1
        nome = kwargs.get('nome', 'Mondo')
        return f'print("Ciao, {nome}! Questo è un comando custom.")'
    
    def _comando_conta(self, *args, **kwargs):
        """Comando custom: conta fino a N."""
        self.counter += 1
        n = kwargs.get('n', 10)
        return f'''
for i in range(1, {n} + 1):
    print(f"Conteggio: {{i}}")
print("Conteggio completato!")
'''
    
    def _comando_fibonacci(self, *args, **kwargs):
        """Comando custom: sequenza Fibonacci."""
        self.counter += 1
        n = kwargs.get('n', 10)
        return f'''
def fibonacci(n):
    a, b = 0, 1
    sequence = []
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

fib = fibonacci({n})
print(f"Sequenza Fibonacci ({n} termini): {{fib}}")
'''


# ═══════════════════════════════════════════════════════════════
# OGGETTI 3D CUSTOM
# ═══════════════════════════════════════════════════════════════

class PiramideCustom:
    """Oggetto 3D custom: Piramide."""
    
    def __init__(self, posizione=(0, 15, 0)):
        self.nome = "Piramide Custom"
        self.posizione = posizione
        self.altezza = 10.0
        self.base = 8.0
        self.colore = (1.0, 0.84, 0.0)  # Oro
    
    def get_mesh(self):
        """Genera mesh piramide."""
        # Vertici base
        x_base = np.array([-self.base/2, self.base/2, self.base/2, -self.base/2, -self.base/2])
        y_base = np.array([0, 0, 0, 0, 0])
        z_base = np.array([-self.base/2, -self.base/2, self.base/2, self.base/2, -self.base/2])
        
        # Vertice apice
        x_apex = np.array([0])
        y_apex = np.array([self.altezza])
        z_apex = np.array([0])
        
        # Applica posizione
        x_base += self.posizione[0]
        y_base += self.posizione[1]
        z_base += self.posizione[2]
        
        x_apex += self.posizione[0]
        y_apex += self.posizione[1]
        z_apex += self.posizione[2]
        
        return (x_base, y_base, z_base), (x_apex, y_apex, z_apex)


class StellaCustom:
    """Oggetto 3D custom: Stella."""
    
    def __init__(self, posizione=(0, 15, 0)):
        self.nome = "Stella Custom"
        self.posizione = posizione
        self.raggio = 5.0
        self.colore = (1.0, 1.0, 0.0)  # Giallo
    
    def get_mesh(self):
        """Genera mesh stella (versione semplificata come sfera con punte)."""
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        
        x = self.raggio * np.outer(np.cos(u), np.sin(v))
        y = self.raggio * np.outer(np.sin(u), np.sin(v))
        z = self.raggio * np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Applica posizione
        x += self.posizione[0]
        y += self.posizione[1]
        z += self.posizione[2]
        
        return x, y, z


if __name__ == "__main__":
    # Test plugin
    print("Testing ExamplePlugin...")
    
    plugin = ExamplePlugin()
    info = plugin.get_info()
    
    print(f"\nPlugin Info:")
    print(f"  Nome: {info.name}")
    print(f"  Versione: {info.version}")
    print(f"  Autore: {info.author}")
    print(f"  Descrizione: {info.description}")
    
    # Test initialize
    plugin.initialize({})
    
    # Test comandi
    print(f"\nComandi registrati: {list(plugin.register_commands().keys())}")
    print(f"Oggetti 3D registrati: {list(plugin.register_3d_objects().keys())}")
    print(f"Template registrati: {list(plugin.register_templates().keys())}")
    
    # Test comando
    code = plugin._comando_saluta(nome="Pythonita")
    print(f"\nCodice generato da comando 'saluta':")
    print(code)
    
    # Test shutdown
    plugin.shutdown()
    
    print("\n✅ Plugin testato con successo!")

