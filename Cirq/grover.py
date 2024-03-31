"""Grover algorithm

This implementation is adopted from:

https://github.com/quantumlib/Cirq/blob/main/examples/grover.py

"""

from random import getrandbits
from cirq import measure, LineQubit, Circuit, Simulator, X, H, TOFFOLI
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
    
# def set_io_qubits(qubit_count):
#     """Add the specified number of input and output qubits."""
#     input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
#     output_qubit = cirq.GridQubit(qubit_count, 0)
#     return (input_qubits, output_qubit)


def grover_oracle(qubits: list[LineQubit]) -> Circuit:
    """Implement function {f(x) = 1 if x==x', f(x) = 0 if x!= x'}."""
    
    num_qubits = len(qubits)
    oracle = Circuit()
    secret_string = f"{getrandbits(num_qubits - 1):=0{num_qubits - 1}b}"
    
    oracle.append([X(qubit) for qubit, bit in zip(qubits, secret_string) if bit == "0"])
    oracle.append([TOFFOLI(qubits[0], qubits[1], qubits[-1])])
    oracle.append([X(qubit) for qubit, bit in zip(qubits, secret_string) if bit == "0"])
    
    return oracle


def grover_algorithm(qubits: list[LineQubit], oracle: Circuit) -> Circuit:
    """Find the value recognized by the oracle in sqrt(N) attempts."""
    # For 2 input qubits, that means using Grover operator only once.
    algorithm = Circuit()

    # Initialize qubits.
    algorithm.append([X(qubits[-1]), H(qubits[-1]), H.on_each(qubits[:-1])])

    # Query oracle.
    c.append(oracle)

    # Construct Grover operator.
    c.append(cirq.H.on_each(*input_qubits))
    c.append(cirq.X.on_each(*input_qubits))
    c.append(cirq.H.on(input_qubits[1]))
    c.append(cirq.CNOT(input_qubits[0], input_qubits[1]))
    c.append(cirq.H.on(input_qubits[1]))
    c.append(cirq.X.on_each(*input_qubits))
    c.append(cirq.H.on_each(*input_qubits))

    # Measure the result.
    c.append(cirq.measure(*input_qubits, key='result'))

    return c


def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)


def main():
    qubit_count = 2
    circuit_sample_count = 10

    # Set up input and output qubits.
    (input_qubits, output_qubit) = set_io_qubits(qubit_count)

    # Choose the x' and make an oracle which can recognize it.
    x_bits = [random.randint(0, 1) for _ in range(qubit_count)]
    print(f'Secret bit sequence: {x_bits}')

    # Make oracle (black box)
    oracle = make_oracle(input_qubits, output_qubit, x_bits)

    # Embed the oracle into a quantum circuit implementing Grover's algorithm.
    circuit = make_grover_circuit(input_qubits, output_qubit, oracle)
    print('Circuit:')
    print(circuit)

    # Sample from the circuit a couple times.
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)

    frequencies = result.histogram(key='result', fold_func=bitstring)
    print(f'Sampled results:\n{frequencies}')

    # Check if we actually found the secret value.
    most_common_bitstring = frequencies.most_common(1)[0][0]
    print(f'Most common bitstring: {most_common_bitstring}')
    print(f'Found a match: {most_common_bitstring == bitstring(x_bits)}')


if __name__ == '__main__':
    main()