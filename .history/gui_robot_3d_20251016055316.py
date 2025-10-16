"""
GUI Pythonita con Visualizzatore 3D Robot.
Interfaccia completa: Comando → Codice → Preview 3D animato!
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import threading

from core.generatore import GeneratoreCodice
from visualizzatore.modelli_3d import ManoRobotica, BraccioRobotico

# UX Improvements
try:
    from pythonita.gui.ux_improvements import (
        Tooltip, StatusBar, UserFriendlyError, LoadingIndicator, add_tooltip
    )
    UX_IMPROVEMENTS_AVAILABLE = True
except ImportError:
    UX_IMPROVEMENTS_AVAILABLE = False
    print("[WARN] UX improvements not available")

# Export Manager
try:
    from pythonita.utils.export import get_export_manager, export_code, export_screenshot
    EXPORT_AVAILABLE = True
except ImportError:
    EXPORT_AVAILABLE = False
    print("[WARN] Export manager not available")


class PythonitaGUI3D:
    """GUI con visualizzazione 3D robot."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Pythonita IA v3.1 - Visualizzatore 3D Robot")
        self.root.geometry("1400x800")
        
        # Generatore con template robot
        self.generatore = GeneratoreCodice(template='robot', use_ai=False, use_cache=False)
        
        # Modelli 3D
        self.mano = ManoRobotica()
        self.braccio = BraccioRobotico()
        
        # Setup UI
        self._setup_ui()
        
        # UX Components
        if UX_IMPROVEMENTS_AVAILABLE:
            self.status_bar = StatusBar(self.root)
            self.status_bar.set_ready()
            print("[GUI] UX improvements enabled ✅")
        else:
            self.status_bar = None
        
        # Timer per aggiornamenti
        self.after_id = None
    
    def _setup_ui(self):
        """Configura interfaccia utente."""
        # Frame superiore: controlli
        frame_controlli = tk.Frame(self.root, bg='#2c3e50', pady=10)
        frame_controlli.pack(fill=tk.X)
        
        tk.Label(frame_controlli, text="Pythonita IA - Visualizzatore 3D Robot",
                font=('Arial', 14, 'bold'), bg='#2c3e50', fg='white').pack()
        
        # Frame template
        frame_template = tk.Frame(frame_controlli, bg='#2c3e50')
        frame_template.pack(pady=5)
        
        tk.Label(frame_template, text="Template:", bg='#2c3e50', fg='white',
                font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        self.template_var = tk.StringVar(value='robot')
        templates = ['robot', 'mano_bionica', 'generico']
        
        for tmpl in templates:
            rb = tk.Radiobutton(frame_template, text=tmpl.capitalize(),
                              variable=self.template_var, value=tmpl,
                              command=self._cambia_template,
                              bg='#2c3e50', fg='white', selectcolor='#34495e',
                              font=('Arial', 9))
            rb.pack(side=tk.LEFT, padx=5)
        
        # Frame principale: 3 colonne
        frame_main = tk.Frame(self.root)
        frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        frame_main.columnconfigure(0, weight=2)  # Input
        frame_main.columnconfigure(1, weight=2)  # Codice
        frame_main.columnconfigure(2, weight=3)  # 3D
        
        # COLONNA 1: Input
        self._setup_colonna_input(frame_main)
        
        # COLONNA 2: Codice
        self._setup_colonna_codice(frame_main)
        
        # COLONNA 3: Visualizzatore 3D
        self._setup_colonna_3d(frame_main)
        
        # Frame inferiore: bottoni azione
        self._setup_bottoni_azione()
    
    def _setup_colonna_input(self, parent):
        """Setup colonna input."""
        frame = tk.Frame(parent)
        frame.grid(row=0, column=0, sticky='nsew', padx=5)
        
        tk.Label(frame, text="Comando in Italiano",
                font=('Arial', 11, 'bold')).pack(anchor='w')
        
        self.input_box = scrolledtext.ScrolledText(frame, height=15, width=35,
                                                   font=('Consolas', 10), wrap=tk.WORD)
        self.input_box.pack(fill=tk.BOTH, expand=True, pady=5)
        # RIMOSSO auto-update per evitare lag: self.input_box.bind('<KeyRelease>', self._on_key_release)
        
        # Esempi rapidi
        tk.Label(frame, text="Esempi Rapidi:", font=('Arial', 9, 'bold')).pack(anchor='w', pady=(10,5))
        
        esempi_frame = tk.Frame(frame)
        esempi_frame.pack(fill=tk.X)
        
        esempi = [
            ("Apri Mano", "apri mano"),
            ("Chiudi Pugno", "chiudi pugno"),
            ("Pinza", "fai pinza"),
            ("Afferra", "afferra oggetto"),
        ]
        
        for testo, comando in esempi:
            btn = tk.Button(esempi_frame, text=testo, 
                          command=lambda c=comando: self._inserisci_esempio(c),
                          font=('Arial', 8), bg='#3498db', fg='white')
            btn.pack(fill=tk.X, pady=2)
    
    def _setup_colonna_codice(self, parent):
        """Setup colonna codice."""
        frame = tk.Frame(parent)
        frame.grid(row=0, column=1, sticky='nsew', padx=5)
        
        tk.Label(frame, text="Codice Python Generato",
                font=('Arial', 11, 'bold')).pack(anchor='w')
        
        self.output_box = scrolledtext.ScrolledText(frame, height=15, width=40,
                                                    font=('Consolas', 9), wrap=tk.WORD,
                                                    bg='#f9f9f9')
        self.output_box.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def _setup_colonna_3d(self, parent):
        """Setup colonna visualizzatore 3D."""
        frame = tk.Frame(parent)
        frame.grid(row=0, column=2, sticky='nsew', padx=5)
        
        tk.Label(frame, text="Preview 3D (Misure Reali)",
                font=('Arial', 11, 'bold')).pack(anchor='w')
        
        # Canvas matplotlib per 3D
        self.fig = Figure(figsize=(6, 6), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Disegna mano iniziale
        self._disegna_mano_3d()
    
    def _setup_bottoni_azione(self):
        """Setup bottoni azione."""
        frame = tk.Frame(self.root, bg='#ecf0f1', pady=10)
        frame.pack(fill=tk.X)
        
        btn_genera = tk.Button(frame, text="Genera Codice",
                              command=self._aggiorna_codice,
                              font=('Arial', 10, 'bold'), bg='#f39c12', fg='white',
                              padx=20, pady=8)
        btn_genera.pack(side=tk.LEFT, padx=10)
        
        btn_esegui = tk.Button(frame, text="Esegui Animazione 3D",
                              command=self._esegui_animazione,
                              font=('Arial', 10, 'bold'), bg='#27ae60', fg='white',
                              padx=20, pady=8)
        btn_esegui.pack(side=tk.LEFT, padx=10)
        
        btn_reset = tk.Button(frame, text="Reset Posizione",
                            command=self._reset_robot,
                            font=('Arial', 10), bg='#e74c3c', fg='white',
                            padx=20, pady=8)
        btn_reset.pack(side=tk.LEFT, padx=10)
        
        btn_salva = tk.Button(frame, text="Salva Codice",
                            command=self._salva_codice,
                            font=('Arial', 10), bg='#3498db', fg='white',
                            padx=20, pady=8)
        btn_salva.pack(side=tk.LEFT, padx=10)
        
        # Status
        self.status_var = tk.StringVar(value="Pronto")
        self.status_label = tk.Label(frame, textvariable=self.status_var,
                                     bg='#ecf0f1', font=('Arial', 9))
        self.status_label.pack(side=tk.RIGHT, padx=10)
    
    def _cambia_template(self):
        """Cambia template attivo."""
        nuovo_template = self.template_var.get()
        self.generatore.sistema_template.scegli_template(nuovo_template)
        self.status_var.set(f"Template: {nuovo_template}")
        self._aggiorna_codice()
    
    def _inserisci_esempio(self, comando):
        """Inserisce esempio nel box input e genera automaticamente."""
        self.input_box.delete('1.0', tk.END)
        self.input_box.insert('1.0', comando)
        self._aggiorna_codice()  # Genera subito per gli esempi
    
    # RIMOSSA funzione _on_key_release - ora si usa il bottone "Genera Codice"
    
    def _aggiorna_codice(self):
        """Aggiorna codice generato."""
        frase = self.input_box.get('1.0', tk.END).strip()
        
        if not frase:
            self.output_box.delete('1.0', tk.END)
            if self.status_bar:
                self.status_bar.set_ready()
            return
        
        try:
            # Status bar update
            if self.status_bar:
                self.status_bar.set_busy("Generando codice...")
            self.status_var.set("Generando...")
            self.root.update()
            
            # Genera codice
            codice = self.generatore.genera(frase)
            
            # Mostra codice
            self.output_box.delete('1.0', tk.END)
            self.output_box.insert('1.0', codice)
            
            # Success feedback
            if self.status_bar:
                self.status_bar.set_success("Codice generato! Premi 'Esegui Animazione'")
            self.status_var.set("Codice generato! Premi 'Esegui Animazione'")
            
        except Exception as e:
            # User-friendly error handling
            if UX_IMPROVEMENTS_AVAILABLE:
                UserFriendlyError.show_error(
                    self.root, e, 
                    "Errore durante la generazione del codice"
                )
                if self.status_bar:
                    self.status_bar.set_error(str(e)[:50])
            else:
                messagebox.showerror("Errore", f"Errore generazione: {e}")
            
            self.status_var.set("Errore! Riprova")
    
    def _esegui_animazione(self):
        """Esegue animazione 3D basata sul comando."""
        frase = self.input_box.get('1.0', tk.END).strip().lower()
        
        if not frase:
            return
        
        self.status_var.set("Animazione in corso...")
        
        # Identifica azione
        if "apri mano" in frase or "apri" in frase:
            self._anima_apri_mano()
        elif "chiudi" in frase and "pugno" in frase:
            self._anima_chiudi_pugno()
        elif "pinza" in frase:
            self._anima_pinza()
        elif "afferra" in frase:
            self._anima_afferra()
        elif "alza braccio" in frase:
            self._anima_alza_braccio()
        else:
            # Default: mostra stato
            self._disegna_mano_3d()
            self.status_var.set("Preview 3D aggiornata")
    
    def _anima_apri_mano(self):
        """Animazione apertura mano."""
        def anima():
            for i in range(20, -1, -1):
                perc = (i / 20) * 100
                self.mano.chiudi_mano(perc)
                self._disegna_mano_3d()
                self.root.after(50)
            self.status_var.set("Mano aperta! (0%)")
        
        threading.Thread(target=anima, daemon=True).start()
    
    def _anima_chiudi_pugno(self):
        """Animazione chiusura pugno."""
        def anima():
            for i in range(21):
                perc = (i / 20) * 100
                self.mano.chiudi_mano(perc)
                self._disegna_mano_3d()
                self.root.after(50)
            self.status_var.set("Pugno chiuso! (100%)")
        
        threading.Thread(target=anima, daemon=True).start()
    
    def _anima_pinza(self):
        """Animazione posizione pinza."""
        def anima():
            self.mano.apri_mano()
            self._disegna_mano_3d()
            self.root.after(300)
            
            self.mano.posizione_pinza(apertura_mm=20)
            self._disegna_mano_3d()
            self.status_var.set("Posizione pinza (pollice-indice)")
        
        threading.Thread(target=anima, daemon=True).start()
    
    def _anima_afferra(self):
        """Animazione afferra oggetto."""
        self._anima_chiudi_pugno()
    
    def _anima_alza_braccio(self):
        """Animazione alza braccio."""
        def anima():
            for i in range(31):
                angolo = i * 3  # 0 a 90 gradi
                self.braccio.alza_braccio(angolo)
                self._disegna_braccio_3d()
                self.root.after(30)
            self.status_var.set(f"Braccio alzato a {self.braccio.angolo_spalla}°")
        
        threading.Thread(target=anima, daemon=True).start()
    
    def _disegna_mano_3d(self):
        """Disegna mano 3D."""
        self.ax.clear()
        
        # Setup assi
        self.ax.set_xlabel('X (cm)', fontsize=8)
        self.ax.set_ylabel('Y (cm)', fontsize=8)
        self.ax.set_zlabel('Z (cm)', fontsize=8)
        self.ax.set_title('Mano Robotica', fontsize=10, fontweight='bold')
        
        limite = 12
        self.ax.set_xlim([-limite, limite])
        self.ax.set_ylim([0, limite])
        self.ax.set_zlim([-limite, limite])
        self.ax.view_init(elev=20, azim=45)
        self.ax.grid(True, alpha=0.3)
        
        # Disegna palmo
        larghezza = self.mano.dimensioni.LARGHEZZA_PALMO
        vertices = np.array([
            [-larghezza/2, 0, -2], [larghezza/2, 0, -2],
            [larghezza/2, 0, 2], [-larghezza/2, 0, 2], [-larghezza/2, 0, -2]
        ])
        self.ax.plot(vertices[:, 0], vertices[:, 1], vertices[:, 2],
                    'k-', linewidth=2, label='Palmo')
        
        # Disegna dita
        colori = {'pollice': 'red', 'indice': 'blue', 'medio': 'green',
                 'anulare': 'orange', 'mignolo': 'purple'}
        
        for nome, colore in colori.items():
            vertici = self.mano.get_vertici_dito(nome)
            pos_base = self.mano.get_posizione_base_dito(nome)
            
            xs = [v[0] + pos_base[0] for v in vertici]
            ys = [v[1] + pos_base[1] for v in vertici]
            zs = [v[2] + pos_base[2] for v in vertici]
            
            self.ax.plot(xs, ys, zs, color=colore, linewidth=2, marker='o', markersize=3)
        
        # Info stato
        perc = self._calcola_chiusura()
        info = f"Chiusura: {perc:.0f}%"
        self.ax.text2D(0.02, 0.98, info, transform=self.ax.transAxes,
                      fontsize=9, verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        self.canvas.draw()
    
    def _disegna_braccio_3d(self):
        """Disegna braccio 3D."""
        self.ax.clear()
        
        # Setup
        self.ax.set_xlabel('X (cm)', fontsize=8)
        self.ax.set_ylabel('Y (cm)', fontsize=8)
        self.ax.set_zlabel('Z (cm)', fontsize=8)
        self.ax.set_title('Braccio Robotico', fontsize=10, fontweight='bold')
        
        limite = 40
        self.ax.set_xlim([0, limite])
        self.ax.set_ylim([0, limite])
        self.ax.set_zlim([0, limite])
        self.ax.view_init(elev=15, azim=45)
        self.ax.grid(True, alpha=0.3)
        
        # Calcola posizioni
        p0 = np.array([0, 0, 30])
        
        L1 = self.braccio.dimensioni.LUNGHEZZA_BRACCIO_SUPERIORE
        theta1 = np.radians(self.braccio.angolo_spalla)
        p1 = p0 + np.array([L1 * np.cos(theta1), L1 * np.sin(theta1), 0])
        
        L2 = self.braccio.dimensioni.LUNGHEZZA_AVAMBRACCIO
        theta2 = theta1 + np.radians(self.braccio.angolo_gomito)
        p2 = p1 + np.array([L2 * np.cos(theta2), L2 * np.sin(theta2), 0])
        
        # Disegna
        self.ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]],
                    'b-', linewidth=5, label='Braccio sup.')
        self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                    'r-', linewidth=5, label='Avambraccio')
        
        self.ax.scatter(*p0, color='black', s=80)
        self.ax.scatter(*p1, color='green', s=80)
        self.ax.scatter(*p2, color='red', s=80)
        
        # Info
        info = f"Spalla: {self.braccio.angolo_spalla}°\nGomito: {self.braccio.angolo_gomito}°"
        self.ax.text2D(0.02, 0.98, info, transform=self.ax.transAxes,
                      fontsize=9, verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        self.canvas.draw()
    
    def _calcola_chiusura(self):
        """Calcola percentuale chiusura media."""
        totale = 0
        for angoli in self.mano.angoli_dita.values():
            media = sum(angoli) / len(angoli)
            perc = (media / self.mano.dimensioni.ANGOLO_MAX_DITO) * 100
            totale += perc
        return totale / len(self.mano.angoli_dita)
    
    def _reset_robot(self):
        """Reset posizione robot."""
        self.mano.apri_mano()
        self.braccio.angolo_spalla = 0
        self.braccio.angolo_gomito = 0
        self._disegna_mano_3d()
        self.status_var.set("Posizione resettata")
    
    def _salva_codice(self):
        """Salva codice generato."""
        codice = self.output_box.get('1.0', tk.END).strip()
        if codice:
            with open('output_robot.py', 'w', encoding='utf-8') as f:
                f.write(codice)
            self.status_var.set("Codice salvato in output_robot.py")
    
    def _cambia_template(self):
        """Cambia template."""
        self._aggiorna_codice()


def main():
    """Avvia GUI con visualizzatore 3D."""
    root = tk.Tk()
    app = PythonitaGUI3D(root)
    
    print("""
==================================================================
      PYTHONITA IA v3.1 - VISUALIZZATORE 3D ROBOT
==================================================================

COME USARE:
1. Scrivi comando in italiano (es: "apri mano")
2. Premi "Genera Codice" (bottone arancione)
3. Premi "Esegui Animazione 3D" (bottone verde)
4. Guarda la mano 3D animarsi!

COMANDI DISPONIBILI:
- apri mano / chiudi pugno
- fai pinza
- afferra oggetto
- alza braccio

NOTA: Ora puoi scrivere SENZA LAG!
Il codice si genera solo quando premi il bottone.

La GUI e' aperta!
==================================================================
""")
    
    root.mainloop()


if __name__ == "__main__":
    main()

