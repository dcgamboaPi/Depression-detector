import json
import os

from dotenv import load_dotenv
from google import genai

from utils.prompts import build_prompt

load_dotenv()
GENAI_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GENAI_API_KEY)


def analyze_comment(comment: str) -> dict:
    """
    Sends a comment to Gemini and returns a structured diagnostic analysis.

    Builds a prompt from the comment, calls the Gemini 2.5 Flash model,
    and parses the response as JSON. The model is expected to return a
    JSON object — any markdown code fences are stripped before parsing.

    Parameters
    ----------
    comment : str
        Raw comment text to analyze.

    Returns
    -------
    dict
        Parsed JSON response from the model. Structure depends on the
        prompt template defined in utils/prompts.py.

    Raises
    ------
    json.JSONDecodeError
        If the model response cannot be parsed as valid JSON.
    """
    prompt = build_prompt(comment)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


def extract_diagnostico(comment: str) -> str:
    """
    Returns only the 'diagnostico' field from the model's analysis.

    Convenience wrapper around analyze_comment() for cases where only
    the diagnostic label is needed.

    Parameters
    ----------
    comment : str
        Raw comment text to analyze.

    Returns
    -------
    str
        The value of the 'diagnostico' key from the model's JSON response.
    """
    result = analyze_comment(comment)
    return result["diagnostico"]