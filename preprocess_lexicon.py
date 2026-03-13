import pandas as pd

def load_lexicon(path):

    df = pd.read_excel(path, sheet_name="Lexicon")
    subset = df[df["category"] != "self_focus"].copy()

    # normalizar texto
    subset["term_or_phrase"] = subset["term_or_phrase"].str.lower().str.strip()

    # crear diccionario palabra -> peso
    lexicon = dict(zip(subset["term_or_phrase"], subset["weight_1_to_5"]))

    return lexicon