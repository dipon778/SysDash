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
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    uptime_s = time.time() - psutil.boot_time()
    days = int(uptime_s // 86400)
    hms  = time.strftime("%H:%M:%S", time.gmtime(uptime_s))
    up   = f"{days}d {hms}" if days else hms

    time_p = Panel(Text(now, justify="center"), title="⏰ Now",    border_style="blue")
    up_p   = Panel(Text(up,  justify="center"), title="🕒 Uptime", border_style="green")
    hdr    = Layout(name="header")
    hdr.split_row(Layout(time_p), Layout(up_p))
    return hdr

def make_left(ema_cpu, alpha=0.3, proc_count=5):
    # —— CPU EMA
    cpu_now = psutil.cpu_percent(interval=None, percpu=True)
    if not ema_cpu:
        ema_cpu.extend(cpu_now)
    for i, v in enumerate(cpu_now):
        ema_cpu[i] = alpha*v + (1-alpha)*ema_cpu[i]
    avg = sum(ema_cpu)/len(ema_cpu)

    cpu_tbl = Table(title="🧠 CPU Usage", box=None, expand=True)
    cpu_tbl.add_column("Core", justify="center")
    cpu_tbl.add_column("Usage", justify="center")
    for i, u in enumerate(ema_cpu):
        cpu_tbl.add_row(str(i), f"{u:5.1f}%")
    cpu_tbl.add_row("Avg", f"{avg:5.1f}%")

    # —— Memory
    mem  = psutil.virtual_memory()
    swap = psutil.swap_memory()
    mem_tbl = Table(title="🧮 Memory", box=None, expand=True)
    mem_tbl.add_column("Type"); mem_tbl.add_column("Total"); mem_tbl.add_column("Used"); mem_tbl.add_column("Free")
    mem_tbl.add_row("RAM",  get_size(mem.total), get_size(mem.used),     get_size(mem.available))
    mem_tbl.add_row("Swap", get_size(swap.total),get_size(swap.used),    get_size(swap.free))

    # —— Top Processes
    procs = []
    for p in psutil.process_iter(['pid','name']):
        try:
            cpu = p.cpu_percent(interval=None)
            memp = p.memory_percent()
            procs.append((cpu, memp, p.info['pid'], p.info['name']))
        except Exception:
            continue
    procs.sort(reverse=True, key=lambda x: x[0])
    top = procs[:proc_count]

    proc_tbl = Table(title=f"🚀 Top {proc_count} by CPU", box=None, expand=True)
    proc_tbl.add_column("PID",   justify="right")
    proc_tbl.add_column("Name",  overflow="fold")
    proc_tbl.add_column("CPU %", justify="right")
    proc_tbl.add_column("Mem %",justify="right")
    for cpu, memp, pid, name in top:
        proc_tbl.add_row(str(pid), name or "", f"{cpu:4.1f}", f"{memp:4.1f}")

    left = Layout(name="left")
    left.split_column(
        Layout(Panel(cpu_tbl,  border_style="cyan"), ratio=2),
        Layout(Panel(mem_tbl,  border_style="cyan"), ratio=1),
        Layout(Panel(proc_tbl, border_style="cyan"), ratio=2),
    )
    return left

def make_right(prev_net, interval):
    # —— Disk
    disk = psutil.disk_usage('/')
    disk_tbl = Table(title="💾 Disk", box=None, expand=True)
    disk_tbl.add_column("Total"); disk_tbl.add_column("Used"); disk_tbl.add_column("Free")
    disk_tbl.add_row(get_size(disk.total), get_size(disk.used), get_size(disk.free))

    # —— Network + Speed
    curr_net = psutil.net_io_counters()
    up_spd   = (curr_net.bytes_sent - prev_net.bytes_sent) / interval
    dn_spd   = (curr_net.bytes_recv - prev_net.bytes_recv) / interval

    net_tbl = Table(title="🌐 Network I/O", box=None, expand=True)
    net_tbl.add_column("Stat"); net_tbl.add_column("Total"); net_tbl.add_column("Speed")
    net_tbl.add_row("Sent", get_size(curr_net.bytes_sent), f"{get_size(up_spd)}/s")
    net_tbl.add_row("Recv", get_size(curr_net.bytes_recv), f"{get_size(dn_spd)}/s")

    right = Layout(name="right")
    right.split_column(
        Layout(Panel(disk_tbl, border_style="magenta"), ratio=1),
        Layout(Panel(net_tbl,  border_style="magenta"), ratio=1),
    )
    return right, curr_net

def make_footer():
    return Layout(Panel(Text("Press Ctrl+C to quit", justify="center", style="dim")))

def build_layout(ema_cpu, prev_net, interval):
    root = Layout()
    root.split_column(
        make_header(),
        Layout(name="body", ratio=8),
        make_footer()
    )
    left  = make_left(ema_cpu)
    right, new_net = make_right(prev_net, interval)
    root["body"].split_row(left, right)
    return root, new_net

def main():
    # Pre‑seed CPU & process counters so first frame isn’t empty
    psutil.cpu_percent(interval=None, percpu=True)
    for p in psutil.process_iter():
        try: p.cpu_percent(None)
        except: pass

    ema_cpu  = deque()
    prev_net = psutil.net_io_counters()
    prev_t   = time.time()
    sleep_interval = 0.75  # ~1.33 updates/sec

    with Live(console=console, screen=True, refresh_per_second=2) as live:
        try:
            while True:
                now = time.time()
                interval = now - prev_t
                prev_t = now

                layout, prev_net = build_layout(ema_cpu, prev_net, interval)
                live.update(layout)
                time.sleep(sleep_interval)
        except KeyboardInterrupt:
            console.clear()
            console.print("[bold green]Goodbye – monitor exited![/bold green]")

if __name__ == "__main__":
    main()
