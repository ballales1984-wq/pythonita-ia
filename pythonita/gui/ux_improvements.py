"""
UX Improvements per GUI Pythonita.
Tooltip, progress bar, status bar, error handling user-friendly.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
import time


class Tooltip:
    """
    Tooltip personalizzato per widget Tkinter.
    Mostra suggerimenti al passaggio del mouse.
    """
    
    def __init__(self, widget, text: str, delay=500):
        """
        Crea tooltip.
        
        Args:
            widget: Widget Tkinter
            text: Testo tooltip
            delay: Ritardo prima di mostrare (ms)
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        
        # Bind eventi
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
    
    def enter(self, event=None):
        """Mouse entra su widget."""
        self.schedule()
    
    def leave(self, event=None):
        """Mouse esce da widget."""
        self.unschedule()
        self.hidetip()
    
    def schedule(self):
        """Schedula mostrata tooltip."""
        self.unschedule()
        self.id = self.widget.after(self.delay, self.showtip)
    
    def unschedule(self):
        """Cancella scheduled tooltip."""
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)
    
    def showtip(self, event=None):
        """Mostra tooltip."""
        if self.tipwindow or not self.text:
            return
        
        x, y, cx, cy = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                        background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                        font=("Arial", 9, "normal"))
        label.pack(ipadx=1)
    
    def hidetip(self):
        """Nascondi tooltip."""
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


class ProgressDialog:
    """
    Dialog con progress bar per operazioni lunghe.
    """
    
    def __init__(self, parent, title="Elaborazione in corso...", message="Attendere prego"):
        """
        Crea progress dialog.
        
        Args:
            parent: Finestra parent
            title: Titolo dialog
            message: Messaggio
        """
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centra dialog
        self.dialog.geometry("400x150")
        self._center_window(parent)
        
        # Message
        tk.Label(self.dialog, text=message, font=('Arial', 10)).pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.dialog, length=350, mode='indeterminate')
        self.progress.pack(pady=10)
        self.progress.start(10)
        
        # Status label
        self.status_label = tk.Label(self.dialog, text="", font=('Arial', 9))
        self.status_label.pack(pady=5)
        
        # Bottone cancella (opzionale)
        self.cancelled = False
        tk.Button(self.dialog, text="Annulla", command=self.cancel).pack(pady=10)
    
    def _center_window(self, parent):
        """Centra dialog su parent."""
        self.dialog.update_idletasks()
        
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        
        self.dialog.geometry(f"+{x}+{y}")
    
    def update_status(self, text: str):
        """Aggiorna testo status."""
        self.status_label.config(text=text)
        self.dialog.update()
    
    def cancel(self):
        """Cancella operazione."""
        self.cancelled = True
        self.close()
    
    def close(self):
        """Chiudi dialog."""
        self.progress.stop()
        self.dialog.destroy()


class StatusBar:
    """
    Status bar per mostrare info real-time.
    """
    
    def __init__(self, parent):
        """Crea status bar."""
        self.frame = tk.Frame(parent, bd=1, relief=tk.SUNKEN)
        
        # Label sinistra (messaggio principale)
        self.label_main = tk.Label(self.frame, text="Pronto", anchor=tk.W,
                                   font=('Arial', 9), bg='#ecf0f1')
        self.label_main.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Label destra (info secondaria - es: FPS, tempo)
        self.label_info = tk.Label(self.frame, text="", anchor=tk.E,
                                  font=('Arial', 9), bg='#ecf0f1')
        self.label_info.pack(side=tk.RIGHT, padx=5)
        
        self.frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set_text(self, text: str):
        """Imposta testo principale."""
        self.label_main.config(text=text)
    
    def set_info(self, text: str):
        """Imposta info secondaria."""
        self.label_info.config(text=text)
    
    def set_ready(self):
        """Stato pronto."""
        self.set_text("✅ Pronto")
        self.set_info("")
    
    def set_busy(self, message="Elaborazione..."):
        """Stato occupato."""
        self.set_text(f"⏳ {message}")
    
    def set_error(self, message):
        """Stato errore."""
        self.set_text(f"❌ Errore: {message}")
    
    def set_success(self, message="Operazione completata"):
        """Stato successo."""
        self.set_text(f"✅ {message}")


