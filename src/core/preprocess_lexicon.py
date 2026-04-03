import pandas as pd


def load_lexicon(path: str) -> dict[str, int | float]:
    """
    Load the depression lexicon from a CSV or Excel file into a
    {term: weight} dictionary.

    Positive-sentiment rows carry negative weights in the CSV
    (they were stored that way intentionally so they subtract
    from the depression score when matched).

    Rows from the 'self_focus' category are excluded because
    first-person pronouns are too frequent and noisy to score
    on their own; they should be evaluated at the corpus level.

    Parameters
    ----------
    path : str
        Path to the lexicon file (.csv or .xlsx).

    Returns
    -------
    dict[str, int | float]
        Mapping of term/phrase → weight.
    """
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path, sheet_name="Lexicon")

    df = df[df["category"] != "self_focus"].copy()

    df["term_or_phrase"] = df["term_or_phrase"].str.lower().str.strip()
    df["weight_1_to_5"] = pd.to_numeric(df["weight_1_to_5"], errors="coerce").fillna(0)

    return dict(zip(df["term_or_phrase"], df["weight_1_to_5"]))
