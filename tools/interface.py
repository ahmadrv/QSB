from supported import SupportedResources


class Interface:
    def __init__(self):
        self.supported = SupportedResources()

    def display_menu(self, items):
        for idx, item in enumerate(items, start=1):
            print(f"{idx}. {item}")

    def get_user_choice(self, items):
        self.display_menu(items)
        choice_idx = int(input("Enter the number: ")) - 1
        return items[choice_idx]

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
        platform = self.get_user_choice(platforms)

        providers = list(self.supported._supported[platform])
        provider = self.get_user_choice(providers)

        backends = list(self.supported._supported[platform][provider])
        backend = self.get_user_choice(backends)

        return platform, provider, backend
