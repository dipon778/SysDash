import psutil
from rich.table import Table
from rich.panel import Panel

def get_top_processes_panel():
    """Generate a panel displaying the top processes by CPU usage."""
    # Filter out processes with None as cpu_percent and sort by CPU usage
    processes = sorted(
        (p for p in psutil.process_iter(['pid', 'name', 'cpu_percent']) if p.info['cpu_percent'] is not None),
        key=lambda p: p.info['cpu_percent'],
        reverse=True
    )[:5]

    table = Table(title="Top Processes", show_header=True, header_style="bold magenta")
    table.add_column("PID", justify="right")
    table.add_column("Name", justify="left")
    table.add_column("CPU %", justify="right")

    for proc in processes:
        try:
            table.add_row(str(proc.info['pid']), proc.info['name'], f"{proc.info['cpu_percent']:.1f}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return Panel(table, title="🔥 Top Apps", border_style="red")
