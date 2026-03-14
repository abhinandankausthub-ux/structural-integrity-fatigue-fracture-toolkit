import numpy as np
import matplotlib.pyplot as plt

def sn_curve(material):

    sigma_f = material.get("sigma_f", 0)
    b = material.get("b", 0)

    # cycle range
    N = np.logspace(2,7,200)

    # Basquin relation
    sigma = sigma_f*(2*N)**b

    fig, ax = plt.subplots()

    ax.loglog(N, sigma, linewidth=3, label="S-N Curve")

    # optional endurance limit visualization
    endurance_cycles = 1e6
    endurance_strength = sigma_f*(2*endurance_cycles)**b

    ax.axvline(endurance_cycles, linestyle="--", color="gray", label="Endurance Region")

    ax.set_xlabel("Cycles to Failure")
    ax.set_ylabel("Stress Amplitude (MPa)")
    ax.set_title("S–N Fatigue Curve")

    ax.legend()

    return fig
