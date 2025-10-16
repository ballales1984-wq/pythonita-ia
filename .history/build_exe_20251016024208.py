"""
Script per creare eseguibile Pythonita IA.
Genera file .exe standalone per Windows.
"""

import PyInstaller.__main__
import os
import sys
from pathlib import Path

def build_exe():
    """Costruisce l'eseguibile."""
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║      PYTHONITA IA - BUILD ESEGUIBILE v3.1.0                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    # Percorsi
    root_dir = Path(__file__).parent
    main_script = str(root_dir / 'gui_robot_3d.py')
    icon_path = str(root_dir / 'icon.ico') if (root_dir / 'icon.ico').exists() else None
    
    print("[1] Preparazione build...")
    print(f"    Script principale: {main_script}")
    print(f"    Directory root: {root_dir}")
    
    # Argomenti PyInstaller
    args = [
        main_script,
        '--name=PythonitaIA',
        '--onefile',  # Single exe file
        '--windowed',  # No console window
        '--clean',
        
        # Aggiungi dati necessari
        f'--add-data={root_dir / "core"};core',
        f'--add-data={root_dir / "visualizzatore"};visualizzatore',
        f'--add-data={root_dir / "examples"};examples',
        
        # Hidden imports
        '--hidden-import=numpy',
        '--hidden-import=matplotlib',
        '--hidden-import=tkinter',
        '--hidden-import=spacy',
        '--hidden-import=core',
        '--hidden-import=core.generatore',
        '--hidden-import=core.parser',
        '--hidden-import=core.cache',
        '--hidden-import=core.validator',
        '--hidden-import=visualizzatore',
        '--hidden-import=visualizzatore.modelli_3d',
        '--hidden-import=visualizzatore.oggetti_3d',
        '--hidden-import=visualizzatore.viewer_3d',
        
        # Collect submodules
        '--collect-all=matplotlib',
        '--collect-all=numpy',
        '--collect-all=spacy',
        
        # Ottimizzazioni
        '--optimize=2',
        '--strip',
        
        # Output
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.',
    ]
    
    # Aggiungi icona se esiste
    if icon_path and os.path.exists(icon_path):
        args.append(f'--icon={icon_path}')
        print(f"    Icona: {icon_path}")
    else:
        print("    Icona: Nessuna (usando default)")
    
    print("\n[2] Avvio build PyInstaller...")
    print("    Questo potrebbe richiedere 2-5 minuti...")
    print("")
    
    try:
        PyInstaller.__main__.run(args)
        
        print("\n╔══════════════════════════════════════════════════════════════════╗")
        print("║                                                                  ║")
        print("║  ✅ BUILD COMPLETATA CON SUCCESSO!                                ║")
        print("║                                                                  ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        
        exe_path = root_dir / 'dist' / 'PythonitaIA.exe'
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n📦 File eseguibile creato:")
            print(f"   Path: {exe_path}")
            print(f"   Size: {size_mb:.1f} MB")
            print(f"\n🚀 Esegui con:")
            print(f"   .\\dist\\PythonitaIA.exe")
        else:
            print("\n⚠️  Warning: File exe non trovato in dist/")
            
    except Exception as e:
        print(f"\n❌ ERRORE durante build:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def build_cli_exe():
    """Costruisce exe per versione CLI."""
    print("\n[OPZIONALE] Costruendo anche versione CLI...")
    
    root_dir = Path(__file__).parent
    
    args = [
        str(root_dir / 'main.py'),
        '--name=PythonitaIA_CLI',
        '--onefile',
        '--console',  # Con console per CLI
        '--clean',
        f'--add-data={root_dir / "core"};core',
        '--hidden-import=core',
        '--optimize=2',
        '--distpath=dist',
        '--workpath=build',
    ]
    
    try:
        PyInstaller.__main__.run(args)
        print("   ✅ CLI exe creato: dist/PythonitaIA_CLI.exe")
    except Exception as e:
        print(f"   ⚠️  CLI build fallito: {e}")


if __name__ == "__main__":
    print("\nQuale versione vuoi compilare?")
    print("1. GUI con Visualizzatore 3D (Consigliato)")
    print("2. CLI (Riga di comando)")
    print("3. Entrambe")
    
    try:
        scelta = input("\nScelta (1-3): ").strip()
    except:
        scelta = "1"
    
    if scelta == "1":
        build_exe()
    elif scelta == "2":
        # Solo CLI
        root_dir = Path(__file__).parent
        PyInstaller.__main__.run([
            str(root_dir / 'main.py'),
            '--name=PythonitaIA_CLI',
            '--onefile',
            '--console',
            f'--add-data={root_dir / "core"};core',
            '--hidden-import=core',
        ])
    elif scelta == "3":
        build_exe()
        build_cli_exe()
    else:
        print("Scelta non valida, build GUI...")
        build_exe()
    
    print("\n✅ Build completata!")
    print("Controlla la cartella 'dist/' per i file .exe")

