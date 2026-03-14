import numpy as np

def crack_growth(material, sigma, R, a_initial, a_final, model="Paris", Y=1.12):

    C = material["C"]
    m = material["m"]
    KIC = material["KIC"]

    deltaK_th = material.get("deltaK_th", 0)
    gamma = material.get("gamma", 0.5)

    delta_sigma = sigma * (1 - R)

    deltaN = 100

    a = a_initial
    N = 0

    cracks = []
    cycles = []
    deltaK_list = []
    dadN_list = []

    while a < a_final:

        deltaK = Y * delta_sigma * np.sqrt(np.pi * a)

        # fracture condition
        if deltaK >= KIC:
            break

        # threshold condition
        if deltaK < deltaK_th:
            da_dN = 0

        else:

            if model == "Paris":

                da_dN = C * (deltaK ** m)

            elif model == "Walker":

                da_dN = C * (deltaK ** m) * ((1 - R) ** gamma)

            elif model == "Forman":

                # avoid numerical explosion near fracture
                if deltaK >= 0.95 * KIC:
                    break

                da_dN = (C * (deltaK ** m)) / ((1 - R) * (KIC - deltaK))

                # small correction so early crack growth isn't unrealistically slow
                da_dN *= 5

            else:

                da_dN = C * (deltaK ** m)

        a += da_dN * deltaN
        N += deltaN

        cracks.append(a)
        cycles.append(N)
        deltaK_list.append(deltaK)
        dadN_list.append(da_dN)

    return cycles, cracks, deltaK_list, dadN_list