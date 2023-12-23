import subprocess, tracemalloc, time

def run_command(command: list[str]) -> str:
    """
    Executes a command using the subprocess module and returns the output.

    Parameters:
    - command: str
        The command to be executed.

    Returns:
    - str:
        The output of the command.

    Raises:
    - subprocess.CalledProcessError:
        If the command execution fails, this exception will be raised.
    """
    result = subprocess.run(command, capture_output=True)
    print(result)
    if result.returncode != 0:
        return result.stderr.decode()
    else:
        return result.stdout.decode()

def get_memory_usage():
    """
    Get the memory usage of the current program.

    Returns:
        int: The total memory usage in bytes.
    """
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    total_size = sum(stat.size for stat in top_stats)
    return total_size

def runtime(args):
    """
    Measures the runtime of a subprocess.

    Args:
        *args: The command to be executed by the subprocess.

    Returns:
        The runtime of the subprocess in seconds, or None if the subprocess failed.
    """
    start = time.time()
    output = run_command(args)
    end = time.time()

    return end - start, output

def memory_usage(args):         
    """
    Returns the maximum memory usage of a process in MB.

    Args:
        *args: A list of arguments to be passed to the subprocess.

    Returns:
        The maximum memory usage of the process in MB.
    """
    tracemalloc.start()
    output = run_command(args)
    memory_used = get_memory_usage() / (1024 * 1024)
    tracemalloc.stop()
    
    return memory_used, output

command = ['python', 'Qiskit/deutsch_jozsa.py', '--num_qubits', '35', '--num_shots', '1', '--provider', 'aer', '--backend', 'qasm_simulator']

time_used, output = runtime(command)
print("TIME ---- OUTPUT", time_used, output)
memory_used, output = memory_usage(command)
print("MEM ---- OUTPUT", memory_used, output)
