import subprocess, time, psutil

def runtime(cmd):
    """
    Run a command and return its runtime in seconds.
    """
    start = time.time()
    subprocess.check_call(cmd, shell=True)
    return time.time() - start

def memory_usage(cmd):
    """
    Run a command and return its maximum memory usage in kilobytes.
    """
    # Run the subprocess
    process = subprocess.Popen(cmd)

    # Get the process ID
    pid = process.pid

   # Initialize a variable to track the maximum memory usage
    max_memory_usage = 0

    # Loop until the subprocess finishes
    while process.poll() is None:
        # Get memory usage
        memory_info = psutil.Process(pid).memory_info()
        memory_usage = memory_info.rss

        # Update the maximum memory usage if necessary
        if memory_usage > max_memory_usage:
            max_memory_usage = memory_usage

    return max_memory_usage