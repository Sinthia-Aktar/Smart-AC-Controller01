
import psutil
import time
import csv
from datetime import datetime
import os

CPU_LIMIT = 80
RAM_LIMIT = 80
DISK_LIMIT = 85

FILE = "monitor_log.csv"

if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Time", "CPU", "RAM", "Disk",
            "Download MB/s", "Upload MB/s"
        ])

old_net = psutil.net_io_counters()

print("SERVER MONITORING STARTED")
print("Press CTRL + C to stop")

try:
    while True:

        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("C:\\").percent

        new_net = psutil.net_io_counters()

        download = (
            new_net.bytes_recv - old_net.bytes_recv
        ) / 1024 / 1024

        upload = (
            new_net.bytes_sent - old_net.bytes_sent
        ) / 1024 / 1024

        old_net = new_net

        os.system("cls")

        print("=" * 40)
        print("   SERVER MONITORING SYSTEM")
        print("=" * 40)

        print(f"CPU Usage      : {cpu:.2f}%")
        print(f"RAM Usage      : {ram:.2f}%")
        print(f"Disk Usage     : {disk:.2f}%")
        print(f"Download Speed : {download:.4f} MB/s")
        print(f"Upload Speed   : {upload:.4f} MB/s")

        print("-" * 40)

        if cpu > CPU_LIMIT:
            print("WARNING: HIGH CPU USAGE!")

        if ram > RAM_LIMIT:
            print("WARNING: HIGH RAM USAGE!")

        if disk > DISK_LIMIT:
            print("WARNING: LOW DISK SPACE!")

        with open(FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                cpu, ram, disk, download, upload
            ])

        print("\nMonitoring is running...")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")