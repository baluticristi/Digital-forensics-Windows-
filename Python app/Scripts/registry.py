import winreg
import json
import os

class RegistryAnalysis:

    def __init__(self, baseline_file):
        self.baseline_file = baseline_file
        self.baseline_data = self.load_baseline_data(self.baseline_file) if os.path.exists(self.baseline_file) else {}

    def load_baseline_data(self, file_path):
        try:
            with open(file_path, 'r') as infile:
                baseline_data = json.load(infile)
            return baseline_data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
            return {}
        except Exception as e:
            print(f"Error loading baseline data from {file_path}: {e}")
            return {}

    def read_registry_key(self, hive, subkey, value_name=None):
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

    def analyze_registry(self):
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
                values = self.read_registry_key(hive, subkey)
                if values:
                    registry_data[f"{hive_name}\\{subkey}"] = values

        return registry_data

    def save_baseline(self):
        baseline_data = self.analyze_registry()
        os.makedirs(os.path.dirname(self.baseline_file), exist_ok=True)
        with open(self.baseline_file, 'w') as outfile:
            json.dump(baseline_data, outfile, indent=4)
        print(f"Baseline data saved to {self.baseline_file}")

    def compare_registry_data(self, current_data):
        changes = {}

        for key, current_values in current_data.items():
            baseline_values = self.baseline_data.get(key, {})
            if current_values != baseline_values:
                changes[key] = {
                    "current": current_values,
                    "baseline": baseline_values
                }

        return changes

    def generate_report(self):
        current_data = self.analyze_registry()
        changes = self.compare_registry_data(current_data)

        report = {
            "Changes Detected": changes
        }

        with open("registry_analysis_report.json", 'w') as outfile:
            json.dump(report, outfile, indent=4)

        print("Analysis report generated: registry_analysis_report.json")

def main():
    baseline_file = "Data/baseline_registry_data.json"  # Path to the baseline registry data file

    analysis = RegistryAnalysis(baseline_file)

    if not analysis.baseline_data:
        analysis.save_baseline()
    else:
        analysis.generate_report()

if __name__ == "__main__":
    main()
