"""
Theme System - Sistema di temi per GUI Pythonita.
Supporta Dark Mode, Light Mode e High Contrast per accessibilità.
"""

from dataclasses import dataclass
from typing import Dict
import json
from pathlib import Path


@dataclass
class ColorScheme:
    """Schema colori per un tema."""
    # Background
    bg_primary: str
    bg_secondary: str
    bg_tertiary: str
    
    # Foreground/Text
    fg_primary: str
    fg_secondary: str
    fg_disabled: str
    
    # Accents
    accent_primary: str
    accent_secondary: str
    accent_success: str
    accent_warning: str
    accent_error: str
    
    # Buttons
    btn_primary_bg: str
    btn_primary_fg: str
    btn_secondary_bg: str
    btn_secondary_fg: str
    btn_danger_bg: str
    btn_danger_fg: str
    
    # Input/Output
    input_bg: str
    input_fg: str
    output_bg: str
    output_fg: str
    
    # Status bar
    status_bg: str
    status_fg: str
    
    # Borders
    border_color: str
    
    def to_dict(self) -> Dict:
        """Converti in dizionario."""
        return {
            'bg_primary': self.bg_primary,
            'bg_secondary': self.bg_secondary,
            'bg_tertiary': self.bg_tertiary,
            'fg_primary': self.fg_primary,
            'fg_secondary': self.fg_secondary,
            'fg_disabled': self.fg_disabled,
            'accent_primary': self.accent_primary,
            'accent_secondary': self.accent_secondary,
            'accent_success': self.accent_success,
            'accent_warning': self.accent_warning,
            'accent_error': self.accent_error,
            'btn_primary_bg': self.btn_primary_bg,
            'btn_primary_fg': self.btn_primary_fg,
            'btn_secondary_bg': self.btn_secondary_bg,
            'btn_secondary_fg': self.btn_secondary_fg,
            'btn_danger_bg': self.btn_danger_bg,
            'btn_danger_fg': self.btn_danger_fg,
            'input_bg': self.input_bg,
            'input_fg': self.input_fg,
            'output_bg': self.output_bg,
            'output_fg': self.output_fg,
            'status_bg': self.status_bg,
            'status_fg': self.status_fg,
            'border_color': self.border_color,
        }


# ═══════════════════════════════════════════════════════════════════
# TEMI PREDEFINITI
# ═══════════════════════════════════════════════════════════════════

LIGHT_THEME = ColorScheme(
    # Background - Tonalità chiare
    bg_primary='#FFFFFF',
    bg_secondary='#F5F5F5',
    bg_tertiary='#E8E8E8',
    
    # Foreground - Testo scuro
    fg_primary='#212121',
    fg_secondary='#666666',
    fg_disabled='#AAAAAA',
    
    # Accents - Colori vivaci
    accent_primary='#2196F3',      # Blu
    accent_secondary='#673AB7',    # Viola
    accent_success='#4CAF50',      # Verde
    accent_warning='#FF9800',      # Arancione
    accent_error='#F44336',        # Rosso
    
    # Buttons
    btn_primary_bg='#F39C12',      # Arancione
    btn_primary_fg='#FFFFFF',
    btn_secondary_bg='#27AE60',    # Verde
    btn_secondary_fg='#FFFFFF',
    btn_danger_bg='#E74C3C',       # Rosso
    btn_danger_fg='#FFFFFF',
    
    # Input/Output
    input_bg='#FFFFFF',
    input_fg='#212121',
    output_bg='#F9F9F9',
    output_fg='#212121',
    
    # Status bar
    status_bg='#ECF0F1',
    status_fg='#2C3E50',
    
    # Borders
    border_color='#CCCCCC',
)


