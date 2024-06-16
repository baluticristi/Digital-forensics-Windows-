import ctypes
import sys
import os
import subprocess


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    if not is_admin():
        # Re-run the program with admin rights
        params = " ".join([f'"{param}"' for param in sys.argv])
        print(f"Requesting elevation with parameters: {params}")  # Debug information
        script = os.path.abspath(sys.argv[0])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}"', None, 1)
        sys.exit()


def create_full_memory_dump(dumpit_path, dump_file_path):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(dump_file_path), exist_ok=True)

        # Run DumpIt to create a full memory dump
        result = subprocess.run([dumpit_path], capture_output=True, text=True)

        # Check if DumpIt ran successfully
        if result.returncode == 0:
            print(f"Full memory dump created successfully at {dump_file_path}.")
        else:
            print(f"Failed to create memory dump. Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error creating memory dump: {e}")
        return False
    return True


def main():
    run_as_admin()  # Ensure the script is running with admin rights
    print("Running as admin.")
    dumpit_path = "C:\\Path\\To\\DumpIt.exe"  # Path to DumpIt executable
    dump_file_path = "C:\\Path\\To\\Output\\full_memory_dump.raw"  # Path to save the memory dump

    if create_full_memory_dump(dumpit_path, dump_file_path):
        print("Memory dump created successfully.")
    else:
        print("Failed to create memory dump.")


if __name__ == "__main__":
    main()
