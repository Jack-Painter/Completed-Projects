Python Script
# Network Traffic Monitoring Script
import psutil
import time
import os

def monitor_network(log_file="C:\\Users\\windows\\Documents\\Python\\logs\\network_log.txt", interval=1):
    """
    Continuously monitor network traffic and log it to a file.

    Args:
        log_file (str): Path to the log file.
        interval (int): Time in seconds between each log entry.
    """
    # Ensure the log file folder exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write("Timestamp | Bytes Sent | Bytes Received\n")

    while True:
        # Retrieve network I/O stats
        net = psutil.net_io_counters()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | Sent: {net.bytes_sent} bytes | Received: {net.bytes_recv} bytes\n"

        # Append log entry
        with open(log_file, "a") as log:
            log.write(log_entry)

        # Wait before next cycle
        time.sleep(interval)

if __name__ == "__main__":
    monitor_network()
