def detect_lexicon(words, lexicon, negations, stop_negation, intensifiers):
    """
    Detect lexicon-based signals in a tokenized text and compute a weighted score.

    This function scans a list of words and checks whether any of them appear
    in a predefined lexicon. If a lexicon term is found, its weight contributes
    to the total score. The function also handles simple linguistic modifiers:

    - Negations: words that suppress scoring for subsequent lexicon terms
      (e.g., "not", "never").
    - Stop-negation markers: words that cancel an active negation scope
      (e.g., "but", "however").
    - Intensifiers: words that increase the weight of the following lexicon term
      (e.g., "very", "extremely").

    Parameters
    ----------
    words : list[str]
        Tokenized text (list of words) to analyze.

    lexicon : dict[str, int]
        Dictionary mapping terms to their corresponding weight.

    negations : set[str]
        Set of words that trigger a negation scope.

    stop_negation : set[str]
        Set of words that terminate an active negation scope.

    intensifiers : dict[str, float]
        Dictionary mapping intensifier words to a multiplier that increases
        the weight of the following lexicon term.

    Returns
    -------
    score : float
        Total weighted score based on lexicon matches.

    found : list[str]
        List of lexicon terms detected in the text (excluding negated ones).
    """
    score = 0
    found = []
    is_negated = False

    for i, word in enumerate(words):

        modifier = 1

        if word in negations:
            is_negated = True
            continue

        if word in stop_negation:
            is_negated = False

        if i > 0 and words[i-1] in intensifiers and not is_negated:
            modifier = intensifiers[words[i-1]]

        if word in lexicon:

            if not is_negated:
                weight = lexicon[word]
                score += weight * modifier
                found.append(word)

    return score, found