DARK_THEME = ColorScheme(
    # Background - Tonalità scure
    bg_primary='#1E1E1E',
    bg_secondary='#252526',
    bg_tertiary='#2D2D30',
    
    # Foreground - Testo chiaro
    fg_primary='#D4D4D4',
    fg_secondary='#CCCCCC',
    fg_disabled='#666666',
    
    # Accents - Colori brillanti per contrasto
    accent_primary='#42A5F5',      # Blu chiaro
    accent_secondary='#9575CD',    # Viola chiaro
    accent_success='#66BB6A',      # Verde chiaro
    accent_warning='#FFA726',      # Arancione chiaro
    accent_error='#EF5350',        # Rosso chiaro
    
    # Buttons
    btn_primary_bg='#FFA726',      # Arancione
    btn_primary_fg='#1E1E1E',
    btn_secondary_bg='#66BB6A',    # Verde
    btn_secondary_fg='#1E1E1E',
    btn_danger_bg='#EF5350',       # Rosso
    btn_danger_fg='#FFFFFF',
    
    # Input/Output
    input_bg='#252526',
    input_fg='#D4D4D4',
    output_bg='#1E1E1E',
    output_fg='#D4D4D4',
    
    # Status bar
    status_bg='#007ACC',
    status_fg='#FFFFFF',
    
    # Borders
    border_color='#3E3E42',
)


HIGH_CONTRAST_THEME = ColorScheme(
    # Background - Massimo contrasto
    bg_primary='#000000',
    bg_secondary='#000000',
    bg_tertiary='#1A1A1A',
    
    # Foreground - Bianco puro
    fg_primary='#FFFFFF',
    fg_secondary='#FFFFFF',
    fg_disabled='#808080',
    
    # Accents - Colori brillanti
    accent_primary='#00FFFF',      # Ciano
    accent_secondary='#FF00FF',    # Magenta
    accent_success='#00FF00',      # Verde lime
    accent_warning='#FFFF00',      # Giallo
    accent_error='#FF0000',        # Rosso puro
    
    # Buttons
    btn_primary_bg='#FFFF00',      # Giallo
    btn_primary_fg='#000000',
    btn_secondary_bg='#00FF00',    # Verde
    btn_secondary_fg='#000000',
    btn_danger_bg='#FF0000',       # Rosso
    btn_danger_fg='#FFFFFF',
    
    # Input/Output
    input_bg='#000000',
    input_fg='#FFFFFF',
    output_bg='#000000',
    output_fg='#00FF00',           # Verde per output
    
    # Status bar
    status_bg='#FFFF00',
    status_fg='#000000',
    
    # Borders
    border_color='#FFFFFF',
)


# ═══════════════════════════════════════════════════════════════════
# THEME MANAGER
# ═══════════════════════════════════════════════════════════════════

