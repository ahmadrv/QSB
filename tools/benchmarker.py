class Benchmark:
    def __init__(self, algorithm_name, simulator_name):
        self.algorithm_name = algorithm_name
        self.simulator_name = simulator_name
        self.metrics = dict()

    def describe(self):
        print(f"Algorithm: {self.algorithm_name}")
        print(f"Simulator Name: {self.simulator_name}")

    def circuit_builder(self, *args, **kwargs):
        # [ ]: Placeholder for algorithm execution logic
        pass

    def runtime(self, *args, **kwargs):
        # [ ]: Placeholder for algorithm execution logic
        pass
