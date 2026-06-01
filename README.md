# 🦙 Ollama-Updater-GUI

A beautiful GUI application that updates Ollama and configures it for external network access with just one click. No more terminal commands or manual service file editing!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Linux-FCC624?logo=linux&logoColor=black)](https://www.linux.org/)

## ✨ Features

- 🚀 **One-Click Update** - Automatically runs `curl -fsSL https://ollama.com/install.sh | sh`
- ⚙️ **Auto-Configuration** - Sets `OLLAMA_HOST=0.0.0.0` in systemd service file
- 🔐 **GUI Password Dialog** - No terminal password prompts - clean GUI authentication
- 📋 **Live Console Output** - Watch the entire process in real-time
- ✅ **Status Checking** - Displays current Ollama version and network configuration
- 🎨 **Modern Dark Theme** - Easy on the eyes with cyberpunk-inspired design
- 🖱️ **Desktop Integration** - Complete with `.desktop` shortcut for one-click launching

## 📸 Screenshots

![Ollama Updater GUI](/screens/Screenshot.png)

*The main interface showing system status and live console output*

## 🚀 Quick Start

### Prerequisites

- **Linux** (Ubuntu/Debian/KDE/GNOME/XFCE)
- **Python 3.8+** (comes pre-installed on most distributions)
- **Ollama** (installed or not - the updater will install it if missing)
- **sudo privileges** (for editing system service files)

## Installation

1. Clone the repository


```
git clone https://github.com/artfix/ollama-updater-gui.git
cd ollama-updater-gui

```

2. Make the launcher executable


```
chmod +x ollama_updater.py
```

3. Create desktop shortcut (optional but recommended)

From this repo download [ollama_updater.desktop](https://github.com/artfix/Ollama-Updater-GUI/blob/main/ollama_updater.desktop) and place it in `/home/USER/.local/share/applications`

4. Refresh desktop apps menu, cmd to run in terminal

```
xdg-desktop-menu forceupdate
```
