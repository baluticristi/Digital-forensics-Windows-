import file_system
import network
import process
import registry
import memory
def main():

    target_directory = "D:\\An 4 Sem 2\\Licenta\\Digital-forensics-Windows-\\Python app"
    output_file = "../Data/file_system_data.json"
    file_system.save_file_system_data(target_directory, output_file)
    print(f"File system gathering report saved to {output_file}")

    report = {}
    report['active_connections'] = network.get_active_connections()
    report['network_interfaces'] = network.get_network_interfaces()
    output_file = "../Data/network_data.json"
    network.save_report(report, output_file)
    print(f"Network gathering report saved to {output_file}")


    report = {}
    report['processes'] = process.get_process_info()
    output_file = "../Data/process_data.json"
    process.save_report(report, output_file)
    print(f"Process gathering report saved to {output_file}")


    registry_file = "../Data/registry_data.json"
    registry.save_registry_data(registry_file)
    print(f"Registry gathering report saved to {registry_file}")


if __name__ == "__main__":
    main()
