# 🐍 Pythonita IA - Italian Natural Language to Python

**Transform Italian commands into Python code with 3D robot visualization**

[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/ballales1984-wq/pythonita-ia)

---

## 📋 Overview

**Pythonita IA** is an advanced system that translates natural Italian commands into executable Python code, with integrated 3D visualization of robotic movements.

Perfect for:
- 🎓 **Students** learning to program
- 🤖 **Robotics developers** prototyping behaviors
- 🧠 **Researchers** in Natural Language Processing
- 👨‍💻 **Developers** who want to code faster

---

## ✨ Key Features

### 🗣️ Natural Language Processing
- **143+ Python commands** recognized
- Full support for Italian language
- Advanced grammatical structures (SVO, interrogatives)
- Multi-command support (combine multiple actions)

### 🤖 3D Visualization
- **18 interactive 3D objects**:
  - Tools (hammer, screwdriver, wrench, pliers)
  - Food (apple, banana, orange, sandwich, ball)
  - Electronics (mouse, keyboard, smartphone)
  - Everyday items (book, pen, watch, cup, bottle, cube)
- Realistic robotic hand and arm models
- Smooth animations (30-45 FPS)
- Performance optimization with adaptive quality

### 🎨 Professional Interface
- **3 GUI themes**: Light, Dark, High Contrast
- Integrated code editor with syntax highlighting
- Real-time status bar with progress indicators
- User-friendly error dialogs
- Tooltips and contextual help

### 💾 Export & Sharing
- Export Python code (.py with professional headers)
- Export 3D screenshots (PNG 300 DPI)
- Export animations (GIF format)
- Automatic folder opening for easy access

### 🔌 Extensibility
- **Plugin system** for third-party extensions
- API for custom commands
- Custom 3D objects registration
- Template system for specific domains

### 🌐 Internationalization
- **Italian** and **English** interfaces
- Persistent language preferences
- Easy to add new languages

### 🛡️ Commercial Features
- **5-tier licensing system** (Free, Trial, Personal, Pro, Enterprise)
- Feature gating based on license
- Offline license validation
- Hardware binding for security

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/ballales1984-wq/pythonita-ia.git
cd pythonita-ia

# Install dependencies
pip install -r requirements.txt

# Download Italian language model for spaCy
python -m spacy download it_core_news_sm

# Launch application
python gui_robot_3d.py
```

### First Usage

1. **Enter an Italian command**:
   ```
   la mano afferra la mela
   ```

2. **Click "Generate Code"**

3. **See the generated Python code**

4. **Click "Run Animation"** to see the 3D visualization

---

## 📚 Examples

### Basic Commands

```
# Lists
crea lista di numeri
aggiungi 5 alla lista

# Conditionals
se x maggiore di 10 stampa risultato

# Loops
per ogni elemento nella lista stampa

# Functions
definisci funzione saluta con parametro nome

# Files
leggi file dati.txt
scrivi nel file output.txt

# Math
calcola radice quadrata di 16
genera numero casuale tra 1 e 100
```

### Robotics Commands

```
# Hand movements
la mano si apre
la mano si chiude
la mano afferra la mela

# Arm movements
il braccio si alza
il braccio si abbassa
il braccio ruota a destra

