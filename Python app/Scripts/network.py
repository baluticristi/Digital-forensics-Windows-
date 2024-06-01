import psutil
import json

def get_active_connections():
    connections = psutil.net_connections()
    active_connections = []

    for conn in connections:
        if conn.status == psutil.CONN_ESTABLISHED:
            active_connections.append({
                'fd': conn.fd,
                'family': conn.family.name,
                'type': conn.type.name,
                'laddr': f"{conn.laddr.ip}:{conn.laddr.port}",
                'raddr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                'status': conn.status,
                'pid': conn.pid
            })

    return active_connections

def get_network_interfaces():
    interfaces = psutil.net_if_addrs()
    interface_details = {}

    for interface, addrs in interfaces.items():
        interface_details[interface] = []
        for addr in addrs:
            interface_details[interface].append({
                'family': addr.family.name,
                'address': addr.address,
                'netmask': addr.netmask,
                'broadcast': addr.broadcast,
                'ptp': addr.ptp
            })

    return interface_details

def save_report(report, output_file):
    with open(output_file, 'w') as outfile:
        json.dump(report, outfile, indent=4)

def main():
    report = {}

    # Get active connections
    report['active_connections'] = get_active_connections()

    # Get network interfaces
    report['network_interfaces'] = get_network_interfaces()

    # Save all data into a single report file
    output_file = "Data/network_analysis_report.json"
    save_report(report, output_file)

    print(f"Network analysis report saved to {output_file}")

if __name__ == "__main__":
    main()
