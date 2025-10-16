"""
Supporto CircuitPython - Python nativo su microcontrollori.
Permette di eseguire codice Python direttamente su hardware.
"""

from typing import List, Dict, Optional
import os


class CircuitPythonDevice:
    """Rappresenta un dispositivo CircuitPython."""
    
    SUPPORTED_BOARDS = [
        'Adafruit Circuit Playground Express',
        'Adafruit Feather M0',
        'Adafruit ItsyBitsy M4',
        'Raspberry Pi Pico',
        'ESP32-S2',
        'ESP32-C3',
        'Seeed XIAO',
        'Arduino Nano RP2040 Connect',
        'Arduino Portenta H7',
    ]
    
    def __init__(self, board_name: str = 'Circuit Playground Express'):
        self.board_name = board_name
        self.drive_letter = None
        self.connected = False
        self.python_version = "3.4+"  # CircuitPython version
        
    def detect_devices(self) -> List[str]:
        """
        Rileva dispositivi CircuitPython connessi.
        Cerca drive CIRCUITPY.
        
        Returns:
            Lista di drive letters trovati
        """
        devices = []
        
        # Windows: cerca drive CIRCUITPY
        try:
            import win32api
            import win32file
            
            drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
            
            for drive in drives:
                try:
                    volume = win32api.GetVolumeInformation(drive)
                    if 'CIRCUITPY' in volume[0]:
                        devices.append(drive)
                        print(f"[CIRCUITPYTHON] 🟢 Trovato: {drive} ({volume[0]})")
                except:
                    pass
                    
        except ImportError:
            # Fallback multipiattaforma
            for letter in 'DEFGHIJKLMNOPQRSTUVWXYZ':
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    # Controlla se esiste boot_out.txt (file CircuitPython)
                    if os.path.exists(os.path.join(drive, 'boot_out.txt')):
                        devices.append(drive)
                        print(f"[CIRCUITPYTHON] 🟢 Trovato: {drive}")
        
        return devices
    
    def connect(self, drive_letter: Optional[str] = None):
        """
        Connetti a dispositivo CircuitPython.
        
        Args:
            drive_letter: Lettera drive (es: 'D:\\'), None = auto-detect
            
        Returns:
            (success, message)
        """
        if drive_letter is None:
            # Auto-detect
            devices = self.detect_devices()
            if not devices:
                return False, "Nessun dispositivo CircuitPython trovato. Collega via USB."
            drive_letter = devices[0]
        
        if not os.path.exists(drive_letter):
            return False, f"Drive {drive_letter} non trovato"
        
        self.drive_letter = drive_letter
        self.connected = True
        
        # Leggi info boot
        boot_file = os.path.join(drive_letter, 'boot_out.txt')
        if os.path.exists(boot_file):
            with open(boot_file, 'r') as f:
                boot_info = f.read()
                # Estrai versione
                for line in boot_info.split('\n'):
                    if 'CircuitPython' in line:
                        print(f"[CIRCUITPYTHON] {line.strip()}")
        
        print(f"[CIRCUITPYTHON] ✅ Connesso a {drive_letter}")
        return True, f"Connesso a {drive_letter}"
    
    def upload_code(self, python_code: str, filename='code.py'):
        """
        Carica codice Python su CircuitPython.
        
        Args:
            python_code: Codice Python da eseguire
            filename: Nome file (default: code.py)
            
        Returns:
            (success, message)
        """
        if not self.connected:
            return False, "Non connesso. Usa connect() prima."
        
        code_path = os.path.join(self.drive_letter, filename)
        
        try:
            with open(code_path, 'w') as f:
                f.write(python_code)
            
            print(f"[CIRCUITPYTHON] 📤 Codice caricato: {filename}")
            print(f"[CIRCUITPYTHON] 🔄 Device riavvierà automaticamente...")
            
            return True, f"Codice caricato su {filename}"
            
        except Exception as e:
            return False, f"Errore scrittura: {e}"
    
    def read_code(self, filename='code.py'):
        """
        Leggi codice dal dispositivo.
        
        Args:
            filename: Nome file da leggere
            
        Returns:
            (success, code)
        """
        if not self.connected:
            return False, ""
        
        code_path = os.path.join(self.drive_letter, filename)
        
        try:
            with open(code_path, 'r') as f:
                code = f.read()
            return True, code
        except Exception as e:
            return False, ""
    
    def list_files(self):
        """Lista file su CircuitPython."""
        if not self.connected:
            return []
        
        try:
            files = os.listdir(self.drive_letter)
            return [f for f in files if f.endswith('.py') or f.endswith('.txt')]
        except:
            return []


# Template esempio CircuitPython
CIRCUITPYTHON_TEMPLATE_LED = """
# CircuitPython - Lampeggia LED built-in
import board
import digitalio
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True   # Accendi
    time.sleep(0.5)
    led.value = False  # Spegni
    time.sleep(0.5)
"""

CIRCUITPYTHON_TEMPLATE_NEOPIXEL = """
# CircuitPython - NeoPixel rainbow
import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2)

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

i = 0
while True:
    for j in range(10):
        pixels[j] = wheel((i + j) & 255)
    pixels.show()
    time.sleep(0.05)
    i = (i + 1) % 256
"""


def get_circuitpython():
    """Get CircuitPython device manager."""
    return CircuitPythonDevice()


if __name__ == "__main__":
    print("CircuitPython Support - Test")
    
    cp = CircuitPythonDevice()
    devices = cp.detect_devices()
    
    if devices:
        print(f"✅ Trovati {len(devices)} dispositivi CircuitPython")
        cp.connect(devices[0])
        print("\nFile su dispositivo:")
        for f in cp.list_files():
            print(f"  - {f}")
    else:
        print("❌ Nessun dispositivo CircuitPython trovato")
        print("Collega un dispositivo supportato via USB")

