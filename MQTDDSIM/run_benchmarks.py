import sys
import os
sys.path.append(os.getcwd())


import benchmark
print(benchmark.Benchmark().metrics)