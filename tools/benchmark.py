import subprocess, time

def runtime(cmd):
    """
    Run a command and return its runtime in seconds.
    """
    start = time.time()
    subprocess.check_call(cmd, shell=True)
    return time.time() - start