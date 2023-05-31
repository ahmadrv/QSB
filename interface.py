import argparse

# Create the argument parser
parser = argparse.ArgumentParser(
    description="The benchmark script that benchmarks MQTDDSIM simulator."
)

# Add named arguments
parser.add_argument(
    "--num_qubits",
    type=int,
    help="The number of qubits that the simulator will simulate.",
)
parser.add_argument(
    "--benchmark_algorithm",
    type=str,
    help="The benchmark algorithm."
    "The options are: 'Deutsch-Jozsa', 'Bernstein-Vazirani', 'Hidden Shift",
)  # [ ]: add more options

# Parse the arguments
args, additional_args = parser.parse_known_args()

# Access the named arguments
name = args.name
age = args.age

# Access the additional arguments
additional_arguments = additional_args

# Print the arguments
print("Named Arguments - Name:", name)
print("Named Arguments - Age:", age)
print("Additional Arguments:", additional_arguments)