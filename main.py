from tools import benchmark

def main():
    expr_rept = 5
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
    backends = ["aer_simulator", "qasm_simulator"]
    benchmarks = ["runtime", "memory_usage"]

    for _ in range(expr_rept):        
        benchmark.run(
            num_qubits,
            num_shots,
            algorithms,
            platforms,
            providers,
            backends,
            benchmarks
        ) 
if __name__ == "__main__":
    main()
