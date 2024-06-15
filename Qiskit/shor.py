from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFT

from tools.provider import get_backend
from tools.interface import args

from random import getrandbits
from math import pi


def main():
    """
    Executes the Phase Estimation algorithm using the specified
    number of qubits and shots.
    """
    controlled_operation = controlled_operation_generator(args.num_qubits)
    psi_prep = psi_register_generator()
    circuit = phase_estimation_algorithm(controlled_operation, psi_prep, args.precision)
    backend = get_backend(args.provider, args.backend)
    transpiled_circuit = transpile(circuit, backend)
    backend.run(
        transpiled_circuit, shots=args.num_shots
    ).result()  # [ ]: Is it essential to return the results of not?!

def controlled_operation_generator():
    pass


def psi_register_generator():
    pass


def phase_estimation_algorithm(
    controlled_operation: QuantumCircuit, psi_prep: QuantumCircuit, precision: int
):
    """
    Ref: https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring
    Carry out phase estimation on a simulator.
    Args:
        controlled_operation: The operation to perform phase estimation on,
                              controlled by one qubit.
        psi_prep: Circuit to prepare |ψ>
        precision: Number of counting qubits to use
    Returns:
        float: Best guess for phase of U|ψ>
    """
    control_register = QuantumRegister(precision)
    output_register = ClassicalRegister(precision)

    target_register = QuantumRegister(psi_prep.num_qubits)
    qc = QuantumCircuit(control_register, target_register, output_register)

    qc.compose(psi_prep, qubits=target_register, inplace=True)

    for index, qubit in enumerate(control_register):
        qc.h(qubit)
        for _ in range(2**index):
            qc.compose(
                controlled_operation,
                qubits=[qubit] + list(target_register),
                inplace=True,
            )

    qc.compose(QFT(precision, inverse=True), qubits=control_register, inplace=True)

    qc.measure(control_register, output_register)
    
    return qc
