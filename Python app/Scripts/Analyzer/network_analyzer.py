import ipaddress

# Known safe IP addresses and subnets (example)
known_safe_ips = [
    "127.0.0.1",  # localhost
    "192.168.0.0/16",  # Private network
    "10.0.0.0/8",  # Private network
    "172.16.0.0/12"  # Private network
]

# Known safe ports
known_safe_ports = [80, 443, 53, 21, 22, 25, 110, 143, 993, 995, 3306, 1433, 3389]


def analyze_network(network_data):
    if not network_data:
        return "Network data is not available."

    active_connections = network_data.get("active_connections", [])
    interfaces = network_data.get("interfaces", {})

    connection_analysis = analyze_network_connections(active_connections)
    interface_analysis = analyze_network_interfaces(interfaces)

    return f"{connection_analysis}\n{interface_analysis}"


def analyze_network_connections(active_connections):
    anomalies = []

    for conn in active_connections:
        raddr = conn['raddr']
        rport = int(raddr.split(':')[1]) if raddr != 'N/A' else None
        rip = raddr.split(':')[0] if raddr != 'N/A' else None

        # Check if remote address is not in known safe IPs
        if rip and not is_known_safe_ip(rip):
            anomalies.append(f"Suspicious remote IP: {raddr} (PID: {conn['pid']}, Local Address: {conn['laddr']})")

        # Check if remote port is not in known safe ports
        if rport and rport not in known_safe_ports:
            anomalies.append(f"Suspicious remote port: {rport} (Remote IP: {rip}, PID: {conn['pid']}, Local Address: {conn['laddr']})")

    if not anomalies:
        return "No anomalies detected in network connections."
    else:
        return "Network connections analysis found the following anomalies:\n" + "\n".join(anomalies)

def is_known_safe_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        for safe_ip in known_safe_ips:
            if ip_obj in ipaddress.ip_network(safe_ip):
                return True
    except ValueError:
        pass
    return False

def analyze_network_interfaces(interfaces):
    anomalies = []

    for interface, addrs in interfaces.items():
        for addr in addrs:
            # Check if IP address is not in known safe IPs
            if addr['family'] == 'AF_INET' and not is_known_safe_ip(addr['address']):
                anomalies.append(f"Suspicious IP address: {addr['address']} on interface {interface}")

    if not anomalies:
        return "No anomalies detected in network interfaces."
    else:
        return "Network interfaces analysis found the following anomalies:\n" + "\n".join(anomalies)
