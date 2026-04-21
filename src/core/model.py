from collections import Counter
from dataclasses import dataclass

from config import (
    DEPRESSION_LEXICON,
    INTENSIFIERS,
    NEGATIONS,
    STOP_NEGATION,
    SUICIDE_PATTERNS,
)
from core.lexicon_detector import detect_lexicon
from core.lexicon_phrases import detect_lexicon_phrases
from core.preprocessing import normalize_text, tokenize
from core.scoring import DepressionResult, SuicideResult, depression_level, suicide_level
from core.suicide_detector import detect_suicide_patterns


@dataclass
class AnalysisResult:
    raw_score: float
    depression: DepressionResult
    suicide: SuicideResult
    patterns_found: list[tuple[str, int]]   # (term, count)
    normalized_text: str                    # useful for debugging


def analyze(text: str) -> AnalysisResult:
    """
    Full depression-language analysis pipeline.

    Order of operations
    -------------------
    1. Normalize text (emoji tokens, lowercase, clean).
    2. Detect suicide patterns first — they carry the highest weights
       and their spans are blanked before lexicon scoring.
    3. Detect multi-word lexicon phrases (longest-match, negation-aware).
    4. Detect single-word lexicon terms + emoji tokens.
    5. Aggregate scores and map to severity levels.
    """
    normalized = normalize_text(text)
    working_text = normalized

    # 1. Suicide patterns
    suicide_score, suicide_hits, working_text = detect_suicide_patterns(
        working_text, SUICIDE_PATTERNS, NEGATIONS
    )

    # 2. Multi-word lexicon phrases
    phrase_score, phrase_hits, working_text = detect_lexicon_phrases(
        working_text, DEPRESSION_LEXICON, NEGATIONS
    )

    # 3. Single-word + emoji tokens
    words = tokenize(working_text)
    word_score, word_hits = detect_lexicon(
        words, DEPRESSION_LEXICON, NEGATIONS, STOP_NEGATION, INTENSIFIERS
    )

    total = suicide_score + phrase_score + word_score
    all_hits = suicide_hits + phrase_hits + word_hits

    return AnalysisResult(
        raw_score=round(total, 2),
        depression=depression_level(total),
        suicide=suicide_level(suicide_score),
        patterns_found=Counter(all_hits).most_common(),
        normalized_text=normalized,
    )
