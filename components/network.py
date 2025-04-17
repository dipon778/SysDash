import psutil
from rich.table import Table
from rich.panel import Panel

from .utils import get_size


def get_network_panel(prev, interval):
    """Return a Panel with network totals and speeds."""
    curr = psutil.net_io_counters()
    up = (curr.bytes_sent - prev.bytes_sent) / interval
    dn = (curr.bytes_recv - prev.bytes_recv) / interval

    tbl = Table(box=None, expand=True)
    tbl.add_column("Stat")
    tbl.add_column("Total", justify="right")
    tbl.add_column("Speed", justify="right")
    tbl.add_row("Sent", get_size(curr.bytes_sent), f"{get_size(up)}/s")
    tbl.add_row("Recv", get_size(curr.bytes_recv), f"{get_size(dn)}/s")

    # Add a title to the panel
    return Panel(tbl, title="🌐 Network I/O", border_style="cyan"), curr