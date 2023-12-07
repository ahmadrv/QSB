from qiskit import QuantumCircuit, transpile

from tools.provider import get_backend
from tools.interface import args

from random import getrandbits


def main():
    """
    Executes the Bernstein-Vazirani algorithm using the specified
    number of qubits and shots.
    """
    oracle = bernstein_vazirani_oracle(args.num_qubits)
    circuit = bernstein_vazirani_algorithm(oracle, args.num_qubits)
    backend = get_backend(args.provider, args.backend)
    transpiled_circuit = transpile(circuit, backend)
    backend.run(
        transpiled_circuit, shots=args.num_shots
    ).result()  # [ ]: Is it essential to return the results of not?!


def bernstein_vazirani_oracle(num_qubits: int) -> QuantumCircuit:
    """
    Creates a quantum circuit representing the oracle for the Bernstein-Vazirani
    algorithm.

    Args:
        num_qubits (int): The number of qubits in the circuit.

    Returns:
        QuantumCircuit: The quantum circuit representing the oracle.
    """
    oracle = QuantumCircuit(num_qubits + 1)
    secret_string = f"{getrandbits(num_qubits):=0{num_qubits}b}"
    secret_string = secret_string[::-1]

    for q in range(num_qubits):
        if secret_string[q] == "1":
            oracle.cx(q, num_qubits)

    oracle = oracle.to_gate()
    return oracle


def bernstein_vazirani_algorithm(
    oracle: QuantumCircuit, num_qubits: int
) -> QuantumCircuit:
    """
    Implements the Bernstein-Vazirani algorithm.

    Args:
        oracle (QuantumCircuit): The oracle circuit representing the secret function.
        num_qubits (int): The number of qubits used in the algorithm.

    Returns:
        QuantumCircuit: The circuit implementing the Bernstein-Vazirani algorithm.
    """
    algorithm = QuantumCircuit(num_qubits + 1, num_qubits)
    algorithm.x(num_qubits)
    algorithm.h(range(num_qubits + 1))
    algorithm.append(oracle, range(num_qubits + 1))
    algorithm.h(range(num_qubits))
    algorithm.measure(range(num_qubits), range(num_qubits))
    return algorithm


if __name__ == "__main__":
    main()
