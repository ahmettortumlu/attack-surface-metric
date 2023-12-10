import socket

def scan_ports(fqdn, start_port, end_port, timeout=1):
    open_ports = []

    try:
        # Resolve the FQDN to obtain the IP address
        ip_address = socket.gethostbyname(fqdn)

        # Scan ports within the specified range
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            result = sock.connect_ex((ip_address, port))

            if result == 0:
                open_ports.append(port)

            sock.close()

        return open_ports

    except socket.gaierror:
        print(f"Error: Unable to resolve the FQDN {fqdn}")
        return []
    except socket.error as e:
        print(f"Error: {e}")
        return []

# Function to scan ports for a list of FQDNs
def scan_ports_for_fqdns(fqdn_list, start_port, end_port):
    results = {}

    for fqdn in fqdn_list:
        open_ports = scan_ports(fqdn, start_port, end_port)
        results[fqdn] = {
            'Open Ports': open_ports
        }

    return results

# Get the list of Fully Qualified Domain Names (FQDNs) from the user
fqdn_list_input = input("Enter a list of FQDNs separated by commas: ")
fqdn_list = [fqdn.strip() for fqdn in fqdn_list_input.split(',')]

# Set the port range to scan (adjust as needed)
start_port = 1
end_port = 1024

# Call the function and get the result
results = scan_ports_for_fqdns(fqdn_list, start_port, end_port)

# Print the results
for fqdn, ports_info in results.items():
    print(f"\nPorts for {fqdn}:")
    if ports_info['Open Ports']:
        print(f"Open Ports: {', '.join(map(str, ports_info['Open Ports']))}")
    else:
        print("No open ports found.")
