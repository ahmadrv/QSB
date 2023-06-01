from qiskit import *
from mqt import ddsim

circ = QuantumCircuit(3)
circ.h(0)
circ.cx(0, 1)
circ.cx(0, 2)

print(circ.draw(fold=-1))

backend = ddsim.DDSIMProvider().get_backend('qasm_simulator')

job = execute(circ, backend, shots=10000)
counts = job.result().get_counts(circ)
print(counts)