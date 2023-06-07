import numpy as np
from qiskit import QuantumCircuit

def dj_oracle(case, n):
    '''
    This function creates a Deutsch-Jozsa oracle based on the input case and
    input qubit size n. The oracle is a black box function that takes n qubits
    as input and outputs 1 qubit. The oracle is either constant or balanced.
    
    return: a Deutsch-Jozsa oracle as a gate
    '''
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

def dj_algorithm(oracle, n):
    
    '''
    This function creates a Deutsch-Jozsa algorithm based on the input oracle
    and input qubit size n.
    '''
    dj_circuit = QuantumCircuit(n+1, n)
    dj_circuit.x(n)
    dj_circuit.h(n)
    
    for qubit in range(n):
        dj_circuit.h(qubit)
        
    dj_circuit.append(oracle, range(n+1))
    
    for qubit in range(n):
        dj_circuit.h(qubit)
    
    for i in range(n):
        dj_circuit.measure(i, i)
    
    return dj_circuit