"""
Controller per Arduino - Comunicazione seriale e comandi hardware.
Supporta LED, sensori, motori, servomotori, display LCD.
"""

import serial
import serial.tools.list_ports
from typing import List, Optional, Tuple, Dict
import time
import logging
import json

logger = logging.getLogger(__name__)


class ArduinoController:
    """
    Controller per comunicazione con Arduino via seriale.
    """
    
    def __init__(self, port: Optional[str] = None, baudrate: int = 9600, timeout: float = 1.0):
        """
        Inizializza controller Arduino.
        
        Args:
            port: Porta COM (es. 'COM3', '/dev/ttyUSB0'). None = auto-detect
            baudrate: Velocità comunicazione (default 9600)
            timeout: Timeout lettura (secondi)
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection: Optional[serial.Serial] = None
        self.is_connected = False
        
        logger.info(f"Arduino controller initialized: port={port}, baudrate={baudrate}")
    
    @staticmethod
    def list_available_ports() -> List[Dict[str, str]]:
        """
        Elenca tutte le porte seriali disponibili.
        
        Returns:
            Lista dizionari con info porte: {'port': 'COM3', 'description': '...', 'hwid': '...'}
        """
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                'port': port.device,
                'description': port.description,
                'hwid': port.hwid
            })
        logger.info(f"Found {len(ports)} serial ports")
        return ports
    
    def connect(self, port: Optional[str] = None) -> Tuple[bool, str]:
        """
        Connette ad Arduino.
        
        Args:
            port: Porta COM (opzionale, usa quello dell'init se None)
            
        Returns:
            (success, message): True/False, messaggio
        """
        try:
            # Auto-detect porta se non specificata
            if port is None and self.port is None:
                ports = self.list_available_ports()
                if not ports:
                    return False, "Nessuna porta seriale trovata"
                
                # Cerca Arduino (prova porte con "Arduino" nel nome)
                arduino_ports = [p for p in ports if 'Arduino' in p['description'] or 'CH340' in p['description']]
                if arduino_ports:
                    port = arduino_ports[0]['port']
                    logger.info(f"Auto-detected Arduino on {port}")
                else:
                    port = ports[0]['port']
                    logger.info(f"Using first available port: {port}")
            
            if port:
                self.port = port
            
            # Connessione
            logger.info(f"Connecting to {self.port} at {self.baudrate} baud...")
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            
            # Attendi inizializzazione Arduino (reset automatico su connessione)
            time.sleep(2)
            
            # Flush buffer
            self.serial_connection.reset_input_buffer()
            self.serial_connection.reset_output_buffer()
            
            self.is_connected = True
            logger.info(f"Connected to Arduino on {self.port}")
            return True, f"Connesso ad Arduino su {self.port}"
            
        except serial.SerialException as e:
            logger.error(f"Serial connection error: {e}")
            self.is_connected = False
            return False, f"Errore connessione: {e}"
        except Exception as e:
            logger.error(f"Unexpected connection error: {e}")
            self.is_connected = False
            return False, f"Errore imprevisto: {e}"
    
    def disconnect(self) -> Tuple[bool, str]:
        """
        Disconnette da Arduino.
        
        Returns:
            (success, message): True/False, messaggio
        """
        try:
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
                self.is_connected = False
                logger.info("Disconnected from Arduino")
                return True, "Disconnesso da Arduino"
            else:
                return True, "Già disconnesso"
        except Exception as e:
            logger.error(f"Disconnect error: {e}")
            return False, f"Errore disconnessione: {e}"
    
    def send_command(self, command: str) -> Tuple[bool, str]:
        """
        Invia comando ad Arduino.
        
        Args:
            command: Comando da inviare (stringa)
            
        Returns:
            (success, response): True/False, risposta Arduino o messaggio errore
        """
        if not self.is_connected or not self.serial_connection:
            return False, "Arduino non connesso"
        
        try:
            # Aggiungi newline se manca
            if not command.endswith('\n'):
                command += '\n'
            
            # Invia
            logger.debug(f"Sending: {command.strip()}")
            self.serial_connection.write(command.encode('utf-8'))
            
            # Attendi risposta
            time.sleep(0.1)
            
            # Leggi risposta
            if self.serial_connection.in_waiting > 0:
                response = self.serial_connection.readline().decode('utf-8').strip()
                logger.debug(f"Received: {response}")
                return True, response
            else:
                return True, "OK"
                
        except Exception as e:
            logger.error(f"Send command error: {e}")
            return False, f"Errore invio: {e}"
    
    def read_response(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Legge risposta da Arduino.
        
        Args:
            timeout: Timeout lettura (usa self.timeout se None)
            
        Returns:
            Risposta Arduino o None
        """
        if not self.is_connected or not self.serial_connection:
            return None
        
        try:
            old_timeout = self.serial_connection.timeout
            if timeout is not None:
                self.serial_connection.timeout = timeout
            
            if self.serial_connection.in_waiting > 0:
                response = self.serial_connection.readline().decode('utf-8').strip()
                logger.debug(f"Read: {response}")
                return response
            
            self.serial_connection.timeout = old_timeout
            return None
            
        except Exception as e:
            logger.error(f"Read error: {e}")
            return None
    
    # ============================================================
    # COMANDI SPECIFICI ARDUINO
    # ============================================================
    
    def digital_write(self, pin: int, value: int) -> Tuple[bool, str]:
        """
        digitalWrite(pin, HIGH/LOW)
        
        Args:
            pin: Numero pin digitale
            value: 0 (LOW) o 1 (HIGH)
        """
        cmd = f"D{pin},{value}"
        return self.send_command(cmd)
    
    def analog_write(self, pin: int, value: int) -> Tuple[bool, str]:
        """
        analogWrite(pin, value) - PWM
        
        Args:
            pin: Numero pin PWM
            value: Valore 0-255
        """
        value = max(0, min(255, value))  # Clamp 0-255
        cmd = f"A{pin},{value}"
        return self.send_command(cmd)
    
    def analog_read(self, pin: int) -> Tuple[bool, int]:
        """
        analogRead(pin)
        
        Args:
            pin: Numero pin analogico
            
        Returns:
            (success, value): True/False, valore letto (0-1023)
        """
        cmd = f"R{pin}"
        success, response = self.send_command(cmd)
        
        if success:
            try:
                value = int(response)
                return True, value
            except ValueError:
                return False, -1
        return False, -1
    
    def servo_write(self, pin: int, angle: int) -> Tuple[bool, str]:
        """
        Controlla servomotore.
        
        Args:
            pin: Pin servo
            angle: Angolo 0-180 gradi
        """
        angle = max(0, min(180, angle))  # Clamp 0-180
        cmd = f"S{pin},{angle}"
        return self.send_command(cmd)
    
    def led_on(self, pin: int) -> Tuple[bool, str]:
        """Accendi LED su pin."""
        return self.digital_write(pin, 1)
    
    def led_off(self, pin: int) -> Tuple[bool, str]:
        """Spegni LED su pin."""
        return self.digital_write(pin, 0)
    
    def led_blink(self, pin: int, times: int = 3, delay: float = 0.5) -> Tuple[bool, str]:
        """
        Lampeggia LED.
        
        Args:
            pin: Pin LED
            times: Numero lampeggi
            delay: Secondi tra on/off
        """
        try:
            for _ in range(times):
                self.led_on(pin)
                time.sleep(delay)
                self.led_off(pin)
                time.sleep(delay)
            return True, f"LED {pin} lampeggiato {times} volte"
        except Exception as e:
            return False, str(e)


# Template comandi Arduino per code generator
ARDUINO_TEMPLATES = {
    'accendi_led': """
# Accendi LED su pin {pin}
import serial
arduino = serial.Serial('{port}', 9600)
arduino.write(b'D{pin},1\\n')
arduino.close()
""",
    'spegni_led': """
# Spegni LED su pin {pin}
import serial
arduino = serial.Serial('{port}', 9600)
arduino.write(b'D{pin},0\\n')
arduino.close()
""",
    'lampeggia_led': """
# Lampeggia LED su pin {pin}
import serial
import time
arduino = serial.Serial('{port}', 9600)
time.sleep(2)
for _ in range({times}):
    arduino.write(b'D{pin},1\\n')
    time.sleep({delay})
    arduino.write(b'D{pin},0\\n')
    time.sleep({delay})
arduino.close()
""",
    'leggi_sensore': """
# Leggi sensore analogico su pin A{pin}
import serial
arduino = serial.Serial('{port}', 9600)
time.sleep(2)
arduino.write(b'R{pin}\\n')
response = arduino.readline().decode('utf-8').strip()
print(f"Valore sensore: {{response}}")
arduino.close()
""",
    'muovi_servo': """
# Muovi servomotore su pin {pin} a {angle} gradi
import serial
arduino = serial.Serial('{port}', 9600)
time.sleep(2)
arduino.write(b'S{pin},{angle}\\n')
arduino.close()
""",
    'pwm_motore': """
# Controlla velocità motore (PWM) su pin {pin}
import serial
arduino = serial.Serial('{port}', 9600)
time.sleep(2)
arduino.write(b'A{pin},{speed}\\n')  # speed 0-255
arduino.close()
"""
}


# Singleton instance
_arduino_controller = None

def get_arduino_controller(port: Optional[str] = None, baudrate: int = 9600) -> ArduinoController:
    """
    Ottiene istanza singleton ArduinoController.
    
    Args:
        port: Porta COM
        baudrate: Baud rate
        
    Returns:
        ArduinoController
    """
    global _arduino_controller
    if _arduino_controller is None:
        _arduino_controller = ArduinoController(port, baudrate)
    return _arduino_controller


# Test standalone
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("TEST ARDUINO CONTROLLER")
    print("=" * 60)
    
    # Lista porte
    print("\n1. Porte seriali disponibili:")
    ports = ArduinoController.list_available_ports()
    for i, p in enumerate(ports):
        print(f"   {i+1}. {p['port']} - {p['description']}")
    
    if not ports:
        print("   Nessuna porta trovata!")
        exit(1)
    
    # Connessione
    controller = ArduinoController()
    print("\n2. Connessione ad Arduino...")
    success, msg = controller.connect()
    print(f"   {msg}")
    
    if success:
        # Test comandi
        print("\n3. Test comandi...")
        
        # LED blink
        print("   - Lampeggio LED pin 13...")
        success, msg = controller.led_blink(13, times=3, delay=0.3)
        print(f"     {msg}")
        
        # Disconnessione
        print("\n4. Disconnessione...")
        success, msg = controller.disconnect()
        print(f"   {msg}")
    
    print("\n" + "=" * 60)

