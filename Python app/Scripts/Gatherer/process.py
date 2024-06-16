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

