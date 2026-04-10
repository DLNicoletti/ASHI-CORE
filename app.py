import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURAZIONE UNIFICATA ---
st.set_page_config(page_title="ASHI-CORE v3.5", layout="wide")

# CSS: Deep Space Blue con accenti Cyber-Green
st.markdown("""
    <style>
    .main { background-color: #000b1a; color: #e0e6ed; font-family: 'Inter', sans-serif; }
    .stMetric { background-color: #001529; border: 1px solid #002b4d; padding: 15px; border-radius: 5px; }
    h1, h2 { color: #00a8ff !important; font-weight: 300; letter-spacing: -0.5px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000b1a; }
    .stTabs [data-baseweb="tab"] { color: #5c7d99; font-size: 14px; }
    .stTabs [aria-selected="true"] { color: #00a8ff !important; border-bottom-color: #00a8ff !important; }
    .stButton>button { background-color: #002b4d; color: #00a8ff; border: 1px solid #00a8ff; border-radius: 4px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE: THE UNIVERSAL INVARIANT ---
def calculate_k(data):
    """Calcolo del coefficiente di connettività strutturale (Baseline 1.441)"""
    mu = np.mean(np.abs(data))
    sigma = np.std(data)
    return sigma / mu if mu != 0 else 0

# --- HEADER ---
st.title("ASHI-CORE")
st.markdown("Multi-Domain Criticality Framework | *Universal Baseline $K_c = 1.441$*")

# --- GLOBAL METRICS ---
m1, m2, m3 = st.columns(3)
m1.metric("CRITICAL THRESHOLD", "1.441")
m2.metric("ALGORITHM", "Percolation Density")
m3.metric("ENGINE", "Active")

st.divider()

# --- ANALYSIS ENGINE SELECTOR ---
tab_space, tab_bio = st.tabs(["🛰️ SPACE TELEMETRY", "🧬 BIO DYNAMICS"])

# --- TAB 1: SPACE (SATELLITE/STOCHASTIC) ---
with tab_space:
    st.subheader("Deep Space Telemetry Stream")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        up_space = st.file_uploader("Upload Satellite CSV (Flux/Radiation)", type="csv", key="space_up")
        
        if up_space:
            data_space = pd.read_csv(up_space).iloc[:, 0].values
        else:
            data_space = np.random.normal(100, 20, 500) # Baseline stocastica
            
        win = 40
        k_space = [calculate_k(data_space[i:i+win]) for i in range(len(data_space)-win)]
        
        fig_s = go.Figure()
        fig_s.add_trace(go.Scatter(y=k_space, line=dict(color='#00a8ff', width=1.5), name="K-Space"))
        fig_s.add_hline(y=1.441, line_dash="dash", line_color="#ff4757")
        fig_s.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_s, use_container_width=True)

    with col2:
        st.write("**Diagnostics**")
        curr_k_s = k_space[-1]
        if curr_k_s >= 1.441:
            st.error(f"K: {curr_k_s:.3f}\n\nREGIME SHIFT")
            st.write("Anomalia strutturale rilevata nel flusso satellitare.")
        else:
            st.success(f"K: {curr_k_s:.3f}\n\nNOMINAL")
            st.write("Il sistema mantiene l'omeostasi operativa.")

# --- TAB 2: BIO (TISSUE/DRUG PERCOLATION) ---
with tab_bio:
    st.subheader("Tissue Barrier Percolation")
    col1_b, col2_b = st.columns([3, 1])
    
    with col1_b:
        up_bio = st.file_uploader("Upload Bio-Dataset (Intramuscular/Interstellar)", type="csv", key="bio_up")
        
        if up_bio:
            data_bio = pd.read_csv(up_bio).iloc[:, 0].values
        else:
            data_bio = np.random.normal(5, 0.5, 500) # Diffusione basale
            
        k_bio = [calculate_k(data_bio[i:i+win]) for i in range(len(data_bio)-win)]
        
        fig_b = go.Figure()
        fig_b.add_trace(go.Scatter(y=k_bio, line=dict(color='#2ed573', width=1.5), name="K-Bio"))
        fig_b.add_hline(y=1.441, line_dash="dash", line_color="#ff4757")
        fig_b.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_b, use_container_width=True)

    with col2_b:
        st.write("**Bio-Insight**")
        curr_k_b = k_bio[-1]
        if curr_k_b >= 1.441:
            st.error(f"K: {curr_k_b:.3f}\n\nPERCOLATION")
            st.write("Soglia tissutale superata. Il farmaco è in circolo sistemico.")
        else:
            st.success(f"K: {curr_k_b:.3f}\n\nCONFINED")
            st.write("Diffusione localizzata. Nessuna connettività globale.")

# --- FOOTER ---
st.divider()
st.caption("ASHI-CORE Framework | Unified Theory of Structural Stability | D. L. Nicoletti")
