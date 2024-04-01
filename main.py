from tools import benchmark

def main():
    expr_rept = 5
    num_qubits = list(range(2, 30))
    num_shots = [1024]
    algorithms = [
                # "deutsch_jozsa",
                # "bernstein_vazirani",
                # "quantum_fourier_transform",
                # "simon",
                "grover"
    ]
    platforms = ["Qiskit"]
    providers = ["aer"]
    backends = ["qasm_simulator"]

    for _ in range(expr_rept):        
        benchmark.run(
            num_qubits,
            num_shots,
            algorithms,
            platforms,
            providers,
            backends
        ) 
if __name__ == "__main__":
    main()
