import random
import time
import threading
import sys
from mcstatus import JavaServer

# Counter for scanned IPs
scanned_ips = 0
lock = threading.Lock()  # To ensure thread-safe access to the counter

# Global list to store IPs to be scanned
ip_list = []
valid_ips = []  # List to store valid Minecraft server IPs

# Read IPs from the input file
def read_ips(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            ip_list.append(line.strip())

# Scan an IP for a Minecraft server with a timeout
def scan_ip(ip):
    global scanned_ips
    try:
        # Attempt to connect to the Minecraft server
        server = JavaServer.lookup(ip, timeout=3)
        # If the server responds, it's a valid Minecraft server
        server.status()  # Queries the server and will throw an exception if invalid
        
        # If it's valid, add to the list of valid IPs (no additional information)
        with lock:
            valid_ips.append(ip)
        print(f"[VALID] {ip}")  # Optional feedback for valid IP
    except Exception:
        # If the server does not respond correctly, ignore it
        pass
    finally:
        # Increment the scanned IP counter safely
        with lock:
            scanned_ips += 1

# Worker function for threads
def worker():
    while True:
        if ip_list:
            ip = ip_list.pop()  # Get the next IP from the list
            scan_ip(ip)
        else:
            break

# Function to calculate and display the scanning rate
def display_ips_per_second():
    global scanned_ips
    while True:
        time.sleep(1)  # Calculate rate every second
        with lock:
            ips = scanned_ips
            scanned_ips = 0  # Reset the counter for the next interval
        print(f"[STATS] Scanning rate: {ips} IPs/second")

# Main function
def main():
    if len(sys.argv) != 4:
        print("Usage: python3 script.py <inputlist.txt> <threads> <outputlist.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    thread_count = int(sys.argv[2])  # Number of scanning threads
    output_file = sys.argv[3]

    # Read IPs from the input file
    read_ips(input_file)

    # Start worker threads
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        threads.append(thread)

    # Start the IPS counter thread
    stats_thread = threading.Thread(target=display_ips_per_second, daemon=True)
    stats_thread.start()

    # Wait for threads to finish
    for thread in threads:
        thread.join()

    # After all scanning is done, sort the valid IPs and write to the output file
    valid_ips.sort()  # Sort the list of valid IPs
    with open(output_file, "w") as file:
        for ip in valid_ips:
            file.write(f"{ip}\n")

    print(f"\n[INFO] Scanning completed. Found {len(valid_ips)} valid Minecraft servers.")

if __name__ == "__main__":
    main()
