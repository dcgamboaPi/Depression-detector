def detect_lexicon(words, lexicon, negations, stop_negation, intensifiers):

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