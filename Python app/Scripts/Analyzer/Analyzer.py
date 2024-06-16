import json
import registry_analyzer
import process_analyzer
import network_analyzer
import file_system_analyzer
def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def load_all_data(file_system_path, network_path, process_path, registry_path):
    file_system_data = load_json_file(file_system_path)
    network_data = load_json_file(network_path)
    process_data = load_json_file(process_path)
    registry_data = load_json_file(registry_path)

    return file_system_data, network_data, process_data, registry_data


######DATA ANALYSIS######
def analyze_file_system(file_system_data):
    if not file_system_data:
        return "File system data is not available."

    if isinstance(file_system_data, list):
        file_count = len(file_system_data)
        directory_count = sum(1 for item in file_system_data if item.get("type") == "directory")
    else:
        file_count = len(file_system_data.get("files", []))
        directory_count = len(file_system_data.get("directories", []))

    return f"File system analysis: {file_count} files and {directory_count} directories."


def generate_report(file_system_analysis, network_analysis, process_analysis, registry_analysis):
    report = {
        "File System Analysis": file_system_analysis,
        "Network Analysis": network_analysis,
        "Process Analysis": process_analysis,
        "Registry Analysis": registry_analysis,
    }
    return report

def save_report(report, output_file):
    with open(output_file, 'w') as outfile:
        json.dump(report, outfile, indent=4)


def main():
    file_system_path = "../Data/file_system_data.json"
    network_path = "../Data/network_data.json"
    process_path = "../Data/process_data.json"
    registry_path = "../Data/registry_data.json"
    output_file = "../analysis_report.json"

    file_system_data,  network_data, process_data, registry_data = load_all_data(
        file_system_path, network_path, process_path, registry_path)

    file_system_analysis = file_system_analyzer.analyze_file_system(file_system_data)
    network_analysis = network_analyzer.analyze_network(network_data)
    process_analysis = process_analyzer.analyze_processes(process_data)
    registry_analysis = registry_analyzer.analyze_registry(registry_data)

    report = generate_report(file_system_analysis, network_analysis, process_analysis, registry_analysis)
    save_report(report, output_file)

    print(f"Analysis report saved to {output_file}")

if __name__ == "__main__":
    main()
