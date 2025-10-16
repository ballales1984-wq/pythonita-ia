"""Script automazione build exe ottimizzato."""

import subprocess
import sys
from pathlib import Path
import shutil

def clean_build():
    """Pulisci directory build precedenti."""
    dirs_to_clean = ['build', 'dist']
    for d in dirs_to_clean:
        if Path(d).exists():
            shutil.rmtree(d)
            print(f"[OK] Pulito {d}/")

def build_exe(include_spacy=True):
    """
    Build exe ottimizzato.
    
    Args:
        include_spacy: Include modello spaCy (aumenta size)
    """
    print("="*70)
    print("BUILD PYTHONITA IA - EXE OPTIMIZED")
    print("="*70)
    
    # Parametri base
    params = [
        'pyinstaller',
        '--name=PythonitaIA',
        '--onefile',
        '--windowed',
        '--clean',
        '--add-data=core:core',
        '--add-data=visualizzatore:visualizzatore',
        '--hidden-import=numpy',
        '--hidden-import=matplotlib',
        '--hidden-import=tkinter',
        '--collect-all=matplotlib',
        '--collect-all=numpy',
        '--optimize=2',
        'gui_robot_3d.py'
    ]
    
    if include_spacy:
        params.extend([
            '--hidden-import=spacy',
            '--collect-all=spacy',
            '--collect-submodules=spacy'
        ])
    
    print(f"\n[BUILD] {'Con' if include_spacy else 'Senza'} spaCy...")
    print("[INFO] Attendere 3-5 minuti...")
    
    result = subprocess.run(params)
    
    if result.returncode == 0:
        print("\n" + "="*70)
        print("[OK] BUILD COMPLETATA!")
        print("="*70)
        
        exe_path = Path('dist/PythonitaIA.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\nFile: {exe_path}")
            print(f"Size: {size_mb:.1f} MB")
            
            # Copia su desktop
            desktop = Path.home() / "Desktop" / "PythonitaIA.exe"
            shutil.copy(exe_path, desktop)
            print(f"\n[OK] Copiato su: {desktop}")
        
        return True
    else:
        print("\n[ERRORE] Build fallita!")
        return False

if __name__ == "__main__":
    clean_build()
    success = build_exe(include_spacy=True)
    sys.exit(0 if success else 1)

