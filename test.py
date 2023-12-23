import subprocess

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
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print(result)
    
    # if result.returncode != 0:
    #     print(f"Command failed with return code {result.returncode}")
    #     print(f"Standard output: {result.stdout.decode()}")
    #     print(f"Standard error: {result.stderr.decode()}")
    # else:
    #     print(f"Standard output: {result.stdout.decode()}")


command = ['python', 'Qiskit/deutsch_jozsa.py', '--num_qubits', '1', '--num_shots', '1', '--provider', 'aer', '--backend', 'aer_simulator']

run_command(command)