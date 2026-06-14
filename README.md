# Sistema de Alerta Temprana de Riesgo Académico Estudiantil

Proyecto integrador del Diplomado en Desarrollo Web para Analítica de Datos. Este proyecto propone una aplicación web analítica que clasifica a estudiantes de secundaria según su nivel de riesgo académico (con riesgo / sin riesgo), con el fin de apoyar al coordinador académico en la asignación temprana de acompañamiento y tutorías.

---

## Problema y pregunta analítica

En las instituciones de educación secundaria, un número significativo de estudiantes presenta bajo rendimiento académico que puede terminar en la reprobación de asignaturas. Los coordinadores académicos y profesores no cuentan actualmente con una herramienta para identificar de forma temprana a los estudiantes en riesgo, y suelen detectar el problema cuando el periodo ya está muy avanzado.

**Pregunta analítica:** ¿Es posible clasificar el nivel de riesgo académico de un estudiante de secundaria (con riesgo / sin riesgo) a partir de sus ausencias, tiempo de estudio, materias reprobadas previamente y la calificación del primer periodo, con el fin de apoyar al coordinador académico en la asignación temprana de acompañamiento y tutorías?

- **Tipo de tarea:** Clasificación binaria
- **Variable objetivo:** `riesgo` (1 si G3 < 10, 0 si G3 ≥ 10)
- **Métrica principal:** F1-score (justificada por desbalance de clases: 84.6% sin riesgo / 15.4% con riesgo)

---

## Dataset

- **Nombre:** Student Performance (`student-por.csv`)
- **Fuente:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/320/student+performance)
- **Licencia:** CC BY 4.0
- **Cita:** Cortez, P. (2008). *Student Performance* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T
- **Tamaño:** 649 registros, 33 variables

---

## Resultados del modelo

Se entrenaron y compararon tres modelos de clasificación:

| Modelo | Accuracy | F1-score | Precision | Recall | AUC-ROC |
|---|---|---|---|---|---|
| **Regresión Logística** ← seleccionado | 89.2% | **66.7%** | 63.6% | 70.0% | 90.0% |
| Random Forest | 87.7% | 61.9% | 59.1% | 65.0% | 90.2% |
| Pipeline LR+Scaler | 86.9% | 56.4% | 57.9% | 55.0% | 89.2% |

**Modelo seleccionado:** Regresión Logística simple  
**Justificación:** Mayor F1-score (66.7%) sobre el conjunto de prueba. Detecta 14 de 20 estudiantes en riesgo (Recall: 70%).

---

## Metodología

El proyecto sigue la metodología **CRISP-DM** (Cross Industry Standard Process for Data Mining), un estándar para proyectos de ciencia de datos compuesto por seis fases iterativas.

---

## Arquitectura de la solución
[Dataset original] → [Pipeline limpieza] → [Modelo ML] → [Dashboard Streamlit]

Ver detalles en `docs/arquitectura.md`.

---

## Estructura del repositorio
riesgo-academico-estudiantil/

├── data/

│   ├── raw/                    ← Dataset original

│   └── processed/              ← Dataset limpio y conjuntos train/test

├── docs/

│   ├── ficha_proyecto.md

│   ├── analisis_dataset.md

│   ├── wireframe_dashboard.png

│   ├── comparacion_modelos.png

│   ├── matriz_y_roc.png

│   ├── diccionario_datos.md

│   ├── arquitectura.md

│   └── reflexion_etica.md

├── models/

│   ├── modelo_final.pkl

│   ├── pipeline_final.pkl

│   └── model_metadata.json

├── notebooks/

│   ├── 01_exploracion.ipynb

│   ├── 02_eda_limpieza.ipynb

│   └── 03_modelado.ipynb

├── app_final.py

├── .gitignore

├── requirements.txt

└── README.md

---

## Instalación y ejecución

```bash
pip install -r requirements.txt
streamlit run app_final.py
```

Abrir en el navegador: `http://localhost:8501`

---

## Consideraciones éticas

El resultado del modelo es una **alerta de apoyo**, no una decisión automática. Ningún estudiante debe ser etiquetado basándose únicamente en la predicción del modelo. Ver detalles en `docs/reflexion_etica.md`.

---

## Autor

Carlos Andrés Pareja Osorno — Tecnología en Desarrollo de Software  
Diplomado en Desarrollo Web para Analítica de Datos — 2026
