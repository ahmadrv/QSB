import argparse

parser = argparse.ArgumentParser(
    description="Here is the interface of QSB for benchmark Qiskit."
)

parser.add_argument(
    "--num_qubits",
    type=int,
    help="The number of qubits that the simulator will simulate.",
)

parser.add_argument(
    "--num_shots",
    type=int,
    help="The number of shots that the simulator will simulate.",
)

parser.add_argument(
    "--algorithm",
    type=str,
    help="The algorithm that it should be 'deutsch_jozsa', 'grover' or ... .",
    # [ ]: Add other algorithms.
)

parser.add_argument(
    "--provider",
    type=str,
    help="The provider that it should be 'qiskit_aer' or 'qiskit_ddsim' .",
    # [ ]: Add other providers.
)

parser.add_argument(
    "--backend",
    type=str,
    help="The backend that it should be 'qasm_simulator', 'statevector_simulator' or ... .",
    # [ ]: Add other backends.
)

parser.add_argument(
    "--benchmark",
    type=str,
    help="The benchmark type that it should be 'runtime', 'memory_usage' or ... .",
    # [ ]: Add other benchmarks.
)

args, additional_args = parser.parse_known_args()


if args.algorithm == "deutsch_jozsa":
    
    parser.add_argument(
    "--deutsch_jozsa_case",
    type=str,
    help="The Deutsch-Jozsa case that it should be 'balanced' or 'constant'.",
    )
    
    args, additional_args = parser.parse_known_args()

elif args.algorithm == "grover":
    pass
