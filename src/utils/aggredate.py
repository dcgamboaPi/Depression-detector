import pandas as pd
import numpy as np
from scipy import stats

def build_user_features(grp):
    grp = grp.sort_values("timestamp")
    scores = grp["score"]

    # ── Score stats ───────────────────────────────
    score_mean   = scores.mean()
    score_std    = scores.std(ddof=0)
    score_max    = scores.max()
    pct_high     = (scores > 4).mean()      # % tweets con señal depresiva

    # ── Tendencia temporal ────────────────────────
    # ¿El score sube (empeora) o baja (mejora) con el tiempo?
    if len(scores) >= 3:
        slope, *_ = stats.linregress(np.arange(len(scores)), scores.values)
    else:
        slope = 0.0

    # ── Comportamiento temporal ───────────────────
    pct_nocturnal = grp["hour"].between(0, 5).mean()   # % tweets de madrugada
    pct_weekend   = (grp["dayofweek"] >= 5).mean()

    # ── Silencio entre posts ──────────────────────
    gaps = grp["timestamp"].diff().dropna().dt.total_seconds() / 86400
    gap_mean = gaps.mean() if len(gaps) > 0 else 0
    gap_std  = gaps.std()  if len(gaps) > 1 else 0

    # ── Volumen ───────────────────────────────────
    n_tweets = len(grp)
    days_active = (grp["timestamp"].max() - grp["timestamp"].min()).days + 1
    tweets_per_day = n_tweets / days_active

    return pd.Series({
        "score_mean":      score_mean,
        "score_std":       score_std,
        "score_max":       score_max,
        "score_trend":     slope,           # + empeora, - mejora
        "pct_high":        pct_high,
        "pct_nocturnal":   pct_nocturnal,
        "pct_weekend":     pct_weekend,
        "gap_mean":        gap_mean,        # días entre posts
        "gap_std":         gap_std,         # irregularidad
        "tweets_per_day":  tweets_per_day,
        "label":           grp["label"].iloc[0],
    })