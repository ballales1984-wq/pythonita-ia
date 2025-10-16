/*
  Pythonita IA - Arduino Controller Sketch
  
  Questo sketch permette a Pythonita IA di controllare Arduino via seriale.
  
  SUPPORTA:
  - Digital Write (LED, Relè, etc.)
  - Analog Write / PWM (Motori DC, dimming LED, etc.)
  - Analog Read (Sensori analogici)
  - Servo Control (Servomotori)
  
  FORMATO COMANDI:
  - D<pin>,<value>  - Digital Write (es: D13,1 -> Accendi LED pin 13)
  - A<pin>,<value>  - Analog Write / PWM (es: A3,128 -> PWM 50% su pin 3)
  - R<pin>          - Read Analog (es: R0 -> Leggi pin A0)
  - S<pin>,<angle>  - Servo (es: S9,90 -> Muovi servo pin 9 a 90°)
  
  INSTALLAZIONE:
  1. Apri Arduino IDE
  2. Copia/Incolla questo codice
  3. Collega Arduino via USB
  4. Seleziona board e porta in Tools > Board / Port
  5. Carica sketch (pulsante freccia)
  6. Apri Serial Monitor per testare (baud rate 9600)
  7. Prova comando: D13,1 (accende LED built-in)
  
  COLLEGAMENTI:
  - Pin 13: LED built-in (già presente su Arduino Uno/Nano)
  - Pin 9:  Servomotore (filo segnale - arancione/giallo)
  - Pin 3:  Motore DC con transistor/driver L293D (PWM)
  - Pin A0: Sensore analogico (temperatura, luce, potenziometro, etc.)
  - GND:    Ground comune per tutti i componenti esterni
  
  AUTORE: Pythonita IA
  VERSIONE: 1.0
  DATA: 2025-01-16
*/

#include <Servo.h>

Servo servo;  // Oggetto servo
bool servoAttached = false;

void setup() {
  // Inizializza comunicazione seriale a 9600 baud
  Serial.begin(9600);
  
  // Inizializza pin LED built-in (pin 13)
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  
  // Messaggio di avvio
  Serial.println("Pythonita Arduino Controller v1.0");
  Serial.println("Ready to receive commands!");
  Serial.println("Format: D<pin>,<value> | A<pin>,<value> | R<pin> | S<pin>,<angle>");
  
  // Lampeggio LED per conferma avvio
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
  }
}

void loop() {
  // Controlla se ci sono dati da leggere sulla seriale
  if (Serial.available() > 0) {
    // Leggi comando fino a newline
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();  // Rimuovi spazi/newline extra
    
    // Ignora comandi vuoti
    if (cmd.length() == 0) {
      return;
    }
    
    // Estrai tipo comando (primo carattere)
    char type = cmd.charAt(0);
    
    // Esegui comando in base al tipo
    switch (type) {
      case 'D':
        handleDigitalWrite(cmd);
        break;
      case 'A':
        handleAnalogWrite(cmd);
        break;
      case 'R':
        handleAnalogRead(cmd);
        break;
      case 'S':
        handleServo(cmd);
        break;
      default:
        Serial.println("ERROR: Unknown command type");
        Serial.println("Use: D, A, R, or S");
        break;
    }
  }
}

// ============================================================
// GESTORI COMANDI
// ============================================================

void handleDigitalWrite(String cmd) {
  // Formato: D<pin>,<value>
  // Esempio: D13,1 (accendi LED pin 13)
  
  int commaIndex = cmd.indexOf(',');
  if (commaIndex == -1) {
    Serial.println("ERROR: Digital Write requires pin,value");
    return;
  }
  
  // Estrai pin e valore
  int pin = cmd.substring(1, commaIndex).toInt();
  int value = cmd.substring(commaIndex + 1).toInt();
  
  // Validazione
  if (pin < 0 || pin > 13) {
    Serial.println("ERROR: Pin must be 0-13");
    return;
  }
  
  if (value != 0 && value != 1) {
    Serial.println("ERROR: Value must be 0 or 1");
    return;
  }
  
  // Esegui
  pinMode(pin, OUTPUT);
  digitalWrite(pin, value);
  
  // Conferma
  Serial.print("OK: Digital pin ");
  Serial.print(pin);
  Serial.print(" = ");
  Serial.println(value == 1 ? "HIGH" : "LOW");
}

