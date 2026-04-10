import streamlit as st

def render_header():

    st.title("🧠 MindScan")

    st.markdown("""
    Esta aplicación utiliza Inteligencia Artificial para identificar señales
    de tristeza profunda o depresión en comentarios de redes sociales.
    """)

    st.divider()


def render_sidebar():

    st.sidebar.info(
        "Prototipo creado con Streamlit y Gemini 2.5 Flash."
    )