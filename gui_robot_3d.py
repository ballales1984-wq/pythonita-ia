"""
GUI Pythonita con Visualizzatore 3D Robot.
Interfaccia completa: Comando → Codice → Preview 3D animato!
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Dict, Optional, List
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import threading

from pythonita.core.generatore import GeneratoreCodice
from pythonita.visualization.modelli_3d import ManoRobotica, BraccioRobotico

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

# Theme System
try:
    from pythonita.gui.themes import get_theme_manager, get_current_theme
    THEMES_AVAILABLE = True
except ImportError:
    THEMES_AVAILABLE = False
    print("[WARN] Theme system not available")

# Speech Recognition (DISABILITATO - problemi volume microfono persistenti)
try:
    from pythonita.utils.speech_recognition_module import get_speech_recognizer
    SPEECH_RECOGNITION_AVAILABLE = False  # ❌ Disabilitato - problema clipping non risolto
    print("[INFO] Speech recognition disabilitato - usa input manuale")
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("[WARN] Speech recognition not available")

# Arduino Controller
try:
    from pythonita.hardware.arduino_controller import get_arduino_controller
    from pythonita.core.arduino_commands import get_arduino_template
    ARDUINO_AVAILABLE = True
except ImportError:
    ARDUINO_AVAILABLE = False
    print("[WARN] Arduino controller not available")


class PythonitaGUI3D:
    """GUI con visualizzazione 3D robot."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Pythonita IA v3.5 Pro - AI Code Generator")
        
        # ADATTA AUTOMATICAMENTE ALLO SCHERMO
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Usa 85% dello schermo (lascia spazio per taskbar)
        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)
        
        # Posizione centrata
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(1000, 600)  # Minimo funzionale
        
        print(f"[GUI] Schermo: {screen_width}x{screen_height}")
        print(f"[GUI] Finestra: {window_width}x{window_height} (85% schermo)")
        
        # Tema colori moderni
        self.colors = {
            'bg_dark': '#1e1e2e',      # Sfondo scuro elegante
            'bg_medium': '#2d2d44',    # Medio
            'bg_light': '#3d3d5c',     # Chiaro
            'accent': '#00d4ff',       # Cyan brillante
            'success': '#00ff88',      # Verde acceso
            'warning': '#ffaa00',      # Arancione
            'error': '#ff4466',        # Rosso
            'text': '#e0e0e0',         # Testo chiaro
            'text_dim': '#888888',     # Testo secondario
        }
        
        # Configura tema root
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Generatore con template generico e AI attiva (auto-riconosce tipo comando)
        self.generatore = GeneratoreCodice(template='generico', use_ai=True, use_cache=True)
        
        # Sistema logging errori
        from pythonita.utils.error_logger import get_error_logger
        self.error_logger = get_error_logger()
        self.error_logger.log_info("GUI avviata - Pythonita IA v3.4+")
        
        # Sistema visualizzazione automatica
        from pythonita.visualization.auto_visualizer import get_auto_visualizer
        self.auto_visualizer = get_auto_visualizer()
        
        # Agente workflow coordinator
        from pythonita.core.workflow_agent import get_workflow_agent
        self.workflow_agent = get_workflow_agent(status_callback=lambda msg: self.status_var.set(msg))
        
        # Connettore 3D per visualizzazioni geometriche
        from pythonita.visualization.viz_3d_connector import get_viz_3d_connector
        self.viz_3d_connector = get_viz_3d_connector()
        
        # Modelli 3D
        self.mano = ManoRobotica()
        self.braccio = BraccioRobotico()
        
        # Setup UI
        self._setup_ui()
        
        # UX Components
        if UX_IMPROVEMENTS_AVAILABLE:
            self.status_bar = StatusBar(self.root)
            self.status_bar.set_ready()
            print("[GUI] UX improvements enabled")
        else:
            self.status_bar = None
        
        # Theme System
        if THEMES_AVAILABLE:
            self.theme_manager = get_theme_manager()
            print(f"[GUI] Theme system enabled: {self.theme_manager.current_theme_name}")
        else:
            self.theme_manager = None
        
        # Speech Recognition
        if SPEECH_RECOGNITION_AVAILABLE:
            # Usa 'sphinx' per OFFLINE (senza internet, ma limitato per italiano)
            # Usa 'google' per ONLINE (più accurato, richiede internet) ✅ RACCOMANDATO
            speech_engine = 'google'  # Cambia in 'sphinx' se non hai internet
            self.speech_recognizer = get_speech_recognizer(
                language='it-IT',
                engine=speech_engine
            )
            mode = "OFFLINE" if speech_engine == 'sphinx' else "ONLINE"
            print(f"[GUI] Speech recognition enabled ({mode} mode)")
        else:
            self.speech_recognizer = None
        
        # Arduino Controller
        if ARDUINO_AVAILABLE:
            self.arduino_controller = get_arduino_controller()
            self.arduino_connected = False
            print("[GUI] Arduino controller enabled")
        else:
            self.arduino_controller = None
            self.arduino_connected = False
        
        # Timer per aggiornamenti
        self.after_id = None
    
    def _setup_ui(self):
        """Configura interfaccia utente."""
        # Frame superiore: controlli
        frame_controlli = tk.Frame(self.root, bg='#2c3e50', pady=10)
        frame_controlli.pack(fill=tk.X)
        
        tk.Label(frame_controlli, text="Pythonita IA - Visualizzatore 3D Robot",
                font=('Arial', 14, 'bold'), bg='#2c3e50', fg='white').pack()
        
        # Frame template e tema
        frame_settings = tk.Frame(frame_controlli, bg='#2c3e50')
        frame_settings.pack(pady=5)
        
        # Template selector
        frame_template = tk.Frame(frame_settings, bg='#2c3e50')
        frame_template.pack(side=tk.LEFT, padx=20)
        
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
        
        # Theme selector
        if THEMES_AVAILABLE:
            frame_theme = tk.Frame(frame_settings, bg='#2c3e50')
            frame_theme.pack(side=tk.LEFT, padx=20)
            
            tk.Label(frame_theme, text="Tema:", bg='#2c3e50', fg='white',
                    font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
            
            self.theme_var = tk.StringVar(value=self.theme_manager.current_theme_name)
            
            theme_options = {
                'light': '☀️ Light',
                'dark': '🌙 Dark',
                'high_contrast': '🔆 High Contrast'
            }
            
            for theme_key, theme_label in theme_options.items():
                rb = tk.Radiobutton(frame_theme, text=theme_label,
                                  variable=self.theme_var, value=theme_key,
                                  command=self._cambia_tema,
                                  bg='#2c3e50', fg='white', selectcolor='#34495e',
                                  font=('Arial', 9))
                rb.pack(side=tk.LEFT, padx=3)
        
        # Frame principale: 3 colonne
        frame_main = tk.Frame(self.root)
        frame_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        frame_main.columnconfigure(0, weight=1)  # Input
        frame_main.columnconfigure(1, weight=1)  # Codice
        frame_main.columnconfigure(2, weight=1)  # Risultati
        frame_main.columnconfigure(3, weight=2)  # 3D (più largo)
        
        # COLONNA 1: Input
        self._setup_colonna_input(frame_main)
        
        # COLONNA 2: Codice
        self._setup_colonna_codice(frame_main)
        
        # COLONNA 3: Risultati ← AGGIUNTO!
        self._setup_colonna_risultati(frame_main)
        
        # COLONNA 4: Visualizzatore 3D
        self._setup_colonna_3d(frame_main)
        
        # Frame inferiore: bottoni azione
        self._setup_bottoni_azione()
    
    def _setup_colonna_input(self, parent):
        """Setup colonna input."""
        frame = tk.Frame(parent)
        frame.grid(row=0, column=0, sticky='nsew', padx=5)
        
        # Header con pulsante vocale
        header_frame = tk.Frame(frame)
        header_frame.pack(fill=tk.X, anchor='w')
        
        tk.Label(header_frame, text="Comando in Italiano",
                font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        
        # Pulsanti registrazione vocale (RECORD e STOP separati)
        if SPEECH_RECOGNITION_AVAILABLE:
            voice_frame = tk.Frame(header_frame, bg='#2c3e50')
            voice_frame.pack(side=tk.RIGHT, padx=5)
            
            # Riga 1: Selezione microfono
            mic_select_frame = tk.Frame(voice_frame, bg='#2c3e50')
            mic_select_frame.pack(side=tk.TOP, pady=2)
            
            tk.Label(mic_select_frame, text="🎤", bg='#2c3e50', fg='white',
                    font=('Arial', 9)).pack(side=tk.LEFT, padx=2)
            
            # Lista microfoni disponibili
            import speech_recognition as sr
            try:
                self.microfoni_disponibili = sr.Microphone.list_microphone_names()
                # Filtra solo i microfoni di input (non speaker)
                self.microfoni_input = [(i, mic) for i, mic in enumerate(self.microfoni_disponibili)
                                       if 'mic' in mic.lower() or 'audio' in mic.lower()]
                
                # Crea lista nomi per dropdown
                mic_names = [f"[{i}] {mic[:40]}" for i, mic in self.microfoni_input]
                if not mic_names:
                    mic_names = ["Nessun microfono trovato"]
                
                # Dropdown microfoni
                from tkinter import ttk
                self.mic_var = tk.StringVar(value=mic_names[0] if mic_names else "Default")
                self.mic_dropdown = ttk.Combobox(mic_select_frame, textvariable=self.mic_var,
                                                values=mic_names, state='readonly',
                                                width=30, font=('Arial', 8))
                self.mic_dropdown.pack(side=tk.LEFT, padx=2)
                
                # Salva indice microfono selezionato
                self.selected_mic_index = self.microfoni_input[0][0] if self.microfoni_input else None
                
                # Callback cambio microfono
                def on_mic_change(event):
                    selected = self.mic_var.get()
                    try:
                        # Estrai indice da "[X] Nome"
                        idx = int(selected.split(']')[0].split('[')[1])
                        self.selected_mic_index = idx
                        self.status_var.set(f"🎤 Microfono: {selected.split('] ')[1][:20]}...")
                        print(f"[SPEECH] Microfono selezionato: [{idx}] {self.microfoni_disponibili[idx]}")
                    except:
                        pass
                
                self.mic_dropdown.bind('<<ComboboxSelected>>', on_mic_change)
                
            except Exception as e:
                print(f"[SPEECH] Errore caricamento microfoni: {e}")
                self.microfoni_disponibili = []
                self.selected_mic_index = None
            
            # Riga 2: Pulsante PUSH-TO-TALK (stile walkie-talkie)
            buttons_frame = tk.Frame(voice_frame, bg='#2c3e50')
            buttons_frame.pack(side=tk.TOP, pady=2)
            
            self.btn_ptt = tk.Button(buttons_frame, text="🎤 TIENI PREMUTO PER PARLARE",
                                    font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white',
                                    relief=tk.RAISED, bd=3, width=30, height=2)
            self.btn_ptt.pack(side=tk.LEFT, padx=2)
            
            # Eventi push-to-talk
            self.btn_ptt.bind('<ButtonPress-1>', self._on_ptt_press)
            self.btn_ptt.bind('<ButtonRelease-1>', self._on_ptt_release)
            
            # Stato registrazione
            self.recording = False
            self.recording_thread = None
            if UX_IMPROVEMENTS_AVAILABLE:
                add_tooltip(self.btn_ptt, "Tieni premuto per parlare, rilascia per fermare (come walkie-talkie)")
            
            # Riferimenti vecchi per compatibilità
            self.btn_record = self.btn_ptt
            self.btn_stop = None
        
        self.input_box = scrolledtext.ScrolledText(frame, height=15, width=35,
                                                   font=('Consolas', 10), wrap=tk.WORD)
        self.input_box.pack(fill=tk.BOTH, expand=True, pady=5)
        # NON auto-genera più - solo con pulsante
        
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
        
        # Esempi Arduino se disponibile
        if ARDUINO_AVAILABLE:
            esempi.extend([
                ("LED ON", "accendi led pin 13"),
                ("LED Blink", "lampeggia led 3 volte"),
            ])
        
        for testo, comando in esempi:
            btn = tk.Button(esempi_frame, text=testo, 
                          command=lambda c=comando: self._inserisci_esempio(c),
                          font=('Arial', 8), bg='#3498db', fg='white')
            btn.pack(fill=tk.X, pady=2)
        
        # PULSANTE GENERA CODICE CON AI - Stile moderno
        tk.Label(frame, text="", font=('Arial', 1)).pack(pady=5)  # Spazio
        btn_genera = tk.Button(frame, text="⚡ GENERA CODICE CON AI", 
                              command=self._genera_codice_con_ai,
                              font=('Segoe UI', 11, 'bold'), 
                              bg='#00ff88', fg='#1e1e2e',
                              activebackground='#00d4ff',
                              activeforeground='white',
                              relief=tk.FLAT, 
                              cursor='hand2',
                              bd=0)
        btn_genera.pack(fill=tk.X, pady=8, ipady=12)
        
        # Hover effect simulato con binding
        def on_enter(e):
            btn_genera['bg'] = '#00d4ff'
            btn_genera['fg'] = 'white'
        def on_leave(e):
            btn_genera['bg'] = '#00ff88'
            btn_genera['fg'] = '#1e1e2e'
        btn_genera.bind('<Enter>', on_enter)
        btn_genera.bind('<Leave>', on_leave)
        
        # PULSANTE PULISCI/RESET
        btn_reset = tk.Button(frame, text="🔄 PULISCI & NUOVO", 
                             command=self._reset_tutto,
                             font=('Segoe UI', 9, 'bold'), 
                             bg='#3d3d5c', fg='#e0e0e0',
                             activebackground='#ffaa00',
                             activeforeground='white',
                             relief=tk.FLAT, 
                             cursor='hand2',
                             bd=0)
        btn_reset.pack(fill=tk.X, pady=3, ipady=6)
    
    def _setup_colonna_codice(self, parent):
        """Setup colonna codice e risultati."""
        frame = tk.Frame(parent)
        frame.grid(row=0, column=1, sticky='nsew', padx=5)
        
        tk.Label(frame, text="Codice Python Generato",
                font=('Arial', 11, 'bold')).pack(anchor='w')
        
        self.output_box = scrolledtext.ScrolledText(frame, height=15, width=40,
                                                    font=('Consolas', 9), wrap=tk.WORD,
                                                    bg='#f9f9f9')
        self.output_box.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def _setup_colonna_risultati(self, parent):
        """Setup colonna risultati esecuzione."""
        frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        frame.grid(row=0, column=2, sticky='nsew', padx=5)
        
        # Header
        header_frame = tk.Frame(frame, bg=self.colors['bg_dark'])
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(header_frame, text="📊 Risultati Esecuzione",
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['bg_dark'],
                fg=self.colors['success']).pack(anchor='w')
        
        tk.Label(header_frame, text="Output del codice eseguito",
                font=('Segoe UI', 9),
                bg=self.colors['bg_dark'],
                fg=self.colors['text_dim']).pack(anchor='w')
        
        # Area risultati
        self.results_box = scrolledtext.ScrolledText(frame, height=25, width=35,
                                                     font=('Consolas', 11), 
                                                     wrap=tk.WORD,
                                                     bg='#0d1117',
                                                     fg='#00ff88',
                                                     insertbackground='#00ff88',
                                                     selectbackground='#00d4ff')
        self.results_box.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Messaggio iniziale
        self.results_box.insert('1.0', "⏳ In attesa di esecuzione...\n\n"
                                      "Il risultato apparirà qui dopo\n"
                                      "aver cliccato ⚡ GENERA")
        self.results_box.config(state=tk.DISABLED)
    
    def _setup_colonna_3d(self, parent):
        """Setup colonna visualizzazione DINAMICA (controllata da AI)."""
        frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        frame.grid(row=0, column=3, sticky='nsew', padx=5)
        
        # Header
        header_frame = tk.Frame(frame, bg=self.colors['bg_dark'])
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(header_frame, text="🎨 Visualizzazione AI",
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['bg_dark'],
                fg=self.colors['accent']).pack(anchor='w')
        
        tk.Label(header_frame, text="L'AI sceglie la migliore visualizzazione",
                font=('Segoe UI', 9),
                bg=self.colors['bg_dark'],
                fg=self.colors['text_dim']).pack(anchor='w')
        
        # Canvas matplotlib dinamico (2D/3D)
        self.figure_3d = Figure(figsize=(6, 6), dpi=100)
        self.figure_3d.patch.set_facecolor('#1e1e2e')
        # Inizia con 2D (più versatile)
        self.ax_3d = self.figure_3d.add_subplot(111)
        self.ax_3d.set_facecolor('#0d1117')
        self.is_3d_mode = False  # Flag per sapere se è 3D
        
        self.canvas_3d = FigureCanvasTkAgg(self.figure_3d, master=frame)
        self.canvas_3d.draw()
        self.canvas_3d.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Messaggio iniziale + TEST VISIBILITÀ
        self.ax_3d.text(0.5, 0.5, "In attesa...\n\nVisualizzazione AI\napparirà qui",
                       ha='center', va='center',
                       fontsize=14, color='#ff0000', fontweight='bold',
                       transform=self.ax_3d.transAxes)
        
        # RETTANGOLO DI TEST per verificare visibilità
        import matplotlib.patches as patches
        rect = patches.Rectangle((0.1, 0.1), 0.8, 0.8,
                                linewidth=3, edgecolor='#00ff00',
                                facecolor='none',
                                transform=self.ax_3d.transAxes)
        self.ax_3d.add_patch(rect)
        
        self.ax_3d.axis('off')
        self.ax_3d.set_xlim(0, 1)
        self.ax_3d.set_ylim(0, 1)
        
        # FORZA aggiornamento
        self.canvas_3d.draw()
        self.canvas_3d.flush_events()
        self.canvas_3d.get_tk_widget().update_idletasks()
        self.canvas_3d.get_tk_widget().update()
        
        print(f"[DEBUG] Canvas iniziale: size={self.canvas_3d.get_tk_widget().winfo_width()}x{self.canvas_3d.get_tk_widget().winfo_height()}")
    
    def _setup_bottoni_azione(self):
        """Setup bottoni azione."""
        frame = tk.Frame(self.root, bg='#ecf0f1', pady=10)
        frame.pack(fill=tk.X)
        
        # Pulsante "Genera Codice" RIMOSSO - ora è automatico!
        # (si genera mentre scrivi o dopo riconoscimento vocale)
        
        btn_esegui = tk.Button(frame, text="▶️ Esegui Animazione 3D",
                              command=self._esegui_animazione,
                              font=('Arial', 10, 'bold'), bg='#27ae60', fg='white',
                              padx=20, pady=8)
        btn_esegui.pack(side=tk.LEFT, padx=10)
        
        btn_reset = tk.Button(frame, text="Reset Posizione",
                            command=self._reset_robot,
                            font=('Arial', 10), bg='#e74c3c', fg='white',
                            padx=20, pady=8)
        btn_reset.pack(side=tk.LEFT, padx=10)
        
        btn_salva = tk.Button(frame, text="💾 Export Codice",
                            command=self._export_codice,
                            font=('Arial', 10), bg='#3498db', fg='white',
                            padx=20, pady=8)
        btn_salva.pack(side=tk.LEFT, padx=10)
        
        btn_screenshot = tk.Button(frame, text="📸 Export Screenshot",
                                  command=self._export_screenshot,
                                  font=('Arial', 10), bg='#9b59b6', fg='white',
                                  padx=20, pady=8)
        btn_screenshot.pack(side=tk.LEFT, padx=10)
        
        # Arduino panel button
        if ARDUINO_AVAILABLE:
            btn_arduino = tk.Button(frame, text="🤖 Arduino",
                                  command=self._mostra_pannello_arduino,
                                  font=('Arial', 10), bg='#16a085', fg='white',
                                  padx=20, pady=8)
            btn_arduino.pack(side=tk.LEFT, padx=10)
            if UX_IMPROVEMENTS_AVAILABLE:
                add_tooltip(btn_arduino, "Configura e controlla Arduino")
        
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
        """Inserisce esempio nel box input."""
        self.input_box.delete('1.0', tk.END)
        self.input_box.insert('1.0', comando)
        # NON genera automaticamente - utente preme pulsante
    
    def _genera_codice_con_ai(self):
        """Genera codice con AI coordinato dall'agente."""
        print("[DEBUG] Pulsante AI cliccato!")
        
        frase = self.input_box.get('1.0', tk.END).strip()
        print(f"[DEBUG] Frase letta: '{frase}'")
        
        if not frase:
            messagebox.showwarning("Input vuoto", "Scrivi prima un comando in italiano!")
            return
        
        # USA L'AGENTE PER COORDINARE IL WORKFLOW
        risultato = self.workflow_agent.esegui_workflow(
            comando=frase,
            generatore=lambda cmd: self._genera_codice_interno(cmd),
            esecutore=lambda cod: self._esegui_codice_interno(cod),
            visualizzatore=lambda cmd, cod, out: self._visualizza_intelligente(cmd, cod, out)
        )
        
        # Mostra risultati
        if risultato["successo"]:
            self.status_var.set(f"✅ Workflow completato in {risultato['tempo_totale']:.1f}s")
            self.error_logger.log_info(f"Workflow OK: {len(risultato['step_completati'])} step")
        else:
            self.status_var.set(f"❌ Workflow fallito: {risultato['errori'][0] if risultato['errori'] else 'Unknown'}")
            if risultato['errori']:
                self.error_logger.log_error(f"Workflow fallito", Exception(risultato['errori'][0]))
    
    def _visualizza_intelligente(self, comando: str, codice: str, output: str) -> bool:
        """
        AI sceglie visualizzazione appropriata e la mostra nella COLONNA 4.
        
        Logica:
        - Geometria (cerchio, cubo) → Plot geometrico nella canvas
        - Robot (mano, braccio) → Modello 3D robot
        - Funzione → Grafico matematico
        - Tutto nella stessa colonna 4!
        """
        comando_lower = comando.lower()
        visualizzato = False
        
        try:
            # Pulisci canvas precedente
            self._pulisci_canvas_3d()
            
            # GEOMETRIA → Plot 2D/3D
            if any(kw in comando_lower for kw in ['cerchio', 'area', 'quadrato', 'triangolo']):
                print("[VIZ-AI] Riconosciuto: GEOMETRIA")
                visualizzato = self._plot_geometria_in_canvas(comando, output)
            
            # ROBOT → Mano/Braccio 3D
            elif any(kw in comando_lower for kw in ['mano', 'braccio', 'afferra', 'apri', 'chiudi']):
                print("[VIZ-AI] Riconosciuto: ROBOT")
                visualizzato = self._plot_robot_in_canvas(comando)
            
            # SFERA/CUBO 3D → Oggetti 3D
            elif any(kw in comando_lower for kw in ['sfera', 'cubo', 'cilindro', 'box', 'volume']):
                print("[VIZ-AI] Riconosciuto: OGGETTO 3D")
                visualizzato = self._plot_oggetto_3d_in_canvas(comando, output)
            
            # FUNZIONE MATEMATICA → Plot funzione
            elif any(kw in comando_lower for kw in ['funzione', 'seno', 'coseno', 'sin', 'cos']):
                print("[VIZ-AI] Riconosciuto: FUNZIONE")
                visualizzato = self._plot_funzione_in_canvas(comando)
            
            # LISTA/ARRAY → Grafico dati
            elif 'fibonacci' in comando_lower or 'lista' in comando_lower:
                print("[VIZ-AI] Riconosciuto: SEQUENZA")
                visualizzato = self._plot_sequenza_in_canvas(output)
            
            else:
                # Default: mostra testo risultato
                print("[VIZ-AI] Nessuna visualizzazione specifica, mostra testo")
                self._mostra_testo_in_canvas(output)
                visualizzato = True
            
            if visualizzato:
                print("[VIZ-AI] ✅ Visualizzazione completata nella colonna 4!")
                return True
                
        except Exception as e:
            print(f"[VIZ-AI] Errore: {e}")
            self.error_logger.log_error("Errore visualizzazione AI", e)
        
        return False
    
    def _pulisci_canvas_3d(self):
        """Pulisce canvas 3D per nuova visualizzazione e resetta modalità."""
        print("[VIZ-DEBUG] Pulizia canvas 3D...")
        
        # Rimuovi asse corrente
        try:
            self.ax_3d.clear()
            self.ax_3d.remove()
        except:
            pass
        
        # Ricrea sempre in 2D (convertiremo a 3D solo se necessario)
        self.ax_3d = self.figure_3d.add_subplot(111)
        self.ax_3d.set_facecolor('#0d1117')
        self.is_3d_mode = False
        
        # Refresh
        self.canvas_3d.draw()
        self.canvas_3d.flush_events()
        
        print("[VIZ-DEBUG] Canvas pulito e pronto!")
    
    def _plot_geometria_in_canvas(self, comando: str, risultato: str) -> bool:
        """Plotta geometria 2D nella canvas colonna 4."""
        print(f"[VIZ-DEBUG] Inizio plot geometria, is_3d_mode={self.is_3d_mode}")
        
        # FORZA reset a 2D per geometria
        try:
            self.ax_3d.clear()
            self.ax_3d.remove()
        except:
            pass
        
        # Ricrea asse 2D fresco
        self.ax_3d = self.figure_3d.add_subplot(111)
        self.ax_3d.set_facecolor('#0d1117')
        self.is_3d_mode = False
        
        print("[VIZ-DEBUG] Asse 2D ricreato")
        
        # Usa auto_visualizer ma integrato nella canvas
        raggio = self._estrai_numero_da_comando(comando)
        if not raggio:
            raggio = 3  # Default
        
        # Disegna cerchio con plot() invece di patches
        theta = np.linspace(0, 2*np.pi, 100)
        x_circle = raggio * np.cos(theta)
        y_circle = raggio * np.sin(theta)
        
        # Cerchio riempito (facecolor)
        self.ax_3d.fill(x_circle, y_circle, color='#00d4ff', alpha=0.6, label='Area')
        
        # Bordo cerchio
        self.ax_3d.plot(x_circle, y_circle, color='#00ff88', linewidth=3, label='Perimetro')
        
        # Testo area
        area = np.pi * raggio**2
        self.ax_3d.text(0, raggio + 0.8, f'Area = {area:.2f}',
                       ha='center', va='bottom',
                       fontsize=16, fontweight='bold',
                       color='#00ff88',
                       bbox=dict(boxstyle='round,pad=0.5', 
                                facecolor='#1e1e2e', 
                                edgecolor='#00ff88',
                                alpha=0.8))
        
        # Aggiungi linea raggio
        self.ax_3d.plot([0, raggio], [0, 0], 
                       color='#ff6b6b', linewidth=2.5, 
                       label=f'R = {raggio}')
        self.ax_3d.text(raggio/2, -0.3, f'r={raggio}',
                       ha='center', fontsize=12, color='#ff6b6b')
        
        lim = raggio * 1.6
        self.ax_3d.set_xlim(-lim, lim)
        self.ax_3d.set_ylim(-lim, lim)
        self.ax_3d.set_aspect('equal')
        self.ax_3d.set_title(f'🔵 Cerchio - Raggio {raggio}',
                            fontsize=16, fontweight='bold', 
                            color='#00d4ff', pad=15)
        self.ax_3d.grid(True, alpha=0.3, color='#3d3d5c', linestyle='--')
        self.ax_3d.set_xlabel('X', color='#888888')
        self.ax_3d.set_ylabel('Y', color='#888888')
        
        # FORZA l'aggiornamento canvas matplotlib
        self.canvas_3d.draw()
        self.canvas_3d.flush_events()
        
        # FORZA l'aggiornamento Tkinter
        self.canvas_3d.get_tk_widget().update_idletasks()
        self.canvas_3d.get_tk_widget().update()
        
        # Forza refresh della finestra principale
        self.root.update_idletasks()
        self.root.update()
        
        print(f"[VIZ-DEBUG] Cerchio disegnato: r={raggio}, area={area:.2f}")
        print(f"[VIZ-DEBUG] Canvas aggiornato e visibile!")
        return True
    
    def _plot_sfera_3d(self, comando: str, codice: str, output: str) -> bool:
        """Disegna sfera 3D per calcoli di volume/superficie."""
        print("[VIZ-DEBUG] Disegno sfera 3D...")
        
        # Estrai raggio dal comando o codice
        raggio = self._estrai_numero_da_comando(comando)
        if not raggio:
            raggio = 3  # Default
        
        # FORZA modalità 3D
        try:
            self.ax_3d.clear()
            self.ax_3d.remove()
        except:
            pass
        
        self.ax_3d = self.figure_3d.add_subplot(111, projection='3d')
        self.ax_3d.set_facecolor('#0d1117')
        self.is_3d_mode = True
        
        # Crea sfera 3D
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        x = raggio * np.outer(np.cos(u), np.sin(v))
        y = raggio * np.outer(np.sin(u), np.sin(v))
        z = raggio * np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Plot sfera
        self.ax_3d.plot_surface(x, y, z, color='#00d4ff', alpha=0.7, 
                               edgecolor='#00ff88', linewidth=0.5)
        
        # Calcola volume
        volume = (4/3) * np.pi * raggio**3
        
        # Titolo e labels
        self.ax_3d.set_title(f'🌐 Sfera - R={raggio}\nVolume={volume:.2f}',
                            fontsize=14, fontweight='bold', color='#00d4ff', pad=15)
        self.ax_3d.set_xlabel('X', color='#888888')
        self.ax_3d.set_ylabel('Y', color='#888888')
        self.ax_3d.set_zlabel('Z', color='#888888')
        
        # Limiti
        lim = raggio * 1.3
        self.ax_3d.set_xlim(-lim, lim)
        self.ax_3d.set_ylim(-lim, lim)
        self.ax_3d.set_zlim(-lim, lim)
        
        # Vista
        self.ax_3d.view_init(elev=20, azim=45)
        
        # FORZA refresh
        self.canvas_3d.draw()
        self.canvas_3d.flush_events()
        self.canvas_3d.get_tk_widget().update_idletasks()
        self.canvas_3d.get_tk_widget().update()
        
        print(f"[VIZ-DEBUG] Sfera 3D disegnata: r={raggio}, volume={volume:.2f}")
        return True
    
    def _plot_robot_in_canvas(self, comando: str) -> bool:
        """Mostra mano/braccio robot nella canvas."""
        # Usa il visualizzatore robot esistente
        print("[VIZ-AI] Rendering mano robotica...")
        self._aggiorna_3d()
        return True
    
    def _plot_oggetto_3d_in_canvas(self, comando: str, risultato: str) -> bool:
        """Plotta oggetto 3D nella canvas."""
        # Per ora usa visualizzatore esterno, poi integreremo nella canvas
        self.viz_3d_connector.visualizza_da_risultato(comando, risultato, "")
        return True
    
    def _plot_funzione_in_canvas(self, comando: str) -> bool:
        """Plotta funzione matematica nella canvas."""
        self.ax_3d.clear()
        self.ax_3d.set_facecolor('#0d1117')
        
        x = np.linspace(-2*np.pi, 2*np.pi, 1000)
        
        if 'seno' in comando.lower() or 'sin' in comando.lower():
            y = np.sin(x)
            title = 'y = sin(x)'
        else:
            y = np.cos(x)
            title = 'y = cos(x)'
        
        self.ax_3d.plot(x, y, color='#00d4ff', linewidth=2.5)
        self.ax_3d.grid(True, alpha=0.2, color='#3d3d5c')
        self.ax_3d.set_title(title, fontsize=14, fontweight='bold', color='#00d4ff')
        
        self.canvas_3d.draw()
        return True
    
    def _plot_sequenza_in_canvas(self, output: str) -> bool:
        """Plotta sequenza numeri nella canvas."""
        try:
            # Estrai numeri dall'output
            import re
            numeri = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', output)]
            
            if numeri:
                self.ax_3d.clear()
                self.ax_3d.set_facecolor('#0d1117')
                self.ax_3d.plot(numeri, 'o-', color='#00d4ff', linewidth=2, markersize=8)
                self.ax_3d.grid(True, alpha=0.2, color='#3d3d5c')
                self.ax_3d.set_title('Sequenza', fontsize=14, fontweight='bold', color='#00d4ff')
                self.canvas_3d.draw()
                return True
        except:
            pass
        return False
    
    def _mostra_testo_in_canvas(self, testo: str):
        """Mostra testo nella canvas."""
        self.ax_3d.clear()
        self.ax_3d.set_facecolor('#0d1117')
        self.ax_3d.axis('off')
        self.ax_3d.text(0.5, 0.5, testo[:200],
                       ha='center', va='center',
                       fontsize=12, color='#e0e0e0',
                       wrap=True)
        self.canvas_3d.draw()
    
    def _estrai_numero_da_comando(self, comando: str) -> Optional[float]:
        """Estrae primo numero dal comando."""
        import re
        match = re.search(r'(\d+(?:\.\d+)?)', comando)
        return float(match.group(1)) if match else None
    
    def _genera_codice_interno(self, comando: str) -> str:
        """Genera codice (chiamato dall'agente)."""
        self._aggiorna_codice()
        return self.output_box.get('1.0', tk.END).strip()
    
    def _esegui_codice_interno(self, codice: str) -> Dict:
        """Esegue codice e restituisce risultato (chiamato dall'agente)."""
        import io
        from contextlib import redirect_stdout, redirect_stderr
        
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        
        namespace = {
            '__builtins__': __builtins__,
            'math': __import__('math'),
            'numpy': __import__('numpy'),
        }
        
        try:
            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                exec(codice, namespace)
            
            output = output_buffer.getvalue()
            errors = error_buffer.getvalue()
            
            # Aggiorna UI risultati
            self.results_box.config(state="normal")
            self.results_box.delete('1.0', "end")
            
            if output:
                self.results_box.insert('1.0', f"✅ RISULTATO:\n\n{output}\n")
            else:
                self.results_box.insert('1.0', "✅ Codice eseguito.\n\n")
            
            if errors:
                self.results_box.insert("end", f"\n⚠️ WARNING:\n{errors}")
            
            self.results_box.config(state="disabled")
            
            return {
                "output": output,
                "errore": errors if errors else None
            }
            
        except Exception as e:
            self.error_logger.log_error("Esecuzione fallita", e)
            
            # Mostra errore in results_box
            self.results_box.config(state="normal")
            self.results_box.delete('1.0', "end")
            self.results_box.insert('1.0', f"❌ ERRORE:\n\n{str(e)}\n")
            self.results_box.config(state="disabled")
            
            return {
                "output": "",
                "errore": str(e)
            }
    
    def _esegui_codice_automatico(self):
        """Esegue automaticamente il codice generato e mostra risultati."""
        codice = self.output_box.get('1.0', tk.END).strip()
        
        if not codice or codice.startswith("#"):
            return
        
        try:
            print("[EXEC] Esecuzione codice...")
            
            # Crea namespace sicuro per esecuzione
            import io
            import sys
            from contextlib import redirect_stdout, redirect_stderr
            
            # Cattura output
            output_buffer = io.StringIO()
            error_buffer = io.StringIO()
            
            # Namespace con librerie comuni
            namespace = {
                '__builtins__': __builtins__,
                'math': __import__('math'),
                'numpy': __import__('numpy'),
                'matplotlib': __import__('matplotlib'),
                'plt': __import__('matplotlib.pyplot'),
            }
            
            # Esegui codice
            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                exec(codice, namespace)
            
            # Mostra risultati
            output = output_buffer.getvalue()
            errors = error_buffer.getvalue()
            
            # Mostra risultati nella colonna dedicata
            self.results_box.config(state=tk.NORMAL)
            self.results_box.delete('1.0', tk.END)
            
            if output:
                print(f"[EXEC] Output: {output}")
                self.results_box.insert('1.0', f"✅ RISULTATO:\n\n{output}\n")
                self.results_box.tag_add("result", "1.0", "2.0")
                self.results_box.tag_config("result", foreground='#00ff88', font=('Segoe UI', 12, 'bold'))
            else:
                self.results_box.insert('1.0', "✅ Codice eseguito senza output.\n\n")
            
            if errors:
                print(f"[EXEC] Errors: {errors}")
                self.results_box.insert(tk.END, f"\n⚠️ WARNING:\n{errors}")
            
            self.results_box.config(state=tk.DISABLED)
                
            # VISUALIZZAZIONE AUTOMATICA INTELLIGENTE
            print("[VIZ] Analisi comando per visualizzazione...")
            frase_originale = self.input_box.get('1.0', tk.END).strip()
            
            try:
                # L'AI decide se e come visualizzare
                ha_visualizzato = self.auto_visualizer.analizza_e_visualizza(
                    comando=frase_originale,
                    codice=codice,
                    risultato=output
                )
                
                if ha_visualizzato:
                    print("[VIZ] ✅ Grafico generato automaticamente!")
                    self.status_var.set("✅ Codice eseguito + grafico visualizzato!")
                else:
                    print("[VIZ] Nessuna visualizzazione necessaria")
                    self.status_var.set("✅ Codice eseguito!")
            except Exception as viz_error:
                print(f"[VIZ] Errore visualizzazione: {viz_error}")
                self.status_var.set("✅ Codice eseguito!")
            
        except Exception as e:
            print(f"[EXEC] ERRORE esecuzione: {e}")
            self.error_logger.log_error("Errore esecuzione codice", e)
            self.error_logger.log_esecuzione(successo=False, errore=str(e))
            messagebox.showerror("❌ Errore Esecuzione", 
                               f"Errore durante l'esecuzione:\n{str(e)[:200]}")
            self.status_var.set("❌ Errore esecuzione")
    
    def _apri_log(self):
        """Apre cartella log in Esplora Risorse."""
        try:
            self.error_logger.apri_cartella_log()
            messagebox.showinfo("📋 Log Aperti", 
                              f"Cartella log aperta:\n{self.error_logger.log_dir}\n\n"
                              f"File disponibili:\n"
                              f"• pythonita_[data].log (generale)\n"
                              f"• errors_[data].log (solo errori)\n"
                              f"• session_[data].json (statistiche)")
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile aprire log: {e}")
    
    def _reset_tutto(self):
        """Pulisce input e output per nuova domanda."""
        print("[DEBUG] Reset sistema - nuova domanda")
        self.input_box.delete('1.0', tk.END)
        self.output_box.delete('1.0', tk.END)
        self.status_var.set("✅ Pronto per nuova domanda")
        
        # Chiudi eventuali grafici aperti
        try:
            import matplotlib.pyplot as plt
            plt.close('all')
        except:
            pass
        
        print("[DEBUG] Sistema resettato, pronto!")
    
    def _on_key_release(self, event):
        """[RIMOSSO] Non auto-genera più."""
        pass
    
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
        self.ax_3d.clear()
        
        # Setup assi
        self.ax_3d.set_xlabel('X (cm)', fontsize=8)
        self.ax_3d.set_ylabel('Y (cm)', fontsize=8)
        self.ax_3d.set_zlabel('Z (cm)', fontsize=8)
        self.ax_3d.set_title('Mano Robotica', fontsize=10, fontweight='bold')
        
        limite = 12
        self.ax_3d.set_xlim([-limite, limite])
        self.ax_3d.set_ylim([0, limite])
        self.ax_3d.set_zlim([-limite, limite])
        self.ax_3d.view_init(elev=20, azim=45)
        self.ax_3d.grid(True, alpha=0.3)
        
        # Disegna palmo
        larghezza = self.mano.dimensioni.LARGHEZZA_PALMO
        vertices = np.array([
            [-larghezza/2, 0, -2], [larghezza/2, 0, -2],
            [larghezza/2, 0, 2], [-larghezza/2, 0, 2], [-larghezza/2, 0, -2]
        ])
        self.ax_3d.plot(vertices[:, 0], vertices[:, 1], vertices[:, 2],
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
            
            self.ax_3d.plot(xs, ys, zs, color=colore, linewidth=2, marker='o', markersize=3)
        
        # Info stato
        perc = self._calcola_chiusura()
        info = f"Chiusura: {perc:.0f}%"
        self.ax_3d.text2D(0.02, 0.98, info, transform=self.ax_3d.transAxes,
                      fontsize=9, verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        self.canvas_3d.draw()
    
    def _disegna_braccio_3d(self):
        """Disegna braccio 3D."""
        self.ax_3d.clear()
        
        # Setup
        self.ax_3d.set_xlabel('X (cm)', fontsize=8)
        self.ax_3d.set_ylabel('Y (cm)', fontsize=8)
        self.ax_3d.set_zlabel('Z (cm)', fontsize=8)
        self.ax_3d.set_title('Braccio Robotico', fontsize=10, fontweight='bold')
        
        limite = 40
        self.ax_3d.set_xlim([0, limite])
        self.ax_3d.set_ylim([0, limite])
        self.ax_3d.set_zlim([0, limite])
        self.ax_3d.view_init(elev=15, azim=45)
        self.ax_3d.grid(True, alpha=0.3)
        
        # Calcola posizioni
        p0 = np.array([0, 0, 30])
        
        L1 = self.braccio.dimensioni.LUNGHEZZA_BRACCIO_SUPERIORE
        theta1 = np.radians(self.braccio.angolo_spalla)
        p1 = p0 + np.array([L1 * np.cos(theta1), L1 * np.sin(theta1), 0])
        
        L2 = self.braccio.dimensioni.LUNGHEZZA_AVAMBRACCIO
        theta2 = theta1 + np.radians(self.braccio.angolo_gomito)
        p2 = p1 + np.array([L2 * np.cos(theta2), L2 * np.sin(theta2), 0])
        
        # Disegna
        self.ax_3d.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]],
                    'b-', linewidth=5, label='Braccio sup.')
        self.ax_3d.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                    'r-', linewidth=5, label='Avambraccio')
        
        self.ax_3d.scatter(*p0, color='black', s=80)
        self.ax_3d.scatter(*p1, color='green', s=80)
        self.ax_3d.scatter(*p2, color='red', s=80)
        
        # Info
        info = f"Spalla: {self.braccio.angolo_spalla}°\nGomito: {self.braccio.angolo_gomito}°"
        self.ax_3d.text2D(0.02, 0.98, info, transform=self.ax_3d.transAxes,
                      fontsize=9, verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        self.canvas_3d.draw()
    
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
    
    def _export_codice(self):
        """Export codice con Export Manager."""
        codice = self.output_box.get('1.0', tk.END).strip()
        
        if not codice:
            messagebox.showwarning("Nessun Codice", "Genera prima del codice da esportare!")
            return
        
        if EXPORT_AVAILABLE:
            try:
                comando = self.input_box.get('1.0', tk.END).strip()
                filepath = export_code(codice, comando, {"template": self.template_var.get()})
                
                self.status_var.set(f"✅ Codice esportato: {filepath.name}")
                messagebox.showinfo("Export Completato", 
                                   f"Codice salvato in:\n{filepath}\n\nApri cartella export?")
                
                # Opzionale: apri cartella
                if messagebox.askyesno("Apri Cartella", "Vuoi aprire la cartella export?"):
                    get_export_manager().open_export_folder()
                    
            except Exception as e:
                messagebox.showerror("Errore Export", f"Errore durante export:\n{e}")
        else:
            # Fallback al vecchio metodo
            with open('output_robot.py', 'w', encoding='utf-8') as f:
                f.write(codice)
            self.status_var.set("Codice salvato in output_robot.py")
    
    def _export_screenshot(self):
        """Export screenshot 3D."""
        if EXPORT_AVAILABLE:
            try:
                filepath = export_screenshot(self.fig, name=f"robot_3d_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                
                self.status_var.set(f"✅ Screenshot esportato: {filepath.name}")
                messagebox.showinfo("Export Completato",
                                   f"Screenshot salvato in:\n{filepath}")
                
            except Exception as e:
                messagebox.showerror("Errore Export", f"Errore durante export screenshot:\n{e}")
        else:
            messagebox.showwarning("Export Non Disponibile",
                                  "Export manager non installato. Usa screenshot di sistema (Win+Shift+S)")
            self.status_var.set("Export non disponibile")
    
    def _cambia_template(self):
        """Cambia template."""
        self._aggiorna_codice()
    
    def _cambia_tema(self):
        """Cambia tema GUI."""
        if not THEMES_AVAILABLE:
            return
        
        nuovo_tema = self.theme_var.get()
        self.theme_manager.set_theme(nuovo_tema)
        
        # Applica tema a tutti i widget
        self._applica_tema()
        
        # Feedback
        if self.status_bar:
            self.status_bar.set_text(f"✨ Tema cambiato: {nuovo_tema}")
    
    def _applica_tema(self):
        """Applica tema corrente a tutta la GUI."""
        if not THEMES_AVAILABLE:
            return
        
        tema = self.theme_manager.get_theme()
        
        try:
            # Root window
            self.root.config(bg=tema.bg_primary)
            
            # Text widgets
            if hasattr(self, 'input_box'):
                self.input_box.config(
                    bg=tema.input_bg,
                    fg=tema.input_fg,
                    insertbackground=tema.fg_primary
                )
            
            if hasattr(self, 'output_box'):
                self.output_box.config(
                    bg=tema.output_bg,
                    fg=tema.output_fg,
                    insertbackground=tema.fg_primary
                )
            
            # Status label
            if hasattr(self, 'status_label'):
                self.status_label.config(
                    bg=tema.status_bg,
                    fg=tema.status_fg
                )
            
            # Aggiorna matplotlib per tema scuro/chiaro
            if tema.bg_primary == '#1E1E1E' or tema.bg_primary == '#000000':  # Dark themes
                self.figure_3d.patch.set_facecolor('#2D2D30')
                self.ax_3d.set_facecolor('#1E1E1E')
                self.ax_3d.xaxis.label.set_color(tema.fg_primary)
                self.ax_3d.yaxis.label.set_color(tema.fg_primary)
                self.ax_3d.zaxis.label.set_color(tema.fg_primary)
                self.ax_3d.tick_params(colors=tema.fg_primary)
            else:  # Light theme
                self.figure_3d.patch.set_facecolor('white')
                self.ax_3d.set_facecolor('#f0f0f0')
                self.ax_3d.xaxis.label.set_color(tema.fg_primary)
                self.ax_3d.yaxis.label.set_color(tema.fg_primary)
                self.ax_3d.zaxis.label.set_color(tema.fg_primary)
                self.ax_3d.tick_params(colors=tema.fg_primary)
            
            # Ridisegna canvas
            self.canvas_3d.draw()
            
            print(f"[THEME] Tema applicato: {self.theme_manager.current_theme_name}")
            
        except Exception as e:
            print(f"[THEME] Errore applicazione tema: {e}")
    
    def _on_ptt_press(self, event):
        """Evento: pulsante push-to-talk PREMUTO - inizia registrazione."""
        self._avvia_registrazione()
        # Feedback visivo
        self.btn_ptt.config(relief=tk.SUNKEN, bg='#c0392b', text="🔴 STO REGISTRANDO...")
    
    def _on_ptt_release(self, event):
        """Evento: pulsante push-to-talk RILASCIATO - ferma registrazione."""
        self._ferma_registrazione()
        # NON ripristinare subito - mostra stato "processing"
        self.btn_ptt.config(relief=tk.RAISED, bg='#f39c12', text="🔄 RICONOSCENDO...", state='disabled')
        self.status_var.set("🔄 Analisi in corso...")
    
    def _avvia_registrazione(self):
        """Avvia registrazione vocale con feedback immediato."""
        if not SPEECH_RECOGNITION_AVAILABLE or not self.speech_recognizer:
            messagebox.showwarning("Funzione Non Disponibile",
                                  "Speech recognition non installato.\nInstalla: pip install SpeechRecognition pyaudio")
            return
        
        if self.recording:
            return  # Già in registrazione
        
        try:
            self.recording = True
            
            # Aggiorna UI immediatamente
            self.status_var.set("⏳ Calibrando microfono...")
            self.root.update()
            
            # Esegui riconoscimento in thread separato
            def riconosci():
                import speech_recognition as sr
                import time
                
                try:
                    # Usa microfono selezionato dall'utente
                    mic_index = self.selected_mic_index if hasattr(self, 'selected_mic_index') and self.selected_mic_index is not None else None
                    with sr.Microphone(device_index=mic_index) as source:
                        # Fase 1: Calibrazione (0.7 secondi)
                        self.root.after(0, lambda: self.status_var.set("⏳ Calibrando... (0.7s)"))
                        self.speech_recognizer.recognizer.adjust_for_ambient_noise(source, duration=0.7)
                        
                        # Fase 2: PRONTO - ora puoi parlare!
                        self.root.after(0, lambda: self.status_var.set("🔴 STO ASCOLTANDO... (rilascia quando finisci)"))
                        
                        # Fase 3: Ascolto (max 20 secondi)
                        if not self.recording:  # Check se stop premuto durante calibrazione
                            return
                        
                        audio = self.speech_recognizer.recognizer.listen(
                            source, 
                            timeout=20,  # Aspetta fino a 20s prima che inizi a parlare
                            phrase_time_limit=20  # Max 20s di parlato (frasi lunghe)
                        )
                        
                        if not self.recording:  # Check se stop premuto durante ascolto
                            return
                        
                        # Salva audio in file WAV per debug e ascolto
                        import wave
                        import numpy as np
                        from datetime import datetime
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        audio_filename = f"registrazione_{timestamp}.wav"
                        
                        # Analizza volume
                        audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                        volume_max = np.max(np.abs(audio_data))
                        volume_avg = np.mean(np.abs(audio_data))
                        
                        with wave.open(audio_filename, 'wb') as wf:
                            wf.setnchannels(1)
                            wf.setsampwidth(audio.sample_width)
                            wf.setframerate(audio.sample_rate)
                            wf.writeframes(audio.get_raw_data())
                        
                        print(f"[AUDIO] File salvato: {audio_filename}")
                        print(f"[AUDIO] Volume MAX: {volume_max}, AVG: {volume_avg:.0f}")
                        
                        # Diagnosi volume
                        if volume_max < 100:
                            print(f"[AUDIO] ⚠️  VOLUME TROPPO BASSO! Aumenta microfono in Windows")
                        elif volume_max < 500:
                            print(f"[AUDIO] ⚠️  Volume basso, potrebbe non funzionare")
                        elif volume_max > 30000:
                            print(f"[AUDIO] ❌ VOLUME TROPPO ALTO! Audio DISTORTO (clipping)")
                            print(f"[AUDIO] 💡 SOLUZIONE: Abbassa volume microfono a 70-80% in Windows")
                            self.root.after(0, lambda: messagebox.showwarning(
                                "Audio Distorto", 
                                "⚠️ Volume microfono TROPPO ALTO!\n\n"
                                f"Volume rilevato: {volume_max} (MAX: 32767)\n"
                                "L'audio è distorto e Google non può riconoscerlo.\n\n"
                                "SOLUZIONE:\n"
                                "1. Vai in Impostazioni Windows → Audio → Input\n"
                                "2. Abbassa volume microfono a 70-80%\n"
                                "3. Disattiva 'Amplificazione microfono' se presente\n"
                                "4. Riprova la registrazione"
                            ))
                        else:
                            print(f"[AUDIO] ✅ Volume OK")
                        self.root.after(0, lambda: self.status_var.set(f"💾 Salvato: {audio_filename}"))
                        
                        # Fase 4: Riconoscimento
                        self.root.after(0, lambda: self.status_var.set("🔄 Riconoscendo..."))
                        text = self.speech_recognizer._recognize_audio(audio)
                        
                        # Risultato
                        if text:
                            self.root.after(0, lambda: self._on_voice_result(True, text))
                        else:
                            self.root.after(0, lambda: self._on_voice_result(False, "Nessun testo riconosciuto"))
                
                except sr.WaitTimeoutError:
                    self.root.after(0, lambda: self._on_voice_result(False, "Timeout: nessun audio rilevato"))
                except Exception as e:
                    self.root.after(0, lambda: self._on_voice_result(False, f"Errore: {e}"))
                finally:
                    self.recording = False
                    self.root.after(0, self._reset_recording_buttons)
            
            self.recording_thread = threading.Thread(target=riconosci, daemon=True)
            self.recording_thread.start()
            
        except Exception as e:
            self.recording = False
            messagebox.showerror("Errore Registrazione", f"Errore durante registrazione:\n{e}")
            self._reset_recording_buttons()
    
    def _ferma_registrazione(self):
        """Ferma la registrazione in corso."""
        self.recording = False
        # NON ripristinare pulsante qui - lo fa _on_voice_result quando finisce il riconoscimento
    
    def _reset_recording_buttons(self):
        """Ripristina stato pulsanti registrazione."""
        if hasattr(self, 'btn_ptt'):
            self.btn_ptt.config(relief=tk.RAISED, bg='#e74c3c', 
                               text="🎤 TIENI PREMUTO PER PARLARE", state='normal')
    
    def _on_voice_result(self, success, text):
        """Callback con risultato riconoscimento vocale."""
        # Ripristina pulsanti
        self._reset_recording_buttons()
        self.recording = False
        
        if success:
            # Inserisci testo riconosciuto
            self.input_box.delete('1.0', tk.END)
            self.input_box.insert('1.0', text)
            
            # Feedback successo
            if self.status_bar:
                self.status_bar.set_success(f"Riconosciuto: '{text}'")
            self.status_var.set(f"✓ Riconosciuto: '{text}'")
            
            # Auto-genera codice
            self._aggiorna_codice()
        else:
            # Errore
            messagebox.showwarning("Riconoscimento Fallito", text)
            if self.status_bar:
                self.status_bar.set_error("Riconoscimento fallito")
            self.status_var.set("❌ Riconoscimento fallito")
    
    def _mostra_pannello_arduino(self):
        """Mostra pannello configurazione e controllo Arduino."""
        if not ARDUINO_AVAILABLE:
            messagebox.showwarning("Funzione Non Disponibile",
                                  "Arduino controller non installato.\nInstalla: pip install pyserial")
            return
        
        # Crea finestra pannello Arduino
        arduino_window = tk.Toplevel(self.root)
        arduino_window.title("Pannello Arduino - Pythonita IA")
        arduino_window.geometry("600x500")
        arduino_window.transient(self.root)
        
        # Header
        header_frame = tk.Frame(arduino_window, bg='#16a085', pady=10)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="🤖 Controllo Arduino",
                font=('Arial', 14, 'bold'), bg='#16a085', fg='white').pack()
        
        # --- SEZIONE CONNESSIONE ---
        conn_frame = tk.LabelFrame(arduino_window, text="Connessione", font=('Arial', 10, 'bold'), padx=10, pady=10)
        conn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Porta COM
        porta_frame = tk.Frame(conn_frame)
        porta_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(porta_frame, text="Porta COM:", font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
        # Lista porte disponibili
        porte = self.arduino_controller.list_available_ports()
        porte_str = [p['port'] for p in porte] if porte else ['Nessuna porta']
        
        self.arduino_porta_var = tk.StringVar(value=porte_str[0] if porte else 'COM3')
        porta_menu = ttk.Combobox(porta_frame, textvariable=self.arduino_porta_var,
                                 values=porte_str, state='readonly', width=15)
        porta_menu.pack(side=tk.LEFT, padx=5)
        
        # Baudrate
        tk.Label(porta_frame, text="Baud:", font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        self.arduino_baud_var = tk.IntVar(value=9600)
        baud_menu = ttk.Combobox(porta_frame, textvariable=self.arduino_baud_var,
                                values=[9600, 19200, 38400, 57600, 115200], state='readonly', width=10)
        baud_menu.pack(side=tk.LEFT, padx=5)
        
        # Bottoni connessione
        btn_frame = tk.Frame(conn_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.arduino_status_var = tk.StringVar(value="Non connesso")
        tk.Label(btn_frame, textvariable=self.arduino_status_var, font=('Arial', 9),
                fg='red').pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Connetti", command=lambda: self._arduino_connect(arduino_window),
                 bg='#27ae60', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Disconnetti", command=lambda: self._arduino_disconnect(arduino_window),
                 bg='#e74c3c', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🔄 Aggiorna Porte", command=lambda: self._arduino_refresh_ports(porta_menu),
                 font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
        # --- SEZIONE CONTROLLO MANUALE ---
        control_frame = tk.LabelFrame(arduino_window, text="Controllo Manuale", font=('Arial', 10, 'bold'), padx=10, pady=10)
        control_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # LED Control
        led_frame = tk.Frame(control_frame)
        led_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(led_frame, text="LED Pin:", font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        self.arduino_led_pin_var = tk.IntVar(value=13)
        tk.Spinbox(led_frame, from_=0, to=13, textvariable=self.arduino_led_pin_var,
                  width=5, font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(led_frame, text="ON", command=lambda: self._arduino_led_on(),
                 bg='#f39c12', fg='white', width=8).pack(side=tk.LEFT, padx=3)
        tk.Button(led_frame, text="OFF", command=lambda: self._arduino_led_off(),
                 bg='#95a5a6', fg='white', width=8).pack(side=tk.LEFT, padx=3)
        tk.Button(led_frame, text="Blink 3x", command=lambda: self._arduino_led_blink(),
                 bg='#3498db', fg='white', width=10).pack(side=tk.LEFT, padx=3)
        
        # Servo Control
        servo_frame = tk.Frame(control_frame)
        servo_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(servo_frame, text="Servo Pin:", font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        self.arduino_servo_pin_var = tk.IntVar(value=9)
        tk.Spinbox(servo_frame, from_=0, to=13, textvariable=self.arduino_servo_pin_var,
                  width=5, font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
        tk.Label(servo_frame, text="Angolo:", font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        self.arduino_servo_angle_var = tk.IntVar(value=90)
        tk.Scale(servo_frame, from_=0, to=180, orient=tk.HORIZONTAL,
                variable=self.arduino_servo_angle_var, length=200).pack(side=tk.LEFT, padx=5)
        
        tk.Button(servo_frame, text="Muovi", command=lambda: self._arduino_servo_move(),
                 bg='#9b59b6', fg='white', width=10).pack(side=tk.LEFT, padx=5)
        
        # Sensore Read
        sensor_frame = tk.Frame(control_frame)
        sensor_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(sensor_frame, text="Sensore Pin A:", font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        self.arduino_sensor_pin_var = tk.IntVar(value=0)
        tk.Spinbox(sensor_frame, from_=0, to=5, textvariable=self.arduino_sensor_pin_var,
                  width=5, font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(sensor_frame, text="Leggi Valore", command=lambda: self._arduino_sensor_read(),
                 bg='#16a085', fg='white', width=15).pack(side=tk.LEFT, padx=5)
        
        self.arduino_sensor_value_var = tk.StringVar(value="---")
        tk.Label(sensor_frame, textvariable=self.arduino_sensor_value_var,
                font=('Arial', 10, 'bold'), fg='#2c3e50').pack(side=tk.LEFT, padx=10)
        
        # Console output
        console_frame = tk.Frame(control_frame)
        console_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(console_frame, text="Console Arduino:", font=('Arial', 9, 'bold')).pack(anchor='w')
        self.arduino_console = scrolledtext.ScrolledText(console_frame, height=8, width=60,
                                                         font=('Consolas', 8), bg='#1e1e1e', fg='#00ff00')
        self.arduino_console.pack(fill=tk.BOTH, expand=True)
        self.arduino_console.insert('1.0', "Console Arduino - Pronta\n")
    
    def _arduino_connect(self, window):
        """Connetti ad Arduino."""
        porta = self.arduino_porta_var.get()
        baud = self.arduino_baud_var.get()
        
        self.arduino_controller.port = porta
        self.arduino_controller.baudrate = baud
        
        success, msg = self.arduino_controller.connect()
        
        if success:
            self.arduino_connected = True
            self.arduino_status_var.set("✓ Connesso")
            window.nametowidget(window.winfo_children()[1]).winfo_children()[2].winfo_children()[0].config(fg='green')
            self.arduino_console.insert(tk.END, f"[OK] {msg}\n")
        else:
            self.arduino_connected = False
            self.arduino_status_var.set("✗ Non connesso")
            self.arduino_console.insert(tk.END, f"[ERROR] {msg}\n")
            messagebox.showerror("Errore Connessione", msg)
    
    def _arduino_disconnect(self, window):
        """Disconnetti da Arduino."""
        success, msg = self.arduino_controller.disconnect()
        self.arduino_connected = False
        self.arduino_status_var.set("Non connesso")
        window.nametowidget(window.winfo_children()[1]).winfo_children()[2].winfo_children()[0].config(fg='red')
        self.arduino_console.insert(tk.END, f"[INFO] {msg}\n")
    
    def _arduino_refresh_ports(self, menu_widget):
        """Aggiorna lista porte disponibili."""
        porte = self.arduino_controller.list_available_ports()
        porte_str = [p['port'] for p in porte] if porte else ['Nessuna porta']
        menu_widget.config(values=porte_str)
        self.arduino_console.insert(tk.END, f"[INFO] Trovate {len(porte)} porte\n")
    
    def _arduino_led_on(self):
        """Accendi LED."""
        if not self.arduino_connected:
            messagebox.showwarning("Arduino Non Connesso", "Connetti Arduino prima di inviare comandi")
            return
        pin = self.arduino_led_pin_var.get()
        success, msg = self.arduino_controller.led_on(pin)
        self.arduino_console.insert(tk.END, f"[LED] Pin {pin} ON - {msg}\n")
        self.arduino_console.see(tk.END)
    
    def _arduino_led_off(self):
        """Spegni LED."""
        if not self.arduino_connected:
            messagebox.showwarning("Arduino Non Connesso", "Connetti Arduino prima di inviare comandi")
            return
        pin = self.arduino_led_pin_var.get()
        success, msg = self.arduino_controller.led_off(pin)
        self.arduino_console.insert(tk.END, f"[LED] Pin {pin} OFF - {msg}\n")
        self.arduino_console.see(tk.END)
    
    def _arduino_led_blink(self):
        """Lampeggia LED."""
        if not self.arduino_connected:
            messagebox.showwarning("Arduino Non Connesso", "Connetti Arduino prima di inviare comandi")
            return
        pin = self.arduino_led_pin_var.get()
        success, msg = self.arduino_controller.led_blink(pin, times=3, delay=0.3)
        self.arduino_console.insert(tk.END, f"[LED] Pin {pin} BLINK - {msg}\n")
        self.arduino_console.see(tk.END)
    
    def _arduino_servo_move(self):
        """Muovi servo."""
        if not self.arduino_connected:
            messagebox.showwarning("Arduino Non Connesso", "Connetti Arduino prima di inviare comandi")
            return
        pin = self.arduino_servo_pin_var.get()
        angle = self.arduino_servo_angle_var.get()
        success, msg = self.arduino_controller.servo_write(pin, angle)
        self.arduino_console.insert(tk.END, f"[SERVO] Pin {pin} -> {angle}° - {msg}\n")
        self.arduino_console.see(tk.END)
    
    def _arduino_sensor_read(self):
        """Leggi sensore."""
        if not self.arduino_connected:
            messagebox.showwarning("Arduino Non Connesso", "Connetti Arduino prima di inviare comandi")
            return
        pin = self.arduino_sensor_pin_var.get()
        success, value = self.arduino_controller.analog_read(pin)
        if success:
            self.arduino_sensor_value_var.set(f"{value} / 1023")
            self.arduino_console.insert(tk.END, f"[SENSOR] Pin A{pin} = {value}\n")
        else:
            self.arduino_console.insert(tk.END, f"[ERROR] Lettura sensore fallita\n")
        self.arduino_console.see(tk.END)


def main():
    """Avvia GUI con visualizzatore 3D."""
    root = tk.Tk()
    app = PythonitaGUI3D(root)
    
    print("""
==================================================================
      PYTHONITA IA v3.1 - VISUALIZZATORE 3D ROBOT
==================================================================

COME USARE:
1. 🎤 TIENI PREMUTO il pulsante e parla (stile walkie-talkie) OPPURE scrivi
2. ✅ Il codice si genera AUTOMATICAMENTE
3. ▶️  Premi "Esegui Animazione 3D" (bottone verde)
4. 🤖 Guarda la mano 3D animarsi!

COMANDI DISPONIBILI:
- apri mano / chiudi pugno
- fai pinza
- afferra oggetto
- alza braccio

NOTA: Sistema PUSH-TO-TALK (walkie-talkie) 📻
Tieni premuto → Parla → Rilascia → Codice generato automaticamente! 🚀

La GUI e' aperta!
==================================================================
""")
    
    root.mainloop()


if __name__ == "__main__":
    main()

