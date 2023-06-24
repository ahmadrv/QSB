from pathlib import Path
import supported


class Command:
    def __init__(
        self,
        num_qubits: int,
        num_shots: int,
        algorithm: str,
        platform: str,
        provider: str,
        backend: str,
        benchmark_type: str,
        deutsch_jozsa_case: str,
    ) -> None:
        self.num_qubits = num_qubits
        self.num_shots = num_shots
        self.algorithm = self._check_support(algorithm, supported.algorithms)
        self.platform = self._check_support(platform, supported.platforms)
        self.benchmark_type = self._check_support(benchmark_type, supported.benchmarks)
        self.provider = self._check_support(
            provider, supported.providers[self.platform]
        )
        self.backend = self._check_support(backend, supported.backends[self.provider])

        self.path = str(Path(self.platform) / self.algorithm) + ".py"

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
            f"{self.benchmark_type}",
        ]

        if self.algorithm == "deutsch_jozsa":
            if deutsch_jozsa_case is not None:
                self.deutsch_jozsa_case = self._check_support(
                    deutsch_jozsa_case, supported.deutsch_jozsa_cases
                )
                self.output += ["--deutsch_jozsa_case", f"{self.deutsch_jozsa_case}"]
            else:
                raise ValueError(
                    "If algorithm is Deutsch-Jozsa, case must be specified!"
                )

    def _check_support(self, item, supported):
        if item not in supported:
            raise NotImplementedError(
                f"{item} is not implemented yet! Please choose from {supported}"
            )
        else:
            return item


def command_generator(
    max_num_qubits: int,
    num_shots: int,
    algorithm: str,
    platform: str,
    provider: str,
    backend: str,
    benchmark_type: str,
    deutsch_jozsa_case: str,
):
    for qnum in range(3, max_num_qubits + 1):
        yield Command(
            num_qubits=qnum,
            num_shots=num_shots,
            algorithm=algorithm,
            platform=platform,
            provider=provider,
            backend=backend,
            benchmark_type=benchmark_type,
            deutsch_jozsa_case=deutsch_jozsa_case,
        )

def general_command_generator(
    max_num_qubits: int,
    num_shots: int,
    algorithms: list,
    platforms: list,
    providers: list,
    backends: list,
    benchmark_types: list,
    deutsch_jozsa_cases: list,
):
    for qnum in range(3, max_num_qubits + 1):
        for alg in algorithms:
            for plat in platforms:
                for prov in providers[plat]:
                    for back in backends[prov]:
                        for bench in benchmark_types:
                            if alg == "deutsch_jozsa":
                                for case in deutsch_jozsa_cases:
                                    yield Command(
                                        num_qubits=qnum,
                                        num_shots=num_shots,
                                        algorithm=alg,
                                        platform=plat,
                                        provider=prov,
                                        backend=back,
                                        benchmark_type=bench,
                                        deutsch_jozsa_case=case,
                                    )
                            else:
                                yield Command(
                                    num_qubits=qnum,
                                    num_shots=num_shots,
                                    algorithm=alg,
                                    platform=plat,
                                    provider=prov,
                                    backend=back,
                                    benchmark_type=bench,
                                    deutsch_jozsa_case=None,
                                )