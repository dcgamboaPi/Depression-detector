from collections import Counter

from config import *
from preprocessing import *
from suicide_detector import detect_suicide_patterns
from lexicon_detector import detect_lexicon
from lexicon_phrases import detect_lexicon_phrases
from scoring import depression_level, suicide_level


def analyze_depression(text):

    text = normalize_text(text)

    # suicide patterns detection

    suicide_score, suicide_patterns, text = detect_suicide_patterns(
        text, SUICIDE_PATTERNS, NEGATIONS
    )

    words = tokenize(text)

    # depression sentences detection
    phrase_score, phrase_patterns, text = detect_lexicon_phrases(
        text, DEPRESSION_LEXICON
    )

    # depression simple words detection

    lex_score, lex_patterns = detect_lexicon(
        words,
        DEPRESSION_LEXICON,
        NEGATIONS,
        STOP_NEGATION,
        INTENSIFIERS
    )

    total_score = suicide_score + phrase_score + lex_score

    patterns = suicide_patterns + phrase_patterns + lex_patterns

    return {
        "total_score": total_score,
        "patterns_found": Counter(patterns).most_common(),
        "depression_level": depression_level(total_score),
        "suicide_risk": suicide_level(suicide_score)
    }