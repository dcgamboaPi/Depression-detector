import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# 1. Cargar resultados
df = pd.read_csv("../data/output_scores.csv")

# 2. Convertir a binario
df["pred_binary"] = df["depression_level"].apply(
    lambda x: 0 if x in ["positive", "none"] else 1
)

# 3. Métricas numéricas
print("=== ACCURACY ===")
print(accuracy_score(df["label"], df["pred_binary"]))

print("\n=== PRECISION, RECALL, F1 ===")
print(classification_report(df["label"], df["pred_binary"]))

print("\n=== MATRIZ DE CONFUSIÓN ===")
print(confusion_matrix(df["label"], df["pred_binary"]))

# 4. Matriz de confusión visual
cm = confusion_matrix(df["label"], df["pred_binary"])
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["No depresión", "Depresión"],
            yticklabels=["No depresión", "Depresión"])
plt.xlabel("Predicho")
plt.ylabel("Real")
plt.title("Matriz de Confusión - Depression Detector")
plt.tight_layout()
plt.show()