import numpy as np
import matplotlib.pyplot as plt

def reliability_simulation(material, sigma, R, a_initial, a_final, runs=1000):

    C = material.get("C",1e-11)
    m = material.get("m",3)
    KIC = material.get("KIC",100)

    lives=[]

    for i in range(runs):

        sigma_rand = np.random.normal(sigma,0.1*sigma)

        delta_sigma = sigma_rand*(1-R)

        a = a_initial
        N = 0

        while a < a_final:

            deltaK = 1.12*delta_sigma*np.sqrt(np.pi*a)

            if deltaK >= KIC:
                break

            da_dN = C*(deltaK**m)

            a += da_dN*100
            N += 100

        lives.append(N)

    fig, ax = plt.subplots()

    ax.hist(lives,bins=30)

    ax.set_xlabel("Fatigue Life (cycles)")
    ax.set_ylabel("Frequency")
    ax.set_title("Reliability Simulation")

    return fig