from cirq import LineQubit, Circuit, measure, H, CNOT

from tools.provider import get_backend
from tools.interface import args

from random import getrandbits
from numpy import array
from galois import GF


def main():
    """
    Executes the Simon's algorithm using the specified
    number of qubits and shots.
    """
    qubits = LineQubit.range(args.num_qubits * 2)
    oracle = simon_oracle(qubits)
    simon_algorithm(qubits, oracle, args.num_shots)


def simon_oracle(qubits: list[LineQubit]) -> Circuit:
    """
    Implements the Simon oracle for the Simon's algorithm.

    Args:
        qubits (list[LineQubit]): The list of qubits to apply the oracle on.

    Returns:
        Circuit: The circuit representing the Simon oracle.
    """
    half_qubits = len(qubits) // 2
    secret_string = f"{getrandbits(half_qubits):0{half_qubits}b}"
    oracle = Circuit()

    for q in range(half_qubits):
        oracle.append(CNOT(qubits[q], qubits[q + half_qubits]))

    if "1" not in secret_string:
        return oracle

    i = secret_string.find("1")

    for q in range(half_qubits):
        if secret_string[q] == "1":
            oracle.append(CNOT(qubits[i], qubits[q + half_qubits]))

    return oracle


def simon_measurements(
    qubits: list[LineQubit], oracle: Circuit, num_shots: int
) -> list[str]:
    """
    Perform Simon's algorithm measurements.

    Args:
        qubits (list[LineQubit]): The list of qubits to be used in the algorithm.
        oracle (Circuit): The oracle circuit for Simon's algorithm.
        num_shots (int): The number of measurement shots to perform.

    Returns:
        list[str]: The measurement results.

    """
    half_qubits = len(qubits) // 2
    algorithm = Circuit()
    algorithm.append([H.on_each(qubits[:half_qubits])])
    algorithm.append(oracle)
    algorithm.append([H.on_each(qubits[:half_qubits])])
    algorithm.append([measure(qubits[:half_qubits], key="result")])

    backend = get_backend(args.provider, args.backend)
    return [backend.run(algorithm).measurements["result"][0] for _ in range(num_shots)]


def simon_algorithm(qubits: list[LineQubit], oracle: Circuit, num_shots: int) -> str:
    """
    Runs the Simon's algorithm on the given qubits using the specified oracle circuit.

    Args:
        qubits (list[LineQubit]): The qubits to run the algorithm on.
        oracle (Circuit): The oracle circuit to be used in the algorithm.
        num_shots (int): The number of times to run the algorithm.

    Returns:
        str: The result of the algorithm as a binary string.
    """
    measurements = simon_measurements(qubits, oracle, num_shots)
    matrix = array(measurements).astype(int)
    null_space = GF(2)(matrix).null_space()

    if len(null_space) == 0:
        return "0" * len(measurements[0])
    return "".join(array(null_space[0]).astype(str))


if __name__ == "__main__":
    main()
