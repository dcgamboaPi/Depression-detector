import streamlit as st

def render_header():
    st.markdown("<h1>🧠 MindScan</h1>", unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align: center; color: #7f8c8d; font-size:16px;'>
    Detect signs of depression in social media comments using AI
    </p>
    """, unsafe_allow_html=True)

    st.divider()


def render_sidebar():


        with st.sidebar:
            st.markdown("""
            <div style="
                background: white;
                padding: 20px;
                border-radius: 16px;
                box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
                border: 1px solid #eee;
            ">
            
            <h4 style="color:#4a4aff;">ℹ️ About MindScan</h4>
            
            <p style="font-size:14px; color:#6b6b6b;">
            AI-powered tool to detect early signals of depression 
            in social media comments.
            </p>
            
            <hr>
            
            <p style="font-weight:600;">Built with</p>
            
            <p>🚀 Streamlit</p>
            <p>🤖 GPT-4.1-mini</p>
            
            </div>
                        

            """, unsafe_allow_html=True)

def general_config():
     # CONFIG

    st.set_page_config(page_title="MindScan", layout="centered")
    # UI

    st.markdown("""
    <style>

    /* ===== FONDO APP ===== */
    [data-testid="stAppViewContainer"] {
        background: #f7f9fc;
    }

    /* ===== HEADER (oculto) ===== */
    [data-testid="stHeader"] {
        display: none;
    }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background-color: #eef4ff;
        border-right: 1px solid #e6eaf2;
    }

    [data-testid="stSidebar"] > div {
        background-color: #eef4ff;
    }

    [data-testid="stSidebar"] * {
        color: #2c3e50;
    }

    /* ===== CONTENEDOR PRINCIPAL ===== */
    .block-container {
        max-width: 1000px;
        margin-top: 60px !important;
        padding: 2rem 3rem;
        background-color: white;
        border-radius: 20px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.08);
    }

    /* ===== TITULO ===== */
    h1 {
        text-align: center;
        color: #2c3e50;
    }

    /* ===== BOTÓN ===== */
    .stButton > button {
        background: linear-gradient(135deg, #6c63ff, #5a8dee);
        color: white;
        border-radius: 12px;
        height: 3em;
        width: 100%;
        font-weight: 600;
        border: none;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #5848e5, #4a7bdc);
    }

    /* ===== TEXTAREA ===== */
    textarea {
        border-radius: 10px !important;
    }

    </style>
    """, unsafe_allow_html=True)
    
