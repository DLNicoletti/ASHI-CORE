import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- NASA MISSION CONTROL CONFIG ---
st.set_page_config(
    page_title="ASHI-CORE | Mission Control",
    page_icon="🛰️",
    layout="wide"
)

# Style: NASA Deep Space Console
st.markdown("""
    <style>
    .main { background-color: #000b14; color: #00ff41; font-family: 'Courier New', monospace; }
    .stMetric { background-color: #001524; border: 1px solid #005f73; padding: 10px; border-radius: 0px; }
    [data-testid="stMetricValue"] { color: #00ff41 !important; }
    h1, h2, h3 { color: #94d2bd !important; text-transform: uppercase; letter-spacing: 2px; }
    .stButton>button { 
        background-color: transparent; border: 1px solid #94d2bd; color: #94d2bd;
        border-radius: 0px; font-weight: bold;
    }
    .stButton>button:hover { background-color: #94d2bd; color: #000b14; }
    </style>
    """, unsafe_allow_html=True)

# --- CORE ENGINE: K-PARAMETER ---
class AshiCoreEngine:
    def __init__(self):
        self.Kc = 1.441  # Critical Threshold
        
    def calculate_k(self, data):
        """K = σ / μ (Coefficient of Variation)"""
        mu = np.mean(np.abs(data))
        sigma = np.std(data)
        return sigma / mu if mu != 0 else 0

# --- UI HEADER ---
st.title("🛰️ ASHI-CORE v2.0.2")
st.caption("Telemetry Phase Transition Detection | Critical Threshold Kc = 1.441")

# Mission Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("OPERATIONAL STATE", "ACTIVE")
m2.metric("CRITICAL Kc", "1.441")
m3.metric("ENGINE", "E0-SUBJECT-ZERO")
m4.metric("BUILD", "1B80001")

st.divider()

# --- TELEMETRY ANALYSIS ---
col_left, col_right = st.columns([3, 1])

with col_left:
    st.subheader("📡 Stochastic Telemetry Stream")
    
    # Simulazione Flusso Dati (Proton Flux / Thermal)
    if 'telemetry' not in st.session_state:
        # Segnale stabile di base
        st.session_state.telemetry = np.random.normal(10, 2, 500)
    
    if st.button("EXECUTE REGIME SHIFT (Simulate Instability)"):
        # Introduce instabilità globale (accoppiamento dei nodi)
        shift = np.random.normal(10, 16, 200) # sigma aumenta drasticamente
        st.session_state.telemetry = np.append(st.session_state.telemetry, shift)

    # Calcolo K in tempo reale
    window = 50
    k_values = [AshiCoreEngine().calculate_k(st.session_state.telemetry[i:i+window]) 
                for i in range(len(st.session_state.telemetry)-window)]
    
    # Plotting
    fig = go.Figure()
    # K-Parameter line
    fig.add_trace(go.Scatter(y=k_values, name="K-Parameter", line=dict(color='#00ff41', width=1.5)))
    # Kc Threshold
    fig.add_hline(y=1.441, line_dash="dot", line_color="#ae2012", 
                  annotation_text="CRITICAL THRESHOLD (Kc)", annotation_position="top left")
    
    fig.update_layout(
        template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        height=450,
        yaxis=dict(gridcolor='#002133'),
        xaxis=dict(gridcolor='#002133')
    )
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("📋 LOGS")
    current_k = k_values[-1] if k_values else 0
    
    if current_k >= 1.441:
        st.error(f"WARNING: K={current_k:.3f}\n\nTRANSITION REGIME DETECTED")
        st.warning("Global coupling detected in telemetry stream. System dynamics unstable.")
    else:
        st.success(f"STATUS: K={current_k:.3f}\n\nSTABLE REGIME")
        st.info("Variability localized. μ/σ ratio within safety limits.")

    st.divider()
    st.write("**CAPABILITIES:**")
    st.markdown("- Pre-critical detection\n- Edge-compatible\n- Training-free")
    
    st.write("**CITATION:**")
    st.code("D. L. Nicoletti\nDOI: 10.5281/zenodo.19103017", language="text")

# --- FOOTER ---
st.divider()
st.markdown("<p style='text-align: center; color: #555;'>PROPRIETARY RESEARCH LICENSE | Davide Luca Nicoletti</p>", unsafe_allow_html=True)
