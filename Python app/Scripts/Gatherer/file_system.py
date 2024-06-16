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


def save_file_system_data(directory, output_file):
    all_files_metadata = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            metadata = get_file_metadata(file_path)
            if metadata:
                metadata['sha256'] = hash_file(file_path, 'sha256')
                metadata['md5'] = hash_file(file_path, 'md5')
                all_files_metadata.append(metadata)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as outfile:
        json.dump(all_files_metadata, outfile, indent=4)
