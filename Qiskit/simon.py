from qiskit import QuantumCircuit, transpile

from tools.provider import get_backend
from tools.interface import args

import numpy as np
import galois
import random


def main():
    """
    This is the main function that executes the Simon's algorithm.
    It creates an oracle gate using the simon_oracle function and then runs
    the Simon's algorithm using the oracle gate.
    """
    oracle_gate = simon_oracle(args.num_qubits)
    simon_algorithm(oracle_gate)

def simon_oracle(n: int) -> QuantumCircuit:
    """
    Creates a Simon oracle circuit.

    Args:
        n (int): The number of qubits.

    Returns:
        QuantumCircuit: The Simon oracle circuit.
    """
    secret_string = f"{random.getrandbits(n):=0{n}b}"
    qc = QuantumCircuit(2*n)
    permuts = np.random.permutation(2**n)
    query_gate = np.zeros((4**n, 4**n))
    for x in range(2**n):
        for y in range(2**n):
            z = y ^ permuts[min(x, x ^ int(secret_string, 2))]
            query_gate[x + 2**n * z, x + 2**n * y] = 1

    qc.unitary(query_gate, range(2*n))
    qc.name = "Oracle"
    return qc


def simon_measurements(oracle: QuantumCircuit) -> QuantumCircuit:
    """
    Perform Simon's algorithm measurements on the given problem circuit.

    Args:
        oracle (QuantumCircuit): The problem circuit to be used in Simon's algorithm.

    Returns:
        QuantumCircuit: The circuit with Simon's algorithm measurements applied.
    """
    n = oracle.num_qubits // 2
    qc = QuantumCircuit(2 * n, n)
    qc.h(range(n))
    qc.compose(oracle, inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))

    backend = get_backend(args.provider, args.backend)
    transpiled_circuit = transpile(qc, backend)
    result = backend.run(
        transpiled_circuit, shots=args.num_shots, memory=True
    ).result()

    return result.get_memory()


def simon_algorithm(oracle: QuantumCircuit):
    """
    Implements the Simon's algorithm to solve the given problem.

    Args:
        oracle (QuantumCircuit): The quantum circuit representing the problem.

    Returns:
        str: The solution to the problem.
    """
    measurements = simon_measurements(oracle)
    matrix = np.array([list(bitstring) for bitstring in measurements]).astype(int)
    null_space = galois.GF(2)(matrix).null_space()

    if len(null_space) == 0:
        return "0" * len(measurements[0])
    return "".join(np.array(null_space[0]).astype(str))

if __name__ == "__main__":
    main()
