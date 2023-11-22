from qiskit import QuantumCircuit, transpile

from tools.provider import get_backend
from tools.interface import args

import numpy as np
import random


def main():
    """
    Main function that executes the Deutsch-Jozsa algorithm.
    """
    oracle_gate = deutsch_jozsa_oracle(args.num_qubits)
    circuit = deutsch_jozsa_algorithm(oracle_gate, args.num_qubits)
    backend = get_backend(args.provider, args.backend)
    transpiled_circuit = transpile(circuit, backend)
    backend.run(transpiled_circuit, shots=args.num_shots).result()


def generate_balanced_binary(n: int) -> str:
    """
    Generates a balanced binary string of length n.

    Args:
        n (int): The length of the binary string.

    Returns:
        str: The generated balanced binary string.
    """
    binary_number = ["0", "1"] * (n // 2)
    if n % 2 != 0:
        binary_number.append(str(random.choice([0, 1])))
    random.shuffle(binary_number)
    return "".join(binary_number)


def deutsch_jozsa_oracle(n: int) -> QuantumCircuit:
    """
    Creates a Deutsch-Jozsa oracle circuit.

    Args:
        n (int): The number of input qubits.

    Returns:
        QuantumCircuit: The Deutsch-Jozsa oracle circuit.
    """
    qc = QuantumCircuit(n + 1)
    cases = ["constant", "balanced"]
    case = random.choice(cases)

    if case == "balanced":
        b_str = generate_balanced_binary(n)
        for qubit in range(len(b_str)):
            if b_str[qubit] == "1":
                qc.x(qubit)
        for qubit in range(n):
            qc.cx(qubit, n)
        for qubit in range(len(b_str)):
            if b_str[qubit] == "1":
                qc.x(qubit)

    if case == "constant":
        output = np.random.randint(2)
        if output == 1:
            qc.x(n)

    oracle_gate = qc.to_gate()
    oracle_gate.name = "Oracle"
    return oracle_gate


def deutsch_jozsa_algorithm(oracle: QuantumCircuit, n: int) -> QuantumCircuit:
    """
    Implements the Deutsch-Jozsa algorithm.

    Args:
        oracle (QuantumCircuit): The oracle circuit representing the function f(x).
        n (int): The number of qubits used in the algorithm.

    Returns:
        QuantumCircuit: The final quantum circuit after applying the Deutsch-Jozsa algorithm.
    """
    qc = QuantumCircuit(n + 1, n)
    
    qc.x(n)
    qc.h(n)

    qc.h(range(n))
    qc.append(oracle, range(n + 1))
    qc.h(range(n))

    qc.measure(range(n), range(n))

    return qc


if __name__ == "__main__":
    main()
