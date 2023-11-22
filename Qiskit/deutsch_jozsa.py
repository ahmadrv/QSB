from qiskit import QuantumCircuit, transpile

from tools.provider import get_backend
from tools.interface import args

import numpy as np


def main():
    """
    Main function that executes the Deutsch-Jozsa algorithm.
    """
    oracle = deutsch_jozsa_oracle(args.num_qubits)
    circuit = deutsch_jozsa_algorithm(oracle)
    backend = get_backend(args.provider, args.backend)
    transpiled_circuit = transpile(circuit, backend)
    backend.run(transpiled_circuit, shots=args.num_shots).result()


def deutsch_jozsa_oracle(num_qubits: int) -> QuantumCircuit:
    """
    Create a random Deutsch-Jozsa oracle.
    """
    qc = QuantumCircuit(num_qubits + 1)
    if np.random.randint(0, 2):
        qc.x(num_qubits)
    if np.random.randint(0, 2):
        return qc

    on_states = np.random.choice(
        range(2**num_qubits),
        2**num_qubits // 2,
        replace=False,
    )

    def add_cx(qc, bit_string):
        for qubit, bit in enumerate(reversed(bit_string)):
            if bit == "1":
                qc.x(qubit)
        return qc

    for state in on_states:
        qc.barrier()
        qc = add_cx(qc, f"{state:0b}")
        qc.mct(list(range(num_qubits)), num_qubits)
        qc = add_cx(qc, f"{state:0b}")

    qc.barrier()

    return qc


def deutsch_jozsa_algorithm(oracle: QuantumCircuit) -> QuantumCircuit:
    """
    Implements the Deutsch-Jozsa algorithm.

    Args:
        oracle (QuantumCircuit): The oracle circuit representing
        the function f(x).
        n (int): The number of qubits used in the algorithm.

    Returns:
        QuantumCircuit: The final quantum circuit after applying
        the Deutsch-Jozsa algorithm.
    """
    n = oracle.num_qubits - 1
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    qc.compose(oracle, inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc


if __name__ == "__main__":
    main()
