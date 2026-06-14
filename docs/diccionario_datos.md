# Diccionario de Datos — Student Performance

**Dataset:** Student Performance (`student-por.csv`)  
**Fuente:** UCI Machine Learning Repository  
**Cita:** Cortez, P. (2008). Student Performance [Dataset]. UCI ML Repository. https://archive.ics.uci.edu/dataset/320/student+performance
**Licencia:** CC BY 4.0  

---

## Variables de entrada (X)

| Variable | Tipo | Descripción | Rango / Valores |
|---|---|---|---|
| `school` | Categórica | Escuela del estudiante | GP = Gabriel Pereira, MS = Mousinho da Silveira |
| `sex` | Categórica | Sexo del estudiante | F = Femenino, M = Masculino |
| `age` | Numérica | Edad del estudiante | 15 a 22 años |
| `address` | Categórica | Zona de residencia | U = Urbana, R = Rural |
| `famsize` | Categórica | Tamaño del núcleo familiar | LE3 = ≤3 personas, GT3 = >3 personas |
| `Pstatus` | Categórica | Estado de convivencia de los padres | T = Juntos, A = Separados |
| `Medu` | Ordinal | Nivel educativo de la madre | 0=ninguno, 1=primaria, 2=secundaria básica, 3=secundaria, 4=superior |
| `Fedu` | Ordinal | Nivel educativo del padre | 0=ninguno, 1=primaria, 2=secundaria básica, 3=secundaria, 4=superior |
| `Mjob` | Categórica | Ocupación de la madre | teacher, health, services, at_home, other |
| `Fjob` | Categórica | Ocupación del padre | teacher, health, services, at_home, other |
| `reason` | Categórica | Razón para elegir la escuela | home, reputation, course, other |
| `guardian` | Categórica | Tutor del estudiante | mother, father, other |
| `traveltime` | Ordinal | Tiempo de desplazamiento al colegio | 1=<15min, 2=15–30min, 3=30–60min, 4=>60min |
| `studytime` | Ordinal | Tiempo semanal de estudio | 1=<2h, 2=2–5h, 3=5–10h, 4=>10h |
| `failures` | Numérica | Materias reprobadas anteriormente | 0 a 3 |
| `schoolsup` | Categórica | Apoyo educativo extra de la escuela | yes, no |
| `famsup` | Categórica | Apoyo educativo familiar | yes, no |
| `paid` | Categórica | Clases particulares pagadas | yes, no |
| `activities` | Categórica | Actividades extracurriculares | yes, no |
| `nursery` | Categórica | Asistió a jardín de infantes | yes, no |
| `higher` | Categórica | Desea cursar educación superior | yes, no |
| `internet` | Categórica | Acceso a internet en casa | yes, no |
| `romantic` | Categórica | Tiene relación sentimental | yes, no |
| `famrel` | Ordinal | Calidad de las relaciones familiares | 1=muy mala a 5=excelente |
| `freetime` | Ordinal | Tiempo libre después del colegio | 1=muy poco a 5=mucho |
| `goout` | Ordinal | Frecuencia de salidas con amigos | 1=muy poca a 5=muy alta |
| `Dalc` | Ordinal | Consumo de alcohol entre semana | 1=muy bajo a 5=muy alto |
| `Walc` | Ordinal | Consumo de alcohol en fin de semana | 1=muy bajo a 5=muy alto |
| `health` | Ordinal | Estado de salud actual | 1=muy malo a 5=muy bueno |
| `absences` | Numérica | Número de ausencias escolares | 0 a 32 |
| `G1` | Numérica | Calificación del primer periodo | 0 a 19 |

---

## Variable objetivo (y)

| Variable | Tipo | Descripción | Valores |
|---|---|---|---|
| `riesgo` | Binaria | Riesgo de reprobar la asignatura | 1 = en riesgo (G3 < 10), 0 = sin riesgo (G3 ≥ 10) |

---

## Variables excluidas del modelo

| Variable | Razón de exclusión |
|---|---|
| `G3` | Es la nota final — variable que da origen a `riesgo`. Usarla sería fuga de datos. |
| `G2` | Correlación de 0.92 con G3. Usarla equivale a casi conocer la respuesta final. |

---

## Distribución de la variable objetivo

| Clase | Cantidad | Porcentaje |
|---|---|---|
| Sin riesgo (0) | 549 | 84.6% |
| Con riesgo (1) | 100 | 15.4% |
| **Total** | **649** | **100%** |

> ⚠️ El desbalance de clases (84.6% vs 15.4%) justifica el uso de **F1-score** como métrica principal en lugar de la exactitud (accuracy).