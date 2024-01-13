from cirq import LineQubit, ControlledGate, Circuit, Simulator, measure, X, H

from tools.provider import get_backend
from tools.interface import args

from random import sample, randint


def main():
    """
    Executes the Deutsch-Jozsa algorithm using the specified
    number of qubits and shots.
    """
    qubits = LineQubit.range(args.num_qubits + 1)
    oracle = deutsch_jozsa_oracle(qubits)
    circuit = deutsch_jozsa_algorithm(qubits, oracle)
    backend = get_backend(args.provider, args.backend)
    backend.run(
        circuit, repetitions=args.num_shots
    )  # [ ]: Is it essential to return the results of not?!


def deutsch_jozsa_oracle(qubits: list[LineQubit]):
    """
    Constructs the oracle circuit for the Deutsch-Jozsa algorithm.

    Args:
        qubits (list[LineQubit]): The list of qubits to be used in the circuit.

    Returns:
        Circuit: The constructed oracle circuit.
    """
    num_qubits = len(qubits) - 1
    oracle = Circuit()

    if args.oracle_type == 'constant':
        if randint(0, 1):
            oracle.append(X(qubits[-2]))
        return oracle

    elif args.oracle_type == 'balanced':
        on_states = sample(range(2 ** (num_qubits)), 2 ** (num_qubits) // 2)

        def add_cx(qubits, bit_string):
            circuit = Circuit()
            for qubit, bit in zip(qubits[:-1], bit_string):
                if bit == "1":
                    circuit.append(X(qubit))
            return circuit

        mct = ControlledGate(sub_gate=X, num_controls=num_qubits)

        for state in on_states:
            oracle.append(add_cx(qubits, f"{state:0b}"))
            oracle.append(mct(*qubits))
            oracle.append(add_cx(qubits, f"{state:0b}"))

        return oracle


def deutsch_jozsa_algorithm(qubits: list[LineQubit], oracle: Circuit) -> Circuit:
    """
    Implements the Deutsch-Jozsa algorithm.

    Args:
        qubits (list[LineQubit]): The list of qubits to be used in the algorithm.
        oracle (Circuit): The oracle circuit representing the function to be evaluated.

    Returns:
        Circuit: The circuit implementing the Deutsch-Jozsa algorithm.
    """
    algorithm = Circuit()
    algorithm.append([X(qubits[-1]), H.on_each(*qubits)])
    algorithm.append(oracle)
    algorithm.append([H.on_each(qubits[:-1]), measure(qubits[:-1], key="result")])
    return algorithm


if __name__ == "__main__":
    main()
