from qiskit import transpile
from mqt import ddsim

from pprint import pprint

from pathlib import Path
import sys
sys.path.append(str(Path().resolve() / 'Qiskit'))

from interface import parser
from deutsch_jozsa import dj_oracle, dj_algorithm

args, additional_args = parser.parse_known_args()

if __name__ == '__main__':
    
    provider = ddsim.DDSIMProvider()
    backend = provider.get_backend('qasm_simulator')
    
    print("Available Backends: ")
    pprint(provider.backends())
        
    oracle_gate = dj_oracle(args.deutsch_jozsa_case, args.num_qubits)
    circuit = dj_algorithm(oracle_gate, args.num_qubits)
    
    transpiled_circuit = transpile(circuit, backend)
    
    backend.run(transpiled_circuit)