from config import EMOJI_WEIGHT


def detect_lexicon(
    words: list[str],
    lexicon: dict[str, int | float],
    negations: set[str],
    stop_negation: set[str],
    intensifiers: dict[str, float],
) -> tuple[float, list[str]]:
    """
    Detect single-word lexicon matches and score them.

    Logic:
    - Negation scope opens on a negation word and closes on a
      stop-negation word.  Negated matches are skipped (score 0).
    - An intensifier immediately before a match multiplies its weight.
    - Special tokens "positive_emoji" and "negative_emoji" (injected
      by the preprocessing step) are handled here with EMOJI_WEIGHT
      so emoji sentiment is integrated into the same score.

    Parameters
    ----------
    words : list[str]
        Tokenized, normalized text.
    lexicon : dict[str, int | float]
        Term → weight mapping (positive terms have negative weights).
    negations : set[str]
        Words that open a negation scope.
    stop_negation : set[str]
        Words that close a negation scope.
    intensifiers : dict[str, float]
        Multipliers for the following lexicon term.

    Returns
    -------
    score : float
        Weighted sum of matched terms.
    found : list[str]
        Terms that were matched (and not negated).
    """
    score: float = 0.0
    found: list[str] = []
    is_negated = False

    for i, word in enumerate(words):

        # ── Scope management ──────────────────────────────────────────
        if word in negations:
            is_negated = True
            continue

        if word in stop_negation:
            is_negated = False
            continue

        if is_negated:
            continue

        # ── Emoji tokens ──────────────────────────────────────────────
        if word == "positive_emoji":
            score -= EMOJI_WEIGHT
            found.append("positive_emoji")
            continue

        if word == "negative_emoji":
            score += EMOJI_WEIGHT
            found.append("negative_emoji")
            continue

        # ── Lexicon match ─────────────────────────────────────────────
        if word in lexicon:
            modifier = (
                intensifiers[words[i - 1]]
                if i > 0 and words[i - 1] in intensifiers
                else 1.0
            )
            score += lexicon[word] * modifier
            found.append(word)

    return score, found
