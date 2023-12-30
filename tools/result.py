import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime
from matplotlib import rcParams
# import plotly.graph_objects as go
import pandas as pd
import database
import os

# rcParams["font.family"] = "serif"
# rcParams["font.style"] = "normal"
# rcParams["text.usetex"] = True

def make_figure():
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111)
    
    return ax, fig


def add_plot(
    platform: str,
    provider: str,
    backend: str,
    algorithm: str,
    benchmark_type: str,
):

    conn = database.create_connection()

    with conn:
        df = pd.read_sql_query(  # [ ]: Exception Handler Needed!
            f"""
            SELECT *
            FROM benchmarks
            WHERE platform = '{platform}'
            AND provider = '{provider}'
            AND backend = '{backend}' 
            AND algorithm = '{algorithm}'
            AND type = '{benchmark_type}'
            AND output IS NULL;
            """,
            conn,
        )
        df = df.drop(["id", "date"], axis=1)
        df = (
            df.groupby(
                [
                    "platform",
                    "provider",
                    "backend",
                    "algorithm",
                    "num_qubit",
                    "num_shot",
                    "type",
                ]
            )
            .mean()
            .reset_index()
            .sort_values(by=["num_qubit"])
        )

        ax.plot(df["num_qubit"], df["value"], marker='o', label=f"{platform} {provider} {backend}")
        ax.set_xlabel("Number of Qubit")
        ax.set_ylabel("Runtime (s)" if benchmark_type == "runtime" else "Memory Usage (KB)")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.legend()


if __name__ == "__main__":
    ax, fig = make_figure()
    
    algorithm = "deutsch_jozsa"
    bench_type = "runtime"  # "memory_usage" or "runtime"
    
    add_plot("Qiskit", "aer", "qasm_simulator", algorithm, bench_type)
    add_plot("Qiskit", "aer", "aer_simulator", algorithm, bench_type)
    
    fig.suptitle(algorithm, fontsize=30)
    plt.savefig(f"results/plots/{algorithm}-{bench_type}-{datetime.now()}.png")
