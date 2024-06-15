import subprocess, time, psutil


def mem_use(pid):
    process = psutil.Process(pid)
    memory_info = process.memory_info()
    return memory_info.rss / (1024 * 1024)


def memory_usage(command):
    mem_use_list = list()
    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as proc:
        while proc.poll() is None:
            mem_use_list.append(mem_use(proc.pid))
            time.sleep(0.1)
        if proc.poll() == 0:
            outs = proc.stdout.read1().decode("utf-8")
        else:
            outs = proc.stderr.read1().decode("utf-8")

        print(proc.args)
        proc.kill()

    return max(mem_use_list), outs


def runtime(command):
    start = time.time()
    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as proc:
        while proc.poll() is None:
            time.sleep(0.1)
        end = time.time()
        if proc.poll() == 0:
            outs = proc.stdout.read1().decode("utf-8")
        else:
            outs = proc.stderr.read1().decode("utf-8")

        print(proc.args)
        proc.kill()

    return end - start, outs


if __name__ == "__main__":
    for i in range(2, 10):
        cmd = [
            "python",
            "Qiskit/deutsch_jozsa.py",
            "--num_qubits",
            str(i),
            "--num_shots",
            "1",
            "--provider",
            "aer",
            "--backend",
            "aer_simulator",
        ]
        memory_usage(cmd)
        print("------------------------------")
        runtime(cmd)
        print()
