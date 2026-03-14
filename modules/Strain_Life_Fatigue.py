import numpy as np
import matplotlib.pyplot as plt

def strain_life_curve(material):

    sigma_f = material["sigma_f"]
    b = material["b"]
    epsilon_f = material["epsilon_f"]
    c = material["c"]
    E = material["E"]

    N = np.logspace(1,7,200)

    elastic = (sigma_f/E)*(2*N)**b
    plastic = epsilon_f*(2*N)**c

    strain = elastic + plastic

    fig, ax = plt.subplots()

    ax.loglog(N, elastic, '--', label="Elastic")
    ax.loglog(N, plastic, '--', label="Plastic")
    ax.loglog(N, strain, linewidth=3, label="Total")

    ax.set_xlabel("Cycles to Failure")
    ax.set_ylabel("Strain Amplitude")
    ax.set_title("Strain-Life (Coffin-Manson)")

    ax.legend()

    return fig
