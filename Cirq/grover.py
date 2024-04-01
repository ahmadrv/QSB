"""Grover algorithm

This implementation is adopted from:

https://github.com/quantumlib/Cirq/blob/main/examples/grover.py

"""

from random import getrandbits
from cirq import measure, LineQubit, Circuit, X, H, TOFFOLI, CNOT
from tools.provider import get_backend
from tools.interface import args

def main():
    
    qubits = LineQubit.range(args.num_qubits + 1)
    oracle = grover_oracle(qubits)
    circuit = grover_algorithm(qubits, oracle)
    backend = get_backend(args.provider, args.backend)
    backend.run(
        circuit, repetitions=args.num_shots
    )  # [ ]: Is it essential to return the results of not?!


def grover_oracle(qubits: list[LineQubit]) -> Circuit:    
    num_qubits = len(qubits)
    oracle = Circuit()
    secret_string = f"{getrandbits(num_qubits - 1):=0{num_qubits - 1}b}"
    
    oracle.append([X(qubit) for qubit, bit in zip(qubits, secret_string) if bit == "0"])
    oracle.append([TOFFOLI(qubits[0], qubits[1], qubits[-1])])
    oracle.append([X(qubit) for qubit, bit in zip(qubits, secret_string) if bit == "0"])
    
    return oracle


def grover_algorithm(qubits: list[LineQubit], oracle: Circuit) -> Circuit:
    algorithm = Circuit()
    algorithm.append([X(qubits[-1]), H(qubits[-1]), H.on_each(qubits[:-1])])
    algorithm.append(oracle)
    algorithm.append([H.on_each(qubits[:-1]), X.on_each(qubits[:-1])])
    algorithm.append(H.on(qubits[1]))
    algorithm.append(CNOT(qubits[0], qubits[1]))
    algorithm.append(H.on(qubits[1]))
    algorithm.append(X.on_each(qubits[:-1]))
    algorithm.append(H.on_each(qubits[:-1]))
    algorithm.append(measure(qubits[:-1], key='result'))

    return algorithm

def test():
    from cirq import Simulator
    num_qubits = 5
    circuit_sample_count = 10
    
    qubits = LineQubit.range(num_qubits + 1)

    # Make oracle (black box)
    oracle, secret_string = grover_oracle(qubits)

    # Embed the oracle into a quantum circuit implementing Grover's algorithm.
    circuit = grover_algorithm(qubits, oracle)
    print('Circuit:')
    print(circuit)

    # Sample from the circuit a couple times.
    simulator = Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)
    
    def bitstring(bits):
        return ''.join(str(int(b)) for b in bits)

    frequencies = result.histogram(key='result', fold_func=bitstring)
    print(f'Sampled results:\n{frequencies}')

    # Check if we actually found the secret value.
    most_common_bitstring = frequencies.most_common(1)[0][0]
    print(f'Most common bitstring: {most_common_bitstring}')
    print(f'Found a match: {most_common_bitstring == bitstring(secret_string)}')

if __name__ == '__main__':
    main()