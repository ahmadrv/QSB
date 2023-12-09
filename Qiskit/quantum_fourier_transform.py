from qiskit import QuantumCircuit, transpile

from tools.provider import get_backend
from tools.interface import args

from random import getrandbits
from math import pi


def main():
    """
    Executes the Quantum Fourier transform algorithm using the specified
    number of qubits and shots.
    """
    circuit = qft_algorithm(args.num_qubits)
    backend = get_backend(args.provider, args.backend)
    transpiled_circuit = transpile(circuit, backend)
    backend.run(transpiled_circuit, shots=args.num_shots).result()


def bin_to_qstate(num_qubits: int) -> QuantumCircuit:
    """
    Converts a binary number to a quantum state.

    Args:
        num_qubits (int): The number of qubits in the quantum circuit.

    Returns:
        QuantumCircuit: The quantum circuit representing the binary number as
        a quantum state.
    """
    input_layer = QuantumCircuit(num_qubits, num_qubits)
    random_string = f"{getrandbits(num_qubits):=0{num_qubits}b}"

    for idx, bit in enumerate(reversed(random_string)):
        if bit == "1":
            input_layer.x(idx)

    return input_layer


def qft(num_qubits: int) -> QuantumCircuit:
    """
    Applies the Quantum Fourier Transform (QFT) on a given number of qubits.

    Args:
        num_qubits (int): The number of qubits to apply the QFT on.

    Returns:
        QuantumCircuit: The quantum circuit representing the QFT.
    """
    qft_qc = QuantumCircuit(num_qubits, num_qubits)

    for target in range(num_qubits - 1, -1, -1):
        qft_qc.h(target)

        for control in range(target - 1, -1, -1):
            r = target - control + 1
            qft_qc.cp(2 * pi / 2**r, control, target)

    for qubit in range(num_qubits // 2):
        qft_qc.swap(qubit, num_qubits - qubit - 1)

    return qft_qc


def qft_algorithm(num_qubits: int) -> QuantumCircuit:
    """
    Applies the Quantum Fourier Transform (QFT) algorithm to a given number of
    qubits.

    Args:
        num_qubits (int): The number of qubits to apply the QFT algorithm to.

    Returns:
        QuantumCircuit: The circuit representing the QFT algorithm applied to
        the given number of qubits.
    """
    algorithm = bin_to_qstate(num_qubits)
    qft_qc = qft(num_qubits)
    algorithm.compose(qft_qc, inplace=True)
    algorithm.compose(qft_qc.inverse(), inplace=True)
    algorithm.measure(range(num_qubits), range(num_qubits))
    return algorithm


if __name__ == "__main__":
    main()