class UserFriendlyError:
    """
    Gestione errori user-friendly.
    Converte errori tecnici in messaggi comprensibili.
    """
    
    ERROR_MESSAGES = {
        'ModuleNotFoundError': {
            'title': 'Modulo Mancante',
            'message': 'Un componente necessario non è installato.\n\nInstalla le dipendenze con:\npip install -r requirements.txt'
        },
        'FileNotFoundError': {
            'title': 'File Non Trovato',
            'message': 'Un file necessario non è stato trovato.\n\nVerifica che tutti i file del programma siano presenti.'
        },
        'ConnectionError': {
            'title': 'Errore Connessione',
            'message': 'Impossibile connettersi al servizio AI.\n\nVerifica che Ollama sia avviato:\nollama serve'
        },
        'ValueError': {
            'title': 'Valore Non Valido',
            'message': 'Il comando inserito non è valido o contiene errori.\n\nProva con un comando più semplice.'
        },
        'KeyError': {
            'title': 'Parametro Mancante',
            'message': 'Manca un parametro necessario per l\'operazione.\n\nControlla che il comando sia completo.'
        },
        'AttributeError': {
            'title': 'Errore Interno',
            'message': 'Si è verificato un errore interno.\n\nProva a riavviare il programma.'
        },
    }
    
    @staticmethod
    def show_error(parent, exception: Exception, context: str = ""):
        """
        Mostra errore in modo user-friendly.
        
        Args:
            parent: Finestra parent
            exception: Eccezione verificatasi
            context: Contesto errore
        """
        error_type = type(exception).__name__
        error_info = UserFriendlyError.ERROR_MESSAGES.get(error_type)
        
        if error_info:
            title = error_info['title']
            message = error_info['message']
        else:
            title = "Errore"
            message = f"Si è verificato un errore:\n\n{str(exception)}"
        
        if context:
            message = f"{context}\n\n{message}"
        
        # Log tecnico (per debugging)
        print(f"[ERROR] {error_type}: {exception}")
        import traceback
        traceback.print_exc()
        
        # Mostra dialog user-friendly
        messagebox.showerror(title, message, parent=parent)
    
    @staticmethod
    def wrap_function(func: Callable, parent=None, context: str = "") -> Callable:
        """
        Wrapper che cattura errori e li mostra in modo user-friendly.
        
        Args:
            func: Funzione da wrappare
            parent: Finestra parent per dialog
            context: Contesto operazione
            
        Returns:
            Funzione wrappata
        """
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                UserFriendlyError.show_error(parent, e, context)
                return None
        
        return wrapped


class LoadingIndicator:
    """
    Indicatore di caricamento animato.
    """
    
    def __init__(self, label_widget: tk.Label):
        """
        Crea loading indicator.
        
        Args:
            label_widget: Widget Label dove mostrare animazione
        """
        self.label = label_widget
        self.running = False
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_frame = 0
        self.original_text = ""
    
    def start(self, text="Caricamento"):
        """Avvia animazione."""
        self.original_text = text
        self.running = True
        self._animate()
    
    def stop(self, final_text="Completato"):
        """Ferma animazione."""
        self.running = False
        if self.label.winfo_exists():
            self.label.config(text=final_text)
    
    def _animate(self):
        """Frame animazione."""
        if not self.running or not self.label.winfo_exists():
            return
        
        frame = self.frames[self.current_frame]
        self.label.config(text=f"{frame} {self.original_text}")
        
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        
        # Schedule prossimo frame
        self.label.after(100, self._animate)


# Helper functions
def add_tooltip(widget, text: str):
    """
    Aggiunge tooltip a widget.
    
    Args:
        widget: Widget Tkinter
        text: Testo tooltip
    """
    Tooltip(widget, text)


def run_with_progress(parent, func: Callable, title="Elaborazione", message="Attendere"):
    """
    Esegue funzione mostrando progress dialog.
    
    Args:
        parent: Finestra parent
        func: Funzione da eseguire
        title: Titolo dialog
        message: Messaggio dialog
    """
    progress = ProgressDialog(parent, title, message)
    
    def worker():
        try:
            result = func(progress)
            progress.close()
            return result
        except Exception as e:
            progress.close()
            UserFriendlyError.show_error(parent, e)
    
    # Run in thread per non bloccare GUI
    import threading
    thread = threading.Thread(target=worker)
    thread.start()


if __name__ == "__main__":
    # Test UX components
    root = tk.Tk()
    root.title("UX Components Test")
    root.geometry("500x400")
    
    # Test tooltip
    btn1 = tk.Button(root, text="Hover per tooltip")
    btn1.pack(pady=20)
    add_tooltip(btn1, "Questo è un tooltip di esempio!")
    
    # Test status bar
    status = StatusBar(root)
    status.set_text("Test status bar")
    status.set_info("FPS: 30")
    
    # Test progress
    def show_progress():
        progress = ProgressDialog(root, "Test", "Elaborazione test...")
        root.after(2000, progress.close)
    
    tk.Button(root, text="Test Progress", command=show_progress).pack(pady=10)
    
    # Test error
    def show_error():
        try:
            raise ValueError("Test errore")
        except Exception as e:
            UserFriendlyError.show_error(root, e, "Test context")
    
    tk.Button(root, text="Test Error Dialog", command=show_error).pack(pady=10)
    
    # Test loading indicator
    label = tk.Label(root, text="", font=('Arial', 12))
    label.pack(pady=20)
    
    loader = LoadingIndicator(label)
    
    def toggle_loading():
        if not loader.running:
            loader.start("Generazione codice")
        else:
            loader.stop("✅ Completato!")
    
    tk.Button(root, text="Toggle Loading", command=toggle_loading).pack(pady=10)
    
    root.mainloop()

