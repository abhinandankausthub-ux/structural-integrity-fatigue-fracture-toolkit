import numpy as np
import matplotlib.pyplot as plt

def mean_stress_diagram(material):

    sigma_u = material["ultimate_strength"]
    sigma_y = material["yield_strength"]

    mean = np.linspace(0, sigma_u, 200)

    goodman = sigma_u*(1 - mean/sigma_u)
    soderberg = sigma_y*(1 - mean/sigma_y)

    fig, ax = plt.subplots()

    ax.plot(mean, goodman, label="Goodman", linewidth=3)
    ax.plot(mean, soderberg, label="Soderberg", linewidth=3)

    ax.fill_between(mean, 0, goodman, alpha=0.2)

    ax.set_xlabel("Mean Stress (MPa)")
    ax.set_ylabel("Alternating Stress (MPa)")
    ax.set_title("Mean Stress Fatigue Diagram")

    ax.legend()

    return fig
