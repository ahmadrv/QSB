from cirq import measure, LineQubit, Circuit, Simulator, X, H, CNOT

from tools.provider import get_backend
from tools.interface import args

from random import getrandbits


def main():
    """
    Executes the Bernstein-Vazirani algorithm using the specified
    number of qubits and shots.
    """
    qubits = LineQubit.range(args.num_qubits + 1)
    oracle = bernstein_vazirani_oracle(qubits)
    circuit = bernstein_vazirani_algorithm(oracle)
    backend = get_backend(args.provider, args.backend)
    backend.run(
        circuit, repetitions=args.num_shots
    )  # [ ]: Is it essential to return the results of not?!


def bernstein_vazirani_oracle(qubits: list[LineQubit]) -> Circuit:
    """
    Constructs the oracle circuit for the Bernstein-Vazirani algorithm.

    Args:
        qubits (list[LineQubit]): The list of qubits to be used in the circuit.

    Returns:
        Circuit: The constructed oracle circuit.
    """
    num_qubits = len(qubits)
    oracle = Circuit()
    secret_string = f"{getrandbits(num_qubits - 1):=0{num_qubits - 1}b}"

    for qubit, bit in zip(qubits, secret_string):
        if bit == "1":
            oracle.append([CNOT(qubit, qubits[-1])])

    return oracle


def bernstein_vazirani_algorithm(qubits: list[LineQubit], oracle: Circuit) -> Circuit:
    """
    Implements the Bernstein-Vazirani algorithm.

    Args:
        qubits (list[LineQubit]): The list of qubits to be used in the algorithm.
        oracle (Circuit): The oracle circuit that encodes the secret string.

    Returns:
        Circuit: The circuit representing the Bernstein-Vazirani algorithm.
    """
    algorithm = Circuit()
    algorithm.append([X(qubits[-1]), H.on_each(*qubits)])
    algorithm.append(oracle)
    algorithm.append([H.on_each(qubits[:-1]), measure(qubits[:-1], key="result")])
    return algorithm


if __name__ == "__main__":
    main()
