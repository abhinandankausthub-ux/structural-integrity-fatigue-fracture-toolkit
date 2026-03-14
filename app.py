import streamlit as st
import json
import numpy as np
import matplotlib.pyplot as plt
import io
import rainflow

# Dark theme for matplotlib
plt.style.use("dark_background")

plt.rcParams.update({
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "--",
    "axes.edgecolor": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "lines.linewidth": 2.5
})

from modules.Stress_Strain import stress_strain_curve
from modules.Stress_Life_Fatigue import sn_curve
from modules.Strain_Life_Fatigue import strain_life_curve
from modules.Crack_Growth import crack_growth
from modules.Stress_intensity import stress_intensity_plot
from modules.Reliability import reliability_simulation
from modules.Mean_Stress import mean_stress_diagram
from modules.Crack_Growth_Diagram import crack_growth_regime
from reports.Report_Generator import generate_report

st.set_page_config(page_title="Structural Integrity Toolkit", layout="wide")

st.title("Structural Integrity & Fatigue/Fracture Analysis Toolkit")

# ---------------------------------------------------
# Load Materials
# ---------------------------------------------------

with open("materials.json", "r") as f:
    materials = json.load(f)

material_names = list(materials.keys())

# ---------------------------------------------------
# Crack Geometry Library
# ---------------------------------------------------

geometry_factors = {
    "Edge Crack": 1.12,
    "Center Crack": 1.0,
    "Through Crack": 1.0,
    "Surface Crack": 1.3,
    "Semi-Elliptical Surface Crack": 1.4,
    "Corner Crack": 1.5,
    "Embedded Crack": 1.2,
    "Hole Crack": 2.0,
    "Radial Crack at Hole": 2.2,
    "Corner Crack at Hole": 2.3,
    "Multiple Site Damage (MSD)": 2.0,
    "Bolt Hole Crack": 2.4,
    "Fastener Hole Crack": 2.4,
    "Lug Crack": 2.5,
    "Pipe Surface Crack": 1.6,
    "Pipe Through Crack": 1.3,
    "Plate Weld Crack": 1.7,
    "T-Joint Weld Crack": 1.8,
    "Fillet Weld Toe Crack": 1.9,
    "Pressure Vessel Surface Crack": 1.6
}

# ---------------------------------------------------
# Tabs
# ---------------------------------------------------

tabs = st.tabs([
    "Material Manager",
    "Stress-Strain",
    "S-N Fatigue",
    "Strain-Life",
    "Crack Growth",
    "Stress Intensity",
    "Reliability",
    "Mean Stress Diagram",
    "Crack Growth Regimes",
    "Material Comparison",
    "Variable Amplitude Fatigue",
    "Report Builder"
])

# ===================================================
# MATERIAL MANAGER
# ===================================================

with tabs[0]:

    st.header("Material Database")
    st.write(material_names)

    name = st.text_input("Material Name", key="material_name_input")

    st.subheader("Basic Properties")

    E = st.number_input("Young's Modulus E (MPa)", key="E_input")
    nu = st.number_input("Poisson Ratio", key="nu_input")

    yield_strength = st.number_input("Yield Strength (MPa)", key="yield_input")
    ultimate_strength = st.number_input("Ultimate Strength (MPa)", key="ultimate_input")

    st.subheader("Fracture Properties (optional)")

    KIC = st.number_input("Fracture Toughness KIC (MPa√m)", value=0.0, key="KIC_input")
    deltaK_th = st.number_input("Threshold ΔK", value=0.0, key="deltaK_input")

    st.subheader("Crack Growth Constants (optional)")

    C = st.number_input(
    "Paris Constant C",
    value=1e-11,
    format="%.2e",
    key="C_input"
)
    m = st.number_input("Paris Exponent m", value=0.0, key="m_input")
    gamma = st.number_input("Walker Gamma (optional)", value=0.5, key="gamma_input")

    st.subheader("Strain-Life Fatigue (optional)")

    sigma_f = st.number_input("Fatigue Strength Coefficient σf", value=0.0, key="sigmaf_input")
    b = st.number_input("Fatigue Strength Exponent b", value=0.0, key="b_input")

    epsilon_f = st.number_input("Fatigue Ductility Coefficient εf", value=0.0, key="epsilonf_input")
    c = st.number_input("Fatigue Ductility Exponent c", value=0.0, key="c_input")

    if st.button("Estimate Missing Fatigue Constants", key="estimate_button"):

        if ultimate_strength > 0:

            sigma_f = 1.5 * ultimate_strength
            b = -0.09
            epsilon_f = 0.5
            c = -0.6
            C = 1e-11
            m = 3
            gamma = 0.5
            st.success("Estimated fatigue constants populated.")

    if st.button("Add Material", key="add_material_button"):

        materials[name] = {
            "protected": False,
            "E": E,
            "nu": nu,
            "yield_strength": yield_strength,
            "ultimate_strength": ultimate_strength,
            "KIC": KIC,
            "deltaK_th": deltaK_th,
            "C": C,
            "m": m,
            "gamma": gamma,
            "sigma_f": sigma_f,
            "b": b,
            "epsilon_f": epsilon_f,
            "c": c
        }

        with open("materials.json", "w") as f:
            json.dump(materials, f, indent=4)

        st.success("Material Added")

