
import psutil
from rich.table import Table
from rich.panel import Panel


def get_cpu_panel(ema_cpu, alpha=0.3):
    """Return a Panel with EMA-smoothed per-core CPU usage."""
    # fetch non-blocking
    cpu_now = psutil.cpu_percent(interval=None, percpu=True)
    if not ema_cpu:
        ema_cpu.extend(cpu_now)
    for i, v in enumerate(cpu_now):
        ema_cpu[i] = alpha * v + (1 - alpha) * ema_cpu[i]
    avg = sum(ema_cpu) / len(ema_cpu)

    tbl = Table(title="🧠 CPU Usage", box=None, expand=True)
    tbl.add_column("Core", justify="center")
    tbl.add_column("Usage", justify="center")
    for i, u in enumerate(ema_cpu):
        tbl.add_row(str(i), f"{u:5.1f}%")
    tbl.add_row("Avg", f"{avg:5.1f}%")

    return Panel(tbl, border_style="cyan")