def get_backend(provider_name: str, simulation_type: str):
    """
    Get the backend simulator based on the provider name and simulation type.

    Args:
        provider_name (str): The name of the provider.
        simulation_type (str): The type of simulation.

    Returns:
        object: The backend simulator object.

    Raises:
        ValueError: If the provider name or simulation type is not supported.
    """
    if provider_name == "cirq":
        if simulation_type == "pure":
            from cirq import Simulator

            return Simulator()
        elif simulation_type == "mixed":
            from cirq import DensityMatrixSimulator

            return DensityMatrixSimulator()

    elif provider_name == "qsimcirq":
        if simulation_type == "QSimSimulator":
            from qsimcirq import QSimSimulator

            return QSimSimulator()
        elif simulation_type == "QSimhSimulator":
            from qsimcirq import QSimhSimulator

            return QSimhSimulator()
    
    raise ValueError("Unsupported provider name or simulation type.")
