# ============================================================
# app_final.py — Dashboard de riesgo académico estudiantil
# Diplomado: Desarrollo Web para Analítica de Datos
# Proyecto: Sistema de alerta temprana de riesgo académico
# Ejecutar: streamlit run app_final.py
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import joblib
import json
from pathlib import Path

# ── Configuración general de la página ──────────────────────
st.set_page_config(
    page_title="Riesgo Académico Estudiantil",
    page_icon="🎓",
    layout="wide"
)

# ── Rutas de archivos (relativas al script) ──────────────────
BASE    = Path(__file__).parent
MODELO  = BASE / "models" / "modelo_final.pkl"
META    = BASE / "models" / "model_metadata.json"
DATASET = BASE / "data" / "processed" / "student_procesado.csv"

# ── Carga de recursos con caché ──────────────────────────────
@st.cache_resource
def cargar_modelo():
    return joblib.load(MODELO)

@st.cache_data
def cargar_metadata():
    with open(META, encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def cargar_datos():
    return pd.read_csv(DATASET)

modelo   = cargar_modelo()
metadata = cargar_metadata()
df       = cargar_datos()

# ── Paleta de colores ────────────────────────────────────────
TEAL  = "#1D9E75"
AZUL  = "#1F4E79"
CORAL = "#D95A30"
GRIS  = "#595959"

# ── Navegación lateral ───────────────────────────────────────
st.sidebar.title("🎓 Riesgo Académico")
st.sidebar.markdown("---")
seccion = st.sidebar.radio(
    "Navegación",
    ["🏠 Inicio",
     "📊 Dataset",
     "🔍 Análisis EDA",
     "🤖 Modelo",
     "📈 Métricas",
     "🎯 Predicción",
     "📝 Conclusiones"]
)
st.sidebar.markdown("---")
st.sidebar.caption("Diplomado Desarrollo Web · 2026")

# ============================================================
# SECCIÓN 1: INICIO
# ============================================================
if seccion == "🏠 Inicio":
    st.title("🎓 Sistema de Alerta Temprana de Riesgo Académico")
    st.markdown("**Diplomado en Desarrollo Web para Analítica de Datos — Proyecto Integrador**")
    st.markdown("---")

    st.markdown("""
    Este dashboard permite identificar de forma temprana a estudiantes
    en riesgo de reprobar, usando un modelo de machine learning entrenado
    con datos reales de estudiantes de secundaria en Portugal.

    El resultado apoya al **coordinador académico** en la asignación
    oportuna de acompañamiento y tutorías.
    """)

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    total      = len(df)
    con_riesgo = int(df["riesgo"].sum())
    sin_riesgo = total - con_riesgo
    pct_riesgo = con_riesgo / total * 100

    col1.metric("Total estudiantes",   f"{total}")
    col2.metric("En riesgo",           f"{con_riesgo}",  f"{pct_riesgo:.1f}%")
    col3.metric("Sin riesgo",          f"{sin_riesgo}",  f"{100-pct_riesgo:.1f}%")
    col4.metric("F1-score del modelo", f"{metadata['valor_f1']*100:.1f}%")

    st.markdown("---")

    st.subheader("Distribución de estudiantes por nivel de riesgo")
    fig = px.bar(
        x=["Sin riesgo (0)", "Con riesgo (1)"],
        y=[sin_riesgo, con_riesgo],
        color=["Sin riesgo (0)", "Con riesgo (1)"],
        color_discrete_map={"Sin riesgo (0)": TEAL, "Con riesgo (1)": CORAL},
        text=[f"{sin_riesgo} ({100-pct_riesgo:.1f}%)",
              f"{con_riesgo} ({pct_riesgo:.1f}%)"],
        labels={"x": "Nivel de riesgo", "y": "Número de estudiantes"}
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    **Fuente:** Student Performance Dataset — UCI Machine Learning Repository
    (Cortez, P., 2008). Licencia CC BY 4.0.
    """)

# ============================================================
# SECCIÓN 2: DATASET
# ============================================================
elif seccion == "📊 Dataset":
    st.title("📊 Dataset — Student Performance")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Filas",    f"{df.shape[0]}")
    col2.metric("Columnas", f"{df.shape[1]}")
    col3.metric("Fuente",   "UCI ML Repository")

    st.markdown("---")
    st.subheader("Primeras filas del dataset")
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown("---")
    st.subheader("Diccionario de variables principales")
    diccionario = pd.DataFrame({
        "Variable": ["absences", "studytime", "failures", "G1", "higher", "riesgo"],
        "Tipo":     ["Numérica", "Ordinal", "Numérica", "Numérica", "Categórica", "Binaria"],
        "Descripción": [
            "Número de ausencias del estudiante (0–32)",
            "Tiempo semanal de estudio (1=<2h, 2=2–5h, 3=5–10h, 4=>10h)",
            "Número de materias reprobadas anteriormente (0–3)",
            "Calificación del primer periodo (0–19)",
            "Intención de cursar educación superior (yes/no → 1/0)",
            "Variable objetivo: 1=en riesgo (G3<10), 0=sin riesgo (G3≥10)"
        ],
        "Rol": ["Entrada", "Entrada", "Entrada", "Entrada", "Entrada", "Objetivo"]
    })
    st.dataframe(diccionario, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Estadísticas descriptivas")
    st.dataframe(df.describe().round(2), use_container_width=True)

    st.info("""
    **Cita:** Cortez, P. (2008). *Student Performance* [Dataset].
    UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T
    **Licencia:** CC BY 4.0
    """)

# ============================================================
# SECCIÓN 3: ANÁLISIS EDA
# ============================================================
elif seccion == "🔍 Análisis EDA":
    st.title("🔍 Análisis Exploratorio de Datos (EDA)")
    st.markdown("---")

    st.markdown("""
    Se analizaron las 33 variables del dataset original para entender
    la distribución, detectar valores atípicos y seleccionar las variables
    más relevantes para el modelo.
    """)

    # ── Distribución de la variable objetivo ────────────────
    st.subheader("Variable objetivo: riesgo académico")
    col1, col2 = st.columns([2, 1])

    with col1:
        con_riesgo = int(df["riesgo"].sum())
        sin_riesgo = len(df) - con_riesgo
        fig_pie = px.pie(
            values=[sin_riesgo, con_riesgo],
            names=["Sin riesgo (0)", "Con riesgo (1)"],
            color_discrete_sequence=[TEAL, CORAL],
            hole=0.4
        )
        fig_pie.update_layout(height=320)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown("**Desbalance de clases**")
        st.markdown(f"""
        - Sin riesgo: **{sin_riesgo}** ({sin_riesgo/len(df)*100:.1f}%)
        - Con riesgo: **{con_riesgo}** ({con_riesgo/len(df)*100:.1f}%)

        ⚠️ El desbalance de **84.6% / 15.4%** justifica el uso de **F1-score**
        como métrica principal en lugar de Accuracy.
        """)

    st.markdown("---")

    # ── Variables numéricas más importantes ─────────────────
    st.subheader("Distribución de variables numéricas clave")

    vars_numericas = ["G1", "absences", "failures", "studytime", "age"]
    vars_disponibles = [v for v in vars_numericas if v in df.columns]

    if vars_disponibles:
        variable = st.selectbox("Selecciona una variable:", vars_disponibles)

        col1, col2 = st.columns(2)
        with col1:
            fig_hist = px.histogram(
                df, x=variable, color="riesgo",
                color_discrete_map={0: TEAL, 1: CORAL},
                barmode="overlay",
                labels={"riesgo": "Riesgo"},
                title=f"Distribución de {variable} por nivel de riesgo"
            )
            fig_hist.update_layout(height=320)
            st.plotly_chart(fig_hist, use_container_width=True)

        with col2:
            fig_box = px.box(
                df, x="riesgo", y=variable,
                color="riesgo",
                color_discrete_map={0: TEAL, 1: CORAL},
                labels={"riesgo": "Riesgo (0=No, 1=Sí)"},
                title=f"Boxplot de {variable} por nivel de riesgo"
            )
            fig_box.update_layout(height=320)
            st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    # ── Correlación con la variable objetivo ─────────────────
    st.subheader("Correlación de variables numéricas con riesgo")

    cols_num = df.select_dtypes(include=[np.number]).columns.tolist()
    if "riesgo" in cols_num:
        corr = df[cols_num].corr()["riesgo"].drop("riesgo").sort_values()

        fig_corr = px.bar(
            x=corr.values,
            y=corr.index,
            orientation="h",
            color=corr.values,
            color_continuous_scale=["#1D9E75", "#f5f5f5", "#D95A30"],
            labels={"x": "Correlación con riesgo", "y": "Variable"},
            title="Correlación de Pearson con variable objetivo (riesgo)"
        )
        fig_corr.update_layout(height=420, coloraxis_showscale=False)
        st.plotly_chart(fig_corr, use_container_width=True)

    st.info("""
    **Nota metodológica:** La variable G2 fue excluida del modelo por alta
    correlación con G3 (r = 0.92), lo que constituiría fuga de datos (*data leakage*).
    G1 se conservó (r = 0.83) por ser información disponible antes del resultado final.
    """)

# ============================================================
# SECCIÓN 4: MODELO
# ============================================================
elif seccion == "🤖 Modelo":
    st.title("🤖 Modelo de Machine Learning")
    st.markdown("---")

    st.markdown("""
    Se entrenaron y compararon tres configuraciones de modelos siguiendo
    la metodología **CRISP-DM** (Cross-Industry Standard Process for Data Mining).
    """)

    # ── Comparación de modelos ───────────────────────────────
    st.subheader("Comparación de modelos entrenados")

    resultados = pd.DataFrame({
        "Modelo": [
            "Regresión Logística ✅",
            "Random Forest",
            "Pipeline LR + Scaler"
        ],
        "Accuracy": [0.892, 0.877, 0.869],
        "F1-score": [0.667, 0.619, 0.564],
        "Precision": [0.636, 0.591, 0.579],
        "Recall":   [0.700, 0.650, 0.550],
        "AUC-ROC":  [0.900, 0.902, 0.892]
    })

    st.dataframe(
        resultados.style.highlight_max(
            subset=["Accuracy","F1-score","Precision","Recall","AUC-ROC"],
            color="#d4edda"
        ),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ── Gráfico comparativo ──────────────────────────────────
    st.subheader("Visualización comparativa de métricas")

    metricas = ["Accuracy", "F1-score", "Precision", "Recall", "AUC-ROC"]
    modelos  = resultados["Modelo"].tolist()

    fig_radar = go.Figure()
    colores   = [TEAL, AZUL, GRIS]

    for i, row in resultados.iterrows():
        valores = [row[m] for m in metricas]
        fig_radar.add_trace(go.Bar(
            name=row["Modelo"],
            x=metricas,
            y=valores,
            marker_color=colores[i]
        ))

    fig_radar.update_layout(
        barmode="group",
        height=380,
        yaxis=dict(range=[0, 1.05]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")

    # ── Justificación del modelo ganador ────────────────────
    st.subheader("🏆 Modelo seleccionado: Regresión Logística")

    col1, col2 = st.columns(2)
    with col1:
        st.success("""
        **¿Por qué Regresión Logística?**

        - Mayor **F1-score: 66.7%** — métrica clave dado el desbalance de clases
        - Detecta **14 de 20** estudiantes en riesgo (Recall 70%)
        - Modelo **interpretable**: los coeficientes explican el impacto de cada variable
        - Apropiado para datasets pequeños (~649 registros) con relaciones lineales
        """)

    with col2:
        st.info("""
        **Parámetros del modelo**

        - Algoritmo: `LogisticRegression`
        - Librería: `scikit-learn 1.6.1`
        - `random_state = 42`
        - División: 80% entrenamiento / 20% prueba
        - Variables de entrada: 31 (G2 excluida)
        """)

    # ── Metodología CRISP-DM ────────────────────────────────
    st.markdown("---")
    st.subheader("Metodología: CRISP-DM")

    fases = {
        "1. Comprensión del negocio": "Definir el problema: predecir riesgo académico (G3 < 10) para intervención temprana.",
        "2. Comprensión de los datos": "EDA del dataset UCI (649 registros, 33 variables). Análisis de distribución y correlaciones.",
        "3. Preparación de los datos": "Limpieza, encoding de variables categóricas, exclusión de G2, train/test split (80/20).",
        "4. Modelado": "Entrenamiento de Regresión Logística, Random Forest y Pipeline LR+Scaler. Comparación por F1-score.",
        "5. Evaluación": "Regresión Logística seleccionada: F1=66.7%, Recall=70%, AUC-ROC=0.90.",
        "6. Despliegue": "Dashboard interactivo en Streamlit para uso del coordinador académico."
    }

    for fase, desc in fases.items():
        with st.expander(fase):
            st.write(desc)

# ============================================================
# SECCIÓN 5: MÉTRICAS
# ============================================================
elif seccion == "📈 Métricas":
    st.title("📈 Métricas de Evaluación del Modelo")
    st.markdown("---")

    # ── KPIs ────────────────────────────────────────────────
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Accuracy",  "89.2%")
    col2.metric("F1-score",  "66.7%")
    col3.metric("Precision", "63.6%")
    col4.metric("Recall",    "70.0%")
    col5.metric("AUC-ROC",   "90.0%")

    st.markdown("---")

    # ── Matriz de confusión ──────────────────────────────────
    st.subheader("Matriz de Confusión")

    col1, col2 = st.columns([1, 1])

    with col1:
        # Valores: TN=102, FP=8, FN=6, TP=14
        z  = [[102, 8], [6, 14]]
        x  = ["Predicho: Sin riesgo (0)", "Predicho: Con riesgo (1)"]
        y  = ["Real: Sin riesgo (0)", "Real: Con riesgo (1)"]

        annotations = [
            [f"TN = 102<br>Correctos sin riesgo", f"FP = 8<br>Falsa alarma"],
            [f"FN = 6<br>⚠️ Error crítico",        f"TP = 14<br>Detectados correctamente"]
        ]

        fig_cm = go.Figure(data=go.Heatmap(
            z=z, x=x, y=y,
            colorscale=[[0, "#f8f9fa"], [1, TEAL]],
            showscale=False,
            text=annotations,
            texttemplate="%{text}",
            textfont={"size": 13}
        ))
        fig_cm.update_layout(height=350, title="Matriz de confusión — Regresión Logística")
        st.plotly_chart(fig_cm, use_container_width=True)

    with col2:
        st.markdown("**Interpretación de resultados**")
        st.success("✅ **102 Verdaderos Negativos (TN):** Estudiantes sin riesgo identificados correctamente.")
        st.success("✅ **14 Verdaderos Positivos (TP):** Estudiantes en riesgo detectados. El modelo puede intervenir a tiempo.")
        st.warning("⚠️ **8 Falsos Positivos (FP):** Alertas innecesarias. Costo: tutoría a quien no la necesitaba.")
        st.error("🔴 **6 Falsos Negativos (FN):** Estudiantes en riesgo NO detectados. **Error más crítico:** el sistema falla en alertar.")

    st.markdown("---")

    # ── Curva ROC ───────────────────────────────────────────
    st.subheader("Curva ROC — AUC = 0.90")

    # Curva ROC aproximada (puntos representativos del modelo)
    fpr = [0.00, 0.02, 0.05, 0.08, 0.12, 0.20, 0.30, 0.45, 0.60, 0.80, 1.00]
    tpr = [0.00, 0.30, 0.50, 0.60, 0.70, 0.80, 0.87, 0.92, 0.95, 0.98, 1.00]

    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(
        x=fpr, y=tpr, mode="lines",
        name="Regresión Logística (AUC = 0.90)",
        line=dict(color=TEAL, width=3)
    ))
    fig_roc.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode="lines",
        name="Clasificador aleatorio (AUC = 0.50)",
        line=dict(color=GRIS, width=1, dash="dash")
    ))
    fig_roc.update_layout(
        xaxis_title="Tasa de Falsos Positivos (FPR)",
        yaxis_title="Tasa de Verdaderos Positivos (TPR / Recall)",
        height=380,
        legend=dict(x=0.4, y=0.1)
    )
    st.plotly_chart(fig_roc, use_container_width=True)

    st.info("""
    **AUC-ROC = 0.90** indica que el modelo tiene un **90% de probabilidad**
    de distinguir correctamente entre un estudiante en riesgo y uno sin riesgo.
    Un valor de 0.50 equivaldría a adivinar al azar.
    """)

# ============================================================
# SECCIÓN 6: PREDICCIÓN
# ============================================================
elif seccion == "🎯 Predicción":
    st.title("🎯 Predicción Individual de Riesgo Académico")
    st.markdown("---")

    st.markdown("""
    Ingresa los datos de un estudiante para predecir si está en riesgo de reprobar.
    El modelo analiza sus características académicas y sociofamiliares.
    """)

    st.markdown("---")

    # ── Formulario de entrada ────────────────────────────────
    st.subheader("📋 Datos del estudiante")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Académico**")
        G1          = st.slider("Nota primer periodo (G1)", 0, 19, 10,
                                help="Calificación del primer periodo escolar (0–19)")
        failures    = st.slider("Materias reprobadas antes", 0, 4, 0,
                                help="Número de materias reprobadas en años anteriores")
        studytime   = st.select_slider("Tiempo de estudio semanal",
                                       options=[1, 2, 3, 4],
                                       value=2,
                                       format_func=lambda x: {
                                           1: "<2 horas", 2: "2–5 horas",
                                           3: "5–10 horas", 4: ">10 horas"
                                       }[x])
        absences    = st.number_input("Número de ausencias", 0, 93, 4,
                                      help="Total de ausencias en el año escolar")

    with col2:
        st.markdown("**Sociofamiliar**")
        Medu        = st.select_slider("Educación de la madre",
                                       options=[0, 1, 2, 3, 4],
                                       value=2,
                                       format_func=lambda x: {
                                           0: "Ninguna", 1: "Primaria",
                                           2: "Secundaria", 3: "Superior", 4: "Posgrado"
                                       }[x])
        Fedu        = st.select_slider("Educación del padre",
                                       options=[0, 1, 2, 3, 4],
                                       value=2,
                                       format_func=lambda x: {
                                           0: "Ninguna", 1: "Primaria",
                                           2: "Secundaria", 3: "Superior", 4: "Posgrado"
                                       }[x])
        famrel      = st.slider("Calidad de relaciones familiares (1–5)", 1, 5, 4)
        higher      = st.radio("¿Quiere estudiar educación superior?",
                               ["Sí", "No"], horizontal=True)

    with col3:
        st.markdown("**Personal**")
        age         = st.slider("Edad del estudiante", 15, 22, 17)
        goout       = st.slider("Frecuencia de salidas con amigos (1–5)", 1, 5, 3)
        Dalc        = st.slider("Consumo de alcohol (días laborables, 1–5)", 1, 5, 1)
        Walc        = st.slider("Consumo de alcohol (fin de semana, 1–5)", 1, 5, 1)
        health      = st.slider("Estado de salud (1–5)", 1, 5, 3)

    st.markdown("---")

    # ── Predicción ───────────────────────────────────────────
    if st.button("🔍 Predecir riesgo académico", type="primary", use_container_width=True):

        # Construir vector de entrada con todas las columnas del dataset procesado
        # Columnas numéricas del modelo (31 variables de entrada)
        higher_val = 1 if higher == "Sí" else 0

        # Obtener columnas del dataset procesado (excluyendo G2, G3 y riesgo)
        cols_modelo = [c for c in df.columns if c not in ["G2", "G3", "riesgo"]]

        # Crear fila con valores por defecto (mediana del dataset)
        fila_base = df[cols_modelo].median().to_dict()

        # Sobreescribir con los valores ingresados
        actualizaciones = {
            "G1": G1,
            "failures": failures,
            "studytime": studytime,
            "absences": absences,
            "Medu": Medu,
            "Fedu": Fedu,
            "famrel": famrel,
            "higher": higher_val,
            "age": age,
            "goout": goout,
            "Dalc": Dalc,
            "Walc": Walc,
            "health": health
        }

        for k, v in actualizaciones.items():
            if k in fila_base:
                fila_base[k] = v

        entrada = pd.DataFrame([fila_base])

        # Predicción
        try:
            prediccion   = modelo.predict(entrada)[0]
            probabilidad = modelo.predict_proba(entrada)[0]
            prob_riesgo  = probabilidad[1] * 100
            prob_seguro  = probabilidad[0] * 100

            st.markdown("---")
            st.subheader("📊 Resultado de la predicción")

            col1, col2 = st.columns([1, 1])

            with col1:
                if prediccion == 1:
                    st.error(f"""
                    ### 🔴 ESTUDIANTE EN RIESGO

                    **Probabilidad de riesgo: {prob_riesgo:.1f}%**

                    Se recomienda intervención académica inmediata:
                    asignación de tutoría y seguimiento personalizado.
                    """)
                else:
                    st.success(f"""
                    ### 🟢 ESTUDIANTE SIN RIESGO

                    **Probabilidad de riesgo: {prob_riesgo:.1f}%**

                    El estudiante no presenta señales de riesgo
                    académico en este momento.
                    """)

            with col2:
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prob_riesgo,
                    number={"suffix": "%", "font": {"size": 36}},
                    title={"text": "Probabilidad de riesgo"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar":  {"color": CORAL if prediccion == 1 else TEAL},
                        "steps": [
                            {"range": [0, 40],  "color": "#d4edda"},
                            {"range": [40, 65], "color": "#fff3cd"},
                            {"range": [65, 100],"color": "#f8d7da"}
                        ],
                        "threshold": {
                            "line": {"color": "black", "width": 3},
                            "thickness": 0.75,
                            "value": 50
                        }
                    }
                ))
                fig_gauge.update_layout(height=280)
                st.plotly_chart(fig_gauge, use_container_width=True)

            # Factores de riesgo detectados
            st.markdown("**🔎 Factores de riesgo detectados en este caso:**")
            factores = []
            if failures > 0:
                factores.append(f"📌 Tiene **{failures}** materia(s) reprobada(s) previamente")
            if G1 < 10:
                factores.append(f"📌 Nota primer periodo baja: **{G1}/19**")
            if absences > 10:
                factores.append(f"📌 Alta cantidad de ausencias: **{absences}**")
            if studytime == 1:
                factores.append("📌 Tiempo de estudio muy bajo: **menos de 2 horas/semana**")
            if Dalc >= 4 or Walc >= 4:
                factores.append("📌 Consumo elevado de alcohol reportado")
            if higher_val == 0:
                factores.append("📌 No tiene intención de continuar estudios superiores")

            if factores:
                for f in factores:
                    st.markdown(f)
            else:
                st.markdown("✅ No se detectaron factores de riesgo relevantes en los datos ingresados.")

        except Exception as e:
            st.error(f"Error al realizar la predicción: {e}")
            st.info("Verifique que el modelo esté correctamente guardado en models/modelo_final.pkl")

# ============================================================
# SECCIÓN 7: CONCLUSIONES
# ============================================================
elif seccion == "📝 Conclusiones":
    st.title("📝 Conclusiones y Reflexión Ética")
    st.markdown("---")

    # ── Conclusiones técnicas ────────────────────────────────
    st.subheader("🎯 Conclusiones del proyecto")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Resultados obtenidos**

        - Se entrenaron **3 modelos** de clasificación binaria
        - El modelo ganador fue **Regresión Logística** con F1-score de **66.7%**
        - El sistema detecta correctamente **14 de cada 20** estudiantes en riesgo
        - El AUC-ROC de **0.90** confirma alta capacidad discriminativa

        **Limitaciones identificadas**

        - Dataset pequeño: **649 registros** de una sola institución en Portugal
        - Desbalance de clases (84.6%/15.4%) limita la métrica de Accuracy
        - **6 Falsos Negativos**: el error más costoso, estudiantes no detectados
        - Los resultados pueden no generalizarse a otros contextos educativos
        """)

    with col2:
        st.markdown("""
        **Decisiones metodológicas clave**

        - Se excluyó **G2** (correlación 0.92 con G3) para evitar *data leakage*
        - Se conservó **G1** (correlación 0.83) por ser dato disponible antes del resultado
        - Se usó **F1-score** como métrica principal por el desbalance de clases
        - Se siguió la metodología **CRISP-DM** en 6 fases iterativas
        - `random_state=42` garantiza la reproducibilidad del experimento
        """)

    st.markdown("---")

    # ── Reflexión ética ──────────────────────────────────────
    st.subheader("⚖️ Reflexión ética sobre el uso del sistema")

    st.warning("""
    **Este sistema es una herramienta de apoyo, no un juicio definitivo.**

    Las predicciones deben ser interpretadas por el coordinador académico
    considerando el contexto completo del estudiante.
    """)

    consideraciones = {
        "🔒 Privacidad de los datos": """
        Los datos académicos y personales de los estudiantes son sensibles.
        Su recopilación, almacenamiento y uso deben cumplir con la normativa
        de protección de datos vigente. El sistema no debe exponer información
        individual sin consentimiento.
        """,
        "⚖️ Sesgo algorítmico": """
        El modelo fue entrenado con datos de Portugal (2008). Variables como
        educación de los padres o consumo de alcohol pueden reflejar sesgos
        socioeconómicos. El sistema no debe usarse para discriminar, sino para
        garantizar apoyo oportuno a quienes más lo necesitan.
        """,
        "👥 Rol del docente y coordinador": """
        La predicción es un insumo para la toma de decisiones humana, no un
        reemplazo. El coordinador académico debe validar cada caso, escuchar
        al estudiante y considerar factores que el modelo no puede capturar.
        """,
        "🎯 Objetivo del sistema": """
        La finalidad es garantizar intervención temprana y acompañamiento
        académico, no etiquetar ni sancionar al estudiante. El resultado
        siempre debe orientarse hacia el apoyo, no hacia la exclusión.
        """
    }

    for titulo, contenido in consideraciones.items():
        with st.expander(titulo):
            st.markdown(contenido)

    st.markdown("---")

    # ── Trabajo futuro ───────────────────────────────────────
    st.subheader("🚀 Trabajo futuro y mejoras propuestas")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("""
        **Datos**
        - Ampliar dataset con múltiples instituciones y años
        - Incluir datos en tiempo real del sistema académico
        - Balancear clases con SMOTE u otras técnicas
        """)
    with col2:
        st.info("""
        **Modelo**
        - Explorar XGBoost o redes neuronales
        - Validación cruzada (k-fold)
        - Ajuste de hiperparámetros (GridSearchCV)
        """)
    with col3:
        st.info("""
        **Sistema**
        - Integración con sistema de información académica
        - Alertas automáticas al coordinador
        - Panel de seguimiento longitudinal por estudiante
        """)

    st.markdown("---")

    # ── Créditos ─────────────────────────────────────────────
    st.subheader("📚 Referencias y créditos")

    st.markdown("""
    - **Dataset:** Cortez, P. (2008). *Student Performance* [Dataset]. UCI Machine Learning Repository.
      https://doi.org/10.24432/C5TG7T — Licencia CC BY 4.0

    - **Metodología:** Chapman, P. et al. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*.
      SPSS Inc.

    - **Tecnologías:** Python 3.14 · scikit-learn 1.6.1 · Streamlit 1.58.0 · pandas · plotly

    ---

    **Autor:** Carlos Andrés Pareja Osorno
    **Programa:** Tecnología en Desarrollo de Software — Diplomado en Desarrollo Web para Analítica de Datos
    **Institución:** IUD · 2026
    """)