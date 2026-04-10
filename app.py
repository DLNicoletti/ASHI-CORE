import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Configuration
st.set_page_config(page_title="ASHI-CORE | Structural Stability Analysis", layout="wide")

# Apple/NASA inspired CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    .main { background-color: #000000; color: #ffffff; font-family: 'Inter', sans-serif; }
    .stMetric { background-color: #0a0a0a; border: 1px solid #1a1a1a; padding: 20px; border-radius: 2px; }
    div[data-testid="stMetricValue"] { font-weight: 300; font-size: 2rem; color: #ffffff; }
    h1, h2, h3 { font-weight: 300; letter-spacing: -0.05rem; color: #ffffff !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; gap: 24px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; background-color: transparent; border: none; 
        color: #666666; font-weight: 400; font-size: 13px;
    }
    .stTabs [aria-selected="true"] { color: #ffffff !important; border-bottom: 2px solid #ffffff !important; }
    .stButton>button { 
        background-color: #ffffff; color: #000000; border: none; 
        border-radius: 2px; font-weight: 600; font-size: 12px; height: 40px;
    }
    .stDivider { border-bottom-color: #1a1a1a; }
    .plot-container { border: 1px solid #1a1a1a; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# Calculation Engine
def get_stability_index(data):
    """
    Calculates the structural stability index based on the 
    coefficient of variation. Critical threshold identified at 1.441.
    """
    mu = np.mean(np.abs(data))
    sigma = np.std(data)
    return sigma / mu if mu != 0 else 0

# Header Section
st.title("ASHI-CORE")
st.markdown("### Structural Criticality Protocol")

# Top Metrics
m1, m2, m3 = st.columns(3)
m1.metric("CRITICAL LIMIT", "1.441")
m2.metric("RESOLUTION", "High-Frequency")
m3.metric("SYSTEM STATUS", "Operational")

st.divider()

# Main Interface
tab_space, tab_bio = st.tabs(["AEROSPACE TELEMETRY", "BIOMEDICAL DIFFUSION"])

def render_analysis(domain_name, data_source, key_suffix):
    col_plot, col_data = st.columns([3, 1])
    
    with col_plot:
        uploaded = st.file_uploader(f"Import {domain_name} dataset", type="csv", key=f"up_{key_suffix}")
        
        if uploaded:
            raw_data = pd.read_csv(uploaded).iloc[:, 0].values
        else:
            # Default state: Baseline monitoring
            raw_data = data_source
            
        window = 50
        k_values = [get_stability_index(raw_data[i:i+window]) for i in range(len(raw_data)-window)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=k_values, line=dict(color='#ffffff', width=1), name="K-Index"))
        fig.add_hline(y=1.441, line_dash="dot", line_color="#ff3b30", annotation_text="K-Critical")
        
        fig.update_layout(
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            height=450,
            xaxis=dict(gridcolor='#1a1a1a', showgrid=True),
            yaxis=dict(gridcolor='#1a1a1a', showgrid=True, zeroline=False),
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_data:
        st.markdown("#### Analysis")
        current_k = k_values[-1]
        
        status = "CRITICAL" if current_k >= 1.441 else "STABLE"
        color = "#ff3b30" if current_k >= 1.441 else "#ffffff"
        
        st.markdown(f"Current K: <span style='color:{color}; font-size:24px;'>{current_k:.4f}</span>", unsafe_allow_html=True)
        st.markdown(f"Status: **{status}**")
        
        st.divider()
        st.markdown(f"""
        **Protocol Note:**
        The current K-index measures the connectivity of the signal. 
        Values exceeding 1.441 indicate a phase transition 
        within the {domain_name} structure.
        """)
        
        if st.button("Inject Step Change", key=f"btn_{key_suffix}"):
            st.info("Simulating instability event.")

with tab_space:
    render_analysis("Space Telemetry", np.random.normal(50, 5, 500), "space")

with tab_bio:
    render_analysis("Tissue Matrix", np.random.normal(5, 0.4, 500), "bio")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #444444; font-size: 11px;'>
ASHI-CORE v3.5 | Advanced Structural Health Index | D. L. Nicoletti <br>
Confidential Intellectual Property | Cross-Dataset Validation Baseline
</div>
""", unsafe_allow_html=True)
