from tools import benchmark

def main():
    expr_rept = 1
    num_qubits = list(range(2, 30))
    num_shots = [1]
    algorithms = [
                "deutsch_jozsa",
                # "bernstein_vazirani",
                # "quantum_fourier_transform",
                # "simon"
    ]
    platforms = ["Qiskit"]
    providers = ["aer"]
    backends = ["aer_simulator"]    # "qasm_simulator", aer_simulator
    oracle_types = ["balanced"] # "basic", "balanced", "constant"

    for _ in range(expr_rept):        
        benchmark.run(
            num_qubits,
            num_shots,
            algorithms,
            platforms,
            providers,
            backends,
            oracle_types
        ) 
if __name__ == "__main__":
    main()
