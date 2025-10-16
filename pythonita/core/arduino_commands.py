"""
Template e regole per comandi Arduino.
Integrazione con il sistema di code generation di Pythonita.
"""

# Template comandi Arduino
ARDUINO_COMMAND_TEMPLATES = {
    'accendi_led': {
        'keywords': ['accendi', 'attiva', 'turn on', 'on'],
        'entities': ['led', 'luce', 'light'],
        'template': """# Accendi LED su pin {pin}
import serial
import time

arduino = serial.Serial('{port}', 9600, timeout=1)
time.sleep(2)  # Attendi reset Arduino

# Accendi LED
arduino.write(b'D{pin},1\\n')
print("LED pin {pin} acceso")

arduino.close()
""",
        'default_params': {'pin': 13, 'port': 'COM3'}
    },
    
    'spegni_led': {
        'keywords': ['spegni', 'disattiva', 'turn off', 'off'],
        'entities': ['led', 'luce', 'light'],
        'template': """# Spegni LED su pin {pin}
import serial
import time

arduino = serial.Serial('{port}', 9600, timeout=1)
time.sleep(2)

# Spegni LED
arduino.write(b'D{pin},0\\n')
print("LED pin {pin} spento")

arduino.close()
""",
        'default_params': {'pin': 13, 'port': 'COM3'}
    },
    
    'lampeggia_led': {
        'keywords': ['lampeggia', 'blink', 'flash'],
        'entities': ['led', 'luce', 'light'],
        'template': """# Lampeggia LED su pin {pin}
import serial
import time

arduino = serial.Serial('{port}', 9600, timeout=1)
time.sleep(2)

# Lampeggia {times} volte
for i in range({times}):
    arduino.write(b'D{pin},1\\n')  # Accendi
    time.sleep({delay})
    arduino.write(b'D{pin},0\\n')  # Spegni
    time.sleep({delay})
    print(f"Lampeggio {{i+1}}/{times}")

arduino.close()
print("Lampeggio completato")
""",
        'default_params': {'pin': 13, 'times': 3, 'delay': 0.5, 'port': 'COM3'}
    },
    
    'leggi_sensore': {
        'keywords': ['leggi', 'read', 'misura', 'measure'],
        'entities': ['sensore', 'sensor', 'temperatura', 'luce', 'distanza'],
        'template': """# Leggi sensore analogico su pin A{pin}
import serial
import time

arduino = serial.Serial('{port}', 9600, timeout=1)
time.sleep(2)

# Richiedi lettura sensore
arduino.write(b'R{pin}\\n')
time.sleep(0.1)

# Leggi risposta
if arduino.in_waiting > 0:
    valore = arduino.readline().decode('utf-8').strip()
    print(f"Valore sensore pin A{pin}: {{valore}}")
else:
    print("Nessuna risposta dall'Arduino")

arduino.close()
""",
        'default_params': {'pin': 0, 'port': 'COM3'}
    },
    
    'muovi_servo': {
        'keywords': ['muovi', 'ruota', 'move', 'rotate'],
        'entities': ['servo', 'servomotore', 'motore'],
        'template': """# Muovi servomotore su pin {pin}
import serial
import time

arduino = serial.Serial('{port}', 9600, timeout=1)
time.sleep(2)

# Muovi servo a {angle} gradi
arduino.write(b'S{pin},{angle}\\n')
print(f"Servo pin {pin} mosso a {angle} gradi")

arduino.close()
""",
        'default_params': {'pin': 9, 'angle': 90, 'port': 'COM3'}
    },
    
    'controlla_motore': {
        'keywords': ['controlla', 'control', 'velocità', 'speed'],
        'entities': ['motore', 'motor', 'ventola', 'fan'],
        'template': """# Controlla velocità motore (PWM) su pin {pin}
import serial
import time

arduino = serial.Serial('{port}', 9600, timeout=1)
time.sleep(2)

# Imposta velocità {speed} (0-255)
arduino.write(b'A{pin},{speed}\\n')
print(f"Motore pin {pin} impostato a velocità {speed}/255")

arduino.close()
""",
        'default_params': {'pin': 3, 'speed': 128, 'port': 'COM3'}
    },
    
    'sequenza_led': {
        'keywords': ['sequenza', 'sequence', 'animazione'],
        'entities': ['led', 'luci', 'lights'],
        'template': """# Sequenza LED multipli
import serial
import time

arduino = serial.Serial('{port}', 9600, timeout=1)
time.sleep(2)

led_pins = {pins}  # Lista pin LED

# Sequenza avanti
for pin in led_pins:
    arduino.write(f'D{{pin}},1\\n'.encode())
    time.sleep({delay})
    arduino.write(f'D{{pin}},0\\n'.encode())

# Sequenza indietro
for pin in reversed(led_pins):
    arduino.write(f'D{{pin}},1\\n'.encode())
    time.sleep({delay})
    arduino.write(f'D{{pin}},0\\n'.encode())

arduino.close()
print("Sequenza LED completata")
""",
        'default_params': {'pins': [8, 9, 10, 11], 'delay': 0.2, 'port': 'COM3'}
    },
    
    'monitor_sensore': {
        'keywords': ['monitora', 'monitor', 'osserva', 'watch'],
        'entities': ['sensore', 'sensor'],
        'template': """# Monitora sensore in tempo reale
import serial
import time

arduino = serial.Serial('{port}', 9600, timeout=1)
time.sleep(2)

print("Monitoraggio sensore pin A{pin} - Premi Ctrl+C per fermare")

try:
    while True:
        arduino.write(b'R{pin}\\n')
        time.sleep(0.1)
        
        if arduino.in_waiting > 0:
            valore = arduino.readline().decode('utf-8').strip()
            print(f"Sensore A{pin}: {{valore}}", end='\\r')
        
        time.sleep({interval})
        
except KeyboardInterrupt:
    print("\\nMonitoraggio terminato")
    arduino.close()
""",
        'default_params': {'pin': 0, 'interval': 0.5, 'port': 'COM3'}
    },
}


