import os
import stat
import hashlib
import json


def get_file_metadata(file_path):
    try:
        file_stats = os.stat(file_path)
        metadata = {
            'file_path': file_path,
            'size': file_stats.st_size,
            'creation_time': file_stats.st_ctime,
            'modification_time': file_stats.st_mtime,
            'access_time': file_stats.st_atime,
            'permissions': stat.filemode(file_stats.st_mode),
        }
        return metadata
    except Exception as e:
        print(f"Error getting metadata for {file_path}: {e}")
        return None


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


def save_baseline_hashes(directory, output_file):
    all_files_metadata = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            metadata = get_file_metadata(file_path)
            if metadata:
                metadata['sha256'] = hash_file(file_path, 'sha256')
                metadata['md5'] = hash_file(file_path, 'md5')
                all_files_metadata.append(metadata)
    with open(output_file, 'w') as outfile:
        json.dump(all_files_metadata, outfile, indent=4)


def load_baseline_hashes(baseline_file):
    try:
        with open(baseline_file, 'r') as infile:
            return json.load(infile)
    except Exception as e:
        print(f"Error loading baseline hashes: {e}")
        return []


def log_changes(change_log, change_type, file_path, details):
    with open(change_log, 'a') as log_file:
        log_entry = {
            'change_type': change_type,
            'file_path': file_path,
            'details': details
        }
        log_file.write(json.dumps(log_entry) + '\n')


def check_integrity(directory, baseline_file, change_log):
    baseline_hashes = load_baseline_hashes(baseline_file)
    baseline_hash_dict = {file['file_path']: file for file in baseline_hashes}

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            current_metadata = get_file_metadata(file_path)
            if current_metadata:
                current_metadata['sha256'] = hash_file(file_path, 'sha256')
                current_metadata['md5'] = hash_file(file_path, 'md5')
                if file_path in baseline_hash_dict:
                    baseline_metadata = baseline_hash_dict[file_path]
                    if (current_metadata['sha256'] != baseline_metadata['sha256'] or
                            current_metadata['md5'] != baseline_metadata['md5']):
                        log_changes(change_log, 'modified', file_path, current_metadata)
                        print(f"Integrity check failed for {file_path}: Hash mismatch")
                    elif current_metadata != baseline_metadata:
                        log_changes(change_log, 'metadata_change', file_path, current_metadata)
                        print(f"Metadata change detected for {file_path}")
                else:
                    log_changes(change_log, 'new_file', file_path, current_metadata)
                    print(f"New file detected: {file_path}")
            else:
                print(f"Could not get metadata for {file_path}")

    for baseline_path in baseline_hash_dict.keys():
        if not os.path.exists(baseline_path):
            log_changes(change_log, 'deleted', baseline_path, baseline_hash_dict[baseline_path])
            print(f"File deleted: {baseline_path}")


def main():
    target_directory = "D:\An 4 Sem 2\Licenta\Digital-forensics-Windows-\Python app"  # Replace with the directory you want to analyze
    baseline_file = "Data/baseline_hashes.json"  # File to save baseline hashes
    change_log = "Data/change_log.json"  # Log file to record changes

    save_baseline_hashes(target_directory, baseline_file)
    check_integrity(target_directory, baseline_file, change_log)


if __name__ == "__main__":
    main()
