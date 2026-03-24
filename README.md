# Depression Detector
## Overview
Depression Detector is a modular, lexicon-based NLP pipeline for identifying depressive language signals in short-form social text (tweets, forum posts, chat messages). It operates entirely without a trained model, making it interpretable, lightweight, and easy to extend.

The system is designed as a baseline layer. Its output scores are intended to feed a supervised classifier rather than serve as standalone diagnostic decisions.

> **Important:** This tool is not a clinical instrument. It must never be used as a standalone diagnostic decision. Always combine lexical signals with context, temporal patterns, and human review.
---

## Scope

### What it does

Depression Detector analyzes individual text comments written in English on Twitter / X and assigns each one a weighted depression-language score. The score reflects the presence and intensity of clinically informed lexical signals — it does not classify users, diagnose conditions, or make predictions across time.

| ✅ In scope | ❌ Out of scope |
|---|---|
| Short-form English text (tweets, up to ~280 chars) | Long-form text (articles, clinical notes, essays) |
| Score per individual comment | Classification or diagnosis at user level |
| High-risk pattern detection (suicide language) | Real-time or streaming inference |
| Lexical signals: words, phrases, emojis | Images, audio, video, or metadata |
| Feature input for a downstream supervised model | Standalone clinical screening tool |
| Research and NLP experimentation | Languages other than English |

### Intended users

This baseline is designed for two audiences:

- **Technical teams and researchers** — who will use the per-comment score as a feature in a supervised classifier, evaluate lexicon coverage, or extend the system with new categories.
- **Non-technical stakeholders** — who need to understand what the system detects, what it does not detect, and why human review is always required before any action is taken.

### Platform fit

The lexicon and preprocessing pipeline are optimized for Twitter / X characteristics:

- Short, informal text with abbreviated grammar and slang
- High emoji density — emojis are converted to sentiment tokens and scored
- Hashtags and @mentions are stripped but the underlying words are preserved
- Gen-Z colloquial terms (e.g. `menty b`, `stressy depressy`) are included as a low-weight category
- Repeated characters (e.g. `"sooooo tired"`) are normalized before matching

### What it is not

> ⚠️ A positive score on a single comment does not mean the author is depressed. The system cannot account for sarcasm, figurative language, or context. It has no memory across comments and no knowledge of who the author is. Its output is a linguistic signal, not a clinical judgment.

---


## Quickstart 

## Architecture

The pipeline processes each text through five sequential stages:

| Step | Module | Responsibility |
|---|---|---|
| 1 | `preprocessing.py` | Emoji → sentiment tokens, lowercase, URL/mention removal, accent stripping |
| 2 | `suicide_detector.py` | High-priority pattern scan (longest-match, negation-aware). Blanks matched spans. |
| 3 | `lexicon_phrases.py` | Multi-word lexicon phrases (longest-match first, negation-aware) |
| 4 | `lexicon_detector.py` | Single-word lexicon terms + emoji tokens. Handles negation scope and intensifier multipliers. |
| 5 | `scoring.py` | Maps raw score → severity level (None / Mild / Moderate / High / Severe) |

---

## Project Structure

```
Depression-detector/
├── src/
│   ├── config.py              # All constants: lexicon, emojis, negations, intensifiers
│   ├── preprocess_lexicon.py  # Loads depression_lexicon.csv → {term: weight} dict
│   ├── preprocessing.py       # Text normalization + emoji mapping
│   ├── suicide_detector.py    # High-risk pattern detection
│   ├── lexicon_phrases.py     # Multi-word phrase detection
│   ├── lexicon_detector.py    # Single-word detection + emoji tokens
│   ├── scoring.py             # Score → severity level mapping
│   ├── model.py               # Orchestration — analyze(text) → AnalysisResult
│   └── main.py                # Demo / manual testing
└── data/
    └── depression_lexicon.csv # Term lexicon with weights and sentiment
```

---

## Lexicon

### File: `data/depression_lexicon.csv`

The lexicon is the core knowledge base. Each row maps a term or phrase to a clinical category, term type, and weight.

| Column | Type | Example | Range | Notes |
|---|---|---|---|---|
| `category` | string | anhedonia | — | Clinical grouping |
| `term_or_phrase` | string | feel empty | — | Lowercased |
| `term_type` | word / phrase | phrase | — | Phrases processed first |
| `weight_1_to_5` | integer | 4 | +5 to −5 | Negative = positive sentiment |
| `sentiment` | negative / positive | negative | — | Positive weights stored as negative numbers |

### Weight Convention

**Negative terms** carry positive weights (+1 to +5) — they add to the depression score.

**Positive terms** carry negative weights (−1 to −5) — they subtract from the depression score.

This means a text dominated by wellbeing and recovery language will produce a negative or near-zero total score.

### Categories

