import psutil
from rich.table import Table
from rich.panel import Panel

def get_top_processes_panel(limit=5):
    """Return a Panel showing top processes by CPU usage."""
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Sort by CPU usage descending
    procs.sort(key=lambda p: p['cpu_percent'], reverse=True)
    top = procs[:limit]

    table = Table(title="🔥 Top Apps", box=None, expand=True)
    table.add_column("PID", justify="right")
    table.add_column("Name", style="cyan")
    table.add_column("CPU %", justify="right")
    table.add_column("Mem %", justify="right")

    for p in top:
        table.add_row(str(p['pid']), p['name'][:20], f"{p['cpu_percent']:.1f}", f"{p['memory_percent']:.1f}")

    return Panel(table, border_style="red")
