import argparse


parser = argparse.ArgumentParser(
    description="Here is the interface of QSB. In this script, common ar\
    guments are defined."
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