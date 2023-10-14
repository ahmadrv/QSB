"""
This module contains information about the supported algorithms, platforms, providers, backends, and benchmarks.

Attributes:
    algorithms (list): A list of supported algorithms.
    platforms (list): A list of supported platforms.
    providers (dict): A dictionary of supported providers and their corresponding backends.
    backends (dict): A dictionary of supported backends and their corresponding simulators.
    benchmarks (list): A list of supported benchmarks.
"""

algorithms = ["deutsch_jozsa", "bernstein_vazirani"]

platforms = ["Qiskit"]

providers = {"Qiskit": ["aer", "ddsim"]}

backends = {                           # [ ]: The correspond algorithm for commented backends should be implemented
    "aer": [
        "aer_simulator",
        "qasm_simulator",
        # "statevector_simulator",
        # "unitary_simulator",
        # "pulse_simulator",
    ],
    "ddsim": [
        "qasm_simulator",
        # "statevector_simulator",
        "hybrid_qasm_simulator",
        #"hybrid_statevector_simulator",
        # "path_sim_qasm_simulator",
        # "path_sim_statevector_simulator",
        # "unitary_simulator",
    ],
}

benchmarks = ["runtime", "memory_usage"]