# ===================================================
# STRESS STRAIN
# ===================================================

with tabs[1]:

    material_name = st.selectbox("Material", material_names, key="ss_material")

    if st.button("Run Stress-Strain Analysis", key="run_ss"):

        fig = stress_strain_curve(materials[material_name])
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300)
        buf.seek(0)

        st.download_button(
            "Download Plot",
            buf,
            file_name="Stress-Strain.png",
            mime="image/png"
        )

# ===================================================
# S-N FATIGUE
# ===================================================

with tabs[2]:

    material_name = st.selectbox("Material", material_names, key="sn_material")

    if st.button("Run S-N Fatigue Analysis", key="run_sn"):

        fig = sn_curve(materials[material_name])
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300)
        buf.seek(0)

        st.download_button(
            "Download Plot",
            buf,
            file_name="sn_curve.png",
            mime="image/png"
        )

# ===================================================
# STRAIN LIFE
# ===================================================

with tabs[3]:

    material_name = st.selectbox("Material", material_names, key="sl_material")

    material = materials[material_name]

    if material["sigma_f"] == 0:
        st.error("Strain-life constants missing.")
        st.stop()

    if st.button("Run Strain-Life Analysis", key="run_sl"):

        fig = strain_life_curve(material)
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300)
        buf.seek(0)

        st.download_button(
            "Download Plot",
            buf,
            file_name="strain_life.png",
            mime="image/png"
        )

# ===================================================
# CRACK GROWTH
# ===================================================

with tabs[4]:

    material_name = st.selectbox("Material", material_names, key="cg_material")

    material = materials[material_name]

    sigma = st.number_input("Stress (MPa)", value=120.0, key="cg_sigma")
    R = st.number_input("Stress Ratio", value=0.1, key="cg_R")

    a_initial = st.number_input(
        "Initial Crack Length (m)",
        min_value=0.00001,
        value=0.001,
        step=0.0001,
        format="%.4f",
        key="cg_ai"
    )

    a_final = st.number_input(
        "Critical Crack Length (m)",
        min_value=0.001,
        value=0.02,
        step=0.001,
        format="%.4f",
        key="cg_af"
    )

    model = st.selectbox("Crack Growth Model", ["Paris", "Walker", "Forman"], key="cg_model")

    crack_type = st.selectbox(
        "Crack Geometry",
        list(geometry_factors.keys()),
        key="crack_geometry_growth"
    )

    Y = geometry_factors[crack_type]

    if st.button("Run Crack Growth Simulation", key="run_cg"):

        cycles, cracks, deltaK, dadN = crack_growth(
            material, sigma, R, a_initial, a_final, model, Y
        )

        if len(cycles) == 0:
            st.warning("Simulation produced no data. Increase stress.")
        else:

            fig, ax = plt.subplots()
            ax.plot(cycles, np.array(cracks) * 1000, color="cyan")
            ax.set_xlabel("Cycles")
            ax.set_ylabel("Crack Length (mm)")
            ax.set_title("Crack Growth Evolution")
            st.pyplot(fig)

            buf1 = io.BytesIO()
            fig.savefig(buf1, format="png", dpi=300)
            buf1.seek(0)

            st.download_button(
                "Download Crack Growth Evolution Plot",
                buf1,
                file_name="crack_growth_evolution.png",
                mime="image/png"
            )

            fig2, ax2 = plt.subplots()
            ax2.loglog(deltaK, dadN, color="orange")
            ax2.set_xlabel("ΔK (MPa√m)")
            ax2.set_ylabel("da/dN (m/cycle)")
            ax2.set_title("Fatigue Crack Growth Rate")
            st.pyplot(fig2)

            buf2 = io.BytesIO()
            fig2.savefig(buf2, format="png", dpi=300)
            buf2.seek(0)

            st.download_button(
                "Download Crack Growth Rate Plot",
                buf2,
                file_name="crack_growth_rate.png",
                mime="image/png"
            )

            fig3, ax3 = plt.subplots()
            ax3.plot(np.array(cracks) * 1000, deltaK, color="lime")
            ax3.set_xlabel("Crack Length (mm)")
            ax3.set_ylabel("ΔK (MPa√m)")
            ax3.set_title("Stress Intensity Evolution")
            st.pyplot(fig3)

            buf3 = io.BytesIO()
            fig3.savefig(buf3, format="png", dpi=300)
            buf3.seek(0)

            st.download_button(
                "Download Stress Intensity Plot",
                buf3,
                file_name="stress_intensity_evolution.png",
                mime="image/png"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Predicted Fatigue Life",
                f"{cycles[-1]:,.0f} cycles"
            )

            col2.metric(
                "Final Crack Length",
                f"{cracks[-1] * 1000:.2f} mm"
            )

            col3.metric(
                "Max ΔK",
                f"{max(deltaK):.2f} MPa√m"
            )

