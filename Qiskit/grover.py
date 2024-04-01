from qiskit import QuantumCircuit, transpile, Aer

from tools.provider import get_backend
from tools.interface import args

from random import getrandbits

def main():
    """
    Executes the Bernstein-Vazirani algorithm using the specified
    number of qubits and shots.
    """
    oracle = grover_oracle(args.num_qubits)
    circuit = grover_algorithm(oracle, args.num_qubits)
    backend = get_backend(args.provider, args.backend)
    transpiled_circuit = transpile(circuit, backend)
    backend.run(
        transpiled_circuit, shots=args.num_shots
    ).result()  # [ ]: Is it essential to return the results of not?!

def grover_oracle(num_qubits: int) -> QuantumCircuit:
    oracle = QuantumCircuit(num_qubits + 1)
    secret_string = f"{getrandbits(num_qubits):=0{num_qubits}b}"
    secret_string = secret_string[::-1]
    
    oracle.x([idx for idx, bit in zip(range(num_qubits), secret_string) if bit == "0"])
    oracle.toffoli(0, 1, num_qubits)
    oracle.x([idx for idx, bit in zip(range(num_qubits), secret_string) if bit == "0"])
    
    return oracle, secret_string

def grover_algorithm(
    oracle: QuantumCircuit, num_qubits: int
) -> QuantumCircuit:
    
    algorithm = QuantumCircuit(num_qubits + 1, num_qubits)
    algorithm.x(num_qubits)
    algorithm.h(num_qubits)
    algorithm.h(range(num_qubits + 1))
    algorithm.append(oracle, range(num_qubits + 1))
    algorithm.h(range(num_qubits + 1))
    algorithm.x(range(num_qubits + 1))
    algorithm.h(1)
    algorithm.cx(0, 1)
    algorithm.h(1)
    algorithm.x(range(num_qubits + 1))
    algorithm.h(range(num_qubits + 1))
    algorithm.measure(range(num_qubits), range(num_qubits))
    
    return algorithm

def test():
    num_qubits = 5
    backend = Aer.get_backend('aer_simulator')
    oracle, secret_string = grover_oracle(num_qubits)
    circuit = grover_algorithm(oracle, num_qubits)
    shots = 1024
    transpiled_circuit = transpile(circuit, backend)
    results = backend.run(transpiled_circuit, shots=args.num_shots).result()
    answer = results.get_counts()
    print(answer, secret_string)
    
if __name__ == '__main__':
    test()