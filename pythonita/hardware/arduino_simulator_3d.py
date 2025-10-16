"""
Simulatore Arduino 3D Virtuale.
Simula Arduino Uno/Mega con visualizzazione 3D della board.
Non richiede hardware fisico - tutto virtuale!
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Rectangle, Circle
import matplotlib.patches as mpatches
from typing import Dict, List, Tuple, Optional
import threading
import time


class Pin:
    """Rappresenta un pin fisico dell'Arduino."""
    
    def __init__(self, numero: int, tipo: str, posizione: Tuple[float, float]):
        """
        Args:
            numero: Numero pin (0-53)
            tipo: 'digital', 'analog', 'pwm', 'power'
            posizione: (x, y) sulla board in cm
        """
        self.numero = numero
        self.tipo = tipo
        self.posizione = posizione
        self.mode = 'INPUT'  # INPUT, OUTPUT
        self.value = 0  # 0 o 1 per digital, 0-1023 per analog
        self.pwm_value = 0  # 0-255
        self.connesso = False  # LED/componente connesso?
        
    def digitalWrite(self, value):
        """Scrive valore digitale (HIGH/LOW)."""
        if self.mode != 'OUTPUT':
            return False
        self.value = 1 if value else 0
        return True
    
    def digitalRead(self):
        """Legge valore digitale."""
        return self.value
    
    def analogRead(self):
        """Legge valore analogico (0-1023)."""
        # Simula lettura con un po' di rumore
        base = self.value
        noise = np.random.randint(-10, 10)
        return max(0, min(1023, base + noise))
    
    def analogWrite(self, value):
        """Scrive valore PWM (0-255)."""
        self.pwm_value = max(0, min(255, value))
        return True


class ComponenteVirtuale:
    """Classe base per componenti virtuali (LED, Servo, ecc)."""
    
    def __init__(self, nome: str, pin: int):
        self.nome = nome
        self.pin = pin
        self.stato = 'OFF'
        
    def aggiorna(self, **kwargs):
        """Aggiorna stato del componente."""
        pass


class LEDVirtuale(ComponenteVirtuale):
    """LED virtuale con animazione."""
    
    def __init__(self, pin: int, colore='red'):
        super().__init__(f"LED_{pin}", pin)
        self.colore = colore
        self.luminosita = 0  # 0-255
        
    def accendi(self):
        self.stato = 'ON'
        self.luminosita = 255
        
    def spegni(self):
        self.stato = 'OFF'
        self.luminosita = 0
        
    def set_pwm(self, value):
        """Imposta luminosità PWM."""
        self.luminosita = value
        self.stato = 'PWM' if value > 0 else 'OFF'


class ServoVirtuale(ComponenteVirtuale):
    """Servomotore virtuale."""
    
    def __init__(self, pin: int):
        super().__init__(f"SERVO_{pin}", pin)
        self.angolo = 90  # Posizione centrale
        self.min_angle = 0
        self.max_angle = 180
        
    def muovi(self, angolo: int):
        """Muove il servo all'angolo specificato."""
        self.angolo = max(self.min_angle, min(self.max_angle, angolo))
        self.stato = f"{self.angolo}°"


