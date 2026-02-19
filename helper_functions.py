import pandas as pd
import matplotlib.pyplot as plt
from typing import Literal

def plot_crossoverv2(df: pd.DataFrame, 
                     sweep_param :Literal["n", "d"] = "n", 
                     plot_std: bool = False):
    
    colors = {"qpp-cpu": "black", "nvidia":"#76B900"}
    labels = {"qpp-cpu": "CPU (qpp-cpu)", "nvidia":"GPU (nvidia)"}

    param_map = {"n": "n_qubits", "d": "depth"}
    sweep_param = param_map[sweep_param]

    if sweep_param == "n_qubits":
        cnst_str = "depth"
        x_label = "Number of qubits (n)"
        cnst = df.depth.iloc[0]
  
    if sweep_param == "depth":
        cnst_str = "n_qubits"
        x_label = "Circuit depth (d)"
        cnst = df.n_qubits.iloc[0]
 
    plt.figure()
    for tgt in ["qpp-cpu", "nvidia"]:
        sub = df[(df.target == tgt) & (df.ok == True)].sort_values(sweep_param)
        if plot_std:
            plt.errorbar(sub[sweep_param], sub.avg_time, yerr=sub.std_time, marker="o", label=labels[tgt],color=colors[tgt])
        else:
            plt.plot(sub[sweep_param], sub.min_time, marker="o", label=labels[tgt], color=colors[tgt])
    plt.yscale("log")
    plt.xlabel(f"{x_label}")
    plt.ylabel("Time for cudaq.get_state() (seconds, log scale)")
    plt.title(f"CPU vs GPU statevector simulation ({cnst_str}={cnst})")
    plt.grid(True, which="both")
    plt.legend()
    plt.show()