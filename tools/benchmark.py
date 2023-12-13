import subprocess, time, psutil
from datetime import datetime
from tools import command, database


def runtime(*args) -> float:
    """
    Measures the runtime of a subprocess.

    Args:
        *args: The command to be executed by the subprocess.

    Returns:
        The runtime of the subprocess in seconds, or None if the subprocess failed.
    """
    start = time.time()
    try:
        process = subprocess.Popen(args)
        process.wait()
    except Exception as e:
        print(f"Runtime measurement failed: {e}")
        return None

    return time.time() - start


def memory_usage(*args) -> float:
    """
    Returns the maximum memory usage of a process in MB.

    Args:
        *args: A list of arguments to be passed to the subprocess.

    Returns:
        The maximum memory usage of the process in MB.
    """
    with subprocess.Popen(list(args)) as process:
        pid = process.pid
        max_memory_usage = 0

        while process.poll() is None:
            memory_info = psutil.Process(pid).memory_info()
            memory_usage = memory_info.rss

            if memory_usage > max_memory_usage:
                max_memory_usage = memory_usage

        return max_memory_usage / 1048576


def run(
    num_qubits: list[int],
    num_shots: list[int],
    algorithm: list[str],
    platform: list[str],
    provider: list[str],
    backend: list[str],
    benchmarks: list[str],
):
    """
    Runs benchmarks for quantum algorithms on different platforms and providers.

    Args:
        num_qubits (list[int]): List of number of qubits to run the benchmarks on.
        num_shots (list[int]): List of number of shots to run the benchmarks for.
        algorithm (list[str]): List of quantum algorithms to run the benchmarks for.
        platform (list[str]): List of platforms to run the benchmarks on.
        provider (list[str]): List of providers to run the benchmarks on.
        backend (list[str]): List of backends to run the benchmarks on.
        benchmarks (list[str]): List of benchmarks to run.

    Returns:
        None
    """

    commands = command.command_generator(
        num_qubits,
        num_shots,
        algorithm,
        platform,
        provider,
        backend,
        benchmarks,
    )

    for cmd in commands:
        
        conn = database.create_connection()
        database.initialization(conn)
        
        benchmark = (
            cmd.platform,
            cmd.provider,
            cmd.backend,
            cmd.algorithm,
            cmd.num_qubits,
            cmd.num_shots,
            cmd.benchmark_type,
        )

        try:
            if cmd.benchmark_type == "runtime":
                benchmark += (runtime(*cmd.output), datetime.now())

            elif cmd.benchmark_type == "memory_usage":
                benchmark += (memory_usage(*cmd.output), datetime.now())

            benchmark_id = database.create_benchmark(conn, benchmark)
        except Exception as e:
            print(f"ERROR: {e}")
            break
        
        print(benchmark_id)