class ArduinoSimulator3D:
    """
    Simulatore Arduino Uno/Mega con visualizzazione 3D.
    Simula completamente un Arduino senza hardware fisico.
    """
    
    def __init__(self, board_type='Uno'):
        """
        Inizializza simulatore.
        
        Args:
            board_type: 'Uno', 'Mega', 'Nano'
        """
        self.board_type = board_type
        self.connected = False
        self.baud_rate = 9600
        
        # Crea pin virtuali
        self.pins: Dict[int, Pin] = {}
        self._setup_pins()
        
        # Componenti virtuali
        self.componenti: Dict[int, ComponenteVirtuale] = {}
        
        # LED built-in (pin 13)
        self.led_builtin = LEDVirtuale(13, 'orange')
        self.componenti[13] = self.led_builtin
        
        # Log comandi
        self.command_log: List[str] = []
        
        # Visualizzazione 3D
        self.visualizer = None
        self.visualizer_thread = None
        
        print(f"[SIMULATOR] Arduino {board_type} virtuale inizializzato")
        print(f"[SIMULATOR] {len(self.pins)} pin disponibili")
    
    def _setup_pins(self):
        """Setup pin Arduino Uno."""
        # Pin digitali 0-13
        for i in range(14):
            x = 2 + (i % 7) * 2
            y = 2 if i < 7 else 4
            self.pins[i] = Pin(i, 'digital', (x, y))
        
        # Pin PWM: 3, 5, 6, 9, 10, 11
        for p in [3, 5, 6, 9, 10, 11]:
            self.pins[p].tipo = 'pwm'
        
        # Pin analogici A0-A5 (14-19)
        for i in range(6):
            x = 2 + i * 2
            self.pins[14 + i] = Pin(14 + i, 'analog', (x, 6))
    
    def connect(self, port='SIM', baudrate=9600):
        """
        Connetti al simulatore.
        
        Args:
            port: Porta (ignorato, sempre 'SIM')
            baudrate: Baud rate (default 9600)
            
        Returns:
            (success, message)
        """
        self.connected = True
        self.baud_rate = baudrate
        self.command_log.append(f"CONNECT:{port}:{baudrate}")
        
        print(f"[SIMULATOR] 🟢 Connesso (virtuale)")
        print(f"[SIMULATOR] Port: {port} (simulato)")
        print(f"[SIMULATOR] Baudrate: {baudrate}")
        
        return True, f"Arduino {self.board_type} Simulator connected"
    
    def disconnect(self):
        """Disconnetti dal simulatore."""
        self.connected = False
        self.command_log.append("DISCONNECT")
        print(f"[SIMULATOR] 🔴 Disconnesso")
        return True, "Disconnected"
    
    def led_on(self, pin: int):
        """Accendi LED su pin."""
        if pin not in self.pins:
            return False, f"Pin {pin} non esiste"
        
        self.pins[pin].mode = 'OUTPUT'
        self.pins[pin].digitalWrite(1)
        
        # Crea LED virtuale se non esiste
        if pin not in self.componenti:
            self.componenti[pin] = LEDVirtuale(pin)
        
        if isinstance(self.componenti[pin], LEDVirtuale):
            self.componenti[pin].accendi()
        
        self.command_log.append(f"LED_ON:{pin}")
        print(f"[SIMULATOR] 💡 LED pin {pin} → ON")
        
        return True, "LED acceso"
    
    def led_off(self, pin: int):
        """Spegni LED su pin."""
        if pin not in self.pins:
            return False, f"Pin {pin} non esiste"
        
        self.pins[pin].digitalWrite(0)
        
        if pin in self.componenti and isinstance(self.componenti[pin], LEDVirtuale):
            self.componenti[pin].spegni()
        
        self.command_log.append(f"LED_OFF:{pin}")
        print(f"[SIMULATOR] ⚫ LED pin {pin} → OFF")
        
        return True, "LED spento"
    
    def led_blink(self, pin: int, times: int = 3, delay: float = 0.5):
        """Lampeggia LED."""
        for i in range(times):
            self.led_on(pin)
            time.sleep(delay)
            self.led_off(pin)
            time.sleep(delay)
            print(f"[SIMULATOR] ✨ Lampeggio {i+1}/{times}")
        
        return True, f"LED lampeggiato {times} volte"
    
    def servo_write(self, pin: int, angle: int):
        """Muovi servomotore."""
        if pin not in self.pins:
            return False, f"Pin {pin} non esiste"
        
        # Crea servo virtuale se non esiste
        if pin not in self.componenti:
            self.componenti[pin] = ServoVirtuale(pin)
        
        if isinstance(self.componenti[pin], ServoVirtuale):
            self.componenti[pin].muovi(angle)
        
        self.command_log.append(f"SERVO:{pin}:{angle}")
        print(f"[SIMULATOR] 🎚️  Servo pin {pin} → {angle}°")
        
        return True, f"Servo mosso a {angle}°"
    
    def analog_read(self, pin: int):
        """Leggi valore analogico."""
        analog_pin = pin if pin >= 14 else (14 + pin)  # A0 = 14
        
        if analog_pin not in self.pins:
            return False, 0
        
        value = self.pins[analog_pin].analogRead()
        self.command_log.append(f"READ:A{pin}:{value}")
        print(f"[SIMULATOR] 📊 Sensore A{pin} → {value}/1023")
        
        return True, value
    
    def analog_write(self, pin: int, value: int):
        """Scrivi PWM."""
        if pin not in self.pins:
            return False, f"Pin {pin} non esiste"
        
        if self.pins[pin].tipo != 'pwm':
            print(f"[SIMULATOR] ⚠️  Pin {pin} non supporta PWM")
        
        self.pins[pin].analogWrite(value)
        
        # Se c'è un LED, aggiorna luminosità
        if pin in self.componenti and isinstance(self.componenti[pin], LEDVirtuale):
            self.componenti[pin].set_pwm(value)
        
        self.command_log.append(f"PWM:{pin}:{value}")
        print(f"[SIMULATOR] ⚡ PWM pin {pin} → {value}/255 ({value/255*100:.0f}%)")
        
        return True, f"PWM impostato a {value}"
    
    def get_pin_state(self, pin: int):
        """Ottieni stato di un pin."""
        if pin not in self.pins:
            return None
        return {
            'numero': pin,
            'tipo': self.pins[pin].tipo,
            'mode': self.pins[pin].mode,
            'value': self.pins[pin].value,
            'pwm': self.pins[pin].pwm_value
        }
    
    def get_all_states(self):
        """Ottieni stato di tutti i pin."""
        return {pin: self.get_pin_state(pin) for pin in self.pins.keys()}
    
    def visualizza_3d(self):
        """Apri visualizzatore 3D della board Arduino."""
        from pythonita.hardware.arduino_visualizer_3d import ArduinoVisualizer3D
        
        if not self.visualizer:
            self.visualizer = ArduinoVisualizer3D(self)
            self.visualizer_thread = threading.Thread(target=self.visualizer.run, daemon=True)
            self.visualizer_thread.start()
        
        return True, "Visualizzatore 3D aperto"
    
    def reset(self):
        """Reset completo - tutti i pin a stato iniziale."""
        for pin in self.pins.values():
            pin.mode = 'INPUT'
            pin.value = 0
            pin.pwm_value = 0
        
        for componente in self.componenti.values():
            if isinstance(componente, LEDVirtuale):
                componente.spegni()
            elif isinstance(componente, ServoVirtuale):
                componente.muovi(90)
        
        self.command_log.append("RESET")
        print("[SIMULATOR] 🔄 Reset completo")
        
        return True, "Reset completato"


