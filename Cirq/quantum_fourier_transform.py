from cirq import LineQubit, CZ, Circuit, measure, Simulator, inverse, H, SWAP, X

from tools.provider import get_backend
from tools.interface import args

from random import getrandbits
from math import pi


def main():
    """
    Executes the Quantum Fourier transform algorithm using the specified
    number of qubits and shots.
    """
    qubits = LineQubit.range(args.num_qubits)
    circuit = qft_algorithm(qubits)
    backend = get_backend(args.provider, args.backend)
    backend.run(
        circuit, repetitions=args.num_shots
    )  # [ ]: Is it essential to return the results of not?!


def bin_to_qstate(qubits: list[LineQubit]) -> Circuit:
    """
    Converts a binary string to a quantum state.

    Args:
        qubits (list[LineQubit]): The list of qubits to apply the X gate to.

    Returns:
        Circuit: The quantum circuit representing the binary number as
        a quantum state.
    """
    input_layer = Circuit()
    n = len(qubits)
    random_string = f"{getrandbits(n):=0{n}b}"

    for idx, bit in enumerate(random_string):
        if bit == "1":
            input_layer.append(X(qubits[idx]))

    return input_layer


def qft(qubits: list[LineQubit]) -> Circuit:
    """
    Applies the Quantum Fourier Transform (QFT) to the given list of qubits.

    Args:
        qubits: A list of LineQubit objects representing the qubits to apply
        the QFT to.

    Returns:
        Circuit: A Circuit object representing the QFT circuit.
    """
    qft_qc = Circuit()
    num_qubits = len(qubits)

    for target in range(num_qubits - 1, -1, -1):
        qft_qc.append(H(qubits[target]))

        for control in range(target - 1, -1, -1):
            r = target - control + 1
            gate = CZ(qubits[control], qubits[target]) ** (2 * pi / 2**r)
            qft_qc.append(gate)

    for idx in range(num_qubits // 2):
        qft_qc.append(SWAP(qubits[idx], qubits[num_qubits - idx - 1]))

    return qft_qc


def qft_algorithm(qubits: list[LineQubit]) -> Circuit:
    """
    Applies the Quantum Fourier Transform (QFT) algorithm on the given qubits.

    Args:
        qubits (list[LineQubit]): The qubits to apply the QFT algorithm on.

    Returns:
        Circuit: The circuit representing the QFT algorithm.

    """
    algorithm = bin_to_qstate(qubits)
    qft_qc = qft(qubits)
    algorithm.append(qft_qc)
    algorithm.append(inverse(qft_qc))
    algorithm.append([measure(*qubits, key="result")])
    return algorithm


if __name__ == "__main__":
    main()
