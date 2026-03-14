import numpy as np
import matplotlib.pyplot as plt

def stress_strain_curve(material):

    E = material["E"]
    sigma_y = material["yield_strength"]
    sigma_u = material["ultimate_strength"]

    strain = np.linspace(0, 0.1, 300)

    yield_strain = sigma_y / E

    stress = np.zeros_like(strain)

    # Elastic region
    elastic_region = strain <= yield_strain
    stress[elastic_region] = E * strain[elastic_region]

    # Plastic region with mild hardening
    plastic_region = strain > yield_strain
    stress[plastic_region] = sigma_y + 0.02 * E * (strain[plastic_region] - yield_strain)

    # Limit stress to ultimate strength
    stress = np.minimum(stress, sigma_u)

    fig, ax = plt.subplots()

    ax.plot(strain, stress, linewidth=3, label="Stress–Strain")

    # Mark yield point
    ax.scatter(yield_strain, sigma_y, color="red", label="Yield Point")

    ax.set_xlabel("Strain")
    ax.set_ylabel("Stress (MPa)")
    ax.set_title("Stress–Strain Curve")

    ax.legend()

    return fig
