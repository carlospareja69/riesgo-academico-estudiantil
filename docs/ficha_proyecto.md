# Ficha de Formulación – Proyecto Integrador

## 1. Datos del estudiante

- **Nombre completo:** Carlos Andrés Pareja Osorno
- **Programa:** Tecnología en Desarrollo de Software – Diplomado en Desarrollo Web para Analítica de Datos
- **Código de la asignatura:** EXTEXT2601000_20071
- **Fecha:** 28 de mayo de 2026

## 2. Nombre del proyecto

Sistema de alerta temprana de riesgo académico estudiantil

## 3. Planteamiento del problema

Tomando como contexto a una institución de educación secundaria, podemos ver que un número significativo de estudiantes presentan bajo rendimiento académico, lo cual puede terminar en la reprobación de asignaturas. Por esta razón se pueden ver afectados especialmente los coordinadores académicos y profesores, ya que no cuentan actualmente con una herramienta con la que puedan identificar rápidamente o de forma temprana a los estudiantes en riesgo, por lo que detectan dicho problema cuando el periodo está próximo a terminar o muy avanzado, con poco margen de corrección de la situación.

Por esta razón se propone desarrollar una aplicación web analítica que, a partir del dataset Student Performance (UCI Machine Learning Repository, 649 registros de estudiantes de secundaria en Portugal), permita clasificar a cada uno de los estudiantes según su nivel de riesgo académico (con riesgo / sin riesgo). El modelo que se pretende usar utilizará variables disponibles tempranamente, tales como las ausencias, el tiempo dedicado al estudio, el número de materias reprobadas previamente y la nota del primer periodo, evitando así el uso de la calificación final como variable de entrada para no incurrir en fuga de datos.

El propósito principal es apoyar la decisión del coordinador académico sobre qué estudiantes necesitan acompañamiento o tutorías, optimizando así el recurso de apoyo de la institución hacia quienes más lo necesitan.

## 4. Pregunta analítica

¿Es posible clasificar el nivel de riesgo académico de un estudiante de secundaria (con riesgo / sin riesgo) a partir de sus ausencias, tiempo de estudio, materias reprobadas previamente y la calificación del primer periodo, con el fin de apoyar al coordinador académico en la asignación temprana de acompañamiento y tutorías?

## 5. Tipo de tarea y métrica de evaluación

- **Tipo de tarea:** [X] Clasificación  [ ] Regresión  [ ] Clustering
- **Métrica principal:** F1-score
- **Justificación de la métrica:** La variable objetivo está desbalanceada (84.6 % de estudiantes están sin riesgo, en comparación con el 15.4 % que sí están en riesgo). Así podemos ver que la exactitud (accuracy) sería engañosa: un modelo que clasificara a todos como "sin riesgo" alcanzaría un 84.6 % de exactitud aparente, pero no detectaría a ningún estudiante en riesgo, que es justamente el objetivo. El F1-score equilibra la precisión y el recall sobre la clase minoritaria, ya que mide de forma más fiel la capacidad real del modelo para identificar a los estudiantes que necesitan apoyo.

## 6. Descripción del dataset

- **Nombre:** Student Performance (archivo `student-por.csv`, asignatura de Lengua Portuguesa)
- **Fuente (URL):** https://archive.ics.uci.edu/dataset/320/student+performance
- **Licencia:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Cita:** Cortez, P. (2008). *Student Performance* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T
- **Número de filas:** 649
- **Número de columnas:** 33
- **Descripción general:** Datos del desempeño académico de estudiantes de secundaria en dos escuelas portuguesas, recopilados mediante reportes escolares y cuestionarios. Incluye información personal, social y escolar, junto con las calificaciones de los tres periodos del año.

## 7. Variables

- **Variable objetivo (y):** `riesgo` – variable binaria construida con los datos de la calificación final `G3`. Se asigna 1 (en riesgo) si `G3 < 10`, y 0 (sin riesgo) si `G3 >= 10`, según el criterio de aprobación portugués.

- **Variables de entrada principales (X):**
  - `absences`: número de ausencias del estudiante durante el año (numérica, rango 0–32).
  - `studytime`: tiempo dedicado al estudio (categórica ordinal, escala 1–4).
  - `failures`: número de materias reprobadas anteriormente (numérica, rango 0–3).
  - `G1`: calificación del primer periodo (numérica, rango 0–19).
  - `higher`: intención de cursar educación superior (categórica, sí/no).

## 8. Usuario final y decisión

- **Usuario:** Coordinador académico de la institución.
- **Decisión que apoyará:** Identificar de forma rápida y oportuna a los estudiantes que tienen mayor riesgo de reprobar, para dirigir hacia ellos acompañamiento, tutorías y recursos de apoyo antes de que el periodo siga avanzando.

## 9. Implicaciones éticas

- **Riesgo identificado:** El dataset utilizado contiene variables sensibles de carácter socioeconómico (como la zona de residencia urbana o rural, el nivel educativo de los padres o la situación familiar). Esto significa que, si el modelo se entrenara apoyándose en estas variables, podría aprender sesgos injustos —por ejemplo, penalizar a un estudiante por vivir en zona rural— y reforzar desigualdades existentes.

- **Acción de mitigación:** Se priorizará el uso de variables directamente relacionadas con el comportamiento y el desempeño académico del estudiante (ausencias, tiempo de estudio, reprobaciones, nota del primer periodo) y se excluirán las variables socioeconómicas sensibles. Además, el resultado se mostrará como una alerta de apoyo y no como una etiqueta definitiva, dejando la decisión final en manos del coordinador académico y/o el profesor.

## 10. URL del repositorio GitHub

https://github.com/carlospareja69/riesgo-academico-estudiantil
