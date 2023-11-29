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

args, additional_args = parser.parse_known_args()   # This line should be the last line of this file.