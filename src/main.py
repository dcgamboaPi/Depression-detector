import kagglehub
import pandas as pd

from core.model import analyze
from core.preprocessing import normalize_text
from services.openai_service import extract_diagnostico
from utils.aggredate import build_user_features

pd.set_option("display.max_colwidth", None)

# Descargar y leer dataset
path = kagglehub.dataset_download("infamouscoder/mental-health-social-media")
df_depression = pd.read_csv(f"{path}/Mental-Health-Twitter.csv")

# Método 1 — lexicón
df_depression["text_normalize"] = df_depression["post_text"].apply(normalize_text)
df_depression["score"] = df_depression["post_text"].apply(lambda t: analyze(t).raw_score)

# Método 2 — LLM
df_sample = df_depression.tail(20).copy()
df_sample["openai"] = df_sample["post_text"].apply(extract_diagnostico)




df_depression["timestamp"] = pd.to_datetime(df_depression["post_created"])
df_depression["hour"]      = df_depression["timestamp"].dt.hour
df_depression["dayofweek"] = df_depression["timestamp"].dt.dayofweek


user_features = df_depression.groupby("user_id").apply(build_user_features).reset_index()
print(user_features.head(10))

user_features.to_excel("prueba.xlsx")