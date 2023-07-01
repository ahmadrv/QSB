import matplotlib.pyplot as plt
from matplotlib import rcParams
from pathlib import Path
import pandas as pd
import os

rcParams['font.family'] = 'serif'
rcParams['font.style'] = 'normal'
rcParams['text.usetex'] = True

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
    fig = plt.figure(figsize=(30, 20))
    ax = fig.add_subplot(111, projection="3d")

    for idx, file_path in enumerate(file_paths):
        df = pd.read_csv(file_path)
        df_mean = df.groupby("qubit", as_index=False).mean()

        ax.plot(df_mean["qubit"], df_mean[benchmark], zs=idx, zdir="y", label=file_path)

    ax.set_xlabel("Number of qubit")
    ax.set_ylabel("Simulators")
    ax.set_zlabel(benchmark)
    ax.legend()
    plt.show()


def get_all_files(directory):
    file_list = []

    for root, ـ, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))

    return file_list
