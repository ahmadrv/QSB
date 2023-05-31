#!/bin/sh

# Install required packages
sudo apt-get update -y
pip install mqt.ddsim

# Run benchmark
python ./MQTDDSIM/run_benchmarks.py