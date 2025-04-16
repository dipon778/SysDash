import psutil
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

def display_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    avg_cpu_usage = sum(cpu_usage) / len(cpu_usage)
    table = Table(title="CPU Usage", title_justify="center", style="cyan")
    table.add_column("Core", justify="center", style="magenta")
    table.add_column("Usage (%)", justify="center", style="green")
    
    for i, usage in enumerate(cpu_usage):
        table.add_row(f"Core {i}", f"{usage}%")
    
    table.add_row("Average", f"{avg_cpu_usage:.2f}%")
    console.print(table)

def display_memory_usage():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    table = Table(title="Memory Usage", title_justify="center", style="cyan")
    table.add_column("Type", justify="center", style="magenta")
    table.add_column("Total (GB)", justify="center", style="green")
    table.add_column("Used (GB)", justify="center", style="green")
    table.add_column("Free (GB)", justify="center", style="green")
    
    table.add_row("RAM", f"{memory.total / (1024 ** 3):.2f}", f"{memory.used / (1024 ** 3):.2f}", f"{memory.free / (1024 ** 3):.2f}")
    table.add_row("Swap", f"{swap.total / (1024 ** 3):.2f}", f"{swap.used / (1024 ** 3):.2f}", f"{swap.free / (1024 ** 3):.2f}")
    
    console.print(table)

def display_disk_usage():
    disk = psutil.disk_usage('/')
    table = Table(title="Disk Usage", title_justify="center", style="cyan")
    table.add_column("Total (GB)", justify="center", style="magenta")
    table.add_column("Used (GB)", justify="center", style="green")
    table.add_column("Free (GB)", justify="center", style="green")
    
    table.add_row(f"{disk.total / (1024 ** 3):.2f}", f"{disk.used / (1024 ** 3):.2f}", f"{disk.free / (1024 ** 3):.2f}")
    console.print(table)

def display_network_usage():
    net_io = psutil.net_io_counters()
    table = Table(title="Network Usage", title_justify="center", style="cyan")
    table.add_column("Type", justify="center", style="magenta")
    table.add_column("Bytes Sent", justify="center", style="green")
    table.add_column("Bytes Received", justify="center", style="green")
    
    table.add_row("Network", f"{net_io.bytes_sent}", f"{net_io.bytes_recv}")
    console.print(table)

def display_uptime():
    uptime = time.time() - psutil.boot_time()
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))
    console.print(Panel(Text(f"Uptime: {uptime_str}", style="green"), title="System Uptime", title_align="left"))

def display_clock():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    console.print(Panel(Text(f"Current Time: {current_time}", style="blue"), title="Current Time", title_align="left"))

def main():
    while True:
        console.clear()
        display_cpu_usage()
        display_memory_usage()
        display_disk_usage()
        display_network_usage()
        display_uptime()
        display_clock()
        time.sleep(1)

if __name__ == "__main__":
    main()
