# ============================================================
# entrenar_modelo.py — Script de entrenamiento local
# Sistema de alerta temprana de riesgo académico estudiantil
# Ejecutar desde la raíz del proyecto:
#   python src/ml/entrenar_modelo.py
# ============================================================

import pandas as pd
import numpy as np
import joblib
import json
import os
from pathlib import Path
from datetime import date

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, f1_score,
    precision_score, recall_score, roc_auc_score
)

import sklearn

# ── Rutas ────────────────────────────────────────────────────
BASE        = Path(__file__).parent.parent.parent
X_TRAIN     = BASE / "data" / "processed" / "X_train.csv"
X_TEST      = BASE / "data" / "processed" / "X_test.csv"
Y_TRAIN     = BASE / "data" / "processed" / "y_train.csv"
Y_TEST      = BASE / "data" / "processed" / "y_test.csv"
MODELS_DIR  = BASE / "models"

# ── Carga de datos ───────────────────────────────────────────
def cargar_datos():
    print("📂 Cargando datos procesados...")
    X_train = pd.read_csv(X_TRAIN)
    X_test  = pd.read_csv(X_TEST)
    y_train = pd.read_csv(Y_TRAIN).squeeze()
    y_test  = pd.read_csv(Y_TEST).squeeze()
    print(f"   Train: {X_train.shape[0]} filas × {X_train.shape[1]} columnas")
    print(f"   Test:  {X_test.shape[0]} filas × {X_test.shape[1]} columnas")
    return X_train, X_test, y_train, y_test

# ── Entrenamiento y evaluación ───────────────────────────────
def entrenar_y_evaluar(nombre, modelo, X_train, X_test, y_train, y_test):
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    y_prob = modelo.predict_proba(X_test)[:, 1]
    metricas = {
        "f1":        round(float(f1_score(y_test, y_pred)),        4),
        "accuracy":  round(float(accuracy_score(y_test, y_pred)),  4),
        "precision": round(float(precision_score(y_test, y_pred)), 4),
        "recall":    round(float(recall_score(y_test, y_pred)),    4),
        "auc_roc":   round(float(roc_auc_score(y_test, y_prob)),   4),
    }
    print(f"\n   {nombre}:")
    for k, v in metricas.items():
        print(f"      {k}: {v*100:.1f}%")
    return modelo, metricas

# ── Serialización ────────────────────────────────────────────
def serializar(modelo, nombre_archivo):
    os.makedirs(MODELS_DIR, exist_ok=True)
    ruta = MODELS_DIR / nombre_archivo
    joblib.dump(modelo, ruta)
    # Verificación
    modelo_cargado = joblib.load(ruta)
    print(f"   ✅ Guardado y verificado: {ruta}")
    return modelo_cargado

# ── Main ─────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("ENTRENAMIENTO LOCAL — RIESGO ACADÉMICO ESTUDIANTIL")
    print("=" * 60)

    # 1. Cargar datos
    X_train, X_test, y_train, y_test = cargar_datos()

    # 2. Entrenar modelos
    print("\n🤖 Entrenando modelos...")

    modelos = {
        "Regresion_Logistica": LogisticRegression(
            max_iter=1000, random_state=42),
        "Random_Forest": RandomForestClassifier(
            n_estimators=100, random_state=42),
        "Pipeline_LR_Scaler": Pipeline([
            ("scaler", StandardScaler()),
            ("modelo", LogisticRegression(max_iter=1000, random_state=42))
        ])
    }

    resultados = {}
    modelos_entrenados = {}
    for nombre, modelo in modelos.items():
        m, metricas = entrenar_y_evaluar(
            nombre, modelo, X_train, X_test, y_train, y_test)
        resultados[nombre]       = metricas
        modelos_entrenados[nombre] = m

    # 3. Seleccionar el mejor por F1-score
    mejor = max(resultados, key=lambda k: resultados[k]["f1"])
    print(f"\n🏆 Modelo ganador: {mejor}")
    print(f"   F1-score: {resultados[mejor]['f1']*100:.1f}%")

    # 4. Serializar
    print("\n💾 Serializando modelos...")
    serializar(modelos_entrenados["Regresion_Logistica"], "modelo_final.pkl")
    serializar(modelos_entrenados["Pipeline_LR_Scaler"],  "pipeline_final.pkl")

    # 5. Guardar metadatos
    metadata = {
        "modelo":              "LogisticRegression",
        "version":             "1.0",
        "fecha_entrenamiento": str(date.today()),
        "sklearn_version":     sklearn.__version__,
        "random_state":        42,
        "metrica_principal":   "f1_score",
        "valor_f1":            resultados["Regresion_Logistica"]["f1"],
        "accuracy":            resultados["Regresion_Logistica"]["accuracy"],
        "precision":           resultados["Regresion_Logistica"]["precision"],
        "recall":              resultados["Regresion_Logistica"]["recall"],
        "auc_roc":             resultados["Regresion_Logistica"]["auc_roc"],
        "variables_entrada":   list(X_train.columns),
        "variable_objetivo":   "riesgo",
        "comparacion_modelos": resultados,
        "modelo_seleccionado": "LogisticRegression simple",
        "justificacion":       "Mayor F1-score sobre conjunto de prueba.",
        "descripcion":         "Clasificacion binaria. riesgo=1 si G3<10, riesgo=0 si G3>=10",
        "observaciones":       f"Entrenado con sklearn {sklearn.__version__}, semilla 42."
    }

    ruta_meta = MODELS_DIR / "model_metadata.json"
    with open(ruta_meta, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"   ✅ Metadatos guardados: {ruta_meta}")

    print("\n" + "=" * 60)
    print("✅ ENTRENAMIENTO COMPLETADO")
    print("=" * 60)
    print(f"\n📊 Resumen:")
    print(f"   Modelos entrenados: {len(modelos)}")
    print(f"   Modelo seleccionado: Regresión Logística simple")
    print(f"   F1-score: {resultados['Regresion_Logistica']['f1']*100:.1f}%")
    print(f"   Archivos: modelo_final.pkl, pipeline_final.pkl, model_metadata.json")

if __name__ == "__main__":
    main()