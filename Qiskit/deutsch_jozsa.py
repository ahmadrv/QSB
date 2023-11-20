from qiskit import QuantumCircuit, transpile
from tools.provider import get_backend
from tools.interface import args
import numpy as np
import random

def generate_balanced_binary(n):
    binary_number = ['0', '1'] * (n // 2)
    if n % 2 != 0:
        binary_number.append(str(random.choice([0, 1])))
    random.shuffle(binary_number)
    return ''.join(binary_number)

def dj_oracle(n: int) -> QuantumCircuit:
    """
    This function creates a Deutsch-Jozsa oracle based on the input case and
    input qubit size n. The oracle is a black box function that takes n qubits
    as input and outputs 1 qubit. The oracle is either constant or balanced.

    return: a Deutsch-Jozsa oracle as a gate
    """
    oracle_qc = QuantumCircuit(n + 1)

    cases = ["constant", "balanced"]

    case = random.choice(cases)

    if case == "balanced":
        b_str = generate_balanced_binary(n)
        
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


if __name__ == "__main__":
    oracle_gate = dj_oracle(args.num_qubits)
    circuit = dj_algorithm(oracle_gate, args.num_qubits)

    backend = get_backend(args.provider, args.backend)

    transpiled_circuit = transpile(circuit, backend)

    backend.run(transpiled_circuit, shots=args.num_shots).result()      # [x]: add result() based on https://github.com/Qiskit/qiskit-aer/issues/1210
    
    # [ ]: Print results to pass outputs to the parent on the subprocess
