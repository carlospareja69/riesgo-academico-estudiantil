# Sistema de Alerta Temprana de Riesgo Académico Estudiantil

Proyecto integrador del Diplomado en Desarrollo Web para Analítica de Datos. Este proyecto propone una aplicación web analítica que clasifica a estudiantes de secundaria según su nivel de riesgo académico (con riesgo / sin riesgo), con el fin de apoyar al coordinador académico en la asignación temprana de acompañamiento y tutorías, antes de que el periodo escolar esté demasiado avanzado.

> **Estado actual:** Entrega 1 — Planteamiento y comprensión de los datos. Esta fase corresponde a las dos primeras etapas de la metodología CRISP-DM (comprensión del negocio y comprensión de los datos). El modelo y el dashboard se desarrollan en entregas posteriores.

## Problema y pregunta analítica

En las instituciones de educación secundaria, un número significativo de estudiantes presenta bajo rendimiento académico que puede terminar en la reprobación de asignaturas. Los coordinadores académicos y profesores no cuentan actualmente con una herramienta para identificar de forma temprana a los estudiantes en riesgo, y suelen detectar el problema cuando el periodo ya está muy avanzado. Este proyecto busca anticipar esa detección.

**Pregunta analítica:** ¿Es posible clasificar el nivel de riesgo académico de un estudiante de secundaria (con riesgo / sin riesgo) a partir de sus ausencias, tiempo de estudio, materias reprobadas previamente y la calificación del primer periodo, con el fin de apoyar al coordinador académico en la asignación temprana de acompañamiento y tutorías?

- **Tipo de tarea:** Clasificación binaria
- **Variable objetivo:** `riesgo` (derivada de la nota final G3)
- **Métrica principal:** F1-score (justificada por el desbalance de clases: 84.6 % sin riesgo / 15.4 % en riesgo)

## Dataset

- **Nombre:** Student Performance (`student-por.csv`)
- **Fuente:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/320/student+performance)
- **Licencia:** CC BY 4.0
- **Cita:** Cortez, P. (2008). *Student Performance* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T
- **Tamaño:** 649 registros, 33 variables

## Metodología

El proyecto sigue la metodología **CRISP-DM** (Cross Industry Standard Process for Data Mining), un estándar para proyectos de ciencia de datos compuesto por seis fases iterativas.

## Estructura del repositorio

```
.
├── data/
│   └── raw/
│       └── student-por.csv          # Dataset original (sin modificar)
├── docs/
│   ├── ficha_proyecto.md            # Ficha de formulación del proyecto
│   ├── analisis_dataset.md          # Análisis cualitativo del dataset
│   └── wireframe_dashboard.png      # Boceto inicial del dashboard
├── notebooks/
│   └── 01_exploracion.ipynb         # Exploración inicial con pandas
├── .gitignore
├── requirements.txt
└── README.md
```

## Instalación

```bash
pip install -r requirements.txt
```

## Autor

Carlos Andrés Pareja Osorno — Tecnología en Desarrollo de Software.
