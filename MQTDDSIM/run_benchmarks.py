import sys
import os

# Add the current working directory to the sys.path list.
sys.path.append(os.getcwd())

import benchmark
import interface

print(benchmark.Benchmark().metrics)
print(interface.args)