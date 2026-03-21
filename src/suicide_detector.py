def detect_suicide_patterns(
    text: str,
    patterns: dict[str, int],
    negations: set[str],
) -> tuple[int, list[str], str]:
    """
    Scan *text* for high-risk suicide patterns.

    Improvements over the original:
    - Negation check uses `.split()` on the context window so that
      "dont" inside a longer word doesn't cause a false negative.
    - Patterns are checked longest-first so more specific matches
      take precedence.
    - Each matched span is blanked once to avoid double-counting
      by the downstream lexicon scorer.

    Parameters
    ----------
    text : str
        Normalized input text.
    patterns : dict[str, int]
        Phrase → weight mapping for high-risk expressions.
    negations : set[str]
        Words that negate a match.

    Returns
    -------
    score : int
        Sum of weights for all detected (non-negated) patterns.
    found : list[str]
        Patterns that were matched and scored.
    text : str
        Text with matched patterns removed.
    """
    score: int = 0
    found: list[str] = []

    sorted_patterns = sorted(patterns.items(), key=lambda x: len(x[0]), reverse=True)

    for phrase, weight in sorted_patterns:
        if phrase not in text:
            continue

        index = text.find(phrase)
        context = text[max(0, index - 20): index]

        if any(neg in context.split() for neg in negations):
            text = text.replace(phrase, " ", 1)
            continue

        score += weight
        found.append(phrase)
        text = text.replace(phrase, " ", 1)

    return score, found, text
