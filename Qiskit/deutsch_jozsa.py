from qiskit import QuantumCircuit, transpile

from tools.provider import get_backend
from tools.interface import args

from random import sample, randint


def main():
    """
    Executes the Deutsch-Jozsa algorithm using the specified
    number of qubits and shots.
    """
    oracle = deutsch_jozsa_oracle(args.num_qubits)
    circuit = deutsch_jozsa_algorithm(oracle)
    backend = get_backend(args.provider, args.backend)
    transpiled_circuit = transpile(circuit, backend)
    backend.run(transpiled_circuit, shots=args.num_shots).result()


def deutsch_jozsa_oracle(num_qubits: int) -> QuantumCircuit:
    """
    Creates a quantum circuit representing the oracle for the Deutsch-Jozsa
    algorithm.

    Args:
        num_qubits (int): The number of qubits in the circuit.

    Returns:
        QuantumCircuit: The quantum circuit representing the oracle.
    """
    oracle = QuantumCircuit(num_qubits + 1)

    if randint(0, 1):
        oracle.x(num_qubits)

    if randint(0, 1):
        return oracle

    on_states = sample(range(2**num_qubits), 2**num_qubits // 2)

    def add_cx(circuit, bit_string):
        for qubit, bit in enumerate(reversed(bit_string)):
            if bit == "1":
                circuit.x(qubit)
        return circuit

    for state in on_states:
        oracle = add_cx(oracle, f"{state:0b}")
        oracle.mcx(list(range(num_qubits)), num_qubits)
        oracle = add_cx(oracle, f"{state:0b}")

    return oracle


def deutsch_jozsa_algorithm(oracle: QuantumCircuit) -> QuantumCircuit:
    """
    Implements the Deutsch-Jozsa algorithm.

    Args:
        oracle (QuantumCircuit): The oracle circuit representing the function
        to be evaluated.

    Returns:
        QuantumCircuit: The circuit implementing the Deutsch-Jozsa algorithm.
    """
    num_qubits = oracle.num_qubits - 1
    algorithm = QuantumCircuit(num_qubits + 1, num_qubits)
    algorithm.x(num_qubits)
    algorithm.h(range(num_qubits + 1))
    algorithm.compose(oracle, inplace=True)
    algorithm.h(range(num_qubits))
    algorithm.measure(range(num_qubits), range(num_qubits))
    return algorithm


if __name__ == "__main__":
    main()
