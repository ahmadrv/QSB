from qiskit import QuantumCircuit, execute
from mqt import ddsim
import numpy as np

import sys, os
sys.path.append(os.getcwd())

from tools import interface

parser = interface.parser

parser.add_argument(
    "--deutsch_jozsa_case",
    type=str,
    help="The Deutsch-Jozsa case that it should be 'balanced' or 'constant'.",
)

args, additional_args = parser.parse_known_args()

def dj_oracle(case: str, n: int) -> QuantumCircuit:
    """
    This function creates a Deutsch-Jozsa oracle based on the input case and
    input qubit size n. The oracle is a black box function that takes n qubits
    as input and outputs 1 qubit. The oracle is either constant or balanced.

    return: a Deutsch-Jozsa oracle as a gate
    """
    oracle_qc = QuantumCircuit(n + 1)

    if case == "balanced":
        b = np.random.randint(1, 2**n)

        b_str = format(b, "0" + str(n) + "b")

        for qubit in range(len(b_str)):
            if b_str[qubit] == "1":
                oracle_qc.x(qubit)

        for qubit in range(n):
            oracle_qc.cx(qubit, n)

        for qubit in range(len(b_str)):
            if b_str[qubit] == "1":
                oracle_qc.x(qubit)

    if case == "constant":
        output = np.random.randint(2)
        if output == 1:
            oracle_qc.x(n)

    oracle_gate = oracle_qc.to_gate()
    oracle_gate.name = "Oracle"
    return oracle_gate


def dj_algorithm(oracle: QuantumCircuit, n: int) -> QuantumCircuit:
    """
    This function creates a Deutsch-Jozsa algorithm based on the input oracle
    and input qubit size n.
    """
    dj_circuit = QuantumCircuit(n + 1, n)
    dj_circuit.x(n)
    dj_circuit.h(n)

    for qubit in range(n):
        dj_circuit.h(qubit)

    dj_circuit.append(oracle, range(n + 1))

    for qubit in range(n):
        dj_circuit.h(qubit)

    for i in range(n):
        dj_circuit.measure(i, i)

    return dj_circuit


if __name__ == '__main__':
        
    oracle_gate = dj_oracle(args.deutsch_jozsa_case, args.num_qubits)
    dj_circuit = dj_algorithm(oracle_gate, args.num_qubits)
    
    backend = ddsim.DDSIMProvider().get_backend('qasm_simulator')
    
    execute(dj_circuit, backend, shots=args.num_shots)
    
    dj_circuit.qasm(filename="deutsch_jozsa.qasm")