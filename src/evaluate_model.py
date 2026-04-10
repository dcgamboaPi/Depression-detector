import pandas as pd
import sys
sys.path.insert(0, '.')
from model import analyze

# 1. Cargar datos
df = pd.read_csv("../data/Mental-Health-Twitter.csv")

# 2. Función que extrae los scores
def get_scores(text):
    result = analyze(str(text))
    return pd.Series({
        "raw_score": result.raw_score,
        "depression_level": result.depression.level,
        "suicide_risk": result.suicide.risk
    })

# 3. Aplicar a toda la columna (eficiente)
df[["raw_score", "depression_level", "suicide_risk"]] = df["post_text"].apply(get_scores)

# 4. Guardar resultado
df.to_csv("../data/output_scores.csv", index=False)
print("✅ Hecho! Filas procesadas:", len(df))

# 5. Resumen
print("Distribución de niveles de depresión:")
print(df["depression_level"].value_counts())
print("Distribución de riesgo de suicidio:")
print(df["suicide_risk"].value_counts())