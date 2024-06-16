# Whitelist of known safe processes
known_safe_processes = [
    "System Idle Process",
    "System",
    "svchost.exe",
    "explorer.exe",
    "winlogon.exe",
    "services.exe",
    "lsass.exe",
    "csrss.exe",
    "smss.exe",
    "conhost.exe",
    "taskhostw.exe",
    "dwm.exe"
]
def analyze_processes(process_data):
    if not process_data:
        return "Process data is not available."

    # Ensure process_data is a dictionary with a 'processes' key
    if not isinstance(process_data, dict) or 'processes' not in process_data:
        return "Invalid process data format."

    processes = process_data['processes']
    anomalies = []

    for process in processes:
        pid = process['pid']
        name = process['name']
        exe = process['exe']
        cmdline = process['cmdline']
        memory_info = process['memory_info']
        cpu_percent = process['cpu_percent']
        ppid = process['ppid']
        username = process['username']

        # Check against known safe processes
        if name not in known_safe_processes:
            anomalies.append(f"Suspicious process: {name} (PID: {pid}, Executable: {exe}, User: {username})")

        # Check for suspicious names or paths
        if is_suspicious_process(name, exe):
            anomalies.append(f"Suspicious process name/path: {name} (PID: {pid}, Executable: {exe}, User: {username})")

        # Check for high memory or CPU usage
        if memory_info['rss'] > 500 * 1024 * 1024:  # 500 MB
            anomalies.append(f"High memory usage: {name} (PID: {pid}, Memory: {memory_info['rss'] / (1024 * 1024)} MB)")

        if cpu_percent > 80.0:  # 80% CPU usage
            anomalies.append(f"High CPU usage: {name} (PID: {pid}, CPU: {cpu_percent}%)")

        # Check for processes with unusual privileges
        if username != 'NT AUTHORITY\\SYSTEM' and 'system32' in (exe or '').lower():
            anomalies.append(f"Unusual privilege: {name} (PID: {pid}, Executable: {exe}, User: {username})")

    if not anomalies:
        return "No anomalies detected in process data."
    else:
        return "Process analysis found the following anomalies:\n" + "\n".join(anomalies)


def is_suspicious_process(name, exe):
    # Example logic to identify suspicious processes
    suspicious_indicators = ["unknown", "temp", "appdata", ".exe", ".bat", ".cmd", "powershell", "script"]
    for indicator in suspicious_indicators:
        if (name and indicator.lower() in name.lower()) or (exe and indicator.lower() in exe.lower()):
            return True
    return False
