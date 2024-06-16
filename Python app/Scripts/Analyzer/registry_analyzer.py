def analyze_registry(registry_data):
    if not registry_data:
        return "Registry data is not available."

    anomalies = []

    # Check for unusual startup programs
    startup_locations = [
        r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
        r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run"
    ]

    for location in startup_locations:
        if location in registry_data:
            for program, path in registry_data[location].items():
                if is_suspicious_program(program, path):
                    anomalies.append(f"Suspicious startup program: {program} at {path}")

    # Check for suspicious UserAssist entries
    user_assist_key = r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist"
    if user_assist_key in registry_data:
        for subkey, values in registry_data[user_assist_key].items():
            for program, timestamp in values.items():
                if is_suspicious_program(program, timestamp):
                    anomalies.append(f"Suspicious recently executed program: {program}")

    # Check for unusual services
    services_key = r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services"
    if services_key in registry_data:
        for service, details in registry_data[services_key].items():
            if is_suspicious_service(service, details):
                anomalies.append(f"Suspicious service: {service}")

    # Check for browser hijacking
    browser_settings_keys = [
        r"HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\Main",
        r"HKEY_CURRENT_USER\Software\Mozilla\Mozilla Firefox",
        r"HKEY_CURRENT_USER\Software\Google\Chrome\PreferenceMACs"
    ]

    for key in browser_settings_keys:
        if key in registry_data:
            for setting, value in registry_data[key].items():
                if is_suspicious_browser_setting(setting, value):
                    anomalies.append(f"Suspicious browser setting: {setting} = {value}")

    # Analyze additional registry paths
    additional_paths = {
        "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce": "RunOnce entries",
        "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall": "Uninstall entries",
        "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters": "TCP/IP parameters",
        "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces": "Network interfaces",
        "HKEY_LOCAL_MACHINE\\SYSTEM\\MountedDevices": "Mounted devices",
        "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment": "Session environment variables",
        "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\ComputerName\\ComputerName": "Computer name",
        "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs": "Recent documents",
        "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\Shell\\Bags": "Shell bags",
        "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\Shell\\BagMRU": "Shell BagMRU",
        "HKEY_CURRENT_USER\\Software\\Microsoft\\Internet Explorer\\TypedURLs": "Typed URLs in Internet Explorer",
        "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\TypedPaths": "Typed paths",
        "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU": "Run MRU"
    }

    for path, description in additional_paths.items():
        if path in registry_data:
            if registry_data[path]:
                anomalies.append(f"Found entries in {description}: {registry_data[path]}")
            else:
                anomalies.append(f"No entries found in {description}")

    if not anomalies:
        return "No anomalies detected in registry data."
    else:
        return "Registry analysis found the following anomalies:\n" + "\n".join(anomalies)

# Whitelists for known safe programs, services, and browser settings
known_safe_programs = [
    "SecurityHealth",
    "RtkAudUService",
    "Riot Vanguard",
    "DpTsClnt",
    "OneDrive",
    "MicrosoftEdgeAutoLaunch_E70111A6D3D532660EBE9471C73B8507",
    "Discord",
    "com.squirrel.Teams.Teams",
    "Overwolf",
    "LenovoVantageToolbar",
    "Steam",
    "OpenVPN-GUI",
    "org.openvpn.client",
    "EpicGamesLauncher",
    "Plex Media Server",
    "Docker Desktop",
    "Opera GX Stable",
    "Opera GX Browser Assistant",
    "CCleaner Smart Cleaning"
]

known_safe_services = [
    "wuauserv",  # Windows Update
    "WinDefend",  # Windows Defender Antivirus Service
    "MpsSvc",  # Windows Firewall
    "Audiosrv",  # Windows Audio
    "EventLog",  # Windows Event Log
    "W32Time",  # Windows Time
    "TermService",  # Remote Desktop Services
    "Dhcp",  # DHCP Client
    "Dnscache",  # DNS Client
    "Spooler",  # Print Spooler
    "SamSs",  # Security Accounts Manager
    "Winmgmt",  # Windows Management Instrumentation
    "BITS",  # Background Intelligent Transfer Service
    "NlaSvc",  # Network Location Awareness
    "Schedule",  # Task Scheduler
    "WSearch",  # Windows Search
    "gupdate",  # Google Update Service
    "gupdatem",  # Google Update Service
    "AdobeARMservice",  # Adobe Acrobat Update Service
    "nvsvc",  # NVIDIA Display Driver Service
    "AppleMobileDeviceService",  # Apple Mobile Device Service
    "IAStorDataMgrSvc",  # Intel Rapid Storage Technology
    "RtkAudioService"  # Realtek Audio Service
]

known_safe_browser_settings = [
    # Internet Explorer
    "Start Page",  # Default or user-configured homepage
    "Search Page",  # Default or user-configured search page
    "ProxyEnable",  # Usually 0 (disabled) or 1 (enabled)
    "ProxyServer",  # Empty or specific proxy server
    "ProxyOverride",  # Proxy exceptions

    # Mozilla Firefox
    "browser.startup.homepage",  # Default or user-configured homepage
    "network.proxy.type",  # 0 (No Proxy), 1 (Manual Proxy Configuration), 2 (Proxy Auto-Config), 4 (Auto-detect Proxy)
    "network.proxy.http",  # HTTP proxy server
    "network.proxy.http_port",  # HTTP proxy port
    "network.proxy.ssl",  # SSL proxy server
    "network.proxy.ssl_port",  # SSL proxy port
    "network.proxy.ftp",  # FTP proxy server
    "network.proxy.ftp_port",  # FTP proxy port
    "network.proxy.socks",  # SOCKS host
    "network.proxy.socks_port",  # SOCKS host port
    "network.proxy.socks_version",  # SOCKS version
    "network.proxy.no_proxies_on",  # Proxy exceptions

    # Google Chrome
    "homepage",  # Default or user-configured homepage
    "proxy",  # Proxy settings
    "search_provider",  # Search provider settings
    "default_search_provider_name",  # Default search provider name
    "extensions.settings"  # Extensions settings
]

def is_suspicious_program(program, path):
    if program in known_safe_programs:
        return False
    # Example logic to identify suspicious programs
    suspicious_indicators = ["unknown", "temp", "appdata", ".exe", ".bat", ".cmd"]
    for indicator in suspicious_indicators:
        if indicator.lower() in program.lower() or indicator.lower() in path.lower():
            return True
    return False

def is_suspicious_service(service, details):
    if service in known_safe_services:
        return False
    # Example logic to identify suspicious services
    suspicious_indicators = ["unknown", "temp", "appdata", ".exe", ".dll"]
    for indicator in suspicious_indicators:
        if indicator.lower() in service.lower() or indicator.lower() in str(details).lower():
            return True
    return False

def is_suspicious_browser_setting(setting, value):
    if setting in known_safe_browser_settings:
        return False
    # Example logic to identify suspicious browser settings
    suspicious_indicators = ["homepage", "search", "proxy"]
    for indicator in suspicious_indicators:
        if indicator.lower() in setting.lower() or indicator.lower() in value.lower():
            return True
    return False