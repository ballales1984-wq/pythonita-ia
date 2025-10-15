"""
Esempio pratico: Validazione Input
Dimostra come la validazione proteggerebbe il sistema.
"""

import re
from dataclasses import dataclass


@dataclass
class ValidationResult:
    is_valid: bool
    message: str
    sanitized: str = ""


def validate_simple(text: str) -> ValidationResult:
    """Validazione semplificata."""
    
    # 1. Controllo lunghezza
    if len(text) > 1000:
        return ValidationResult(
            False,
            f"[ERRORE] Input troppo lungo: {len(text)} caratteri (max 1000)"
        )
    
    if len(text) < 1:
        return ValidationResult(
            False,
            "[ERRORE] Input vuoto"
        )
    
    # 2. Pattern pericolosi
    dangerous = [
        r'__import__',
        r'eval\s*\(',
        r'exec\s*\(',
        r'os\.system',
    ]
    
    for pattern in dangerous:
        if re.search(pattern, text, re.IGNORECASE):
            return ValidationResult(
                False,
                f"[ERRORE] Pattern pericoloso rilevato: {pattern}"
            )
    
    # 3. Sanitizzazione
    sanitized = re.sub(r'\s+', ' ', text).strip()
    
    return ValidationResult(
        True,
        "[OK] Input valido",
        sanitized
    )


def demo():
    """Demo validazione."""
    print("="*70)
    print("DEMO: Validazione Input")
    print("="*70)
    
    test_cases = [
        ("stampa ciao mondo", "[OK] Valido"),
        ("", "[ERRORE] Vuoto"),
        ("a" * 2000, "[ERRORE] Troppo lungo"),
        ("__import__('os').system('rm -rf /')", "[ERRORE] Pericoloso"),
        ("eval('malicious code')", "[ERRORE] Pericoloso"),
        ("stampa    ciao    mondo", "[OK] Valido (con sanitizzazione)"),
        ("  stampa test  ", "[OK] Valido (con sanitizzazione)"),
    ]
    
    for i, (input_text, expected) in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}: {expected}")
        print(f"{'='*70}")
        
        # Mostra input (troncato se troppo lungo)
        display = input_text if len(input_text) < 50 else input_text[:47] + "..."
        print(f"Input: '{display}'")
        print(f"Lunghezza: {len(input_text)} caratteri")
        
        # Valida
        result = validate_simple(input_text)
        
        print(f"\nRisultato: {result.message}")
        
        if result.is_valid:
            print(f"Sanitizzato: '{result.sanitized}'")
            if result.sanitized != input_text:
                print("[ATTENZIONE] Input modificato durante sanitizzazione")
        else:
            print("[BLOCCATO] Input NON accettato per sicurezza")
    
    # Statistiche
    print("\n" + "="*70)
    print("[STATISTICHE]")
    print("="*70)
    
    valid = sum(1 for text, _ in test_cases if validate_simple(text).is_valid)
    invalid = len(test_cases) - valid
    
    print(f"Test totali: {len(test_cases)}")
    print(f"[OK] Validi: {valid}")
    print(f"[ERRORE] Invalidi: {invalid}")
    print(f"Tasso blocco: {invalid/len(test_cases)*100:.0f}%")
    
    print("\n[INFO] La validazione previene:")
    print("  - DoS (input troppo lunghi)")
    print("  - Code injection (__import__, eval, exec)")
    print("  - Input malformati")
    print("  - Crash da tipo errato")


if __name__ == "__main__":
    demo()

