import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from utils.prompts import build_prompt

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def analyze_comment(comment: str) -> dict:
    """
    Sends a comment to GPT-4.1 Mini and returns a structured diagnostic analysis.

    Builds a prompt from the comment, calls the OpenAI chat completions API
    with temperature=0 for deterministic output, and parses the response as
    JSON. Any markdown code fences in the response are stripped before parsing.

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

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a mental health text classifier. Always return JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    text = response.choices[0].message.content.strip()
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