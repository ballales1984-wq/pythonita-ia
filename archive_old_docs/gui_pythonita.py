"""
Interfaccia grafica (GUI) per Pythonita usando Tkinter.
Genera codice Python in tempo reale mentre l'utente scrive.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
from controllore import ciclo_di_controllo
from config import Config
import logging

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PythonitaGUI:
    """Classe per gestire l'interfaccia grafica."""
    
    def __init__(self, root):
        self.root = root
        self.root.title(Config.GUI_TITLE)
        self.root.geometry("900x500")
        
        # Configura layout
        self._setup_layout()
        
        # Variabile per debouncing
        self.after_id = None
    
    def _setup_layout(self):
        """Configura il layout della finestra."""
        # Configura griglia responsive
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)
        
        # Frame superiore con istruzioni
        frame_top = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        frame_top.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        istruzioni = tk.Label(
            frame_top,
            text="💡 Scrivi una frase in italiano per generare codice Python",
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        istruzioni.pack()
        
        # Label input (sinistra)
        label_input = tk.Label(
            self.root,
            text="🗣 Frase in italiano",
            font=("Arial", 12, "bold")
        )
        label_input.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        
        # Label output (destra)
        label_output = tk.Label(
            self.root,
            text="🧾 Codice Python generato",
            font=("Arial", 12, "bold")
        )
        label_output.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")
        
        # Text box input con scrollbar
        self.input_box = scrolledtext.ScrolledText(
            self.root,
            height=Config.GUI_INPUT_HEIGHT,
            width=Config.GUI_WIDTH,
            font=("Consolas", 11),
            wrap=tk.WORD
        )
        self.input_box.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.input_box.bind("<KeyRelease>", self._on_key_release)
        
        # Text box output con scrollbar
        self.output_box = scrolledtext.ScrolledText(
            self.root,
            height=Config.GUI_OUTPUT_HEIGHT,
            width=Config.GUI_WIDTH,
            font=("Consolas", 11),
            wrap=tk.WORD,
            bg="#f9f9f9"
        )
        self.output_box.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")
        
        # Frame inferiore con bottoni
        frame_bottom = tk.Frame(self.root)
        frame_bottom.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Bottone per salvare
        btn_salva = tk.Button(
            frame_bottom,
            text="💾 Salva codice",
            command=self._salva_codice,
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5
        )
        btn_salva.pack(side=tk.LEFT, padx=5)
        
        # Bottone per pulire
        btn_pulisci = tk.Button(
            frame_bottom,
            text="🗑️ Pulisci",
            command=self._pulisci,
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=5
        )
        btn_pulisci.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=4, column=0, columnspan=2, sticky="ew")
    
    def _on_key_release(self, event=None):
        """Gestisce l'evento di rilascio tasto (con debouncing)."""
        # Cancella il timer precedente
        if self.after_id:
            self.root.after_cancel(self.after_id)
        
        # Imposta un nuovo timer (300ms di delay)
        self.after_id = self.root.after(300, self._aggiorna_codice)
    
    def _aggiorna_codice(self):
        """Genera e aggiorna il codice Python."""
        frase = self.input_box.get("1.0", tk.END).strip()
        
        if not frase:
            self.output_box.delete("1.0", tk.END)
            self.status_var.set("Pronto")
            return
        
        try:
            self.status_var.set("Generazione codice...")
            self.root.update_idletasks()
            
            # Genera codice
            codice = ciclo_di_controllo(frase)
            
            # Aggiorna output
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, codice)
            
            self.status_var.set("✅ Codice generato")
            
        except Exception as e:
            logger.error(f"Errore generazione: {e}")
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, f"# Errore: {str(e)}")
            self.status_var.set("❌ Errore nella generazione")
    
    def _salva_codice(self):
        """Salva il codice generato in output.py."""
        codice = self.output_box.get("1.0", tk.END).strip()
        
        if not codice or codice.startswith("# Errore"):
            messagebox.showwarning("Attenzione", "Nessun codice valido da salvare")
            return
        
        try:
            with open(Config.OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(codice)
            
            messagebox.showinfo("Successo", f"Codice salvato in {Config.OUTPUT_FILE}")
            self.status_var.set(f"✅ Salvato in {Config.OUTPUT_FILE.name}")
            
        except Exception as e:
            logger.error(f"Errore salvataggio: {e}")
            messagebox.showerror("Errore", f"Impossibile salvare: {str(e)}")
            self.status_var.set("❌ Errore nel salvataggio")
    
    def _pulisci(self):
        """Pulisce entrambe le text box."""
        self.input_box.delete("1.0", tk.END)
        self.output_box.delete("1.0", tk.END)
        self.status_var.set("Pronto")


def main():
    """Avvia l'interfaccia grafica."""
    root = tk.Tk()
    app = PythonitaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