# Sinonimi per estrazione parametri
ARDUINO_SYNONYMS = {
    'pin_numbers': {
        'tredici': 13, 'dodici': 12, 'undici': 11, 'dieci': 10,
        'nove': 9, 'otto': 8, 'sette': 7, 'sei': 6, 'cinque': 5,
        'quattro': 4, 'tre': 3, 'due': 2, 'uno': 1, 'zero': 0
    },
    'angles': {
        'zero': 0, 'novanta': 90, 'centottanta': 180,
        'quarantacinque': 45, 'centotrentacinque': 135
    }
}


def extract_arduino_params(frase: str) -> dict:
    """
    Estrae parametri da comando Arduino.
    
    Args:
        frase: Comando in linguaggio naturale
        
    Returns:
        Dict con parametri estratti (pin, angle, times, etc.)
    """
    params = {}
    frase_lower = frase.lower()
    
    # Estrai numero pin
    import re
    
    # Pattern "pin 13", "pin tredici", "su pin 5"
    pin_match = re.search(r'(?:pin|su)\s+(\d+|[a-z]+)', frase_lower)
    if pin_match:
        pin_str = pin_match.group(1)
        if pin_str.isdigit():
            params['pin'] = int(pin_str)
        elif pin_str in ARDUINO_SYNONYMS['pin_numbers']:
            params['pin'] = ARDUINO_SYNONYMS['pin_numbers'][pin_str]
    
    # Estrai angolo "a 90 gradi", "a novanta gradi"
    angle_match = re.search(r'(?:a|di)\s+(\d+|[a-z]+)\s*(?:gradi?|°)?', frase_lower)
    if angle_match:
        angle_str = angle_match.group(1)
        if angle_str.isdigit():
            params['angle'] = int(angle_str)
        elif angle_str in ARDUINO_SYNONYMS['angles']:
            params['angle'] = ARDUINO_SYNONYMS['angles'][angle_str]
    
    # Estrai numero volte "3 volte", "cinque volte"
    times_match = re.search(r'(\d+|[a-z]+)\s+volt[ei]', frase_lower)
    if times_match:
        times_str = times_match.group(1)
        if times_str.isdigit():
            params['times'] = int(times_str)
    
    # Estrai velocità "velocità 128", "speed 200"
    speed_match = re.search(r'(?:velocità|speed)\s+(\d+)', frase_lower)
    if speed_match:
        params['speed'] = int(speed_match.group(1))
    
    return params


def get_arduino_template(frase: str) -> tuple:
    """
    Identifica template Arduino corretto per la frase.
    
    Args:
        frase: Comando in linguaggio naturale
        
    Returns:
        (template_name, template_code, params) o (None, None, None)
    """
    frase_lower = frase.lower()
    
    # Cerca match con template
    for template_name, template_data in ARDUINO_COMMAND_TEMPLATES.items():
        # Verifica keyword + entity
        has_keyword = any(kw in frase_lower for kw in template_data['keywords'])
        has_entity = any(ent in frase_lower for ent in template_data['entities'])
        
        if has_keyword and has_entity:
            # Estrai parametri
            params = extract_arduino_params(frase)
            
            # Merge con default params
            final_params = template_data['default_params'].copy()
            final_params.update(params)
            
            # Formatta template
            template_code = template_data['template'].format(**final_params)
            
            return template_name, template_code, final_params
    
    return None, None, None


# Test
if __name__ == "__main__":
    test_phrases = [
        "accendi il led sul pin 13",
        "spegni led pin 5",
        "lampeggia led 5 volte",
        "leggi sensore su pin 2",
        "muovi servo a 90 gradi",
        "controlla motore velocità 200",
    ]
    
    print("=" * 60)
    print("TEST ARDUINO COMMAND TEMPLATES")
    print("=" * 60)
    
    for phrase in test_phrases:
        print(f"\nFrase: '{phrase}'")
        template_name, code, params = get_arduino_template(phrase)
        if template_name:
            print(f"Template: {template_name}")
            print(f"Params: {params}")
            print(f"Code:\n{code}")
        else:
            print("Nessun template trovato")
        print("-" * 60)

