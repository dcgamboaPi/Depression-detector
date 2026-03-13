def detect_lexicon_phrases(text, lexicon):
    """
    Detect multi-word lexicon phrases in a text and compute their weighted score.

    This function scans the input text for phrases (multi-word expressions)
    defined in a lexicon. If a phrase is found, its associated weight is added
    to the total score and the phrase is recorded.

    After detecting a phrase, it is removed from the text to prevent double
    counting if the same phrase appears multiple times during subsequent checks.

    Parameters
    ----------
    text : str
        Input text to analyze.

    lexicon : dict[str, int]
        Dictionary mapping phrases to their corresponding weight.

    Returns
    -------
    score : int
        Total score obtained from detected phrases.

    found : list[str]
        List of detected phrases.

    text : str
        Modified text with detected phrases removed to avoid double counting.
    """
    score = 0
    found = []

    for phrase, weight in lexicon.items():

        if " " in phrase and phrase in text:

            score += weight
            found.append(phrase)

            # evitar doble conteo después
            text = text.replace(phrase, "")

    return score, found, text