import sys, os
sys.path.append(os.getcwd())

from benchmark import benchmark
from benchmark import interface

print(benchmark.Benchmark().metrics)
print(interface.args)