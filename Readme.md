# Midnight projects ? :v idk man ...

💡 Project Overview: "SysDash"   
A terminal dashboard that shows:

📊 CPU usage (per core + average)  
💾 RAM and Swap usage  
💽 Disk usage  
🌐 Network upload/download speeds  
🎮 GPU stats (optional)  
⏰ Uptime and system load  
📅 Clock / date widget  
🧠 Process count (maybe top 5 CPU-hungry)  

## Features
- Real-time monitoring of system metrics.
- Displays a goodbye message when interrupted.
- Refreshes the dashboard every 0.75 seconds, with a 2-second goodbye message on exit.

🛠️ Tech Stack Options  
You can build this with either:

✅ Python  
Super quick to get going.  
Use `psutil`, `rich`, `textual`, or `curses`.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/dipon778/SysDash.git
   cd SysDash
   ```

2. Install the required packages:
   ```bash
   pip install psutil rich textual
   ```

## Usage
Run the application:
```bash
python main.py
```
Press `Ctrl+C` to exit and see the goodbye message.
