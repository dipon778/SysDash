import psutil
import time
from collections import deque
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor
    return f"{bytes:.2f} P{suffix}"

def make_system_table(ema_cpu, alpha=0.3):
    cpu_now = psutil.cpu_percent(interval=None, percpu=True)
    # initialize EMA if empty
    if not ema_cpu:
        for u in cpu_now:
            ema_cpu.append(u)
    # update EMA
    for i, u in enumerate(cpu_now):
        ema_cpu[i] = alpha * u + (1 - alpha) * ema_cpu[i]
    avg = sum(ema_cpu) / len(ema_cpu)

    # build table
    tbl = Table(title="🧠 CPU Usage", title_justify="center", style="cyan")
    tbl.add_column("Core", justify="center", style="magenta")
    tbl.add_column("Usage (%)", justify="center", style="green")
    for i, u in enumerate(ema_cpu):
        tbl.add_row(f"Core {i}", f"{u:5.1f}%")
    tbl.add_row("[bold]Average[/bold]", f"[bold yellow]{avg:5.1f}%[/bold yellow]")
    
    # memory
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    mem_tbl = Table(title="🧮 Memory", title_justify="center", style="cyan")
    mem_tbl.add_column("Type", style="magenta")
    mem_tbl.add_column("Total", justify="center")
    mem_tbl.add_column("Used", justify="center", style="yellow")
    mem_tbl.add_column("Free", justify="center", style="green")
    mem_tbl.add_row("RAM", get_size(mem.total), get_size(mem.used), get_size(mem.available))
    mem_tbl.add_row("Swap", get_size(swap.total), get_size(swap.used), get_size(swap.free))

    # disk
    disk = psutil.disk_usage('/')
    disk_tbl = Table(title="💾 Disk", title_justify="center", style="cyan")
    disk_tbl.add_column("Total", style="magenta")
    disk_tbl.add_column("Used", justify="center", style="yellow")
    disk_tbl.add_column("Free", justify="center", style="green")
    disk_tbl.add_row(get_size(disk.total), get_size(disk.used), get_size(disk.free))

    # network
    net = psutil.net_io_counters()
    net_tbl = Table(title="🌐 Network I/O", title_justify="center", style="cyan")
    net_tbl.add_column("Direction", style="magenta")
    net_tbl.add_column("Transferred", justify="center", style="green")
    net_tbl.add_row("Sent", get_size(net.bytes_sent))
    net_tbl.add_row("Recv", get_size(net.bytes_recv))

    # uptime & clock
    uptime_s = time.time() - psutil.boot_time()
    days = int(uptime_s // 86400)
    hms = time.strftime("%H:%M:%S", time.gmtime(uptime_s))
    up_panel = Panel(Text(f"{days}d {hms}" if days else hms, style="green"),
                     title="🕒 Uptime", title_align="left")
    clock_panel = Panel(Text(time.strftime("%Y-%m-%d %H:%M:%S"), style="blue"),
                        title="⏰ Now", title_align="left")

    # assemble
    layout = Table.grid()
    layout.add_row(clock_panel, up_panel)
    layout.add_row(tbl)
    layout.add_row(mem_tbl)
    layout.add_row(disk_tbl, net_tbl)
    return layout

def main():
    ema_cpu = deque()
    with Live(console=console, refresh_per_second=4) as live:
        try:
            while True:
                table = make_system_table(ema_cpu, alpha=0.3)
                live.update(table)
                time.sleep(0.25)
        except KeyboardInterrupt:
            console.clear()
            console.print("[bold green]Exited gracefully – goodbye![/bold green]")

if __name__ == "__main__":
    main()
