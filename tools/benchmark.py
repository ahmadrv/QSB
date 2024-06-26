import subprocess, time, psutil
from datetime import datetime
from tools import command, database


def mem_use(pid):
    process = psutil.Process(pid)
    memory_info = process.memory_info()
    return memory_info.rss / (1024 * 1024)

def check_available_mem():
    return psutil.virtual_memory().available / 1024 ** 2


def measure(command):      
    mem_use_list = list()
    start = time.time()
    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as proc:
        while proc.poll() is None:
            mem_use_list.append(mem_use(proc.pid))
            time.sleep(0.1)
            
            if check_available_mem() - 100 <= mem_use_list[-1]:
                end = time.time()
                print(proc.args)
                proc.kill()
                return end - start, 'OutofMem', 'MemoryError'
        end = time.time() 
        if proc.poll() == 0:
            outs = proc.stdout.read1().decode("utf-8")
        else:
            outs = proc.stderr.read1().decode("utf-8")

        outs = None if outs == "" else outs
        
        print(proc.args)
        proc.kill()

    return end - start, max(mem_use_list), outs


def run(
    num_qubits: list[int],
    num_shots: list[int],
    algorithm: list[str],
    platform: list[str],
    provider: list[str],
    backend: list[str]
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
        backend
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
            cmd.num_shots
        )

        
        bench_time, memory_used, output = measure(cmd.output)
        benchmark += (bench_time, memory_used, output, datetime.now())


        benchmark_id = database.create_benchmark(conn, benchmark)
        print(benchmark_id)


if __name__ == "__main__":
    pass
