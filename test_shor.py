from qiskit import transpile, Aer, execute
from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT, CPhaseGate
from math import gcd, ceil, log2
from fractions import Fraction


def c_amod(N, a):
    if gcd(a, N) != 1:
        raise ValueError("'a' must be coprime with 'N'")

    n_qubits = ceil(log2(N))
    U = QuantumCircuit(n_qubits)

    for i in range(n_qubits):
        U.append(CPhaseGate(a * 2**i % N), [i, (i + 1) % n_qubits])

    U = U.to_gate()
    U.name = f"{a} mod {N}"
    c_U = U.control()

    return c_U

def c_amod15(a):
    """
    Controlled multiplication by a mod 15.
    This is hard-coded for simplicity.
    """
    if a not in [2, 4, 7, 8, 11, 13]:
        raise ValueError("'a' must not have common factors with 15")
    U = QuantumCircuit(4)
    if a in [2, 13]:
        U.swap(2, 3)
        U.swap(1, 2)
        U.swap(0, 1)
    if a in [7, 8]:
        U.swap(0, 1)
        U.swap(1, 2)
        U.swap(2, 3)
    if a in [4, 11]:
        U.swap(1, 3)
        U.swap(0, 2)
    if a in [7, 11, 13]:
        for q in range(4):
            U.x(q)
    U = U.to_gate()
    U.name = f"{a} mod 15"
    c_U = U.control()
    return c_U

def phase_estimation(controlled_operation, psi_prep, precision):
    """
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

    # Prepare |ψ>
    qc.compose(psi_prep, qubits=target_register, inplace=True)

    # Do phase estimation
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

    backend = Aer.get_backend("qasm_simulator")
    transpiled_circuit = transpile(qc, backend)
    result = execute(transpiled_circuit, backend, shots=1024).result()
    counts = result.get_counts()

    # Find the most frequent result
    max_count = max(counts.values())
    most_probable_state = [
        state for state, count in counts.items() if count == max_count
    ][0]

    phase = int(most_probable_state, 2) / 2**precision
    return phase


psi_prep = QuantumCircuit(4)
psi_prep.x(0)

a = 8
N = 15

FACTOR_FOUND = False
ATTEMPT = 0
while not FACTOR_FOUND:
    ATTEMPT += 1
    print(f"\nAttempt {ATTEMPT}")

    phase = phase_estimation(c_amod15(a), psi_prep, precision=8)
    frac = Fraction(phase).limit_denominator(N)
    r = frac.denominator
    if phase != 0:
        # Guess for a factor is gcd(a^{r/2} - 1, N)
        guess = gcd(a ** (r // 2) - 1, N)
        if guess not in [1, N] and (N % guess) == 0:
            # Guess is a factor!
            print(f"Non-trivial factor found: {guess}")
            FACTOR_FOUND = True
