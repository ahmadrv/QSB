def get_backend(provider_name, backend_name):
    '''
    Get the backend from the provider.
    '''
    if provider_name == "aer":
        from qiskit import Aer

        return Aer.get_backend(backend_name)
    
    elif provider_name == "ddsim":
        from mqt import ddsim

        return ddsim.DDSIMProvider().get_backend(backend_name)