# ===================================================
# STRESS INTENSITY
# ===================================================

with tabs[5]:

    material_name = st.selectbox("Material", material_names, key="si_material")

    sigma = st.number_input("Applied Stress (MPa)", value=100.0, key="si_sigma")

    crack_type = st.selectbox(
        "Crack Geometry",
        list(geometry_factors.keys()),
        key="crack_geometry_intensity"
    )

    Y = geometry_factors[crack_type]

    if st.button("Run Stress Intensity Analysis", key="run_si"):

        fig, acrit = stress_intensity_plot(materials[material_name], sigma, Y)
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300)
        buf.seek(0)

        st.download_button(
            "Download Stress Intensity Plot",
            buf,
            file_name="stress_intensity_plot.png",
            mime="image/png"
        )

        st.write("Critical crack length:", round(acrit * 1000, 3), "mm")

# ===================================================
# RELIABILITY
# ===================================================

with tabs[6]:

    material_name = st.selectbox("Material", material_names, key="rel_material")

    sigma = st.number_input("Applied Stress (MPa)", value=120.0, key="rel_sigma")
    R = st.number_input("Stress Ratio", value=0.1, key="rel_R")

    a_initial = st.number_input(
        "Initial Crack Length (m)",
        min_value=0.00001,
        value=0.001,
        step=0.0001,
        format="%.4f",
        key="rel_ai"
    )

    a_final = st.number_input(
        "Critical Crack Length (m)",
        min_value=0.001,
        value=0.02,
        step=0.001,
        format="%.4f",
        key="rel_af"
    )

    samples = st.slider(
        "Monte Carlo Samples",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100
    )

    if st.button("Run Reliability Simulation", key="run_rel"):

        fig = reliability_simulation(
            materials[material_name],
            sigma,
            R,
            a_initial,
            a_final,
            samples
        )

        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300)
        buf.seek(0)

        st.download_button(
            "Download Reliability Plot",
            buf,
            file_name="reliability_distribution.png",
            mime="image/png"
        )

        st.write("""
This histogram shows the distribution of predicted fatigue lives from the Monte Carlo simulation.

Random stress variations were introduced to represent real-world loading uncertainty.
The spread of the distribution represents the reliability of the component under fatigue loading.
""")

# ===================================================
# MEAN STRESS
# ===================================================

with tabs[7]:

    material_name = st.selectbox("Material", material_names, key="mean_material")

    if st.button("Generate Mean Stress Diagram", key="run_mean"):

        fig = mean_stress_diagram(materials[material_name])
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300)
        buf.seek(0)

        st.download_button(
            "Download Mean Stress Diagram",
            buf,
            file_name="mean_stress_diagram.png",
            mime="image/png"
        )

# ===================================================
# CRACK GROWTH REGIME
# ===================================================

with tabs[8]:

    material_name = st.selectbox("Material", material_names, key="regime_material")

    if st.button("Show Crack Growth Regimes", key="run_regime"):

        fig = crack_growth_regime(materials[material_name])
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300)
        buf.seek(0)

        st.download_button(
            "Download Crack Growth Regime Plot",
            buf,
            file_name="crack_growth_regimes.png",
            mime="image/png"
        )

# ===================================================
# MATERIAL COMPARISON
# ===================================================

