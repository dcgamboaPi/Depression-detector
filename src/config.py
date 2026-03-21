from preprocess_lexicon import load_lexicon

# ─────────────────────────────────────────────
# Suicide patterns — weights are intentionally
# above the depression scale (6–7) so they
# always trigger "High Risk" regardless of the
# depression score.
# ─────────────────────────────────────────────
SUICIDE_PATTERNS: dict[str, int] = {
    "want to die": 7,
    "wish i was dead": 7,
    "wish i were dead": 7,
    "don't want to live": 6,
    "dont want to live": 6,
    "life is pointless": 6,
    "no reason to live": 7,
    "end my life": 7,
    "kill myself": 7,
    "rather be dead": 6,
}

# Words that open a negation scope
NEGATIONS: set[str] = {
    "no", "not", "never", "neither",
    "dont", "don't",
    "cant", "can't",
    "wont", "won't",
    "wasnt", "wasn't",
    "isnt", "isn't",
    "doesnt", "doesn't",
    "didnt", "didn't",
    "havent", "haven't",
    "couldnt", "couldn't",
    "shouldnt", "shouldn't",
}

# Words that close a negation scope
STOP_NEGATION: set[str] = {
    "but", "however", "although",
    "though", "yet", "and", "because",
}

# Words that amplify the following lexicon term's weight
INTENSIFIERS: dict[str, float] = {
    "very": 1.5,
    "extremely": 2.0,
    "really": 1.3,
    "so": 1.3,
    "absolutely": 1.8,
    "completely": 1.7,
    "totally": 1.6,
    "utterly": 1.8,
}

# ─────────────────────────────────────────────
# Emoji → sentiment mapping
# "positive" emojis will subtract from score
# "negative" emojis will add to score
# "neutral"  emojis are ignored
# ─────────────────────────────────────────────
EMOJI_SENTIMENT: dict[str, str] = {

    # ── Positive ──────────────────────────────
    # Smiles & Laughter
    "smiling_face": "positive",
    "grinning_face": "positive",
    "beaming_face_with_smiling_eyes": "positive",
    "grinning_face_with_big_eyes": "positive",
    "grinning_face_with_smiling_eyes": "positive",
    "grinning_squinting_face": "positive",
    "face_with_tears_of_joy": "positive",
    "rolling_on_the_floor_laughing": "positive",
    "slightly_smiling_face": "positive",
    "winking_face": "positive",
    "smiling_face_with_halo": "positive",
    # Affection & Love
    "smiling_face_with_heart_eyes": "positive",
    "smiling_face_with_hearts": "positive",
    "face_blowing_a_kiss": "positive",
    "kissing_face": "positive",
    "kissing_face_with_smiling_eyes": "positive",
    "kissing_face_with_closed_eyes": "positive",
    "red_heart": "positive",
    "sparkling_heart": "positive",
    "growing_heart": "positive",
    "heart_with_arrow": "positive",
    "revolving_hearts": "positive",
    "two_hearts": "positive",
    "heart_exclamation": "positive",
    "orange_heart": "positive",
    "yellow_heart": "positive",
    "green_heart": "positive",
    "blue_heart": "positive",
    "purple_heart": "positive",
    # Cool & Confidence
    "smiling_face_with_sunglasses": "positive",
    "star_struck": "positive",
    "partying_face": "positive",
    "hugging_face": "positive",
    "cowboy_hat_face": "positive",
    # Approval & Celebration
    "thumbs_up": "positive",
    "clapping_hands": "positive",
    "raising_hands": "positive",
    "folded_hands": "positive",
    "victory_hand": "positive",
    "ok_hand": "positive",
    "fire": "positive",
    "sparkles": "positive",
    "party_popper": "positive",
    "trophy": "positive",
    "glowing_star": "positive",
    "hundred_points": "positive",
    "check_mark_button": "positive",
    "rocket": "positive",
    "musical_notes": "positive",

    # ── Negative ──────────────────────────────
    # Sadness & Disappointment
    "worried_face": "negative",
    "slightly_worried_face": "negative",
    "crying_face": "negative",
    "loudly_crying_face": "negative",
    "disappointed_face": "negative",
    "pensive_face": "negative",
    "downcast_face_with_sweat": "negative",
    "sad_but_relieved_face": "negative",
    "pleading_face": "negative",
    "broken_heart": "negative",
    # Anger & Frustration
    "angry_face": "negative",
    "enraged_face": "negative",
    "face_with_symbols_on_mouth": "negative",
    "pouting_face": "negative",
    "triumph_face": "negative",
    # Fear & Anxiety
    "fearful_face": "negative",
    "anxious_face_with_sweat": "negative",
    "screaming_in_fear": "negative",
    "flushed_face": "negative",
    "dizzy_face": "negative",
    "nauseated_face": "negative",
    "face_vomiting": "negative",
    # Confusion & Discomfort
    "confused_face": "negative",
    "face_with_raised_eyebrow": "negative",
    "unamused_face": "negative",
    "grimacing_face": "negative",
    "lying_face": "negative",
    # Disapproval
    "thumbs_down": "negative",
    "cross_mark": "negative",
    "skull": "negative",
    "heavy_exclamation_mark": "negative",
    "prohibited": "negative",
    "pile_of_poo": "negative",

    # ── Neutral ───────────────────────────────
    "neutral_face": "neutral",
    "expressionless_face": "neutral",
    "face_without_mouth": "neutral",
    "dotted_line_face": "neutral",
    "zipper_mouth_face": "neutral",
    "thinking_face": "neutral",
    "face_with_monocle": "neutral",
    "shushing_face": "neutral",
    "face_with_hand_over_mouth": "neutral",
    "raised_eyebrow": "neutral",
    "sleepy_face": "neutral",
    "sleeping_face": "neutral",
    "yawning_face": "neutral",
    "tired_face": "neutral",
    "smirking_face": "neutral",
    "face_in_clouds": "neutral",
    "relieved_face": "neutral",
    "shrugging": "neutral",
    "eyes": "neutral",
    "eye": "neutral",
    "wave": "neutral",
    "call_me_hand": "neutral",
    "question_mark": "neutral",
}

# Weight added/subtracted when an emoji is detected
EMOJI_WEIGHT: int = 2

# Load lexicon from CSV (term → weight, negative = positive score, positive = negative score)
DEPRESSION_LEXICON: dict[str, int] = load_lexicon("../data/depression_lexicon.csv")
emoji_sentiment = EMOJI_SENTIMENT