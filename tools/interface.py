from tools.supported import SupportedResources


class Interface:
    def __init__(self):
        self.supported = SupportedResources()

    def _display_menu(self, items):
        for idx, item in enumerate(items, start=1):
            print(f"{idx}. {item}")

    def _get_user_choice(self, items):
        self._display_menu(items)
        choice_idx = int(input("Enter the number: ")) - 1
        return items[choice_idx]
    
    def _get_num_qubits(self):
        return int(input(f"Enter the number of Qubits: "))
    
    def _get_num_shots(self):
        return int(input(f"Enter the number of Shots: "))
        

    def get_user_inputs(self):
        print(
            """
        -----Welcome to the Quantum Simulator Benchmark toolkit-----
        In this tool, we aim to simplify benchmarking quantum simulators
        using benchmark algorithms. Follow the prompts to continue.
        Happy benchmarking :).
        """
        )

        platforms = list(self.supported._supported.keys())
        platform = self._get_user_choice(platforms)

        providers = list(self.supported._supported[platform])
        provider = self._get_user_choice(providers)

        backends = list(self.supported._supported[platform][provider])
        backend = self._get_user_choice(backends)

        algorithms = list(self.supported.algorithms)
        algorithm = self._get_user_choice(algorithms)
        
        benchmarks = list(self.supported.benchmarks)
        benchmark = self._get_user_choice(benchmarks)
        
        num_qubits = self._get_num_qubits()
        num_shots = self._get_num_shots()

        return platform, provider, backend, algorithm, benchmark, num_qubits, num_shots
