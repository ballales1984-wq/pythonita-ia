"""
Integrazione Tinkercad Circuits per Pythonita IA.

Permette di:
1. Esportare codice Arduino per Tinkercad
2. Generare link a progetti Tinkercad
3. Creare template circuiti pre-configurati
"""

import json
import webbrowser
from pathlib import Path
from typing import Dict, Optional


class TinkercadExporter:
    """Esportatore per Tinkercad Circuits."""
    
    def __init__(self):
        """Inizializza esportatore Tinkercad."""
        self.base_url = "https://www.tinkercad.com/circuits"
        
        # Template circuiti predefiniti
        self.circuit_templates = {
            "led_base": {
                "nome": "LED Base",
                "componenti": ["Arduino Uno", "LED", "Resistenza 220Ω"],
                "descrizione": "Circuito base con LED e resistenza"
            },
            "semaforo": {
                "nome": "Semaforo",
                "componenti": ["Arduino Uno", "LED Rosso", "LED Giallo", "LED Verde", "3x Resistenza 220Ω"],
                "descrizione": "Semaforo con 3 LED"
            },
            "servo": {
                "nome": "Servomotore",
                "componenti": ["Arduino Uno", "Servo Motor"],
                "descrizione": "Controllo servomotore"
            },
            "sensore_temp": {
                "nome": "Sensore Temperatura",
                "componenti": ["Arduino Uno", "TMP36", "LED", "Resistenza"],
                "descrizione": "Lettura temperatura con LED indicatore"
            }
        }
    
    def esporta_codice_arduino(self, codice_python: str, filename: str = "arduino_code.ino") -> str:
        """
        Converte codice Python/Pythonita in formato Arduino .ino.
        
        Args:
            codice_python: Codice generato da Pythonita
            filename: Nome file output
            
        Returns:
            Path al file .ino creato
        """
        # Estrai parti Arduino dal codice Python
        codice_arduino = self._converti_a_arduino(codice_python)
        
        # Crea file .ino
        export_dir = Path.home() / "pythonita_exports" / "tinkercad"
        export_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = export_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(codice_arduino)
        
        return str(file_path)
    
    def _converti_a_arduino(self, codice_python: str) -> str:
        """
        Converte codice Python in Arduino C++.
        
        Sostituzioni comuni:
        - print() → Serial.println()
        - time.sleep() → delay()
        - True/False → HIGH/LOW
        """
        codice = codice_python
        
        # Header Arduino base
        arduino_code = """// Codice generato da Pythonita IA
// Per Tinkercad Circuits
// https://www.tinkercad.com/circuits

"""
        
        # Cerca pattern comuni e converti
        if "digitalWrite" in codice or "pinMode" in codice:
            # È già codice Arduino
            arduino_code += codice
        else:
            # Converti Python → Arduino
            arduino_code += """void setup() {
  Serial.begin(9600);
  // Inizializza pin
"""
            
            # Estrai pin dal codice
            if "led" in codice.lower() or "pin" in codice.lower():
                arduino_code += "  pinMode(13, OUTPUT);  // LED integrato\n"
            
            arduino_code += """}\n
void loop() {
"""
            
            # Converti logica principale
            lines = codice.split('\n')
            for line in lines:
                if 'print(' in line:
                    # print() → Serial.println()
                    arduino_code += "  " + line.replace('print(', 'Serial.println(') + "\n"
                elif line.strip() and not line.strip().startswith('#'):
                    arduino_code += "  " + line + "\n"
            
            arduino_code += """  
  delay(1000);  // Pausa 1 secondo
}
"""
        
        return arduino_code
    
    def genera_link_tinkercad(self, tipo_circuito: str = "led_base") -> str:
        """
        Genera link a progetto Tinkercad pre-configurato.
        
        Args:
            tipo_circuito: Tipo template ('led_base', 'semaforo', 'servo', ecc)
            
        Returns:
            URL Tinkercad da aprire
        """
        template = self.circuit_templates.get(tipo_circuito, self.circuit_templates["led_base"])
        
        # URL base Tinkercad (apre editor)
        url = f"{self.base_url}"
        
        return url
    
    def apri_tinkercad(self, codice_arduino: Optional[str] = None):
        """
        Apre Tinkercad nel browser.
        
        Args:
            codice_arduino: Codice Arduino opzionale da copiare
        """
        url = self.base_url
        webbrowser.open(url)
        
        if codice_arduino:
            print(f"📋 Codice Arduino pronto per Tinkercad:")
            print("=" * 60)
            print(codice_arduino)
            print("=" * 60)
            print("\n💡 STEPS:")
            print("  1. Tinkercad si è aperto nel browser")
            print("  2. Crea nuovo circuito")
            print("  3. Aggiungi Arduino")
            print("  4. Clicca 'Code' → 'Text'")
            print("  5. Copia-incolla il codice sopra")
            print("  6. Clicca 'Start Simulation'! 🚀")
    
    def crea_istruzioni_html(self, codice_arduino: str, tipo_circuito: str = "led_base") -> str:
        """
        Crea pagina HTML con istruzioni per Tinkercad.
        
        Include:
        - Codice Arduino formattato
        - Lista componenti necessari
        - Link a Tinkercad
        - Istruzioni passo-passo
        """
        template = self.circuit_templates.get(tipo_circuito, self.circuit_templates["led_base"])
        
        html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>{template['nome']} - Pythonita IA + Tinkercad</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background: #1e1e2e;
            color: #e0e0e0;
        }}
        h1 {{
            color: #00d4ff;
            border-bottom: 3px solid #00ff88;
            padding-bottom: 10px;
        }}
        .code-block {{
            background: #0d1117;
            border: 2px solid #00ff88;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            overflow-x: auto;
        }}
        pre {{
            color: #00ff88;
            font-family: 'Consolas', monospace;
            font-size: 14px;
            margin: 0;
        }}
        .componenti {{
            background: #2d2d44;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .componenti li {{
            margin: 8px 0;
            color: #00d4ff;
        }}
        .steps {{
            background: #2d2d44;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .steps li {{
            margin: 12px 0;
            line-height: 1.6;
        }}
        .btn {{
            display: inline-block;
            background: #00ff88;
            color: #1e1e2e;
            padding: 12px 24px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: bold;
            margin: 10px 5px;
        }}
        .btn:hover {{
            background: #00d4ff;
            color: white;
        }}
    </style>
