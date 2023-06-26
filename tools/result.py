import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import os

# [ ]: Make this module more efficient!!!


def make_csv_with_header(file_path, header):
    """
    This method makes a csv file with header.
    """

    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)
        with open(file_path, "w") as f:
            f.write(header + "\n")


def add_result_to_file(result, file_path):
    """
    This method adds the result to the file.
    """

    with open(file_path, "a") as f:
        f.write(result + "\n")

def plot_result(file_paths, benchmark):
    
    plt.figure(figsize=(20, 10))
    
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        df_mean = df.groupby("qubit", as_index=False).mean()
        
        plt.plot(df_mean["qubit"], df_mean[benchmark], label=file_path)
    
    plt.xlabel("Number of Qubit")
    plt.ylabel(benchmark)
    plt.legend()
    plt.show()

def get_all_files(directory):
    file_list = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    
    return file_list
