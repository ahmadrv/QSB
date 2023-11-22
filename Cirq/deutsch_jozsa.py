from cirq import GridQubit, ControlledGate, Circuit, Simulator, measure, X, H

from tools.interface import args

import numpy as np


def main():
    """
    Executes the Deutsch-Jozsa algorithm.
    """
    input_qubits = [GridQubit(i, 0) for i in range(args.num_qubits)]
    output_qubit = GridQubit(args.num_qubits, 0)
    oracle = deutsch_jozsa_oracle(input_qubits, output_qubit)
    circuit = deutsch_jozsa_algorithm(input_qubits, output_qubit, oracle)
    simulator = Simulator()
    simulator.run(circuit, repetitions=args.num_shots)


def deutsch_jozsa_oracle(input_qubits: list[GridQubit], output_qubit: GridQubit):
    """
    Implements the Deutsch-Jozsa oracle.

    Args:
        input_qubits (list[GridQubit]): List of input qubits.
        output_qubit (GridQubit): Output qubit.

    Yields:
        Gate operations to construct the Deutsch-Jozsa oracle.
    """
    if np.random.randint(0, 2):
        yield X(output_qubit)
    if np.random.randint(0, 2):
        return

    on_states = np.random.choice(
        range(2**args.num_qubits),
        2**args.num_qubits // 2,
        replace=False,
    )

    def add_cx(input_qubits, bit_string):
        for qubit, bit in zip(input_qubits, reversed(bit_string)):
            if bit == "1":
                yield X(qubit)

    mct = ControlledGate(sub_gate=X, num_controls=len(input_qubits))

    for state in on_states:
        yield add_cx(input_qubits, f"{state:0b}")
        yield mct(*input_qubits, output_qubit)
        yield add_cx(input_qubits, f"{state:0b}")


def deutsch_jozsa_algorithm(
    input_qubits: list[GridQubit], output_qubit: GridQubit, oracle
) -> Circuit:
    """
    Implements the Deutsch-Jozsa algorithm.

    Args:
        input_qubits (list[GridQubit]): The input qubits.
        output_qubit (GridQubit): The output qubit.
        oracle: The oracle function.

    Returns:
        Circuit: The quantum circuit representing the Deutsch-Jozsa algorithm.
    """
    qc = Circuit()
    qc.append([X(output_qubit), H(output_qubit), H.on_each(*input_qubits)])
    qc.append(oracle)
    qc.append([H.on_each(*input_qubits), measure(*input_qubits, key="result")])
    return qc


def bitstring(bits):
    """
    Converts a list of bits to a string representation.

    Args:
        bits (list): A list of bits.

    Returns:
        str: The string representation of the bits.
    """
    return "".join(str(int(b)) for b in bits)


if __name__ == "__main__":
    main()
