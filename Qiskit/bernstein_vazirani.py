from qiskit import QuantumCircuit, transpile

from tools.provider import get_backend
from tools.interface import args

import random


def main():
    """
    Executes the Bernstein-Vazirani algorithm using the specified arguments.
    """
    oracle_gate = bernstein_vazirani_oracle(args.num_qubits)
    circuit = bernstein_vazirani_algorithm(oracle_gate, args.num_qubits)
    backend = get_backend(args.provider, args.backend)
    transpiled_circuit = transpile(circuit, backend)
    backend.run(transpiled_circuit, shots=args.num_shots).result()


def bernstein_vazirani_oracle(n: int) -> QuantumCircuit:
    """
    Creates a quantum circuit representing the Bernstein-Vazirani oracle.

    Args:
        n (int): The number of qubits in the circuit.

    Returns:
        QuantumCircuit: The quantum circuit representing the oracle.
    """
    qc = QuantumCircuit(n + 1)

    s = f"{random.getrandbits(n):=0{n}b}"

    s = s[::-1]
    for q in range(n):
        if s[q] == "0":
            qc.i(q)
        else:
            qc.cx(q, n)

    oracle_gate = qc.to_gate()
    oracle_gate.name = "Oracle"
    return oracle_gate


def bernstein_vazirani_algorithm(oracle: QuantumCircuit, n: int) -> QuantumCircuit:
    """
    Implements the Bernstein-Vazirani algorithm.

    Args:
        oracle (QuantumCircuit): The oracle circuit representing the function f(x).
        n (int): The number of qubits used to represent the input x.

    Returns:
        QuantumCircuit: The circuit implementing the Bernstein-Vazirani algorithm.
    """
    qc = QuantumCircuit(n + 1, n)
    
    qc.h(n)
    qc.z(n)

    qc.h(range(n))
    qc.append(oracle, range(n + 1))
    qc.h(range(n))

    qc.measure(range(n), range(n))

    return qc


if __name__ == "__main__":
    main()
