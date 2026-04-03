def build_prompt(comment: str) -> str:
    """
    Builds a structured prompt for binary depression-language classification.

    Instructs the model to analyze a comment and return a JSON object with
    a binary diagnostic label and the key words that supported the decision.

    Classification schema
    ---------------------
    1 : The comment expresses sadness, persistent negative emotions,
        hopelessness, emotional emptiness, or signs of psychological
        distress — even if not extreme.
    0 : The comment is neutral, positive, humorous, or shows no clear
        signs of depression.

    Parameters
    ----------
    comment : str
        Raw comment text to classify.

    Returns
    -------
    str
        Fully formatted prompt ready to send to the model.

    Notes
    -----
    The prompt enforces strict JSON output with no extra text or markdown.
    Expected response format::

        {
          "diagnostico": 0 or 1,
          "palabras_principales": ["word1", "word2", "word3"]
        }
    """
    return f"""
Eres un modelo experto en análisis de lenguaje emocional.

Tu tarea es analizar el siguiente comentario y devolver SOLO un JSON válido.

Definición de clases:
- 1 → El comentario expresa tristeza, emociones negativas persistentes, desesperanza, vacío emocional o signos de malestar psicológico (aunque no sea extremo).
- 0 → El comentario es neutral, positivo, humorístico o no muestra señales claras de depresión.

Comentario: 
"{comment}"

Devuelve el resultado EXACTAMENTE en este formato JSON:

{{
  "diagnostico": 0 o 1,
  "palabras_principales": ["palabra1", "palabra2", "palabra3"]
}}

Restricciones:
- Devuelve SOLO JSON válido.
- Usa comillas dobles.
- No añadas explicaciones.
- No devuelvas texto fuera del JSON.
    """