# Complex actions
la mano afferra il martello e si alza
```

### Multi-Command

```
crea lista e aggiungi 10 elementi e stampa
```

---

## 🎮 Interface

### Main Window

```
┌─────────────────────────────────────────────────────┐
│  Pythonita IA - 3D Robot Visualizer               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Template: [Robot] [Bionic Hand] [Generic]         │
│  Theme:    [☀️ Light] [🌙 Dark] [🔆 High Contrast]│
│                                                     │
├─────────────────────────────────────────────────────┤
│  Input:                     │  3D Visualization    │
│  ┌───────────────────────┐  │  ┌────────────────┐ │
│  │ la mano afferra       │  │  │                │ │
│  │ la mela               │  │  │   🤖  🍎       │ │
│  │                       │  │  │                │ │
│  └───────────────────────┘  │  └────────────────┘ │
│                             │                      │
│  Output:                    │  [Generate Code]     │
│  ┌───────────────────────┐  │  [Run Animation]    │
│  │ # Generated code      │  │  [Stop]             │
│  │ hand.open()           │  │  [Reset View]       │
│  │ hand.grasp("apple")   │  │                     │
│  └───────────────────────┘  │  [💾 Export Code]   │
│                             │  [📸 Screenshot]    │
├─────────────────────────────────────────────────────┤
│  Status: Ready                                      │
└─────────────────────────────────────────────────────┘
```

---

## 🏗️ Project Structure

```
pythonita-ia/
├── pythonita/                  # Main package
│   ├── core/                   # Core logic
│   │   ├── code_generator.py   # Code generation
│   │   ├── parser.py           # NLP parsing
│   │   └── command_registry.py # Command management
│   ├── licensing/              # License system
│   ├── gui/                    # GUI components
│   │   ├── themes.py           # Theme system
│   │   └── ux_improvements.py  # UX enhancements
│   ├── utils/                  # Utilities
│   │   ├── export.py           # Export manager
│   │   └── telemetry.py        # Telemetry
│   ├── plugins/                # Plugin system
│   │   ├── plugin_api.py       # Plugin API
│   │   └── plugin_loader.py    # Plugin loader
│   └── i18n/                   # Internationalization
│       ├── translator.py       # Translation system
│       └── translations/       # Translation files
│           ├── it.json         # Italian
│           └── en.json         # English
├── visualizzatore/             # 3D visualization
│   ├── viewer_3d.py            # 3D viewer
│   ├── oggetti_3d.py           # 3D objects
│   └── performance_optimizer.py # Performance
├── examples/                   # Examples
│   └── example_plugin.py       # Example plugin
├── tests/                      # Test suite
│   └── unit/                   # Unit tests
├── gui_robot_3d.py             # Main GUI application
├── README.md                   # Italian documentation
├── README_EN.md                # English documentation
├── QUICK_START.md              # Quick start guide
├── PLUGIN_DEVELOPMENT_GUIDE.md # Plugin development
└── requirements.txt            # Dependencies
```

---

## 🔌 Plugin Development

Pythonita supports plugins for extending functionality.

### Create a Plugin

```python
from pythonita.plugins import Plugin, PluginInfo

class MyPlugin(Plugin):
    def get_info(self):
        return PluginInfo(
            name="MyPlugin",
            version="1.0.0",
            author="Your Name",
            description="My custom plugin"
        )
    
    def initialize(self, context):
        print("Plugin initialized!")
    
    def shutdown(self):
        print("Plugin shutdown!")
    
    def register_commands(self):
        return {
            'my_command': self._my_handler
        }
    
    def _my_handler(self, **kwargs):
        return 'print("Hello from plugin!")'
```

See `PLUGIN_DEVELOPMENT_GUIDE.md` for full documentation.

---

## 📦 Licensing

### Available Tiers

| Tier | Price | Features |
|------|-------|----------|
| **Free** | €0 | 20 basic commands, Italian only |
| **Trial** | €0 | Full features for 30 days |
| **Personal** | €49 | All commands, GUI, unlimited use |
| **Pro** | €149 | 3D visualization, 18 objects, export, themes |
| **Enterprise** | €499 | Source code, priority support, custom features |

[Buy on Gumroad →](https://ballales.gumroad.com/l/pythonita-ia-pro)

---

## 🛠️ Development

### Requirements

- Python 3.8+
- NumPy
- Matplotlib
- spaCy (Italian model)
- Tkinter
- Pillow

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=pythonita --cov-report=html

# Run specific test
pytest tests/unit/test_generatore.py -v
```

### Build Executable

```bash
# Windows
python build_exe_completo.bat

# Executable will be in dist/ folder
```

---

## 📊 Performance

- **Code generation**: < 500ms (cached), < 2s (AI)
- **3D rendering**: 30-45 FPS
- **Cache hit rate**: 80%+
- **Test coverage**: 80%+
- **Supported commands**: 143+
- **3D objects**: 18

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

- **GitHub Issues**: [Report bugs/features](https://github.com/ballales1984-wq/pythonita-ia/issues)
- **Email**: support@pythonita.io
- **Documentation**: See `QUICK_START.md` and `PLUGIN_DEVELOPMENT_GUIDE.md`

---

## 📜 License

**Proprietary License** - Copyright © 2025 Pythonita Team

This is commercial software. See [LICENSE](LICENSE) for details.

Enterprise licenses include source code access.

---

## 🌟 Acknowledgments

- **spaCy** for Italian NLP
- **Matplotlib** for 3D visualization
- **Ollama + Llama3.2** for local AI
- All contributors and users!

---

## 🗺️ Roadmap

### v3.3.0 (Q1 2025)
- [ ] Web version (browser-based)
- [ ] Cloud sync
- [ ] Mobile app (iOS/Android)

### v3.4.0 (Q2 2025)
- [ ] More languages (Spanish, French, German)
- [ ] Voice commands
- [ ] AI training mode

---

**Made with ❤️ in Italy**

[⭐ Star on GitHub](https://github.com/ballales1984-wq/pythonita-ia) | [🐛 Report Bug](https://github.com/ballales1984-wq/pythonita-ia/issues) | [💡 Request Feature](https://github.com/ballales1984-wq/pythonita-ia/issues/new)

