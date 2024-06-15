class SupportedResources:
    """
    A class that represents the supported resources for quantum algorithms and platforms.

    Attributes:
        _algorithms (set): A set of supported quantum algorithms.
        _supported (dict): A dictionary that maps platforms to their supported providers and backends.
        _benchmarks (set): A set of supported benchmarks.

    Methods:
        algorithms: Returns the supported quantum algorithms.
        benchmarks: Returns the supported benchmarks.
        providers(platform: str) -> list[str]: Returns the supported providers for a given platform.
        backends(platform: str, provider: str) -> list[str]: Returns the supported backends for a given platform and provider.
    """

    def __init__(self):
        self._algorithms = {
            "deutsch_jozsa",
            "bernstein_vazirani",
            "quantum_fourier_transform",
            "simon",
            "grover",
            "shor",
        }

        self._platforms = {"Qiskit", "Cirq"}

        self._supported = {
            "Qiskit": {
                "aer": {
                    "aer_simulator",
                    "qasm_simulator",
                    # "statevector_simulator",
                    # "unitary_simulator",
                    # "pulse_simulator",
                },
                "ddsim": {
                    "qasm_simulator",
                    "hybrid_qasm_simulator",
                    # "statevector_simulator",
                    # "hybrid_statevector_simulator",
                    # "path_sim_qasm_simulator",
                    # "path_sim_statevector_simulator",
                    # "unitary_simulator",
                },
            },
            "Cirq": {
                "cirq": {
                    "pure",
                    # "mixed"
                },
                "qsimcirq": {"QSimSimulator"} #, "QSimhSimulator"},
            },
        }

        self._benchmarks = {"runtime", "memory_usage"}

    @property
    def algorithms(self):
        """
        Returns the supported quantum algorithms.

        Returns:
            set: A set of supported quantum algorithms.
        """
        return self._algorithms

    @property
    def platforms(self):
        """
        Get the supported platforms for the tool.

        Returns:
            set: A set of supported platforms.
        """
        return self._platforms

    @property
    def benchmarks(self):
        """
        Returns the supported benchmarks.

        Returns:
            set: A set of supported benchmarks.
        """
        return self._benchmarks

    def providers(self, platform: str) -> list[str]:
        """
        Returns the supported providers for a given platform.

        Args:
            platform (str): The platform for which to retrieve the supported providers.

        Returns:
            list[str]: A list of supported providers for the given platform.

        Raises:
            ValueError: If an invalid platform is provided.
        """
        _platforms = self._supported.keys()
        if platform not in _platforms:
            raise ValueError(
                "Invalid platform: expected one of {}".format(list(_platforms))
            )
        return list(self._supported[platform].keys())

    def backends(self, platform: str, provider: str) -> list[str]:
        """
        Returns the supported backends for a given platform and provider.

        Args:
            platform (str): The platform for which to retrieve the supported backends.
            provider (str): The provider for which to retrieve the supported backends.

        Returns:
            list[str]: A list of supported backends for the given platform and provider.

        Raises:
            ValueError: If an invalid platform or provider is provided.
        """
        _providers = self.providers(platform)
        if provider not in _providers:
            raise ValueError(
                "Invalid provider: expected one of {}".format(list(_providers))
            )

        return list(self._supported[platform][provider])
