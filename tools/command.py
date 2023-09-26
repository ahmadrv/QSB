from pathlib import Path
import supported
import itertools


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
            "--provider",
            f"{self.provider}",
            "--backend",
            f"{self.backend}",
        ]

    def _check_support(self, item, supported):
        if item not in supported:
            raise NotImplementedError(
                f"{item} is not implemented yet or wrong case is selected!\
                    Please choose from {supported}"
            )
        else:
            return item


def command_generator(
    num_qubits: list[int],
    num_shots: list[int],
    algorithms: list[str],
    platforms: list[str],
    providers: list[str],
    backends: list[str],
    benchmarks: list[str],
):
    combinations_args = itertools.product(num_qubits,
                                          num_shots,
                                          algorithms,
                                          platforms,
                                          providers,
                                          backends,
                                          benchmarks)
    
    for qnum, snum, alg, plat, prov, back, bench in combinations_args:
        yield Command(
            num_qubits=qnum,
            num_shots=snum,
            algorithm=alg,
            platform=plat,
            provider=prov,
            backend=back,
            benchmark_type=bench,
        )
