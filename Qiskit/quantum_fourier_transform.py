from qiskit import QuantumCircuit, transpile

from tools.provider import get_backend
from tools.interface import args

import random
import numpy as np


def main():
    """
    Run the quantum Fourier transform algorithm.
    """
    circuit = qft_algorithm(args.num_qubits)
    backend = get_backend(args.provider, args.backend)
    transpiled_circuit = transpile(circuit, backend)
    backend.run(transpiled_circuit, shots=args.num_shots).result().get_counts()


def qft(n: int) -> QuantumCircuit:
    """
    Applies the Quantum Fourier Transform (QFT) on an n-qubit quantum circuit.

    Args:
        n (int): The number of qubits in the circuit.

    Returns:
        QuantumCircuit: The quantum circuit after applying the QFT.
    """
    qc = QuantumCircuit(n, n)
    for target in range(n - 1, -1, -1):
        qc.h(target)

        for control in range(target - 1, -1, -1):
            r = target - control + 1
            qc.cp(2 * np.pi / 2**r, control, target)

    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)

    return qc


def bin_to_qstate(n: int) -> QuantumCircuit:
    """
    Converts a binary number to a quantum state.

    Args:
        n (int): The number of qubits.

    Returns:
        QuantumCircuit: The quantum circuit representing the binary number as
        a quantum state.
    """
    qc = QuantumCircuit(n, n)
    random_string = f"{random.getrandbits(n):=0{n}b}"
    print(random_string)
    for idx, bit in enumerate(reversed(random_string)):
        if bit == "1":
            qc.x(idx)

    return qc


def qft_algorithm(n: int) -> QuantumCircuit:
    """
    Applies the Quantum Fourier Transform (QFT) algorithm on an n-qubit
    quantum circuit.

    Args:
        n (int): The number of qubits in the circuit.

    Returns:
        QuantumCircuit: The quantum circuit after applying the QFT algorithm.
    """
    qc = bin_to_qstate(n)
    qc_qft = qft(n)
    qc.compose(qc_qft, inplace=True)
    qc.compose(qc_qft.inverse(), inplace=True)
    qc.measure(range(n), range(n))
    return qc


if __name__ == "__main__":
    main()
