import subprocess, time, psutil

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

        # Loop until the subprocess finishes
        while process.poll() is None:
            memory_info = psutil.Process(pid).memory_info()
            memory_usage = memory_info.rss

            if memory_usage > max_memory_usage:
                max_memory_usage = memory_usage

        return max_memory_usage / (1024 * 1024) # Convert to megabytes