import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURAZIONE MINIMALE ---
st.set_page_config(page_title="ASHI-CORE v2.0.2", layout="wide")

# CSS: Deep Blue Professional
st.markdown("""
    <style>
    .main { background-color: #000814; color: #f0f5f9; font-family: 'Inter', sans-serif; }
    .stMetric { background-color: #001d3d; border: 1px solid #003566; padding: 15px; border-radius: 4px; }
    h1, h2 { color: #0077b6 !important; font-weight: 300; letter-spacing: -1px; }
    .stButton>button { background-color: #003566; color: white; border-radius: 2px; border: none; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA ASHI ---
def calculate_k(data):
    mu = np.mean(np.abs(data))
    sigma = np.std(data)
    return sigma / mu if mu != 0 else 0

# --- UI ---
st.title("ASHI-CORE v2.0.2")
st.markdown("Structural Regime Transition Detection | Threshold $K_c = 1.441$")

# Top Metrics
m1, m2, m3 = st.columns(3)
m1.metric("CRITICAL THRESHOLD", "1.441")
m2.metric("SAMPLING", "Stochastic")
m3.metric("STATUS", "Operational")

st.divider()

# --- DATA INPUT & ANALYSIS ---
col_main, col_side = st.columns([3, 1])

with col_main:
    # Upload & Stream Management
    uploaded_file = st.file_uploader("Insert Telemetry CSV", type="csv")
    
    if 'stream' not in st.session_state:
        st.session_state.stream = np.random.normal(10, 2, 400)

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state.stream = df.iloc[:, 0].values
    
    # Computation
    window = 40
    k_path = [calculate_k(st.session_state.stream[i:i+window]) 
              for i in range(len(st.session_state.stream)-window)]
    
    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=k_path, name="K-Parameter", line=dict(color='#00b4d8', width=1.5)))
    fig.add_hline(y=1.441, line_dash="dash", line_color="#ff4b4b", annotation_text="Kc (Criticality)")
    
    fig.update_layout(
        template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_side:
    st.subheader("Analysis")
    current_k = k_path[-1] if k_path else 0
    
    if current_k >= 1.441:
        st.error(f"K = {current_k:.3f}\n\nTRANSITION DETECTED")
        st.write("The system has entered a high-entropy regime.")
    else:
        st.success(f"K = {current_k:.3f}\n\nSTABLE")
        st.write("Variability is localized.")

    if st.button("Inject Step Change"):
        noise = np.random.normal(10, 15, 100)
        st.session_state.stream = np.append(st.session_state.stream, noise)

st.divider()
st.caption("ASHI-CORE Framework | D. L. Nicoletti | DOI: 10.5281/zenodo.19103017")
