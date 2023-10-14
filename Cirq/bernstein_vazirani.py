import random, time
import cirq


def main(qubit_count=8):
    circuit_sample_count = 3

    # Choose qubits to use.
    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    output_qubit = cirq.GridQubit(qubit_count, 0)

    # Pick coefficients for the oracle and create a circuit to query it.
    secret_bias_bit = random.randint(0, 1)
    secret_factor_bits = [random.randint(0, 1) for _ in range(qubit_count)]
    oracle = make_oracle(input_qubits, output_qubit, secret_factor_bits, secret_bias_bit)
      
    start_time = time.time()

    # Embed the oracle into a special quantum circuit querying it exactly once.
    circuit = make_bernstein_vazirani_circuit(input_qubits, output_qubit, oracle)
    
    # Sample from the circuit a couple times.
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)
    frequencies = result.histogram(key='result', fold_func=bitstring)
    
    end_time = time.time()
    
    # Check if we actually found the secret value.
    most_common_bitstring = frequencies.most_common(1)[0][0]
    
    print(f'Time(s) :{end_time - start_time}, #Q: {qubit_count}, Check: {most_common_bitstring == bitstring(secret_factor_bits)}')
  

def make_oracle(input_qubits, output_qubit, secret_factor_bits, secret_bias_bit):
    """Gates implementing the function f(a) = a·factors + bias (mod 2)."""

    if secret_bias_bit:
        yield cirq.X(output_qubit)

    for qubit, bit in zip(input_qubits, secret_factor_bits):
        if bit:  # pragma: no cover
            yield cirq.CNOT(qubit, output_qubit)


def make_bernstein_vazirani_circuit(input_qubits, output_qubit, oracle):
    """Solves for factors in f(a) = a·factors + bias (mod 2) with one query."""

    c = cirq.Circuit()

    # Initialize qubits.
    c.append([cirq.X(output_qubit), cirq.H(output_qubit), cirq.H.on_each(*input_qubits)])

    # Query oracle.
    c.append(oracle)

    # Measure in X basis.
    c.append([cirq.H.on_each(*input_qubits), cirq.measure(*input_qubits, key='result')])

    return c


def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)


if __name__ == '__main__':
    for i in range(2, 100):
        main(i)