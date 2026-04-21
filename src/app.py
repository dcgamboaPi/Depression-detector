import streamlit as st
from ui.layout import render_header, render_sidebar, general_config
import requests

url = "https://dcgamboap-depression-model.hf.space/items"

# CONFIG
st.set_page_config(
    page_title="mindScan",
    page_icon="🧠"
)
render_header()
render_sidebar()
general_config()

comentario = st.text_area(
    "Enter the comment to analyze:",
    placeholder="E.g.: I’ve been feeling very lonely lately...",
    height=150
)

if st.button("🔍 Analyze Comment"):

    if not comentario.strip():

        st.warning("Please write a comment")

    else:

        with st.spinner("OpenAI is thinking..."):

            try:

                r = requests.post(
                    url,
                    json={"comment": comentario}
                )

                response = r.json()
                resultado = response["item"]
                if resultado == 1:

                    st.error("🚨 Result: 1 (Possible indicator of depression)")
                    st.info("This does not replace a medical diagnosis.")
                    

                elif resultado == 0:

                    st.success("✅ Result: 0 (No signs detected)")

                else:

                    st.write(f"Respuesta inesperada: {response}")

            except Exception as e:

                st.error(f"Error técnico: {e}")
                st.write("Status code:", r.status_code)
                st.write("Response text:", r.text)
st.caption("Your data is private and is not stored")