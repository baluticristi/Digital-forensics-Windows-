import psutil
import json

def get_process_info():
    process_list = []

    for proc in psutil.process_iter(attrs=['pid', 'name', 'exe', 'cmdline', 'memory_info', 'cpu_percent', 'ppid', 'username']):
        try:
            pinfo = proc.info
            process_info = {
                'pid': pinfo['pid'],
                'name': pinfo['name'],
                'exe': pinfo['exe'],
                'cmdline': pinfo['cmdline'],
                'memory_info': {
                    'rss': pinfo['memory_info'].rss,
                    'vms': pinfo['memory_info'].vms
                },
                'cpu_percent': pinfo['cpu_percent'],
                'ppid': pinfo['ppid'],
                'username': pinfo['username']
            }
            process_list.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return process_list

def save_report(report, output_file):
    with open(output_file, 'w') as outfile:
        json.dump(report, outfile, indent=4)

def main():
    report = {}

    report['processes'] = get_process_info()

    output_file = "Data/process_analysis_report.json"
    save_report(report, output_file)

    print(f"Process analysis report saved to {output_file}")

if __name__ == "__main__":
    main()