| Category | Sentiment | Examples |
|---|---|---|
| `negative_affect` | negative | worthless, hopeless, miserable |
| `hopeless_future` | negative | no reason to live, pointless future |
| `anhedonia` | negative | feel empty, no joy, nothing matters |
| `self_deprecation` | negative | I'm a failure, hate myself |
| `social_withdrawal` | negative | all alone, nobody cares, isolated |
| `fatigue_cognitive` | negative | can't think, brain fog, exhausted |
| `sleep_disturbance` | negative | can't sleep, wide awake at 3am |
| `appetite_body` | negative | haven't eaten, no appetite |
| `irritability_anger` | negative | everything annoys me, so angry |
| `absolutist` | negative | always, never, nothing, completely |
| `burnout_overlap` | negative | so done, can't anymore, over it |
| `genz_colloquial` | negative | menty b, stressy depressy, it's giving |
| `wellbeing` | positive | grateful, feeling better, at peace |
| `hopeful_future` | positive | looking forward to, bright future |
| `social_connection` | positive | hanging out, we laughed |
| `energy_activity` | positive | motivated, got out of bed, worked out |
| `recovery` | positive | getting help, in recovery, therapy |
| `enjoyment` | positive | had fun, loved it, laughed |

---

## Scoring

### Depression Score → Severity Level

| Raw Score | Level | Interpretation |
|---|---|---|
| > 15 | Severe | Strong, consistent depressive signal across multiple categories |
| > 8 | High | Significant signal — multiple weighted terms detected |
| > 4 | Moderate | Noticeable signal — warrants closer review |
| > 1 | Mild | Weak signal — isolated matches, high false-positive risk |
| ≤ 0 | None / Positive | Positive language dominates or no signal detected |
| < 0 | Positive | Recovery/wellbeing terms outweigh negative terms |

### Suicide Risk → Risk Level

| Suicide Score | Risk Level | Action |
|---|---|---|
| > 6 | High Risk | Immediate human review required |
| > 3 | Moderate Risk | Flag for follow-up |
| > 0 | Low Signal | Monitor — could be figurative language |
| 0 | No Risk | No pattern matched |

---

## Linguistic Modifiers

### Negation

When a negation word is detected, the scorer enters a negation scope and skips all subsequent lexicon matches until a stop-negation word is encountered.

**Negation words:** `not, no, never, don't, won't, can't, isn't, wasn't, doesn't, didn't, haven't, couldn't, shouldn't`

**Stop words:** `but, however, although, though, yet, and, because`

Example:
```
"I don't feel hopeless anymore, but I am tired"
  → hopeless: NEGATED (skipped)
  → tired: SCORED (+1)  ← negation closed by 'but'
```

### Intensifiers

A word immediately before a lexicon term multiplies its weight:

| Word | Multiplier |
|---|---|
| `very` | ×1.5 |
| `really` | ×1.3 |
| `so` | ×1.3 |
| `totally` | ×1.6 |
| `absolutely` | ×1.8 |
| `completely` | ×1.7 |
| `extremely` | ×2.0 |
| `utterly` | ×1.8 |

### Emoji Handling

Emojis are converted to sentiment tokens before any other processing:

```
😢  →  negative_emoji  (+2 to score)
😊  →  positive_emoji  (−2 to score)
🤔  →  thinking_face   (ignored)
```

The emoji weight is controlled by `EMOJI_WEIGHT = 2` in `config.py`.

---

## Usage

### Quick Start

```python
from model import analyze

result = analyze("I feel so hopeless and tired of everything 😢")

print(result.raw_score)           # e.g. 9.0
print(result.depression.level)    # 'high'
print(result.depression.label)    # 'High'
print(result.suicide.risk)        # 'none'
print(result.patterns_found)      # [('hopeless', 1), ('tired', 1), ...]
```

### `AnalysisResult` fields

| Field | Type | Description |
|---|---|---|
| `raw_score` | float | Accumulated weighted score (negative = positive sentiment) |
| `depression` | DepressionResult | level, label, score, threshold_used |
| `suicide` | SuicideResult | risk, label, score |
| `patterns_found` | list[tuple] | [(term, count)] sorted by frequency |
| `normalized_text` | str | Preprocessed text — useful for debugging |

---

## Known Limitations

- **No semantic understanding.** `"I want to kill this project"` will score as high risk.
- **Shallow negation scope.** Long-distance negation like `"I would never say I feel hopeless"` may not be caught.
- **No sarcasm detection.** `"Oh great, another sleepless night"` scores as positive.
- **Score grows with text length.** Longer texts accumulate more hits — normalize by word count for fair comparison.
- **Thresholds are uncalibrated.** Severity thresholds (4, 8, 15) were set heuristically. Calibrate against your labeled data.
- **English only.** The lexicon and negation list are English-only.

---

## Dependencies

```bash
pip install emoji pandas openpyxl scipy
```

| Package | Purpose |
|---|---|
| `emoji` | Demojize emoji characters to `:name:` tokens |
| `pandas` | Load and process the lexicon CSV |
| `openpyxl` | Read lexicon from `.xlsx` (optional) |
| `scipy` | Linear regression for temporal trend features |

---

## Disclaimer

> This tool is a research prototype intended for NLP experimentation. It is not validated as a clinical screening instrument, does not account for demographic variation in language use, and must never be used to make diagnostic or intervention decisions without qualified human oversight. Outputs should always be interpreted in context by a trained professional.
