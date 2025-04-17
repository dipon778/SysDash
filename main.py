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
from components.utils import get_size, get_time_date
from components.top import get_top_processes_panel

import platform
import socket

console = Console()

# Helper functions for header and footer
def make_header():
    """Build the header layout with system time, date, and uptime."""
    current_time = get_time_date()
    uptime_s = time.time() - psutil.boot_time()
    days = int(uptime_s // 86400)
    hms = time.strftime("%H:%M:%S", time.gmtime(uptime_s))
    uptime = f"{days}d {hms}" if days else hms

    header = Layout(name="header")
    header.split_row(
        Panel(current_time, title="⏰ Time & Date", border_style="blue"),
        Panel(uptime, title="🕒 Uptime", border_style="green"),
    )
    return header

def get_os_info_panel():
    """Generate a panel displaying OS information."""
    os_name = platform.system()
    os_version = platform.release()
    kernel = platform.version()
    hostname = socket.gethostname()

    os_info = f"{os_name} {os_version}\n{kernel}\nHost: {hostname}"
    return Panel(os_info, title="💻 OS Info", border_style="cyan")

def make_footer():
    """Build the footer layout with a quit message."""
    return Panel("Press Ctrl+C to quit", style="dim", border_style="dim")

# Layout builder
def build_layout(ema_cpu, prev_net, interval):
    """Construct the main layout with CPU, memory, disk, network, and top apps panels."""
    root = Layout()
    root.split_column(
        make_header(),
        Layout(name="body", ratio=8),
        make_footer()
    )

    # Left: CPU, Memory, and Top Apps
    left = Layout()
    left.split_column(
        get_cpu_panel(ema_cpu),
        get_memory_panel(),
        get_top_processes_panel(),
    )

    # Right: Disk, Network, and OS Info
    right = Layout()
    net_panel, new_net = get_network_panel(prev_net, interval)
    right.split_column(
        get_disk_panel(),
        net_panel,
        get_os_info_panel(),  # Add OS info here
    )

    root['body'].split_row(left, right)
    return root, new_net

# Main function
def main():
    """Main function to run the live system monitor."""
    # Pre-seed CPU and network stats
    psutil.cpu_percent(interval=None, percpu=True)
    prev_net = psutil.net_io_counters()
    ema_cpu = deque()
    prev_time = time.time()

    with Live(console=console, screen=True, refresh_per_second=2) as live:
        try:
            while True:
                now = time.time()
                interval = now - prev_time
                prev_time = now

                layout, prev_net = build_layout(ema_cpu, prev_net, interval)
                live.update(layout)
                time.sleep(1)

        except KeyboardInterrupt:
            console.clear()
            show_exit_message(live)

def show_exit_message(live):
    """Display a farewell message when the user exits."""
    layout = Layout()
    layout.split(
        Panel(" Thanks for using the system monitor!", style="bold green"),
    )
    live.update(layout)
    time.sleep(2)

if __name__ == "__main__":
    main()
