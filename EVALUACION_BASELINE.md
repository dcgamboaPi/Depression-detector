# Evaluación del modelo baseline

## 1. Objetivo
Evaluar el rendimiento del modelo baseline para entender su calidad usando métricas de clasificación.

## 2. Contexto
El proyecto actual no contiene un modelo entrenado serializado tipo sklearn/joblib, sino un baseline basado en reglas, puntuación y léxico.

## 3. Estado inicial de la feature
Se creó la estructura mínima para evaluar el baseline:
- carpeta `data`
- carpeta `results`
- archivo `src/evaluate_model.py`
- archivo `data/baseline_test.csv`

Durante la preparación se detectó que algunos archivos no aparecían en `git status`, por lo que fue necesario revisar las reglas de `.gitignore`.

## 4. Incidencia detectada
La carpeta `data/` estaba ignorada en `.gitignore`, por lo que el archivo `data/baseline_test.csv` no quedaba trazado por Git. Esto impedía versionar el dataset de prueba necesario para reproducir la evaluación.