import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def configure_gemini():
    # Configura tu API Key
    GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GENAI_API_KEY)

    # Seleccionamos el modelo (Flash es el más rápido para pruebas)
    model = genai.GenerativeModel('gemini-2.5-flash')