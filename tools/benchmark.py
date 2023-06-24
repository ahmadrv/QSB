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
    max_num_qubits,
    num_shots,
    algorithm,
    platform,
    provider,
    backend,
    benchmark_type,
    deutsch_jozsa_case=None,
):
    commands = command.command_generator(
        max_num_qubits,
        num_shots,
        algorithm,
        platform,
        provider,
        backend,
        benchmark_type,
        deutsch_jozsa_case,     # [ ]: Use decorators for every algorithm to check if case is needed
    )

    file_header = f"qubit,{benchmark_type}"
    file_name = (
        f"{platform}-{algorithm}-{provider}-{backend}-{benchmark_type}-{deutsch_jozsa_case}-"
        + time.strftime("%Y%m%d_%H%M%S")
        + ".csv"
    )

    result.make_csv_with_header("results/" + file_name, file_header)

    for cmd in commands:
        if benchmark_type == 'runtime':
            output = f"{cmd.num_qubits},{runtime(*cmd.output)}"
        elif benchmark_type == 'memory_usage':
            output = f"{cmd.num_qubits},{memory_usage(*cmd.output)}"
        result.add_result_to_file(output, "results/" + file_name)
    
    return file_name
