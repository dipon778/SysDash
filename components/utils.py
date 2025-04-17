from datetime import datetime

def get_size(bytes, suffix="B"):
    """Human-readable byte size."""
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor
    return f"{bytes:.2f} P{suffix}"

def get_time_date():
    """Return the current time, date, and day."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S (%A)")