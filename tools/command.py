from pathlib import Path
from tools.supported import SupportedResources
import itertools


class Command:
    """
    A class representing a command to be executed.

    Attributes:
    -----------
    num_qubits : int
        The number of qubits to be used in the algorithm.
    num_shots : int
        The number of times the circuit is run to get the measurement statistics.
    algorithm : str
        The name of the algorithm to be executed.
    platform : str
        The name of the platform to be used for the execution.
    provider : str
        The name of the provider to be used for the execution.
    backend : str
        The name of the backend to be used for the execution.
    benchmark_type : str
        The type of benchmark to be executed.

    Methods:
    --------
    _check_support(item: str, supported: list[str]) -> str
        A private method to check if the given item is supported or not.

    """

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
        self.supported = SupportedResources()
        
        self.num_qubits = num_qubits
        self.num_shots = num_shots
        self.algorithm = self._check_support(algorithm, self.supported.algorithms)
        self.platform = self._check_support(platform, self.supported.platforms)
        self.benchmark_type = self._check_support(
            benchmark_type, self.supported.benchmarks
        )
        self.provider = self._check_support(
            provider, self.supported.providers(self.platform)
        )
        self.backend = self._check_support(
            backend, self.supported.backends(self.platform, self.provider)
        )

        self.path = str(Path(self.platform) / self.algorithm) + ".py"

        self.output = [
            "./qsb/bin/python",
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

    def _check_support(self, item: str, supported: list[str]) -> str:
        """
        A private method to check if the given item is supported or not.

        Parameters:
        -----------
        item : str
            The item to be checked for support.
        supported : list[str]
            A list of supported items.

        Returns:
        --------
        str
            The item if it is supported.

        Raises:
        -------
        NotImplementedError
            If the item is not supported.
        """
        if item not in supported:
            raise NotImplementedError(
                f"{item} is not implemented yet or wrong case is selected! "
                + f"Please choose from {supported}"
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
    """
    Generate a command object for each combination of input parameters.

    Args:
        num_qubits (list[int]): List of integers representing the number of qubits.
        num_shots (list[int]): List of integers representing the number of shots.
        algorithms (list[str]): List of strings representing the algorithm names.
        platforms (list[str]): List of strings representing the platform names.
        providers (list[str]): List of strings representing the provider names.
        backends (list[str]): List of strings representing the backend names.
        benchmarks (list[str]): List of strings representing the benchmark types.

    Yields:
        Command: A command object with the given input parameters.
    """
    combinations_args = itertools.product(
        num_qubits, num_shots, algorithms, platforms, providers, backends, benchmarks
    )

    for qnum, snum, alg, plat, prov, back, bench in combinations_args:
        try:
            yield Command(
                num_qubits=qnum,
                num_shots=snum,
                algorithm=alg,
                platform=plat,
                provider=prov,
                backend=back,
                benchmark_type=bench,
            )
        except NotImplementedError as NIE:
            print(NIE)
        except Exception as e:
            print(e)
