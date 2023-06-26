"""
[ ]: Add supported algorithms, platforms, providers, backends and benchmarks here.
"""


algorithms = ["deutsch_jozsa", "bernstain_vazirani"]  # [ ]: Add more algorithms here

platforms = ["Qiskit"]

providers = {"Qiskit": ["aer", "ddsim"]}

backends = {
    "aer": [
        "aer_simulator",  # ##
        "aer_simulator_statevector",
        "aer_simulator_density_matrix",
        "aer_simulator_stabilizer",
        "aer_simulator_matrix_product_state",
        "aer_simulator_extended_stabilizer",
        "aer_simulator_unitary",
        "aer_simulator_superop",
        "qasm_simulator",  # ##
        "statevector_simulator",
        "unitary_simulator",
        "pulse_simulator",
    ],
    "ddsim": [
        "qasm_simulator",  ###
        "statevector_simulator",  ###
        "hybrid_qasm_simulator",
        "hybrid_statevector_simulator",
        "path_sim_qasm_simulator",
        "path_sim_statevector_simulator",
        "unitary_simulator",
    ],
}

benchmarks = ["runtime", "memory_usage"]  # runtime
