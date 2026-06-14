# Reflexión Ética — Sistema de Alerta Temprana de Riesgo Académico

**Proyecto:** Sistema de alerta temprana de riesgo académico estudiantil  
**Autor:** Carlos Andrés Pareja Osorno  
**Fecha:** Junio 2026  

---

## 1. Riesgos identificados en el dataset y el modelo

### Desbalance de clases
El dataset presenta un desbalance significativo: 84.6% de estudiantes sin riesgo frente a 15.4% con riesgo. Esto puede hacer que el modelo tienda a predecir "sin riesgo" con más frecuencia, dejando sin detectar a estudiantes que sí necesitan apoyo. Por esta razón se eligió el F1-score como métrica principal, que penaliza este comportamiento.

### Sesgos socioeconómicos
El dataset incluye variables sensibles como la zona de residencia (urbana/rural), el nivel educativo de los padres y la situación familiar. Un modelo entrenado con estas variables podría aprender patrones injustos — por ejemplo, penalizar a un estudiante simplemente por vivir en zona rural o por tener padres con bajo nivel educativo, independientemente de su desempeño real.

### Fuga de datos
La variable G2 (nota del segundo periodo) presenta una correlación de 0.92 con la nota final G3. Incluirla como variable de entrada equivaldría a predecir con información que prácticamente contiene la respuesta, lo que inflaría artificialmente las métricas sin aportar valor real en un escenario temprano de predicción.

---

## 2. Grupos que podrían verse afectados

- **Estudiantes en zonas rurales:** podrían ser clasificados como "en riesgo" de forma injusta si el modelo aprende que vivir lejos del colegio correlaciona con bajo rendimiento, sin considerar el esfuerzo individual.
- **Estudiantes con padres de bajo nivel educativo:** podrían ser penalizados por factores socioeconómicos fuera de su control.
- **Estudiantes con muchas ausencias justificadas:** el modelo no distingue entre ausencias por enfermedad, situación familiar u otras causas válidas.

---

## 3. Acciones de mitigación implementadas

- **Variables excluidas:** se priorizaron variables directamente relacionadas con el comportamiento académico del estudiante (ausencias, tiempo de estudio, reprobaciones previas, nota del primer periodo) y se excluyeron G2 y G3 para evitar fuga de datos.
- **Métrica apropiada:** se eligió F1-score en lugar de accuracy para no favorecer la clase mayoritaria.
- **Resultado como alerta, no como decisión:** el dashboard presenta el resultado del modelo como una **alerta de apoyo**, no como una etiqueta definitiva. La decisión final siempre queda en manos del coordinador académico.
- **Advertencia visible en el dashboard:** el sistema muestra explícitamente que el resultado es una estimación generada por un modelo y debe ser revisada por una persona responsable antes de tomar cualquier decisión.

---

## 4. Limitaciones conocidas del sistema

- **Contexto específico:** los datos provienen de dos escuelas portuguesas. Las conclusiones no son directamente generalizables a otros países o sistemas educativos sin validación adicional.
- **Tamaño moderado:** con 649 registros, el modelo tiene limitaciones para capturar patrones más complejos.
- **Variables no disponibles:** el dataset no incluye información sobre situaciones personales del estudiante (problemas de salud, situación económica familiar puntual) que podrían explicar mejor el rendimiento académico.
- **Modelo estático:** el modelo fue entrenado con datos de un periodo específico. Con el tiempo, los patrones pueden cambiar y el modelo necesitaría reentrenarse.

---

## 5. Declaración de uso responsable

> ⚠️ **El resultado de este sistema es una alerta de apoyo, no una decisión automática.**
>
> El modelo predice la probabilidad de riesgo académico basándose en patrones históricos. Esta predicción debe ser interpretada por el coordinador académico considerando el contexto individual de cada estudiante. Ningún estudiante debe ser etiquetado, sancionado o excluido de recursos de apoyo basándose únicamente en el resultado del modelo.
>
> El propósito del sistema es **ampliar la capacidad de detección temprana** del equipo docente, no reemplazar el juicio humano.