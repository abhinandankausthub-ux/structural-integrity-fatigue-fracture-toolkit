import numpy as np
import matplotlib.pyplot as plt

def stress_intensity_plot(material, sigma, Y):

    KIC = material["KIC"]

    # crack length range (meters)
    a = np.linspace(0.0001, 0.05, 300)

    # stress intensity
    K = Y * sigma * np.sqrt(np.pi * a)

    # critical crack length (avoid divide-by-zero)
    if sigma == 0:
        a_crit = np.inf
    else:
        a_crit = (KIC / (Y * sigma))**2 / np.pi

    fig, ax = plt.subplots()

    # stress intensity curve
    ax.plot(a * 1000, K, label="Stress Intensity K", linewidth=3)

    # fracture toughness line
    ax.axhline(KIC, color="red", linestyle="--", label="Fracture Toughness KIC")

    # critical crack length
    if np.isfinite(a_crit):
        ax.axvline(a_crit * 1000, color="orange", linestyle="--", label="Critical Crack Length")

    # unsafe fracture region
    ax.fill_between(a * 1000, K, KIC, where=(K >= KIC), color="red", alpha=0.3)

    # safe region
    ax.fill_between(a * 1000, 0, np.minimum(K, KIC), color="green", alpha=0.1)

    ax.set_xlabel("Crack Length (mm)")
    ax.set_ylabel("Stress Intensity (MPa√m)")

    ax.set_title("Fracture Mechanics Safety Diagram")

    ax.legend()

    return fig, a_crit