def detect_lexicon_phrases(
    text: str,
    lexicon: dict[str, int | float],
    negations: set[str],
) -> tuple[float, list[str], str]:
    """
    Detect multi-word lexicon phrases in *text* and return their
    weighted score.

    Improvements over the original:
    - Phrases are evaluated longest-first so that "no reason to live"
      is matched before "reason to live" or "live".
    - A simple negation check inspects the 15-character window
      immediately before each phrase match (same approach as
      suicide_detector) so "I don't feel hopeless" won't score.
    - Matched spans are blanked out to prevent double-counting by the
      single-word scorer that runs afterwards.

    Parameters
    ----------
    text : str
        Normalized input text.
    lexicon : dict[str, int | float]
        Term/phrase → weight mapping.
    negations : set[str]
        Words that negate a match.

    Returns
    -------
    score : float
        Sum of weights for all detected (non-negated) phrases.
    found : list[str]
        Phrases that were matched (and not negated).
    text : str
        Text with matched phrases blanked out.
    """
    score: float = 0.0
    found: list[str] = []

    # Only multi-word entries, sorted longest first to prefer specific matches
    phrases = sorted(
        [(p, w) for p, w in lexicon.items() if " " in p],
        key=lambda x: len(x[0]),
        reverse=True,
    )

    for phrase, weight in phrases:
        if phrase not in text:
            continue

        index = text.find(phrase)
        context = text[max(0, index - 20): index]

        if any(neg in context.split() for neg in negations):
            # Negated — blank it out anyway to avoid single-word sub-matches
            text = text.replace(phrase, " ", 1)
            continue

        score += weight
        found.append(phrase)
        text = text.replace(phrase, " ", 1)

    return score, found, text
