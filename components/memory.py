import psutil
from rich.table import Table
from rich.panel import Panel

from .utils import get_size


def get_memory_panel():
    """Return a Panel with RAM and swap usage."""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    tbl = Table(title="🧾 Memory", box=None, expand=True)
    tbl.add_column("Type")
    tbl.add_column("Total", justify="right")
    tbl.add_column("Used", justify="right")
    tbl.add_column("Free", justify="right")
    tbl.add_row("RAM", get_size(mem.total), get_size(mem.used), get_size(mem.available))
    tbl.add_row("Swap", get_size(swap.total), get_size(swap.used), get_size(swap.free))

    return Panel(tbl, border_style="cyan")