from dataclasses import dataclass


@dataclass(frozen=True)
class DepressionResult:
    level: str
    label: str        # human-readable
    score: float
    threshold_used: str


@dataclass(frozen=True)
class SuicideResult:
    risk: str
    label: str
    score: float


# ── Depression scoring ────────────────────────────────────────────────────────
# Thresholds are defined against the raw accumulated score.
# Adjust these as you calibrate against labeled data.

_DEPRESSION_THRESHOLDS = [
    (15, "severe",   "Severe"),
    (8,  "high",     "High"),
    (4,  "moderate", "Moderate"),
    (1,  "mild",     "Mild"),
    (0,  "none",     "None / Positive"),
]


def depression_level(score: float) -> DepressionResult:
    """
    Map a raw depression score to a severity level.

    Score can be negative when positive-sentiment terms dominate.
    """
    for threshold, level, label in _DEPRESSION_THRESHOLDS:
        if score > threshold:
            return DepressionResult(
                level=level,
                label=label,
                score=round(score, 2),
                threshold_used=f"> {threshold}",
            )
    return DepressionResult(
        level="positive",
        label="Positive / No signal",
        score=round(score, 2),
        threshold_used="≤ 0",
    )


# ── Suicide risk scoring ──────────────────────────────────────────────────────

_SUICIDE_THRESHOLDS = [
    (6, "high",     "High Risk — immediate attention required"),
    (3, "moderate", "Moderate Risk"),
    (0, "low",      "Low Signal"),
]


def suicide_level(score: int) -> SuicideResult:
    for threshold, risk, label in _SUICIDE_THRESHOLDS:
        if score > threshold:
            return SuicideResult(risk=risk, label=label, score=score)
    return SuicideResult(risk="none", label="No Risk", score=score)
