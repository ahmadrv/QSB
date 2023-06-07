import sys, os
sys.path.append(os.getcwd())

from benchmark import benchmark
from benchmark import interface

print(benchmark.Benchmark().metrics)
print(interface.args)

from mqt import ddsim
from qiskit import transpile, execute

# import basic plot tools
from qiskit.visualization import plot_histogram

backend = ddsim.DDSIMProvider().get_backend('qasm_simulator')

job = execute(circ, backend, shots=10000)
counts = job.result().get_counts(circ)
print(counts)
