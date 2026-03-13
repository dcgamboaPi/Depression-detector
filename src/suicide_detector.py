def detect_suicide_patterns(text, patterns, negations):

    score = 0
    found = []

    for phrase, weight in patterns.items():

        if phrase in text:

            index = text.find(phrase)
            context = text[max(0, index-15):index]

            if any(neg in context for neg in negations):
                continue

            score += weight
            found.append(phrase)
            text = text.replace(phrase, "")

    return score, found, text