from cirq import LineQubit, MatrixGate, Circuit, measure, Simulator, H

from tools.interface import args

import numpy as np
import galois
import random


def main():
    """
    Executes the Simon's algorithm.
    """
    qubits = LineQubit.range(2 * args.num_qubits)
    oracle = simon_oracle(qubits)
    simon_algorithm(qubits, oracle)


def simon_oracle(qubits):
    """
    Implements the Simon's algorithm oracle.

    Args:
        qubits (List[cirq.Qid]): The qubits to apply the oracle on.

    Returns:
        cirq.MatrixGate: The matrix gate representing the oracle operation.
    """
    n = args.num_qubits
    secret_string = f"{random.getrandbits(n):0{n}b}"
    print(secret_string)
    permuts = np.random.permutation(2**n)
    query_op = np.zeros((4**n, 4**n))
    for x in range(2**n):
        for y in range(2**n):
            z = y ^ permuts[min(x, x ^ int(secret_string, 2))]
            query_op[x + 2**n * z, x + 2**n * y] = 1

    return MatrixGate(query_op).on(*qubits[n:], *qubits[:n])


def simon_measurements(qubits, oracle):
    """
    Perform Simon's algorithm measurements on the given qubits using the
    specified oracle.

    Args:
        qubits (List[cirq.Qid]): The qubits to perform measurements on.
        oracle (cirq.Gate): The oracle gate to apply.

    Returns:
        List[int]: The measurement results.

    """
    n = args.num_qubits
    qc = Circuit()
    qc.append([H.on_each(*qubits[:n])])
    qc.append(oracle)
    qc.append([H.on_each(*qubits[:n])])
    qc.append([measure(*qubits[:n], key="result")])

    simulator = Simulator()
    return [
        simulator.run(qc).measurements["result"][0] for _ in range(args.num_shots)
    ]


def simon_algorithm(qubits, oracle):
    """
    Implements the Simon's algorithm.

    Args:
        qubits (list): List of qubits to be used in the algorithm.
        oracle (callable): Oracle function that encodes the secret string.

    Returns:
        str: The secret string obtained from the algorithm.
    """
    measurements = simon_measurements(qubits, oracle)
    matrix = np.array(measurements).astype(int)
    null_space = galois.GF(2)(matrix).null_space()

    if len(null_space) == 0:
        return "0" * len(measurements[0])
    return "".join(np.array(null_space[0]).astype(str))


if __name__ == "__main__":
    main()
