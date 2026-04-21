import pandas as pd
import sys
from sklearn.metrics import confusion_matrix


sys.path.insert(0, '.')
from src.core.model import analyze
from src.services.openai_service import extract_diagnostico

# 1. Cargar datos
df = pd.read_csv("./data/Mental-Health-Twitter.csv")

# join users 

df_sorted = df.sort_values(by="post_created")

df_limited = df_sorted.groupby("user_id").tail(20)

df_user = df.groupby("user_id").agg({
    "post_text": " ".join,
    "label": "max"
}).reset_index()

# 2. Función que extrae los scores
def get_scores(text):
    result = analyze(str(text))
    return pd.Series({
        "raw_score": result.raw_score,
        "depression_level": result.depression.level,
        "suicide_risk": result.suicide.risk
    })

# 3. Aplicar a toda la columna (eficiente)
df_user[["raw_score", "depression_level", "suicide_risk"]] = df_user["post_text"].apply(get_scores)
df_user["pred_derpression"] = (df_user["raw_score"] > 0).astype(int)
df_user["openai"] = df_user["post_text"].apply(extract_diagnostico) 

cm1 = confusion_matrix(df_user["label"], df_user["pred_derpression"])
cm2 = confusion_matrix(df_user["label"], df_user["openai"])

# 4. Guardar resultado
df_user.to_csv("./data/output_scores.csv", index=False)
print("✅ Hecho! Filas procesadas:", len(df))

# 5. Resumen
print("Distribución de niveles de depresión:")
print(df_user["depression_level"].value_counts())
print("Distribución de riesgo de suicidio:")
print(df_user["suicide_risk"].value_counts())

print(df_user.head())

print(cm1)
print(cm2)
