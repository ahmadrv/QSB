from pathlib import Path


class Command:
    def __init__(
        self,
        num_qubits: int,
        num_shots: int,
        algorithm: str,
        platform: str,
        provider: str,
        backend: str,
        benchmark: str,
        deutsch_jozsa_case: str,
    ) -> None:
        self.num_qubits = num_qubits
        self.num_shots = num_shots
        self.algorithm = algorithm
        self.platform = platform
        self.benchmark = benchmark

        self.path = str(Path(self.platform) / self.algorithm) + ".py"

        if self.platform == "Qiskit":
            self.provider = provider
            self.backend = backend
        else:
            raise NotImplementedError

        self.output = [
            "python",
            f"{self.path}",
            "--num_qubits",
            f"{self.num_qubits}",
            "--num_shots",
            f"{self.num_shots}",
            "--algorithm",
            f"{self.algorithm}",
            "--platform",
            f"{self.platform}",
            "--provider",
            f"{self.provider}",
            "--backend",
            f"{self.backend}",
            "--benchmark",
            f"{self.benchmark}",
        ]

        if self.algorithm == "deutsch_jozsa":
            self.deutsch_jozsa_case = deutsch_jozsa_case

            self.output += ["--deutsch_jozsa_case", f"{self.deutsch_jozsa_case}"]
