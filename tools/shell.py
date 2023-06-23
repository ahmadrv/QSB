import supported
from command import Command

num_qubits = 40
num_shots = 1024
algorithm = supported.algorithms[0]

if algorithm == "deutsch_jozsa":
    deutsch_jozsa_case = supported.deutsch_jozsa_cases[0]

platform = supported.platforms[0]

if platform == "Qiskit":
    provider = supported.qiskit_providers[0]

    if provider == "aer":
        backend = supported.aer_backends[0]

benchmark = supported.benchmarks[0]

command = Command(
    num_qubits=num_qubits,
    num_shots=num_shots,
    algorithm=algorithm,
    platform=platform,
    provider=provider,
    backend=backend,
    benchmark=benchmark,
    deutsch_jozsa_case=deutsch_jozsa_case,
)


def command_generator():
    for qnum in range(3, num_qubits + 1):
        yield Command(
            num_qubits=qnum,
            num_shots=num_shots,
            algorithm=algorithm,
            platform=platform,
            provider=provider,
            backend=backend,
            benchmark=benchmark,
            deutsch_jozsa_case=deutsch_jozsa_case,
        )
