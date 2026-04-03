import streamlit as st
import json
import ast
from services.openai_service import extract_diagnostico
from ui.layout import render_header, render_sidebar
from core.model import analyze

# CONFIG
st.set_page_config(
    page_title="Detector de Ánimo IA",
    page_icon="🧠"
)

# UI
render_header()
render_sidebar()

comentario = st.text_area(
    "Introduce el comentario a analizar:",
    placeholder="Ej: Me siento muy solo últimamente..."
)

if st.button("🔍 Analizar Comentario"):

    if not comentario.strip():

        st.warning("Por favor escribe un comentario")

    else:

        with st.spinner("openAI está pensando..."):

            try:

                response_ai = extract_diagnostico(comentario)
                response_reglas = analyze(comentario).raw_score

                if response_reglas < 0: 
                    response_lexicon = 0
                else: 
                    response_lexicon = 1

                response = max(response_ai, response_lexicon)

                if response == 1:

                    st.error("🚨 Resultado: 1 (Posible indicador de depresión)")
                    st.info("Esto no sustituye diagnóstico médico")
                    

                elif response == 0:

                    st.success("✅ Resultado: 0 (No se detectan señales)")

                else:

                    st.write(f"Respuesta inesperada: {response}")
                
            except Exception as e:

                st.error(f"Error técnico: {e}")