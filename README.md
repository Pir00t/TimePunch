# ⏱ TimePunch

A time tracking application built with PySide6. "Vibe coded" as a personal project for helping record metrics at work.

![TimePunch](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-GPL3-green.svg)

## ✨ Features

### Core Functionality
- ⏰ **Real-time Task Tracking** - Start/stop tasks with a single click
- 🏷️ **Tag System** - Organize tasks with multi-tag support
- 📊 **Smart Summaries** - Daily, weekly, and monthly reports
- 💾 **SQLite Database** - Reliable local storage
- 🔄 **Task History** - View, edit, and resume past tasks

### User Experience
- 🌙 **Dark/Light Themes** - Toggle between beautiful themes
- ⌨️ **Keyboard Shortcuts** - Power-user friendly
- 📱 **Responsive Layout** - Adapts to your window size

### Keyboard Shortcuts
- `Enter` - Start/Stop current task
- `Ctrl+T` - Focus task input
- `Ctrl+H` - Refresh history
- `Ctrl+W` - Weekly summary
- `Ctrl+M` - Monthly summary

## 🚀 Installation

### Requirements
- Python 3.8 or higher
- PySide6

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/timepunch.git
cd timepunch
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python timepunch.py
```

## 📦 Project Structure

```
timepunch/
├── timepunch.py          # Main application entry point
├── database.py           # SQLite database operations
├── ui/
│   ├── __init__.py      # Package initializer
│   ├── main_window.py   # Main window UI
│   ├── dialogs.py       # Dialog windows
│   └── styles.py        # Theme stylesheets
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── LICENSE              # MIT License
├── .gitignore          # Git ignore rules
└── timepunch.db        # SQLite database (auto-created)
```

## 💡 Usage

### Starting a Task
1. Enter your task name in the input field
2. (Optional) Add tags like "research, email"
3. Click **Start** or press `Enter`
4. The timer begins tracking automatically

### Stopping a Task
1. Click **Stop** or press `Enter` while tracking
2. Task is saved to history automatically
3. View it in the history table

### Managing History
- **Click** any row to resume that task
- **Edit** button to modify task details
- **Del** button to remove tasks

### Viewing Summaries
- Click summary buttons or use shortcuts
- See time breakdown by task and tag
- Export data as needed (via CSV/SQLite)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

Have questions or suggestions? Open an issue on GitHub!
