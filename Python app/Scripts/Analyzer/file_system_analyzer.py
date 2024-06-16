import json
import os
import hashlib

# Suspicious file extensions
suspicious_extensions = ['.exe', '.bat', '.cmd', '.sh', '.dll', '.sys', '.scr']

# Known safe directories (example)
known_safe_directories = [
    "C:\\Windows\\System32",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\Users\\Public",
    "C:\\Users\\<YourUsername>\\Documents"
]

def analyze_file_system(file_system_data):
    if not file_system_data:
        return "File system data is not available."

    anomalies = []

    for file_metadata in file_system_data:
        file_path = file_metadata['file_path']
        size = file_metadata['size']
        creation_time = file_metadata['creation_time']
        modification_time = file_metadata['modification_time']
        access_time = file_metadata['access_time']
        permissions = file_metadata['permissions']
        sha256_hash = file_metadata['sha256']
        md5_hash = file_metadata['md5']

        # Check for suspicious file extensions
        if is_suspicious_extension(file_path):
            anomalies.append(f"Suspicious file extension: {file_path}")

        # Check for large files (example threshold: 100 MB)
        if size > 100 * 1024 * 1024:  # 100 MB
            anomalies.append(f"Large file detected: {file_path} (Size: {size / (1024 * 1024)} MB)")

        # Check for recently modified files (example threshold: last 24 hours)
        if is_recent(modification_time, threshold_hours=24):
            anomalies.append(f"Recently modified file: {file_path} (Modification Time: {modification_time})")

        # Check for recently accessed files (example threshold: last 24 hours)
        if is_recent(access_time, threshold_hours=24):
            anomalies.append(f"Recently accessed file: {file_path} (Access Time: {access_time})")

        # Verify file integrity using hashes (example: comparing current hash to a stored baseline)
        # Assuming you have a baseline file with stored hashes for comparison
        if not verify_file_integrity(file_path, sha256_hash, md5_hash):
            anomalies.append(f"File integrity check failed: {file_path}")

    if not anomalies:
        return "No anomalies detected in file system data."
    else:
        return "File system analysis found the following anomalies:\n" + "\n".join(anomalies)

def is_suspicious_extension(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower() in suspicious_extensions

def is_recent(timestamp, threshold_hours):
    import time
    current_time = time.time()
    return (current_time - timestamp) <= threshold_hours * 3600

def verify_file_integrity(file_path, stored_sha256, stored_md5):
    current_sha256 = hash_file(file_path, 'sha256')
    current_md5 = hash_file(file_path, 'md5')
    return current_sha256 == stored_sha256 and current_md5 == stored_md5

def hash_file(file_path, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    try:
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                hash_func.update(byte_block)
        return hash_func.hexdigest()
    except Exception as e:
        print(f"Error hashing file {file_path}: {e}")
        return None
