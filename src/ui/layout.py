import streamlit as st

def render_header():

    st.title("🧠 MindScan")

    st.markdown("""
    This application uses Artificial Intelligence to identify signs of deep sadness or depression in social media comments.
    """)

    st.divider()


def render_sidebar():

    st.sidebar.info(
        "Prototype created with Streamlit and GPT-4.1-mini."
    )