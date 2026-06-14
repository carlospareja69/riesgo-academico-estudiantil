# Arquitectura del Sistema — Riesgo Académico Estudiantil

**Proyecto:** Sistema de alerta temprana de riesgo académico estudiantil  
**Autor:** Carlos Andrés Pareja Osorno  
**Fecha:** Junio 2026  

---

## 1. Descripción general

El sistema está compuesto por tres capas principales que siguen la metodología **CRISP-DM**:
[Datos crudos] → [Pipeline de preparación] → [Modelo ML] → [Dashboard Streamlit]

---

## 2. Componentes del sistema

### Capa 1 — Datos
| Componente | Archivo | Descripción |
|---|---|---|
| Dataset original | `data/raw/student-por.csv` | Datos crudos sin modificar (649 registros, 33 variables) |
| Dataset procesado | `data/processed/student_procesado.csv` | Dataset limpio con encoding y variable objetivo |
| Conjuntos train/test | `data/processed/X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv` | División 80/20 estratificada |

### Capa 2 — Modelos
| Componente | Archivo | Descripción |
|---|---|---|
| Modelo final | `models/modelo_final.pkl` | Regresión Logística serializada con joblib |
| Pipeline | `models/pipeline_final.pkl` | Pipeline con StandardScaler + Regresión Logística |
| Metadatos | `models/model_metadata.json` | Métricas, versiones y comparación de modelos |

### Capa 3 — Dashboard
| Componente | Archivo | Descripción |
|---|---|---|
| Aplicación web | `app_final.py` | Dashboard Streamlit con 7 secciones |

---

## 3. Flujo de datos
student-por.csv (raw)

↓

Notebook 02: limpieza + encoding + train/test split

↓

student_procesado.csv + X_train/X_test/y_train/y_test

↓

Notebook 03: entrenamiento + evaluación + serialización

↓

modelo_final.pkl + model_metadata.json

↓

app_final.py (Dashboard Streamlit)

↓

Usuario: Coordinador académico

---

## 4. Tecnologías utilizadas

| Capa | Tecnología | Versión | Uso |
|---|---|---|---|
| Lenguaje | Python | 3.14 | Base del proyecto |
| Manipulación de datos | pandas | 2.2.2 | Carga y transformación |
| Modelado | scikit-learn | 1.6.1 | Entrenamiento y evaluación |
| Serialización | joblib | — | Guardar/cargar el modelo |
| Visualización | matplotlib, plotly | — | Gráficas en notebook y dashboard |
| Dashboard | Streamlit | 1.58.0 | Interfaz web interactiva |
| Control de versiones | Git / GitHub | — | Repositorio del proyecto |
| Entorno de desarrollo | Google Colab + VS Code | — | Notebooks y dashboard |

---

## 5. Estructura del repositorio
riesgo-academico-estudiantil/

├── data/

│   ├── raw/                    ← Dataset original (nunca modificar)

│   └── processed/              ← Dataset limpio y conjuntos train/test

├── docs/

│   ├── ficha_proyecto.md       ← Formulación del proyecto (Entrega 1)

│   ├── analisis_dataset.md     ← Análisis cualitativo (Entrega 1)

│   ├── wireframe_dashboard.png ← Boceto inicial del dashboard

│   ├── comparacion_modelos.png ← Gráfica comparativa de modelos

│   ├── matriz_y_roc.png        ← Matriz de confusión y curva ROC

│   ├── diccionario_datos.md    ← Diccionario de variables

│   ├── arquitectura.md         ← Este archivo

│   └── reflexion_etica.md      ← Reflexión ética final

├── models/

│   ├── modelo_final.pkl        ← Modelo serializado (Regresión Logística)

│   ├── pipeline_final.pkl      ← Pipeline serializado

│   └── model_metadata.json     ← Métricas y metadatos

├── notebooks/

│   ├── 01_exploracion.ipynb    ← Exploración inicial con pandas

│   ├── 02_eda_limpieza.ipynb   ← Pipeline de limpieza y preparación

│   └── 03_modelado.ipynb       ← Entrenamiento y evaluación de modelos

├── app_final.py                ← Dashboard Streamlit

├── .gitignore

├── requirements.txt

└── README.md

---

## 6. Instrucciones de ejecución

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar el dashboard
```bash
streamlit run app_final.py
```

### Acceder en el navegador
http://localhost:8501