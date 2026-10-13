import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="QuantumLab Studio", page_icon="⚛️", layout="wide")
st.title("⚛️ QuantumLab Studio")
st.caption("Virtual lab for Quantum Physics, Quantum Optics & Nonlinear Quantum Electronics")
st.info("Prototype v0.1: the Mach–Zehnder interferometer is the first implemented model. Other experiments are planned.")

with st.sidebar:
    st.header("Laboratory")
    st.selectbox("Category", ["Quantum Optics", "Quantum Physics", "Nonlinear Quantum Electronics"])
    experiment = st.selectbox("Experiment", [
        "Mach–Zehnder interferometer",
        "Hong–Ou–Mandel interference (planned)",
        "Quantum tunneling (planned)",
        "Rabi oscillations (planned)"
    ])

st.subheader(experiment)
if experiment == "Mach–Zehnder interferometer":
    st.write("A photon passes through two beam splitters. A phase difference between the two paths changes the output detection probabilities.")
    left, right = st.columns([1, 1.2])
    with left:
        phase_deg = st.slider("Relative phase (degrees)", 0, 360, 0)
        r1 = st.slider("Beam splitter 1 reflectivity", 0.05, 0.95, 0.50, 0.01)
        r2 = st.slider("Beam splitter 2 reflectivity", 0.05, 0.95, 0.50, 0.01)
        st.caption("R is reflectivity; T = 1 − R.")
    def bs(r):
        t = 1-r
        return np.array([[np.sqrt(t), 1j*np.sqrt(r)], [1j*np.sqrt(r), np.sqrt(t)]], dtype=complex)
    inp = np.array([1+0j, 0+0j])
    def probs(phi, a, b):
        state = bs(a) @ inp
        state = np.array([state[0], state[1]*np.exp(1j*phi)])
        out = bs(b) @ state
        p = np.abs(out)**2
        return p/p.sum()
    current = probs(np.deg2rad(phase_deg), r1, r2)
    with right:
        st.markdown("### Virtual optical bench")
        st.graphviz_chart("""
        digraph {
          graph [rankdir=LR, bgcolor="transparent"];
          node [shape=box, style="rounded,filled", fillcolor="#172a42", fontcolor="white", color="#54708f"];
          edge [color="#53c7ff", penwidth=2];
          S [label="Photon source"]; B1 [label="Beam splitter 1"];
          P [label="Phase shifter"]; B2 [label="Beam splitter 2"];
          D0 [label="Detector D0"]; D1 [label="Detector D1"];
          S -> B1; B1 -> P; B1 -> B2; P -> B2; B2 -> D0; B2 -> D1;
        }
        """)
        a, b = st.columns(2)
        a.metric("Detector D0", f"{current[0]:.4f}", f"{current[0]*100:.2f}%")
        b.metric("Detector D1", f"{current[1]:.4f}", f"{current[1]*100:.2f}%")
    phases = np.linspace(0, 2*np.pi, 721)
    values = np.array([probs(p, r1, r2) for p in phases])
    fig = go.Figure()
    fig.add_scatter(x=np.rad2deg(phases), y=values[:,0], name="Detector D0", mode="lines")
    fig.add_scatter(x=np.rad2deg(phases), y=values[:,1], name="Detector D1", mode="lines")
    fig.add_vline(x=phase_deg, line_dash="dot", annotation_text=f"{phase_deg}°")
    fig.update_layout(template="plotly_dark", height=430, title="Interference: detector probability vs phase",
                      xaxis_title="Relative phase (degrees)", yaxis_title="Detection probability",
                      yaxis=dict(range=[0,1]))
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Theory"):
        st.latex(r"B(R)=\begin{pmatrix}\sqrt{T}&i\sqrt{R}\\i\sqrt{R}&\sqrt{T}\end{pmatrix},\quad T=1-R")
        st.latex(r"P(\phi)=\begin{pmatrix}1&0\\0&e^{i\phi}\end{pmatrix}")
        st.write("The output state is B(R₂) P(φ) B(R₁) |0⟩. Detection probabilities are the squared magnitudes of the output amplitudes.")
        st.warning("This ideal model does not yet include optical losses, detector noise, imperfect coherence, or multi-photon effects.")
    csv = "phase_deg,probability_D0,probability_D1\n" + "\n".join(
        f"{x:.1f},{y:.8f},{z:.8f}" for x,y,z in zip(np.rad2deg(phases), values[:,0], values[:,1]))
    st.download_button("Download sweep data (CSV)", csv, "mach_zehnder_sweep.csv", "text/csv")
else:
    st.warning("This item is a roadmap placeholder. Only the Mach–Zehnder simulation is implemented in v0.1.")

st.divider()
st.subheader("Roadmap")
st.write("Next: draggable component canvas, save/load experiment designs, then validated simulations for HOM interference, tunneling, Rabi oscillations, SPDC, cavity QED, quantum circuits and more.")
