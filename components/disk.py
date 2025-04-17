import psutil
from rich.table import Table
from rich.panel import Panel

from .utils import get_size


def get_disk_panel():
    """Return a Panel with disk total/used/free."""
    disk = psutil.disk_usage('/')
    tbl = Table(box=None, expand=True)
    tbl.add_column("Total", justify="right")
    tbl.add_column("Used", justify="right")
    tbl.add_column("Free", justify="right")
    tbl.add_row(get_size(disk.total), get_size(disk.used), get_size(disk.free))

    # Return a panel with a title and consistent styling
    return Panel(tbl, title="📠 Disk Usage", border_style="cyan")