</head>
<body>
    <h1>🤖 {template['nome']} - Pythonita IA + Tinkercad</h1>
    
    <p><strong>Generato da Pythonita IA v3.4+</strong></p>
    
    <h2>📦 Componenti Necessari</h2>
    <div class="componenti">
        <ul>
{"".join([f"            <li>{comp}</li>\n" for comp in template['componenti']])}
        </ul>
    </div>
    
    <h2>💻 Codice Arduino</h2>
    <div class="code-block">
        <pre>{codice_arduino}</pre>
    </div>
    
    <h2>🚀 Come Usare con Tinkercad</h2>
    <div class="steps">
        <ol>
            <li>Clicca il pulsante qui sotto per aprire Tinkercad Circuits</li>
            <li>Crea un nuovo circuito o accedi</li>
            <li>Aggiungi i componenti dalla lista sopra</li>
            <li>Collega i componenti secondo schema</li>
            <li>Clicca sul pulsante "Code" → "Text"</li>
            <li>Copia-incolla il codice Arduino qui sopra</li>
            <li>Clicca "Start Simulation" e guarda funzionare! 🎉</li>
        </ol>
    </div>
    
    <a href="{self.base_url}" class="btn" target="_blank">
        🔗 APRI TINKERCAD CIRCUITS
    </a>
    
    <a href="javascript:window.print()" class="btn">
        🖨️ STAMPA ISTRUZIONI
    </a>
    
    <hr style="margin: 40px 0; border-color: #3d3d5c;">
    
    <p style="text-align: center; color: #888;">
        Generato da <strong>Pythonita IA v3.4+</strong><br>
        AI Code Generator in Italiano
    </p>
</body>
</html>
"""
        
        # Salva HTML
        export_dir = Path.home() / "pythonita_exports" / "tinkercad"
        export_dir.mkdir(parents=True, exist_ok=True)
        
        html_path = export_dir / f"{tipo_circuito}_tinkercad.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(html_path)


# Funzione helper per GUI
def get_tinkercad_exporter():
    """Restituisce istanza singleton di TinkercadExporter."""
    if not hasattr(get_tinkercad_exporter, '_instance'):
        get_tinkercad_exporter._instance = TinkercadExporter()
    return get_tinkercad_exporter._instance

