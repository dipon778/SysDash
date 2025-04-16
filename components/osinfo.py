import platform
import socket
from rich.panel import Panel
from rich.text import Text

def get_os_info_panel():
    os_name = platform.system()
    os_version = platform.release()
    kernel = platform.version()
    hostname = socket.gethostname()

    text = Text()
    text.append(f"{os_name} {os_version}\n", style="bold cyan")
    text.append(f"{kernel}\n")
    text.append(f"Host: {hostname}", style="italic")

    return Panel(text, title="💻 System Info", border_style="cyan")
