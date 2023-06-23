algorithms = ["deutsch_jozsa"]

platforms = ["Qiskit"]

qiskit_providers = ["aer", "ddsim"]

aer_backends = [
    "aer_simulator",
    "aer_simulator_statevector",
    "aer_simulator_density_matrix",
    "aer_simulator_stabilizer",
    "aer_simulator_matrix_product_state",
    "aer_simulator_extended_stabilizer",
    "aer_simulator_unitary",
    "aer_simulator_superop",
    "qasm_simulator",
    "statevector_simulator",
    "unitary_simulator",
    "pulse_simulator",
]

ddsim_backends = [
    "qasm_simulator",
    "statevector_simulator",
    "hybrid_qasm_simulator",
    "hybrid_statevector_simulator",
    "path_sim_qasm_simulator",
    "path_sim_statevector_simulator",
    "unitary_simulator",
]

benchmarks = ["runtime", "memory_usage"]

deutsch_jozsa_cases = ["balanced", "constant"]
