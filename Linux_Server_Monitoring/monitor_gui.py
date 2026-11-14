
import tkinter as tk
from tkinter import ttk
import psutil
from datetime import datetime
import csv
import os

# Settings
CPU_LIMIT = 80
RAM_LIMIT = 80
DISK_LIMIT = 85

running = False
old_net = None
old_time = None

# Window
root = tk.Tk()
root.title("Server Monitoring Dashboard")
root.geometry("750x600")
root.configure(bg="#101827")
root.resizable(False, False)

# Title
tk.Label(
    root, text="SERVER MONITORING SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#101827", fg="white"
).pack(pady=20)

status = tk.Label(
    root, text="● STOPPED",
    font=("Arial", 12, "bold"),
    bg="#101827", fg="#ff6464"
)
status.pack()

# Dashboard
dashboard = tk.Frame(root, bg="#101827")
dashboard.pack(pady=25)

def create_card(title, column):
    card = tk.Frame(
        dashboard, bg="#1e293b",
        width=210, height=125
    )
    card.grid(row=0, column=column, padx=10, pady=10)
    card.pack_propagate(False)

    tk.Label(
        card, text=title,
        font=("Arial", 13, "bold"),
        bg="#1e293b", fg="#94a3b8"
    ).pack(pady=12)

    value = tk.Label(
        card, text="0%",
        font=("Arial", 25, "bold"),
        bg="#1e293b", fg="white"
    )
    value.pack()

    return value

cpu_value = create_card("CPU USAGE", 0)
ram_value = create_card("RAM USAGE", 1)
disk_value = create_card("DISK USAGE", 2)

# Network information
network = tk.Label(
    root,
    text="Download: 0 MB/s     Upload: 0 MB/s",
    font=("Arial", 14),
    bg="#101827", fg="#38bdf8"
)
network.pack(pady=15)

# Alert information
alert = tk.Label(
    root, text="No alerts",
    font=("Arial", 13, "bold"),
    bg="#101827", fg="#4ade80"
)
alert.pack(pady=10)

# Buttons
def start_monitoring():
    global running, old_net, old_time

    if running:
        return

    running = True
    old_net = psutil.net_io_counters()
    old_time = datetime.now()

    status.config(text="● RUNNING", fg="#4ade80")
    update_dashboard()

def stop_monitoring():
    global running
    running = False
    status.config(text="● STOPPED", fg="#ff6464")

def update_dashboard():
    global old_net, old_time

    if not running:
        return

    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("C:\\").percent

    new_net = psutil.net_io_counters()
    new_time = datetime.now()

    seconds = max((new_time - old_time).total_seconds(), 0.001)

    download = (new_net.bytes_recv - old_net.bytes_recv) / 1024 / 1024 / seconds
    upload = (new_net.bytes_sent - old_net.bytes_sent) / 1024 / 1024 / seconds

    old_net = new_net
    old_time = new_time

    cpu_value.config(text=f"{cpu:.1f}%")
    ram_value.config(text=f"{ram:.1f}%")
    disk_value.config(text=f"{disk:.1f}%")

    network.config(
        text=f"Download: {download:.4f} MB/s     Upload: {upload:.4f} MB/s"
    )

    warnings = []

    if cpu > CPU_LIMIT:
        warnings.append("HIGH CPU")

    if ram > RAM_LIMIT:
        warnings.append("HIGH RAM")

    if disk > DISK_LIMIT:
        warnings.append("HIGH DISK")

    if warnings:
        alert.config(
            text="WARNING: " + " | ".join(warnings),
            fg="#ff6464"
        )
    else:
        alert.config(text="System Running Normally", fg="#4ade80")

    # Save monitoring history
    file = "monitor_log.csv"

    if not os.path.exists(file):
        with open(file, "w", newline="") as f:
            csv.writer(f).writerow(
                ["Time", "CPU", "RAM", "Disk", "Download", "Upload"]
            )

    with open(file, "a", newline="") as f:
        csv.writer(f).writerow([
            new_time.strftime("%Y-%m-%d %H:%M:%S"),
            cpu, ram, disk, download, upload
        ])

    root.after(1000, update_dashboard)

# Control buttons
buttons = tk.Frame(root, bg="#101827")
buttons.pack(pady=25)

tk.Button(
    buttons, text="START MONITORING",
    command=start_monitoring,
    bg="#16a34a", fg="white",
    font=("Arial", 12, "bold"),
    width=20, pady=12
).grid(row=0, column=0, padx=10)

tk.Button(
    buttons, text="STOP MONITORING",
    command=stop_monitoring,
    bg="#dc2626", fg="white",
    font=("Arial", 12, "bold"),
    width=20, pady=12
).grid(row=0, column=1, padx=10)

tk.Label(
    root,
    text="Live System Performance Monitoring",
    font=("Arial", 10),
    bg="#101827", fg="#64748b"
).pack(side="bottom", pady=15)

root.mainloop()
