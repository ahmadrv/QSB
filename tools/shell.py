import supported
from command import Command

num_qubits = 5
num_shots = 1024
algorithm = supported.algorithms[0]
platform = supported.platforms[0]

if platform == "Qiskit":
    provider = supported.qiskit_providers[0]

    if provider == "aer":
        backend = supported.aer_backends[0]

benchmark = supported.benchmarks[0]

deutsch_jozsa_case = supported.deutsch_jozsa_cases[0]

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