void handleAnalogWrite(String cmd) {
  // Formato: A<pin>,<value>
  // Esempio: A3,128 (PWM 50% su pin 3)
  
  int commaIndex = cmd.indexOf(',');
  if (commaIndex == -1) {
    Serial.println("ERROR: Analog Write requires pin,value");
    return;
  }
  
  // Estrai pin e valore
  int pin = cmd.substring(1, commaIndex).toInt();
  int value = cmd.substring(commaIndex + 1).toInt();
  
  // Validazione (solo pin PWM: 3, 5, 6, 9, 10, 11 su Arduino Uno)
  if (pin != 3 && pin != 5 && pin != 6 && pin != 9 && pin != 10 && pin != 11) {
    Serial.println("ERROR: PWM pins are 3,5,6,9,10,11");
    return;
  }
  
  if (value < 0 || value > 255) {
    Serial.println("ERROR: Value must be 0-255");
    return;
  }
  
  // Esegui
  pinMode(pin, OUTPUT);
  analogWrite(pin, value);
  
  // Conferma
  Serial.print("OK: PWM pin ");
  Serial.print(pin);
  Serial.print(" = ");
  Serial.print(value);
  Serial.print(" (");
  Serial.print((value / 255.0) * 100, 1);
  Serial.println("%)");
}

void handleAnalogRead(String cmd) {
  // Formato: R<pin>
  // Esempio: R0 (leggi pin A0)
  
  // Estrai pin
  int pin = cmd.substring(1).toInt();
  
  // Validazione (pin analogici A0-A5 su Arduino Uno)
  if (pin < 0 || pin > 5) {
    Serial.println("ERROR: Analog pin must be 0-5 (A0-A5)");
    return;
  }
  
  // Leggi valore
  int value = analogRead(pin);
  
  // Invia valore (solo il numero, per parsing facile)
  Serial.println(value);
}

void handleServo(String cmd) {
  // Formato: S<pin>,<angle>
  // Esempio: S9,90 (muovi servo su pin 9 a 90°)
  
  int commaIndex = cmd.indexOf(',');
  if (commaIndex == -1) {
    Serial.println("ERROR: Servo requires pin,angle");
    return;
  }
  
  // Estrai pin e angolo
  int pin = cmd.substring(1, commaIndex).toInt();
  int angle = cmd.substring(commaIndex + 1).toInt();
  
  // Validazione
  if (pin < 0 || pin > 13) {
    Serial.println("ERROR: Pin must be 0-13");
    return;
  }
  
  if (angle < 0 || angle > 180) {
    Serial.println("ERROR: Angle must be 0-180");
    return;
  }
  
  // Attach servo se necessario
  if (!servoAttached) {
    servo.attach(pin);
    servoAttached = true;
  }
  
  // Muovi servo
  servo.write(angle);
  delay(15);  // Tempo per servo di raggiungere posizione
  
  // Conferma
  Serial.print("OK: Servo pin ");
  Serial.print(pin);
  Serial.print(" -> ");
  Serial.print(angle);
  Serial.println(" degrees");
}

// ============================================================
// TEST COMANDI (Serial Monitor)
// ============================================================
/*
  Apri Serial Monitor (Tools > Serial Monitor, baud rate 9600)
  
  TEST 1: LED Built-in
    D13,1  -> Accendi LED
    D13,0  -> Spegni LED
  
  TEST 2: LED Esterno (collega LED+resistenza tra pin 8 e GND)
    D8,1   -> Accendi
    D8,0   -> Spegni
  
  TEST 3: PWM (collega LED tra pin 3 e GND con resistenza)
    A3,0   -> Spento
    A3,64  -> 25% luminosità
    A3,128 -> 50% luminosità
    A3,255 -> 100% luminosità
  
  TEST 4: Sensore Analogico (collega potenziometro a A0)
    R0     -> Legge valore 0-1023
  
  TEST 5: Servo (collega servo a pin 9: rosso=5V, marrone=GND, arancione=pin 9)
    S9,0   -> Posizione 0°
    S9,90  -> Posizione centrale
    S9,180 -> Posizione massima
*/

