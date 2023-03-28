class Benchmark:    
    def __init__(self, func):
        self.func = func
        self.metrics = dict()
        
    def gate_fidelity(self, *args, **kwargs):
        '''
        
        This metric measures the accuracy of the simulator in reproducing the
        ideal gates in the quantum circuit. It can be calculated by comparing
        the output of the simulator to the expected output for a given circuit.
        '''
        pass
    
    def circuit_depth(self, *args, **kwargs):
        '''
        
        This metric measures the number of layers of gates in the quantum
        circuit. A shorter circuit depth generally implies a faster execution
        time and a lower error rate.
        '''
        pass
     
    def runtime(self, *args, **kwargs):
        
        '''
        This metric measures the time it takes for the simulator to execute
        the quantum circuit. A faster runtime generally implies
        a more efficient simulator.
        '''
        pass
    
    def memory_usage(self, *args, **kwargs):
        
        '''
        This metric measures the amount of memory used by the simulator during
        execution. As the size and complexity of the circuit increases,
        so does the memory usage.
        '''
        pass
    