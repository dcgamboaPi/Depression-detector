from preprocess_lexicon import load_lexicon

#DEPRESSION_LEXICON = {
#    "hopeless": 3, "useless": 3, "die": 5, "death": 5,
#    "sad": 1, "tired": 1, "alone": 2, "lonely": 2,
#    "no hope": 4, "cannot sleep": 2, "anxiety":3, 
#    "depression":5
#}

SUICIDE_PATTERNS = {
    "want to die": 7,
    "wish i was dead": 7,
    "don't want to live": 6,
    "life is pointless": 6
}

NEGATIONS = {"no", "not", "never", "dont", "cant", "wont", "don't", "won't", "can't"}

STOP_NEGATION = {"but", "however", "and", "yet"}

INTENSIFIERS = {
    "very": 1.5,
    "extremely": 2,
    "really": 1.3,
    "so": 1.3
}

DEPRESSION_LEXICON = load_lexicon("../data/depression_lexicon.xlsx")

