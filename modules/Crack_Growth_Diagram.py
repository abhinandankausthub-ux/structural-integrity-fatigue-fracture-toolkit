import numpy as np
import matplotlib.pyplot as plt

def crack_growth_regime(material):

    C = material["C"]
    m = material["m"]
    KIC = material["KIC"]
    deltaK_th = material.get("deltaK_th",1)

    deltaK = np.logspace(-1,2,400)

    dadN = []

    for dk in deltaK:

        if dk < deltaK_th:

            rate = 1e-12

        elif dk < 0.8*KIC:

            rate = C*(dk**m)

        else:

            rate = (C*(dk**m))/(KIC-dk+1e-6)

        dadN.append(rate)

    fig, ax = plt.subplots()

    ax.loglog(deltaK,dadN,linewidth=3)

    ax.axvline(deltaK_th, linestyle="--", label="Threshold ΔK_th")
    ax.axvline(KIC, linestyle="--", label="Fracture Toughness")

    ax.set_xlabel("ΔK (MPa√m)")
    ax.set_ylabel("da/dN (m/cycle)")
    ax.set_title("Fatigue Crack Growth Regimes")

    ax.legend()

    return fig