# Singleton
_simulator = None

def get_arduino_simulator():
    """Ottieni istanza singleton del simulatore."""
    global _simulator
    if _simulator is None:
        _simulator = ArduinoSimulator3D()
    return _simulator


if __name__ == "__main__":
    print("=" * 70)
    print("ARDUINO SIMULATOR 3D - TEST")
    print("=" * 70)
    
    sim = ArduinoSimulator3D(board_type='Uno')
    sim.connect()
    
    print("\nTest 1: LED Built-in (pin 13)")
    sim.led_on(13)
    time.sleep(1)
    sim.led_off(13)
    
    print("\nTest 2: Lampeggio")
    sim.led_blink(13, times=3, delay=0.3)
    
    print("\nTest 3: Servo")
    sim.servo_write(9, 0)
    time.sleep(0.5)
    sim.servo_write(9, 90)
    time.sleep(0.5)
    sim.servo_write(9, 180)
    
    print("\nTest 4: Lettura sensore")
    for i in range(5):
        success, value = sim.analog_read(0)
        print(f"  A0: {value}")
        time.sleep(0.2)
    
    print("\nTest 5: PWM")
    for pwm in [0, 64, 128, 192, 255]:
        sim.analog_write(11, pwm)
        time.sleep(0.3)
    
    sim.disconnect()
    
    print("\n" + "=" * 70)
    print("✅ SIMULATORE FUNZIONANTE!")
    print("=" * 70)

