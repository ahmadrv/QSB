import sys, os
sys.path.append(os.getcwd())

from benchmark import benchmark
from benchmark import interface

from mqt import ddsim
from qiskit import execute

# import basic plot tools
from qiskit.visualization import plot_histogram

from algorithm.deutch_jozsa import dj_oracle, dj_algorithm

n = 4
oracle_gate = dj_oracle('balanced', n)
dj_circuit = dj_algorithm(oracle_gate, n)

backend = ddsim.DDSIMProvider().get_backend('qasm_simulator')

job = execute(dj_circuit, backend, shots=10000)
counts = job.result().get_counts(dj_circuit)

# [ ]: Check where should we put the benchmarking code
