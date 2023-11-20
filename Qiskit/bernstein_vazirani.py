from qiskit import QuantumCircuit, transpile
from tools.provider import get_backend
from tools.interface import args
import random

def bv_oracle(n: int) -> QuantumCircuit:
    
    oracle = QuantumCircuit(n + 1)
    
    s = f'{random.getrandbits(n):=0{n}b}'
    
    s = s[::-1]         # reverse s to fit qiskit's qubit ordering
    for q in range(n):
        if s[q] == '0':
            oracle.i(q)
        else:
            oracle.cx(q, n)
    
    oracle_gate = oracle.to_gate()
    oracle_gate.name = "Oracle"
    return oracle_gate

def bv_algorithm(oracle: QuantumCircuit, n: int) -> QuantumCircuit:
    """
    This function creates a Bernstein-Vazirani algorithm based on the input oracle
    and input qubit size n.
    """
    bv_circuit = QuantumCircuit(n + 1, n)
    bv_circuit.h(n)
    bv_circuit.z(n)

    for qubit in range(n):
        bv_circuit.h(qubit)

    bv_circuit.barrier()
    
    bv_circuit.append(oracle, range(n + 1))
    
    bv_circuit.barrier()

    for qubit in range(n):
        bv_circuit.h(qubit)

    for i in range(n):
        bv_circuit.measure(i, i)

    return bv_circuit

if __name__ == "__main__":
    oracle_gate = bv_oracle(args.num_qubits)
    circuit = bv_algorithm(oracle_gate, args.num_qubits)
    
    backend = get_backend(args.provider, args.backend)
    
    transpiled_circuit = transpile(circuit, backend)
    
    backend.run(transpiled_circuit, shots=args.num_shots).result()      # [x]: add result() based on https://github.com/Qiskit/qiskit-aer/issues/1210
    
    # [ ]: Print results to pass outputs to the parent on the subprocess