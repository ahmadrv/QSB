import sys
import os

# Add the current working directory to the sys.path list.
sys.path.append(os.getcwd())

import benchmark

print(benchmark.Benchmark().metrics)
