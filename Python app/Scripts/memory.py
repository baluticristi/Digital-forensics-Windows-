import ctypes
import ctypes.wintypes as wintypes
import os
import json
import volatility3.framework.interfaces.plugins as plugins
from volatility3.framework import contexts
from volatility3.framework import interfaces
from volatility3.framework.configuration import requirements
from volatility3.framework.renderers import TreeGrid
from volatility3.plugins.windows import pslist, netscan, dlllist


# Define necessary structures and constants
class MINIDUMP_EXCEPTION_INFORMATION(ctypes.Structure):
    _fields_ = [("ThreadId", wintypes.DWORD),
                ("ExceptionPointers", wintypes.LPVOID),
                ("ClientPointers", wintypes.BOOL)]


MiniDumpWithFullMemory = 0x00000002
MiniDumpWithDataSegs = 0x00000001
MiniDumpWithHandleData = 0x00000004
MiniDumpWithFullMemoryInfo = 0x00000800
MiniDumpWithThreadInfo = 0x00001000
MiniDumpWithUnloadedModules = 0x00002000


def create_memory_dump(pid, dump_file_path):
    # Load necessary libraries
    kernel32 = ctypes.windll.kernel32
    dbghelp = ctypes.windll.dbghelp

    # Open the process
    process_handle = kernel32.OpenProcess(0x1F0FFF, False, pid)
    if not process_handle:
        print(f"Failed to open process {pid}.")
        return False

    # Create the dump file
    dump_file_handle = kernel32.CreateFileW(dump_file_path, wintypes.GENERIC_WRITE, 0, None, wintypes.CREATE_ALWAYS, 0,
                                            None)
    if dump_file_handle == wintypes.INVALID_HANDLE_VALUE:
        print(f"Failed to create dump file {dump_file_path}.")
        kernel32.CloseHandle(process_handle)
        return False

    # Write the dump
    success = dbghelp.MiniDumpWriteDump(
        process_handle,
        pid,
        dump_file_handle,
        MiniDumpWithFullMemory | MiniDumpWithDataSegs | MiniDumpWithHandleData | MiniDumpWithFullMemoryInfo | MiniDumpWithThreadInfo | MiniDumpWithUnloadedModules,
        None,
        None,
        None
    )

    # Close handles
    kernel32.CloseHandle(dump_file_handle)
    kernel32.CloseHandle(process_handle)

    if not success:
        print(f"Failed to write dump for process {pid}.")
        return False

    print(f"Memory dump created successfully at {dump_file_path}.")
    return True


def get_volatility_context(memory_file):
    context = contexts.Context()
    config_path = "plugins.windows.pslist.PsList"
    layer_name = context.layers.load_layer(memory_file)
    symbol_table = "windows"
    context.symbol_space.append(symbol_table)
    return context, config_path, layer_name


def list_processes(context, config_path, layer_name):
    processes = []
    plugin = pslist.PsList(context, config_path, layer_name)
    for process in plugin.run():
        processes.append({
            'pid': process.UniqueProcessId,
            'name': process.ImageFileName
        })
    return processes


def list_network_connections(context, config_path, layer_name):
    connections = []
    plugin = netscan.NetScan(context, config_path, layer_name)
    for conn in plugin.run():
        connections.append({
            'protocol': conn.Proto,
            'local_address': f"{conn.LocalIp}:{conn.LocalPort}",
            'remote_address': f"{conn.RemoteIp}:{conn.RemotePort}",
            'state': conn.State
        })
    return connections


def list_loaded_dlls(context, config_path, layer_name):
    dlls = []
    plugin = dlllist.DllList(context, config_path, layer_name)
    for task in plugin.run():
        for dll in task:
            dlls.append({
                'pid': task.UniqueProcessId,
                'process': task.ImageFileName,
                'dll_path': dll.FullDllName
            })
    return dlls


def save_report(report, output_file):
    with open(output_file, 'w') as outfile:
        json.dump(report, outfile, indent=4)


def main():
    pid = 7112  # Replace with the PID of the process you want to dump
    dump_file_path = "Data/process_memory.dmp"
    output_file = "Data/memory_analysis_report.json"

    if create_memory_dump(pid, dump_file_path):
        print("Memory dump created successfully.")

        context, config_path, layer_name = get_volatility_context(dump_file_path)
        report = {}
        report['processes'] = list_processes(context, config_path, layer_name)
        report['network_connections'] = list_network_connections(context, config_path, layer_name)
        report['loaded_dlls'] = list_loaded_dlls(context, config_path, layer_name)

        save_report(report, output_file)
        print(f"Memory analysis report saved to {output_file}")
    else:
        print("Failed to create memory dump.")


if __name__ == "__main__":
    main()
