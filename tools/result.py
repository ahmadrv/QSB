import matplotlib.pyplot as plt
from matplotlib import rcParams
import plotly.graph_objects as go
from pathlib import Path
import pandas as pd
import os

rcParams["font.family"] = "serif"
rcParams["font.style"] = "normal"
rcParams["text.usetex"] = True


def make_csv_with_header(file_path, header):
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)
        with open(file_path, "w") as f:
            f.write(header + "\n")


def add_result_to_file(result, file_path):
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


def plot_result_plotly(file_paths, benchmark):
    fig = go.Figure()

    for idx, file_path in enumerate(file_paths):
        df = pd.read_csv(file_path)
        df_mean = df.groupby("qubit").mean().reset_index()

        fig.add_trace(
            go.Scatter3d(
                x=df_mean["qubit"],
                y=[idx] * len(df_mean),
                z=df_mean[benchmark],
                mode="lines",
                name=file_path,
            )
        )

    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Number of qubits"),
            yaxis=dict(title="Simulators"),
            zaxis=dict(title=benchmark),
        ),
        showlegend=False,  # legend=dict(title="File Paths"),
        width=800,
        height=600,
    )

    fig.show()


def get_all_files(directory):
    file_list = []

    for root, ـ, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))

    return file_list
