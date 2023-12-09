from qiskit import QuantumCircuit, transpile

from tools.provider import get_backend
from tools.interface import args

from random import getrandbits
from numpy import array
from galois import GF


def main():
    """
    Executes the Simon's algorithm using the specified
    number of qubits and shots.
    """
    oracle_gate = simon_oracle(args.num_qubits)
    simon_algorithm(oracle_gate, args.num_shots)


def simon_oracle(num_qubits: int) -> QuantumCircuit:
    """
    Creates a quantum circuit representing the oracle for the Simon's algorithm.

    Args:
        num_qubits (int): The number of qubits in the circuit.

    Returns:
        QuantumCircuit: The quantum circuit representing the oracle.
    """
    secret_string = f"{getrandbits(num_qubits):=0{num_qubits}b}"
    secret_string = secret_string[::-1]
    oracle = QuantumCircuit(num_qubits * 2)

    for q in range(num_qubits):
        oracle.cx(q, q + num_qubits)
    
    if "1" not in secret_string:
        return oracle

    i = secret_string.find("1")

    for q in range(num_qubits):
        if secret_string[q] == "1":
            oracle.cx(i, q + num_qubits)

    return oracle


def simon_measurements(oracle: QuantumCircuit, num_shots: int) -> list[str]:
    """
    Perform Simon's algorithm measurements on the given oracle circuit.

    Args:
        oracle (QuantumCircuit): The oracle circuit to be used in Simon's
        algorithm.

    Returns:
        list[str]: The list of measurement outcomes obtained from running 
        Simon's algorithm.
    """
    half_qubits = oracle.num_qubits // 2
    algorithm = QuantumCircuit(2 * half_qubits, half_qubits)
    algorithm.h(range(half_qubits))
    algorithm.compose(oracle, inplace=True)
    algorithm.h(range(half_qubits))
    algorithm.measure(range(half_qubits), range(half_qubits))

    backend = get_backend(args.provider, args.backend)
    transpiled_circuit = transpile(algorithm, backend)
    result = backend.run(transpiled_circuit, shots=num_shots, memory=True).result()

    return result.get_memory()


def simon_algorithm(oracle: QuantumCircuit, num_shots: int) -> str:
    """
    Implements the Simon's algorithm.

    Args:
        oracle (QuantumCircuit): The oracle circuit for the Simon's problem.

    Returns:
        str: The binary string representing the solution to the Simon's problem.
    """
    measurements = simon_measurements(oracle, num_shots)
    matrix = array([list(bitstring) for bitstring in measurements]).astype(int)
    null_space = GF(2)(matrix).null_space()

    if len(null_space) == 0:
        return "0" * len(measurements[0])
    return "".join(array(null_space[0]).astype(str))


if __name__ == "__main__":
    main()
