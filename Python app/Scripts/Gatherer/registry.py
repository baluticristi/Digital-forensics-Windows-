import winreg
import json
import os
def read_registry_key(hive, subkey, value_name=None):
    try:
        with winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ) as reg_key:
            if value_name:
                value, reg_type = winreg.QueryValueEx(reg_key, value_name)
                if isinstance(value, bytes):
                    value = value.decode('utf-8', errors='ignore')
                return {value_name: value}
            else:
                values = {}
                i = 0
                while True:
                    try:
                        value_name, value, reg_type = winreg.EnumValue(reg_key, i)
                        if isinstance(value, bytes):
                            value = value.decode('utf-8', errors='ignore')
                        values[value_name] = value
                        i += 1
                    except OSError:
                        break
                return values
    except FileNotFoundError:
        print(f"Registry key not found: {subkey}")
        return {}
    except Exception as e:
        print(f"Error reading registry key {subkey}: {e}")
        return {}

def analyze_registry():
    registry_paths = {
        "HKEY_LOCAL_MACHINE": [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            r"SYSTEM\CurrentControlSet\Services",
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce",
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
            r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces",
            r"SYSTEM\MountedDevices",
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
            r"SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName"
        ],
        "HKEY_CURRENT_USER": [
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs",
            r"Software\Microsoft\Windows\CurrentVersion\Uninstall",
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist",
            r"Software\Microsoft\Windows\Shell\Bags",
            r"Software\Microsoft\Windows\Shell\BagMRU",
            r"Software\Microsoft\Internet Explorer\TypedURLs",
            r"Software\Google\Chrome\PreferenceMACs",
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths",
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
        ]
    }

    registry_data = {}
    for hive_name, subkeys in registry_paths.items():
        hive = getattr(winreg, hive_name)
        for subkey in subkeys:
            values = read_registry_key(hive, subkey)
            if values:
                registry_data[f"{hive_name}\\{subkey}"] = values

    return registry_data

def save_registry_data(file_path):
    registry_data = analyze_registry()
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as outfile:
        json.dump(registry_data, outfile, indent=4)
