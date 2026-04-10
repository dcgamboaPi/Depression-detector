import re
import unicodedata

import emoji

from config import EMOJI_SENTIMENT, EMOJI_WEIGHT


# ── Emoji handling ────────────────────────────────────────────────────────────

def map_emojis_to_sentiment(text: str) -> str:
    """
    Replace each emoji with a sentiment token that the lexicon scorer
    can process:
      - positive emoji  → "positive_emoji"  (scores -EMOJI_WEIGHT)
      - negative emoji  → "negative_emoji"  (scores +EMOJI_WEIGHT)
      - unknown / neutral emoji → its demojized name (ignored by scorer)

    The replacement happens *before* any other cleaning so that emoji
    characters are never silently dropped by punctuation-removal regexes.
    """
    text = emoji.demojize(text)

    def _replace(m: re.Match) -> str:
        key = m.group(1).lower()
        sentiment = EMOJI_SENTIMENT.get(key)
        if sentiment == "positive":
            return " positive_emoji "
        if sentiment == "negative":
            return " negative_emoji "
        return f" {key} "   # neutral / unknown — keep name, ignore in scorer

    return re.sub(r":([^:]+):", _replace, text)


# ── Text normalization pipeline ───────────────────────────────────────────────

def normalize_text(text: str) -> str:
    """
    Full preprocessing pipeline:
      1. Emoji → sentiment tokens
      2. Lowercase
      3. Strip URLs
      4. Strip hashtag '#' prefix (keep the word)
      5. Strip @mentions
      6. Collapse repeated characters  (e.g. "soooo" → "soo")
      7. Remove punctuation (keep apostrophes so "don't" stays intact)
      8. Strip accents (NFD → ASCII)
      9. Collapse extra whitespace
    """
    text = map_emojis_to_sentiment(text)
    text = text.lower()
    text = re.sub(r"http\S+", "", text)            # URLs
    text = re.sub(r"#(\w+)", r"\1", text)          # hashtags
    text = re.sub(r"@\w+", "", text)               # mentions
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)     # repeated chars
    text = re.sub(r"[^\w\s']", " ", text)          # punctuation → space
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> list[str]:
    """Return word tokens from already-normalized text."""
    return re.findall(r"\b\w+\b", text)
