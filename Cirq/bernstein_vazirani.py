from cirq import GridQubit, Circuit, measure, Simulator, X, H, CNOT

from tools.interface import args

import random


def main():
    """
    Executes the Bernstein-Vazirani algorithm.

    This function generates the necessary qubits, initializes the secret bias
    and factor bits, creates the oracle and circuit, and runs the simulation.
    """
    input_qubits = [GridQubit(i, 0) for i in range(args.num_qubits)]
    output_qubit = GridQubit(args.num_qubits, 0)
    secret_bias_bit = random.randint(0, 1)
    secret_factor_bits = [random.randint(0, 1) for _ in range(args.num_qubits)]
    oracle = bernstein_vazirani_oracle(
        input_qubits, output_qubit, secret_factor_bits, secret_bias_bit
    )
    circuit = bernstein_vazirani_algorithm(input_qubits, output_qubit, oracle)
    simulator = Simulator()
    simulator.run(circuit, repetitions=args.num_shots)


def bernstein_vazirani_oracle(
    input_qubits: list[GridQubit],
    output_qubit: GridQubit,
    secret_factor_bits: list[int],
    secret_bias_bit: int,
):
    """
    Implements the oracle for the Bernstein-Vazirani algorithm.

    Args:
        input_qubits (list[GridQubit]): The input qubits.
        output_qubit (GridQubit): The output qubit.
        secret_factor_bits (list[int]): The secret factor bits.
        secret_bias_bit (int): The secret bias bit.

    Yields:
        GateOperation: The gate operations representing the oracle.
    """
    if secret_bias_bit:
        yield X(output_qubit)

    for qubit, bit in zip(input_qubits, secret_factor_bits):
        if bit:
            yield CNOT(qubit, output_qubit)


def bernstein_vazirani_algorithm(
    input_qubits: list[GridQubit], output_qubit: GridQubit, oracle
) -> Circuit:
    """
    Implements the Bernstein-Vazirani algorithm.

    Args:
        input_qubits (list[GridQubit]): The list of input qubits.
        output_qubit (GridQubit): The output qubit.
        oracle: The oracle circuit.

    Returns:
        Circuit: The Bernstein-Vazirani algorithm circuit.
    """
    qc = Circuit()
    qc.append([X(output_qubit), H(output_qubit), H.on_each(*input_qubits)])
    qc.append(oracle)
    qc.append([H.on_each(*input_qubits), measure(*input_qubits, key="result")])
    return qc


if __name__ == "__main__":
    main()
