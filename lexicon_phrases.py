def detect_lexicon_phrases(text, lexicon):

    score = 0
    found = []

    for phrase, weight in lexicon.items():

        if " " in phrase and phrase in text:

            score += weight
            found.append(phrase)

            # evitar doble conteo después
            text = text.replace(phrase, "")

    return score, found, text