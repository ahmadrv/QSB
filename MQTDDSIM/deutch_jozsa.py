from qiskit import QuantumCircuit, execute
from tools import benchmarker
from mqt import ddsim
import numpy as np
import types, time


def dj_oracle(case: str, n: int):
    """
    This function creates a Deutsch-Jozsa oracle based on the input case and
    input qubit size n. The oracle is a black box function that takes n qubits
    as input and outputs 1 qubit. The oracle is either constant or balanced.

    return: a Deutsch-Jozsa oracle as a gate
    """
    oracle_qc = QuantumCircuit(n + 1)

    if case == "balanced":
        b = np.random.randint(1, 2**n)

        b_str = format(b, "0" + str(n) + "b")

        for qubit in range(len(b_str)):
            if b_str[qubit] == "1":
                oracle_qc.x(qubit)

        for qubit in range(n):
            oracle_qc.cx(qubit, n)

        for qubit in range(len(b_str)):
            if b_str[qubit] == "1":
                oracle_qc.x(qubit)

    if case == "constant":
        output = np.random.randint(2)
        if output == 1:
            oracle_qc.x(n)

    oracle_gate = oracle_qc.to_gate()
    oracle_gate.name = "Oracle"
    return oracle_gate


def dj_algorithm(oracle: QuantumCircuit, n: int):
    """
    This function creates a Deutsch-Jozsa algorithm based on the input oracle
    and input qubit size n.
    """
    dj_circuit = QuantumCircuit(n + 1, n)
    dj_circuit.x(n)
    dj_circuit.h(n)

    for qubit in range(n):
        dj_circuit.h(qubit)

    dj_circuit.append(oracle, range(n + 1))

    for qubit in range(n):
        dj_circuit.h(qubit)

    for i in range(n):
        dj_circuit.measure(i, i)

    return dj_circuit


def circuit_builder(ID, case: str, n: int):
    oracle_gate = dj_oracle(case, n)
    dj_circuit = dj_algorithm(oracle_gate, n)

    return dj_circuit


def runtime(ID, case, num_qubits):
    ID.metrics["runtime"] = dict()

    dj_circuit = MQTDDSIM_deutch_jozsa.circuit_builder(case, num_qubits)
    backend = ddsim.DDSIMProvider().get_backend("qasm_simulator")

    start_time = time.time()
    execute(dj_circuit, backend, shots=10000)
    end_time = time.time()

    exe_time = end_time - start_time

    ID.metrics["runtime"][num_qubits] = exe_time


MQTDDSIM_deutch_jozsa = benchmarker.Benchmark("Deutch-Jozsa", "MQTDDSIM")

MQTDDSIM_deutch_jozsa.circuit_builder = types.MethodType(
    circuit_builder, MQTDDSIM_deutch_jozsa
)
MQTDDSIM_deutch_jozsa.runtime = types.MethodType(runtime, MQTDDSIM_deutch_jozsa)
