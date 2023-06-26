import subprocess, time, psutil, command, result


def runtime(*args) -> float:
    """
    Run a command and return its runtime in seconds.
    """
    start = time.time()
    process = subprocess.Popen(args)
    process.wait()
    return time.time() - start


def memory_usage(*args) -> float:
    """
    Run a command and return its maximum memory usage in kilobytes.
    """
    with subprocess.Popen(list(args)) as process:
        pid = process.pid
        max_memory_usage = 0

        while process.poll() is None:
            memory_info = psutil.Process(pid).memory_info()
            memory_usage = memory_info.rss

            if memory_usage > max_memory_usage:
                max_memory_usage = memory_usage

        return max_memory_usage / 1048576  # Convert to megabytes


def run(
    num_qubits,
    num_shots,
    algorithm,
    platform,
    provider,
    backend,
    benchmarks,
):
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
        file_path = (
            f"results/{cmd.platform}/{cmd.provider}/{cmd.backend}/"
            f"{cmd.algorithm}/{cmd.benchmark_type}/{cmd.num_shots} shots.csv"
        )

        result.make_csv_with_header(file_path, f"qubit,{cmd.benchmark_type}")

        if cmd.benchmark_type == "runtime":
            output = f"{cmd.num_qubits},{runtime(*cmd.output)}"

        elif cmd.benchmark_type == "memory_usage":
            output = f"{cmd.num_qubits},{memory_usage(*cmd.output)}"

        result.add_result_to_file(output, file_path)
