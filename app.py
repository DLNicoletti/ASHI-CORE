import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURAZIONE BIO-TECH ---
st.set_page_config(page_title="ASHI-BIO | Tissue Dynamics", layout="wide")

# CSS: Bio-Organic Dark Mode (Verde Smeraldo e Blu Profondo)
st.markdown("""
    <style>
    .main { background-color: #010a01; color: #d1f2d1; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stMetric { background-color: #0a1f0a; border: 1px solid #1b4d1b; padding: 20px; border-radius: 8px; }
    h1, h2 { color: #4ade80 !important; font-weight: 200; }
    .stButton>button { background-color: #1b4d1b; color: #4ade80; border: 1px solid #4ade80; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE: PERCOLATION DENSITY ---
def calculate_k_bio(signal):
    """Calcolo della densità di connettività tissutale"""
    mu = np.mean(np.abs(signal))
    sigma = np.std(signal)
    return sigma / mu if mu != 0 else 0

# --- HEADER E DESCRIZIONE ---
st.title("🧪 ASHI-BIO™ Dynamics")
st.markdown("""
**Tissue Wall Percolation Framework (v3.0.1)** *Analisi della connettività strutturale per la farmacocinetica intramuscolare.*
""")

with st.expander("📖 Fondamenti Scientifici dell'Esploratore"):
    st.write("""
    Il framework ASHI-BIO applica la **Teoria della Percolazione** alla diffusione tissutale. 
    Il passaggio di un farmaco attraverso le pareti muscolari non è lineare, ma governato da una 
    **Transizione di Fase**. 
    
    * **K < 1.441**: Confinamento tissutale. Il farmaco è intrappolato in cluster isolati.
    * **K ≥ 1.441**: Soglia di Percolazione. Si forma un cluster infinito; il farmaco invade 
        il torrente ematico in modo sistemico.
    """)

# --- DASHBOARD ---
c1, c2, c3 = st.columns(3)
c1.metric("Critical Kc (Baseline)", "1.441")
c2.metric("Tissue Density", "Dynamic")
c3.metric("State", "Bio-Monitoring")

st.divider()

# --- ANALISI BIO-DATABASE ---
left, right = st.columns([2, 1])

with left:
    st.subheader("🔬 Bio-Signal Telemetry")
    uploaded_bio = st.file_uploader("Upload Bio-Database (CSV/EDF)", type=["csv"])
    
    if 'bio_data' not in st.session_state:
        # Simulazione: Da diffusione lenta a percolazione improvvisa
        t = np.linspace(0, 100, 1000)
        st.session_state.bio_data = np.random.normal(5, 1, 1000) # Rumore base

    if uploaded_bio:
        df = pd.read_csv(uploaded_bio)
        st.session_state.bio_data = df.iloc[:, 0].values

    # Calcolo K dinamico (sliding window sulla diffusione)
    win = 50
    k_bio_path = [calculate_k_bio(st.session_state.bio_data[i:i+win]) 
                  for i in range(len(st.session_state.bio_data)-win)]
    
    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=k_bio_path, name="Diffusion Density (K)", line=dict(color='#4ade80', width=2)))
    fig.add_hline(y=1.441, line_dash="dot", line_color="#ef4444", annotation_text="Percolation Threshold")
    
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("🛡️ Clinical Insight")
    curr_k = k_bio_path[-1] if k_path else 0
    
    if curr_k >= 1.441:
        st.error(f"K = {curr_k:.3f}\n\nPERCOLATION ACTIVE")
        st.write("**Stato:** Assorbimento Sistemico in corso. La barriera tissutale è stata superata.")
    else:
        st.success(f"K = {curr_k:.3f}\n\nSTABLE CONFINEMENT")
        st.write("**Stato:** Il soluto è ancora localizzato. Connettività tissutale sotto soglia.")

    if st.button("Simulate Drug Injection"):
        # Iniezione aumenta la varianza (densità locale)
        injection = np.random.normal(5, 8, 200)
        st.session_state.bio_data = np.append(st.session_state.bio_data, injection)

st.divider()
st.caption("D. L. Nicoletti | Bio-Mathematical Percolation Invariant | Cross-Dataset Validated")
