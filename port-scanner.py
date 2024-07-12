import socket # Low-level network interface
from concurrent.futures import ThreadPoolExecutor # For parallel tasks

# Check if a port is open
def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)  # Set timeout to 1 second
        try:
            sock.connect((host, port))
            return port, True
        except (socket.timeout, ConnectionRefusedError):
            return port, False

# Scan ports in a range
def port_sweep_range(host, start_port, end_port):
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda p: check_port(host, p), range(start_port, end_port + 1))
        for port, is_open in results:
            status = "open" if is_open else "closed"
            print(f"Port {port} is {status}")
            if is_open:
                open_ports.append(port)

    return open_ports

# Function to scan ports from a list
def port_sweep_list(host, ports):
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda p: check_port(host, p), ports)
        for port, is_open in results:
            status = "open" if is_open else "closed"
            print(f"Port {port} is {status}")
            if is_open:
                open_ports.append(port)
    
    return open_ports

if __name__ == "__main__":
    target_host = "127.0.0.1"  # Target IP address

    # List of ports to scan
    #ports_to_scan = []
    # Home PC
    ports_to_scan = [80, 443, 21, 22, 23, 25, 110, 143, 135, 139, 445, 3389, 53, 1900, 5357]
    # Elasticsearch Instance
    #ports_to_scan = [9200, 9300, 5601, 5044, 5000, 9600, 9870, 6379, 8080, 5672]  

    # if ports_to_scan is empty, the script scans the start_port to end_port range:
    start_port_range = 1
    end_port_range = 10

    if ports_to_scan:
        print(f"Scanning ports {ports_to_scan} on {target_host}...")
        open_ports = port_sweep_list(target_host, ports_to_scan)
    else:
        print(f"Scanning ports {start_port_range} to {end_port_range} on {target_host}...")
        open_ports = port_sweep_range(target_host, start_port_range, end_port_range)
    
    if open_ports:
        print(f"Open ports: {open_ports}")
    else:
        print("No open ports found.")
