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
    "--deutsch_jozsa_case",
    type=str,
    help="The Deutsch-Jozsa case that it should be 'balanced' or 'constant'.",
)