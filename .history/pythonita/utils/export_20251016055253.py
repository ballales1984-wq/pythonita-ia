"""
Export Utilities - Salva codice, screenshot e animazioni.
Permette agli utenti di condividere e salvare il loro lavoro.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ExportManager:
    """Gestisce export di codice, screenshot e animazioni."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Inizializza export manager.
        
        Args:
            output_dir: Directory output (default: ~/pythonita_exports/)
        """
        self.output_dir = output_dir or (Path.home() / "pythonita_exports")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Export directory: {self.output_dir}")
    
    def export_code(self, code: str, command: str = "", metadata: Optional[dict] = None) -> Path:
        """
        Esporta codice Python come file .py
        
        Args:
            code: Codice Python da salvare
            command: Comando italiano usato
            metadata: Metadata aggiuntivi
            
        Returns:
            Path del file salvato
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pythonita_{timestamp}.py"
        filepath = self.output_dir / filename
        
        # Header professionale
        header = self._generate_header(command, metadata)
        
        # Salva file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(header)
            f.write('\n\n')
            f.write(code)
        
        logger.info(f"Codice esportato: {filepath}")
        return filepath
    
    def export_screenshot(self, figure, name: Optional[str] = None) -> Path:
        """
        Esporta screenshot della visualizzazione 3D.
        
        Args:
            figure: Figura matplotlib
            name: Nome file (opzionale)
            
        Returns:
            Path del file salvato
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = name or f"pythonita_3d_{timestamp}.png"
        
        if not filename.endswith('.png'):
            filename += '.png'
        
        filepath = self.output_dir / filename
        
        # Salva figura
        figure.savefig(filepath, dpi=300, bbox_inches='tight', 
                      facecolor='white', edgecolor='none')
        
        logger.info(f"Screenshot esportato: {filepath}")
        return filepath
    
    def export_animation_frames(self, figures: list, base_name: str = "animation") -> list:
        """
        Esporta frame di animazione come immagini PNG.
        
        Args:
            figures: Lista di figure matplotlib
            base_name: Nome base per i file
            
        Returns:
            Lista di path dei file salvati
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        anim_dir = self.output_dir / f"{base_name}_{timestamp}"
        anim_dir.mkdir(parents=True, exist_ok=True)
        
        paths = []
        for i, fig in enumerate(figures):
            filename = f"frame_{i:04d}.png"
            filepath = anim_dir / filename
            
            fig.savefig(filepath, dpi=150, bbox_inches='tight')
            paths.append(filepath)
        
        logger.info(f"Esportati {len(paths)} frame in: {anim_dir}")
        return paths
    
    def create_gif(self, frame_paths: list, output_name: str = "animation.gif", 
                  duration: int = 100) -> Optional[Path]:
        """
        Crea GIF da frame di animazione.
        
        Args:
            frame_paths: Lista di path ai frame PNG
            output_name: Nome file GIF output
            duration: Durata di ogni frame in ms
            
        Returns:
            Path del GIF creato o None se fallisce
        """
        try:
            from PIL import Image
            
            if not output_name.endswith('.gif'):
                output_name += '.gif'
            
            filepath = self.output_dir / output_name
            
            # Carica frame
            frames = [Image.open(path) for path in frame_paths]
            
            # Salva come GIF
            frames[0].save(
                filepath,
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=0
            )
            
            logger.info(f"GIF creato: {filepath}")
            return filepath
            
        except ImportError:
            logger.warning("PIL/Pillow non installato. GIF export non disponibile.")
            return None
        except Exception as e:
            logger.error(f"Errore creazione GIF: {e}")
            return None
    
    def export_full_report(self, code: str, command: str, figure,
                          metadata: Optional[dict] = None) -> dict:
        """
        Esporta report completo: codice + screenshot.
        
        Args:
            code: Codice generato
            command: Comando italiano
            figure: Figura 3D
            metadata: Metadata aggiuntivi
            
        Returns:
            Dict con path dei file esportati
        """
        code_path = self.export_code(code, command, metadata)
        screenshot_path = self.export_screenshot(figure)
        
        report = {
            'code': code_path,
            'screenshot': screenshot_path,
            'timestamp': datetime.now().isoformat(),
            'command': command
        }
        
        logger.info("Report completo esportato")
        return report
    
    def _generate_header(self, command: str, metadata: Optional[dict] = None) -> str:
        """Genera header professionale per file Python."""
        header_lines = [
            '"""',
            'Codice generato da Pythonita IA v3.1',
            'https://github.com/ballales1984-wq/pythonita-ia',
            '',
            f'Data: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        ]
        
        if command:
            header_lines.append(f'Comando: "{command}"')
        
        if metadata:
            header_lines.append('')
            header_lines.append('Metadata:')
            for key, value in metadata.items():
                header_lines.append(f'  {key}: {value}')
        
        header_lines.append('"""')
        
        return '\n'.join(header_lines)
    
    def open_export_folder(self):
        """Apre cartella export in file explorer."""
        import subprocess
        import sys
        
        try:
            if sys.platform == 'win32':
                os.startfile(self.output_dir)
            elif sys.platform == 'darwin':  # macOS
                subprocess.run(['open', self.output_dir])
            else:  # Linux
                subprocess.run(['xdg-open', self.output_dir])
            
            logger.info("Cartella export aperta")
        except Exception as e:
            logger.error(f"Errore apertura cartella: {e}")


# Singleton instance
_export_manager: Optional[ExportManager] = None


def get_export_manager() -> ExportManager:
    """Ottiene istanza singleton export manager."""
    global _export_manager
    if _export_manager is None:
        _export_manager = ExportManager()
    return _export_manager


# Convenience functions
def export_code(code: str, command: str = "", metadata: Optional[dict] = None) -> Path:
    """Export codice Python."""
    return get_export_manager().export_code(code, command, metadata)


def export_screenshot(figure, name: Optional[str] = None) -> Path:
    """Export screenshot 3D."""
    return get_export_manager().export_screenshot(figure, name)


def export_full_report(code: str, command: str, figure, metadata: Optional[dict] = None) -> dict:
    """Export report completo."""
    return get_export_manager().export_full_report(code, command, figure, metadata)


if __name__ == "__main__":
    # Test export
    print("Export Manager - Test")
    
    em = ExportManager()
    
    # Test export codice
    code = 'print("Hello from Pythonita!")'
    path = em.export_code(code, "stampa hello", {"test": True})
    print(f"Codice esportato: {path}")
    
    # Test open folder
    print(f"\nCartella export: {em.output_dir}")
    
    print("\n[OK] Export manager tested!")

