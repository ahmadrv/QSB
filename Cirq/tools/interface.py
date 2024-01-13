import argparse

parser = argparse.ArgumentParser(
    description="Here is the interface of QSB for benchmark Cirq."
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
    "--provider",
    type=str,
    help="The provider that it should be 'cirq' or 'qsimcirq' .",
)

parser.add_argument(
    "--backend",
    type=str,
    help="The backend that it should be 'pure', 'QSimSimulator' or ... .",
)

parser.add_argument(
    "--oracle_type",
    type=str,
    help="The backend that it should be 'balanced', 'constant' or 'basic' .",
)

args, additional_args = parser.parse_known_args()   # This line should be the last line of this file.