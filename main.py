import psutil
import time
from collections import deque

from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor
    return f"{bytes:.2f} P{suffix}"

def make_header():
    """Top bar with current time and uptime side by side."""
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    uptime_s = time.time() - psutil.boot_time()
    days = int(uptime_s // 86400)
    hms = time.strftime("%H:%M:%S", time.gmtime(uptime_s))
    uptime_txt = f"{days}d {hms}" if days else hms

    time_panel = Panel(Text(now, justify="center"), title="⏰ Now", border_style="blue")
    up_panel   = Panel(Text(uptime_txt, justify="center"), title="🕒 Uptime", border_style="green")

    header = Layout(name="header")
    header.split_row(Layout(time_panel), Layout(up_panel))
    return header

def make_cpu_mem_layout(ema_cpu, alpha=0.3):
    """Left column: CPU (with EMA) above Memory."""
    # CPU EMA
    cpu_now = psutil.cpu_percent(interval=None, percpu=True)
    if not ema_cpu:
        ema_cpu.extend(cpu_now)
    for i, v in enumerate(cpu_now):
        ema_cpu[i] = alpha * v + (1 - alpha) * ema_cpu[i]
    avg = sum(ema_cpu) / len(ema_cpu)

    cpu_tbl = Table(title="🧠 CPU Usage", box=None, expand=True)
    cpu_tbl.add_column("Core", justify="center")
    cpu_tbl.add_column("Usage", justify="center")
    for i, u in enumerate(ema_cpu):
        cpu_tbl.add_row(f"{i}", f"{u:5.1f}%")
    cpu_tbl.add_row("Avg", f"{avg:5.1f}%")

    # Memory
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    mem_tbl = Table(title="🧮 Memory", box=None, expand=True)
    mem_tbl.add_column("Type"); mem_tbl.add_column("Total"); mem_tbl.add_column("Used"); mem_tbl.add_column("Free")
    mem_tbl.add_row("RAM", get_size(mem.total), get_size(mem.used), get_size(mem.available))
    mem_tbl.add_row("Swap", get_size(swap.total), get_size(swap.used), get_size(swap.free))

    layout = Layout(name="left")
    layout.split_column(
        Layout(Panel(cpu_tbl, border_style="cyan"), ratio=2),
        Layout(Panel(mem_tbl, border_style="cyan"), ratio=1)
    )
    return layout

def make_disk_net_layout():
    """Right column: Disk above Network."""
    # Disk
    disk = psutil.disk_usage('/')
    disk_tbl = Table(title="💾 Disk", box=None, expand=True)
    disk_tbl.add_column("Total"); disk_tbl.add_column("Used"); disk_tbl.add_column("Free")
    disk_tbl.add_row(get_size(disk.total), get_size(disk.used), get_size(disk.free))

    # Network
    net = psutil.net_io_counters()
    net_tbl = Table(title="🌐 Network I/O", box=None, expand=True)
    net_tbl.add_column("Dir"); net_tbl.add_column("Transferred")
    net_tbl.add_row("Sent", get_size(net.bytes_sent))
    net_tbl.add_row("Recv", get_size(net.bytes_recv))

    layout = Layout(name="right")
    layout.split_column(
        Layout(Panel(disk_tbl, border_style="magenta"), ratio=1),
        Layout(Panel(net_tbl, border_style="magenta"), ratio=1),
    )
    return layout

def make_footer():
    """Footer with quit instructions."""
    return Layout(Panel(Text("Press Ctrl+C to quit", justify="center", style="dim")))

def build_layout(ema_cpu):
    """Assemble the full dashboard layout."""
    layout = Layout()
    layout.split_column(
        make_header(),
        Layout(name="body", ratio=8),
        make_footer()
    )
    layout["body"].split_row(
        make_cpu_mem_layout(ema_cpu),
        make_disk_net_layout()
    )
    return layout

def main():
    ema_cpu = deque()
    with Live(build_layout(ema_cpu), refresh_per_second=4, screen=True):
        try:
            while True:
                # Rebuild & update the Live layout in-place
                layout = build_layout(ema_cpu)
                Live().update(layout)  # updates the screen without flicker
                time.sleep(0.25)
        except KeyboardInterrupt:
            console.clear()
            console.print("[bold green]Goodbye – monitor exited![/bold green]")

if __name__ == "__main__":
    main()
