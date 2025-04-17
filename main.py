import time
import psutil
from collections import deque

from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel

from components.cpu import get_cpu_panel
from components.memory import get_memory_panel
from components.disk import get_disk_panel
from components.network import get_network_panel
from components.utils import get_size
from components.top import get_top_processes_panel


console = Console()

# Header & footer builders

import platform
import socket

def make_header():
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    uptime_s = time.time() - psutil.boot_time()
    days = int(uptime_s // 86400)
    hms = time.strftime("%H:%M:%S", time.gmtime(uptime_s))
    up = f"{days}d {hms}" if days else hms

    # OS info
    os_name = platform.system()
    os_version = platform.release()
    kernel = platform.version()
    hostname = socket.gethostname()

    os_info = f"{os_name} {os_version}\n{kernel}\nHost: {hostname}"

    layout = Layout(name="header")
    layout.split_row(
        Panel(now, title="⏰ Time", border_style="blue"),
        Panel(up, title="🕒 Uptime", border_style="green"),
        Panel(os_info, title="💻 OS Info", border_style="cyan")
    )
    return layout


def make_footer():
    return Panel("Press Ctrl+C to quit", style="dim", border_style="dim" )


def build_layout(ema_cpu, prev_net, interval):
    root = Layout()
    root.split_column(
        make_header(),
        Layout(name="body", ratio=8),
        make_footer()
    )

    # left: CPU & Memory
    left = Layout()
    left.split_column(
        get_cpu_panel(ema_cpu),
        get_memory_panel(),
    )

    # right: Disk & Network
    right = Layout()
    net_panel, new_net = get_network_panel(prev_net, interval)
    right.split_column(
        get_disk_panel(),
        net_panel,
    )
    # right: Disk & Network
    right = Layout()
    net_panel, new_net = get_network_panel(prev_net, interval)
    top_panel = get_top_processes_panel()

    right.split_column(
        get_disk_panel(),
        net_panel,
        top_panel
    )


    root['body'].split_row(left, right)
    return root, new_net


def main():
    # Pre-seed
    psutil.cpu_percent(interval=None, percpu=True)
    prev = psutil.net_io_counters()
    ema = deque()
    prev_time = time.time()

    with Live(console=console, screen=True, refresh_per_second=2) as live:
        try:
            while True:
                now = time.time()
                interval = now - prev_time
                prev_time = now

                layout, prev = build_layout(ema, prev, interval)
                live.update(layout)
                time.sleep(1)
                
        except KeyboardInterrupt:
            console.clear()
            layout = Layout()
            layout.split(
                Panel(" Thanks for using the system monitor!" , style="bold green"),
            )
            live.update(layout)
            time.sleep(2)
            
if __name__ == "__main__":
    main()