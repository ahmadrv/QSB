from cirq import LineQubit, CZ, Circuit, measure, Simulator, inverse, H, SWAP, X

from tools.interface import args

import numpy as np
from random import getrandbits


def main():
    qubits = LineQubit.range(args.num_qubits)
    print(qft_algorithm(qubits))


def bin_to_qstate(qubits):
    qc = Circuit()
    n = len(qubits)
    random_string = f"{getrandbits(n):=0{n}b}"
    for idx, bit in enumerate(random_string):
        if bit == "1":
            qc.append(X(qubits[idx]))

    return qc


def qft(qubits):
    qc = Circuit()

    n = len(qubits)

    for target in range(n - 1, -1, -1):
        qc.append(H(qubits[target]))

        for control in range(target - 1, -1, -1):
            r = target - control + 1
            gate = CZ(qubits[control], qubits[target]) ** (2 * np.pi / 2**r)
            qc.append(gate)

    for idx in range(n // 2):
        qc.append(SWAP(qubits[idx], qubits[n - idx - 1]))

    return qc


def qft_algorithm(qubits):
    qc = bin_to_qstate(qubits)
    qc_qft = qft(qubits)
    qc.append(qc_qft)
    qc.append(inverse(qc_qft))
    qc.append([measure(*qubits, key="result")])

    simulator = Simulator()
    return [simulator.run(qc).measurements["result"][0] for _ in range(args.num_qubit)]


if __name__ == "__main__":
    main()
