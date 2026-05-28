# Análisis Cualitativo del Dataset

## 1. Descripción general

El dataset Student Performance recopila información sobre el desempeño académico de estudiantes de educación secundaria en dos escuelas públicas de Portugal. Fue construido por Paulo Cortez (Universidad de Minho) en 2008 a partir de reportes escolares y cuestionarios aplicados a los estudiantes, y se encuentra publicado en el UCI Machine Learning Repository. El propósito original del estudio fue analizar qué factores personales, sociales y escolares influyen en el rendimiento académico, medido a través de las calificaciones obtenidas durante el año.

Para este proyecto se utiliza el archivo correspondiente a la asignatura de Lengua Portuguesa (`student-por.csv`), que contiene un mayor número de registros que el de Matemáticas.

- **Fuente:** UCI Machine Learning Repository
- **Cita:** Cortez, P. (2008). *Student Performance* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T
- **Licencia:** Creative Commons Attribution 4.0 International (CC BY 4.0), que permite el uso y la adaptación de los datos siempre que se otorgue el crédito correspondiente.

## 2. Estructura

Este dataset cuenta con un conjunto de datos que contiene 649 registros y 33 variables. Cada fila representa a un estudiante, y las columnas combinan dos tipos de información:

- **Variables numéricas:** edad, tiempo de estudio semanal, número de ausencias, materias reprobadas previamente y las calificaciones de los tres periodos (G1, G2 y G3), entre otras.
- **Variables categóricas (texto):** escuela, sexo, zona de residencia (urbana/rural), nivel educativo y ocupación de los padres, acceso a internet, apoyo familiar, entre otras.

Esta combinación de variables numéricas y categóricas hace que el dataset sea adecuado para un problema de clasificación, aunque exigirá la codificación de las variables categóricas en fases posteriores del proyecto.

## 3. Variables relevantes

La variable objetivo del proyecto se construye a partir de `G3` (la calificación final, en una escala de 0 a 20). Siguiendo el criterio académico portugués, se considera que un estudiante aprueba con una nota igual o superior a 10. A partir de esto se crea una variable binaria llamada `riesgo`:

- `riesgo = 1` → estudiante en riesgo (G3 menor a 10)
- `riesgo = 0` → estudiante sin riesgo (G3 igual o mayor a 10)

Las variables de entrada seleccionadas son aquellas que estarían disponibles de forma temprana, antes de conocer la nota final:

- `absences` — número de ausencias del estudiante
- `studytime` — tiempo semanal dedicado al estudio
- `failures` — número de materias reprobadas anteriormente
- `G1` — calificación del primer periodo
- `higher` — intención de cursar educación superior

## 4. Calidad de los datos

La exploración inicial con pandas muestra que el dataset tiene una calidad notablemente alta:

- **Valores nulos:** ninguno. Las 33 columnas están completas, sin datos faltantes.
- **Registros duplicados:** ninguno.
- **Rangos coherentes:** las calificaciones (G1, G2, G3) se mantienen dentro del rango esperado de 0 a 19, sin valores imposibles que indiquen errores de digitación.

El único punto que hay que darle atención son las ausencias (`absences`): pese a que la mayoría de los estudiantes registra valores bajos (el 75 % falta seis veces o menos), existe un valor máximo de 32, el cual podríamos denominar como un posible outlier. No es necesariamente un error, pero conviene tenerlo presente en la fase de preparación.

El hecho de no contar con valores nulos y duplicados es una ventaja importante, ya que esto simplificará la fase posterior de limpieza: no será necesaria la imputación de datos faltantes ni la eliminación de registros repetidos.

## 5. Pertinencia

El dataset es el adecuado para responder la pregunta analítica planteada, ya que este contiene las variables necesarias para determinar el riesgo académico de un estudiante. La variable objetivo (`riesgo`) puede derivarse directamente de la calificación final, y las variables de entrada seleccionadas (ausencias, tiempo de estudio, reprobaciones previas y nota del primer periodo) son indicadores razonables del desempeño futuro y están disponibles de forma temprana.

Un hallazgo relevante que respalda esta selección es el análisis de correlación entre las tres calificaciones: la nota del segundo periodo (G2) presenta una correlación muy alta con la nota final (0.92), mientras que la del primer periodo (G1) tiene una correlación algo menor (0.83). Por esta razón, se decide utilizar G1 pero excluir G2 de las variables de entrada: usar G2 implicaría una fuga de datos, ya que equivaldría a predecir la nota final con información que prácticamente la contiene y que no estaría disponible en un momento temprano del año escolar.

## 6. Limitaciones

- **Desbalance de clases:** la variable objetivo está claramente desbalanceada. El 84.6 % de los estudiantes se clasifica como "sin riesgo" y solo el 15.4 % como "en riesgo". Este desbalance es la razón por la cual se elige el F1-score como métrica principal en lugar de la exactitud: un modelo que clasificara a todos como "sin riesgo" alcanzaría un 84.6 % de exactitud aparente, pero sería inútil para detectar a los estudiantes que realmente necesitan apoyo.
- **Riesgo de sesgo en variables sensibles:** el dataset incluye variables como la zona de residencia (urbana/rural), el nivel educativo de los padres o la situación familiar, que podrían introducir sesgos socioeconómicos si se usaran sin cuidado. Estas variables se manejarán con precaución y se documentará su uso.
- **Contexto específico:** los datos provienen de dos escuelas portuguesas en un periodo determinado, por lo que las conclusiones no son directamente generalizables a otros países o sistemas educativos sin una validación adicional.
- **Tamaño moderado:** con 649 registros, el dataset es suficiente para un proyecto académico, pero su tamaño limita la complejidad de los modelos que se pueden entrenar de forma confiable.
