from tools import benchmark


def main():
    expr_rept = 1
    num_qubits = list(range(2, 5))
    num_shots = [1]
    algorithms = [
                "deutsch_jozsa",
                "bernstein_vazirani",
                "quantum_fourier_transform",
                "simon"
    ]
    platforms = ["Qiskit"]
    providers = ["aer"]
    backends = ["aer_simulator"]
    
    benchmarks = ["runtime", "memory_usage"]

    for _ in range(expr_rept):
        file_name = benchmark.run(
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
