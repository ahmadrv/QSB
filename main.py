from tools import benchmark

def main():
    expr_rept = 1
    num_qubits = list(range(27, 35))
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
    
    benchmarks = ["runtime"]

    for _ in range(expr_rept):
        
        try:
        
            benchmark.run(
                num_qubits,
                num_shots,
                algorithms,
                platforms,
                providers,
                backends,
                benchmarks
            )
        except Exception as e:
            raise e    
if __name__ == "__main__":
    main()