class ThemeManager:
    """Gestisce i temi dell'applicazione."""
    
    THEMES = {
        'light': LIGHT_THEME,
        'dark': DARK_THEME,
        'high_contrast': HIGH_CONTRAST_THEME,
    }
    
    def __init__(self):
        """Inizializza theme manager."""
        self.current_theme_name = 'light'
        self.current_theme = LIGHT_THEME
        self.preferences_file = Path.home() / '.pythonita' / 'theme_preferences.json'
        self.preferences_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Carica preferenze salvate
        self._load_preferences()
    
    def get_theme(self, theme_name: str = None) -> ColorScheme:
        """
        Ottiene schema colori di un tema.
        
        Args:
            theme_name: Nome tema ('light', 'dark', 'high_contrast')
                       Se None, ritorna tema corrente
        
        Returns:
            ColorScheme del tema
        """
        if theme_name is None:
            return self.current_theme
        
        return self.THEMES.get(theme_name, LIGHT_THEME)
    
    def set_theme(self, theme_name: str):
        """
        Imposta tema corrente.
        
        Args:
            theme_name: Nome tema ('light', 'dark', 'high_contrast')
        """
        if theme_name in self.THEMES:
            self.current_theme_name = theme_name
            self.current_theme = self.THEMES[theme_name]
            self._save_preferences()
    
    def get_available_themes(self) -> list:
        """Ritorna lista di temi disponibili."""
        return list(self.THEMES.keys())
    
    def apply_to_widget(self, widget, widget_type: str = 'default'):
        """
        Applica tema corrente a un widget Tkinter.
        
        Args:
            widget: Widget Tkinter
            widget_type: Tipo widget ('frame', 'button', 'label', ecc)
        """
        theme = self.current_theme
        
        try:
            if widget_type == 'frame':
                widget.config(bg=theme.bg_primary)
            
            elif widget_type == 'frame_secondary':
                widget.config(bg=theme.bg_secondary)
            
            elif widget_type == 'label':
                widget.config(bg=theme.bg_primary, fg=theme.fg_primary)
            
            elif widget_type == 'button_primary':
                widget.config(bg=theme.btn_primary_bg, fg=theme.btn_primary_fg,
                            activebackground=theme.accent_warning,
                            activeforeground=theme.btn_primary_fg)
            
            elif widget_type == 'button_secondary':
                widget.config(bg=theme.btn_secondary_bg, fg=theme.btn_secondary_fg,
                            activebackground=theme.accent_success,
                            activeforeground=theme.btn_secondary_fg)
            
            elif widget_type == 'button_danger':
                widget.config(bg=theme.btn_danger_bg, fg=theme.btn_danger_fg,
                            activebackground=theme.accent_error,
                            activeforeground=theme.btn_danger_fg)
            
            elif widget_type == 'text_input':
                widget.config(bg=theme.input_bg, fg=theme.input_fg,
                            insertbackground=theme.fg_primary)
            
            elif widget_type == 'text_output':
                widget.config(bg=theme.output_bg, fg=theme.output_fg,
                            insertbackground=theme.fg_primary)
            
            elif widget_type == 'status_bar':
                widget.config(bg=theme.status_bg, fg=theme.status_fg)
            
        except Exception as e:
            print(f"[THEME] Errore applicazione tema a {widget_type}: {e}")
    
    def apply_to_root(self, root):
        """Applica tema a finestra root."""
        try:
            root.config(bg=self.current_theme.bg_primary)
        except:
            pass
    
    def _load_preferences(self):
        """Carica preferenze tema da disco."""
        if self.preferences_file.exists():
            try:
                with open(self.preferences_file, 'r') as f:
                    data = json.load(f)
                    theme_name = data.get('theme', 'light')
                    if theme_name in self.THEMES:
                        self.current_theme_name = theme_name
                        self.current_theme = self.THEMES[theme_name]
            except:
                pass
    
    def _save_preferences(self):
        """Salva preferenze tema su disco."""
        try:
            with open(self.preferences_file, 'w') as f:
                json.dump({'theme': self.current_theme_name}, f)
        except:
            pass


# Singleton instance
_theme_manager = None


def get_theme_manager() -> ThemeManager:
    """Ottiene istanza singleton theme manager."""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager


# Convenience functions
def get_current_theme() -> ColorScheme:
    """Ottiene tema corrente."""
    return get_theme_manager().get_theme()


def set_theme(theme_name: str):
    """Imposta tema."""
    get_theme_manager().set_theme(theme_name)


def apply_theme_to_widget(widget, widget_type: str = 'default'):
    """Applica tema a widget."""
    get_theme_manager().apply_to_widget(widget, widget_type)


if __name__ == "__main__":
    # Test themes
    print("Theme System - Test\n")
    
    tm = ThemeManager()
    
    print("Temi disponibili:", tm.get_available_themes())
    print(f"\nTema corrente: {tm.current_theme_name}")
    
    # Test cambio tema
    for theme_name in ['light', 'dark', 'high_contrast']:
        tm.set_theme(theme_name)
        theme = tm.get_theme()
        print(f"\n{theme_name.upper()} THEME:")
        print(f"  BG Primary: {theme.bg_primary}")
        print(f"  FG Primary: {theme.fg_primary}")
        print(f"  Accent: {theme.accent_primary}")
    
    print("\n[OK] Theme system tested!")

