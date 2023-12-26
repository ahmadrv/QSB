import subprocess, time, tracemalloc
from datetime import datetime
from tools import command, database


def run_command(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True)
    print(result)
    if result.returncode != 0:
        return result.stderr.decode()
    else:
        return result.stdout.decode()


def runtime(args):
    start = time.time()
    output = run_command(args)
    end = time.time()

    output = None if output == "" else output

    return end - start, output


def memory_usage(args):
    tracemalloc.start()
    output = run_command(args)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output = None if output == "" else output
    return peak / 1024, output


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

        if cmd.benchmark_type == "runtime":
            bench_time, output = runtime(cmd.output)
            benchmark += (bench_time, output, datetime.now())

        elif cmd.benchmark_type == "memory_usage":
            memory_used, output = memory_usage(cmd.output)
            benchmark += (memory_used, output, datetime.now())

        benchmark_id = database.create_benchmark(conn, benchmark)
        print(benchmark_id)


if __name__ == "__main__":
    pass
