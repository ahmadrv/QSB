import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime
from matplotlib import rcParams
import pandas as pd
import database

rcParams["font.family"] = "serif"
rcParams["font.style"] = "normal"
rcParams["text.usetex"] = True

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
                    "oracle_type"
                ]
            )
            .mean()
            .reset_index()
            .sort_values(by=["num_qubit"])
        )

        if benchmark_type == "runtime":
            ax.plot(df["num_qubit"], df["runtime"], marker='o', label=f"{algorithm}")
            ax.set_ylabel("Runtime (s)")
        elif benchmark_type == "memory_usage":
            ax.plot(df["num_qubit"], df["memory"], marker='o', label=f"{algorithm}")
            ax.set_ylabel("Memory Usage (KB)")
        
        ax.set_xlabel("Number of Qubit")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.legend()


if __name__ == "__main__":
    ax, fig = make_figure()
    
    platform = "Qiskit"
    provider = "aer"
    backend = "qasm_simulator"
    
    algs = ["deutsch_jozsa",
            "bernstein_vazirani",
            "quantum_fourier_transform",
            "simon"]
    
    for alg in algs:
        bench_type = "runtime"  # "memory_usage" or "runtime"
        
        add_plot(platform, provider, backend, alg, bench_type)
        
        fig.suptitle(f"{platform} {backend}", fontsize=30)

    plt.savefig(f"results/plots/{platform}-{backend}-{bench_type}-{datetime.now()}.pdf")