with tabs[9]:

    selected = st.multiselect("Select Materials", material_names, key="compare_materials")

    comparison = st.selectbox(
        "Comparison Type",
        ["S-N Fatigue", "Strain-Life", "Crack Growth"],
        key="comparison_type"
    )

    if st.button("Run Comparison", key="run_compare"):

        fig, ax = plt.subplots()

        for mat in selected:

            m = materials[mat]

            if comparison == "S-N Fatigue":

                N = np.logspace(3, 7, 200)
                sigma = m["sigma_f"] * (2 * N) ** m["b"]
                ax.loglog(N, sigma, label=mat)

            elif comparison == "Strain-Life":

                N = np.logspace(1, 7, 200)
                strain = (m["sigma_f"] / m["E"]) * (2 * N) ** m["b"] + m["epsilon_f"] * (2 * N) ** m["c"]
                ax.loglog(N, strain, label=mat)

            elif comparison == "Crack Growth":

                dK = np.logspace(0, 2, 200)
                dadN = m["C"] * (dK ** m["m"])
                ax.loglog(dK, dadN, label=mat)

        ax.legend()
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300)
        buf.seek(0)

        st.download_button(
            "Download Comparison Plot",
            buf,
            file_name="material_comparison.png",
            mime="image/png"
        )
# ===================================================
# VARIABLE AMPLITUDE FATIGUE (RAINFLOW)
# ===================================================

with tabs[10]:

    st.header("Variable Amplitude Fatigue (Rainflow Counting)")

    material_name = st.selectbox(
        "Material",
        material_names,
        key="va_material"
    )

    material = materials[material_name]

    st.write("Generate synthetic load history")

    n_points = st.slider(
        "Load history length",
        100,
        5000,
        1000
    )

    max_stress = st.number_input(
        "Maximum Stress (MPa)",
        value=200.0
    )

    if st.button("Run Rainflow Analysis"):

        # Generate synthetic random loading
        stress_history = np.random.normal(
            loc=0,
            scale=max_stress/3,
            size=n_points
        )

        cycles = rainflow.count_cycles(stress_history)

        ranges = []
        counts = []

        for rng, count in cycles:
            ranges.append(rng)
            counts.append(count)

        ranges = np.array(ranges)
        counts = np.array(counts)

        # Miner’s rule damage
        sigma_f = material["sigma_f"]
        b = material["b"]

        Nf = (ranges / sigma_f) ** (1 / b)

        damage = np.sum(counts / Nf)

        predicted_life = 1 / damage if damage > 0 else np.inf

        # Plot load history
        fig1, ax1 = plt.subplots()
        ax1.plot(stress_history)
        ax1.set_title("Stress Time History")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Stress (MPa)")
        st.pyplot(fig1)

        buf1 = io.BytesIO()
        fig1.savefig(buf1, format="png", dpi=300)
        buf1.seek(0)

        st.download_button(
            "Download Load History Plot",
            buf1,
            file_name="load_history.png",
            mime="image/png"
        )

        # Plot rainflow histogram
        fig2, ax2 = plt.subplots()
        ax2.hist(ranges, bins=30)
        ax2.set_title("Rainflow Stress Range Distribution")
        ax2.set_xlabel("Stress Range (MPa)")
        ax2.set_ylabel("Cycle Count")
        st.pyplot(fig2)

        buf2 = io.BytesIO()
        fig2.savefig(buf2, format="png", dpi=300)
        buf2.seek(0)

        st.download_button(
            "Download Rainflow Histogram",
            buf2,
            file_name="rainflow_histogram.png",
            mime="image/png"
        )

        st.metric(
            "Cumulative Damage (Miner's Rule)",
            f"{damage:.4f}"
        )

        st.metric(
            "Predicted Fatigue Life Factor",
            f"{predicted_life:.2f}"
        )
# ===================================================
# REPORT BUILDER
# ===================================================
with tabs[11]:
    material = st.selectbox("Material", material_names, key="report_material")
    analyses = st.multiselect(
        "Select Analyses",
        [
            "Stress-Strain",
            "S-N Fatigue",
            "Strain-Life",
            "Crack Growth",
            "Stress Intensity",
            "Reliability"
        ],
        key="report_analyses"
    )
    if st.button("Generate Report", key="generate_report_button"):
        buffer = generate_report(material, analyses)
        st.download_button(
            "Download Report",
            buffer,
            file_name="analysis_report.pdf",
            mime="application/pdf"
        )