#!/bin/sh

# [ ]: Check installation of python and pip

# Set the version of python
sudo apt install python-is-python3

# Install python virtual environment package
pip install virtualenv

# Create a Python virtual environment
python -m venv QSB

# Activate the virtual environment
source QSB/bin/activate

# Welcome message
echo "This script allows you to select which platform do you want to benchmark."

# Display options
echo "Please select an option:"
echo "1. Benchmark MQTDDSIM"
echo "2. Benchmark QuEST (WIP)"
echo "3. Benchmark Intel-QS (WIP)"
echo "4. Benchmark LIQUi|〉 (WIP)"
echo "5. Benchmark Qiskit (WIP)"
echo "6. Benchmark Cirq (WIP)"

# Read user input
while true; do
    read -p "Enter option number: " option

    # Process user input
    case $option in
    1)
        echo "You selected ---Benchmark MQTDDSIM---"
        echo "Running benchmark..."
        chmod +x ./MQTDDSIM/setup/setup.sh
        ./MQTDDSIM/setup/setup.sh
        break
        ;;
    2)
        echo "You selected ---Benchmark QuEST---"
        echo "Work in progress. Please select another option."
        ;;
    3)
        echo "You selected ---Benchmark Intel-QS---"
        echo "Work in progress. Please select another option."
        ;;
    4)
        echo "You selected ---Benchmark LIQUi|〉---"
        echo "Work in progress. Please select another option."
        ;;
    5)
        echo "You selected ---Benchmark Qiskit---"
        echo "Work in progress. Please select another option."
        ;;
    6)
        echo "You selected ---Benchmark Cirq---"
        echo "Work in progress. Please select another option."
        ;;
    *)
        echo "Invalid option selected"
        ;;
    esac
done
