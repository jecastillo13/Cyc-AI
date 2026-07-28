# Coach IA

## Objetivo

El Coach IA es el componente encargado de transformar los datos del entrenamiento en recomendaciones comprensibles para el ciclista.

Su misión no es calcular métricas fisiológicas, sino interpretar la información generada por el resto del sistema y convertirla en decisiones útiles.

---

# Filosofía

La Inteligencia Artificial nunca inventa información.

Todas las recomendaciones deben estar basadas en datos objetivos obtenidos durante el análisis.

El Coach únicamente interpreta el contexto recibido.

La lógica fisiológica permanece completamente separada del razonamiento del Coach.

---

# Arquitectura

El Coach IA trabaja sobre un único objeto:

```
AthleteContext
```

Este objeto contiene toda la información necesaria para tomar decisiones sin acceder directamente a archivos FIT, CSV o bases de datos.

---

# Información disponible

Actualmente el contexto del atleta contiene:

```
Athlete

Workout

TrainingLoadResult

HistorySummary

TrainingStatus

Metrics
```

Esto permite que el Coach evolucione sin modificar el resto de la arquitectura.

---

# Flujo de decisión

```
FIT

↓

WorkoutAnalyzer

↓

TrainingLoadResult

↓

WorkoutHistory

↓

HistorySummary

↓

TrainingStatus

↓

AthleteContext

↓

Coach IA

↓

Recomendación
```

---

# Principios de decisión

El Coach siempre debe:

- Basarse únicamente en datos disponibles.
- Explicar sus recomendaciones.
- Evitar conclusiones no respaldadas por la información.
- Mantener un lenguaje claro y comprensible.
- Adaptar la recomendación al contexto fisiológico del atleta.

---

# Variables disponibles

Actualmente el Coach dispone de:

- Tipo de entrenamiento.
- Training Load.
- HistorySummary.
- TrainingStatus.

Dentro de `TrainingStatus` están disponibles:

- Training Load.
- ATL.
- CTL.
- TSB.
- Fatigue Score.
- Recovery Score.

Actualmente las recomendaciones utilizan principalmente:

- Tipo de entrenamiento.
- Carga del entrenamiento.
- Historial reciente.

Las métricas fisiológicas ya forman parte del contexto y serán utilizadas progresivamente durante los siguientes sprints.

---

# Modelo de razonamiento

El Coach interpreta la información siguiendo una cadena de decisión.

```
Entrenamiento

↓

Carga

↓

Historial

↓

Estado fisiológico

↓

Recomendación
```

Cada etapa añade contexto antes de generar una recomendación.

---

# Ejemplos de razonamiento

## Caso 1

Si:

- Entrenamiento de resistencia.
- Carga moderada.
- Historial estable.

Entonces:

```
Buen trabajo.

Puedes continuar con el plan previsto.
```

---

## Caso 2

Si:

- ATL elevado.
- CTL estable.
- TSB ligeramente negativo.

Entonces:

```
La carga reciente es elevada.

Un entrenamiento regenerativo favorecerá la recuperación antes de otra sesión intensa.
```

---

## Caso 3

Si:

- CTL bajo.
- Historial con pocos entrenamientos.

Entonces:

```
Existe margen para incrementar progresivamente la carga de entrenamiento.
```

---

## Caso 4

Si:

- TSB muy negativo.
- Fatigue Score elevado.

Entonces:

```
Se detectan signos de fatiga acumulada.

Se recomienda priorizar la recuperación antes de aumentar la intensidad.
```

---

# Explicaciones

Uno de los objetivos del Coach IA es justificar siempre sus recomendaciones.

Ejemplo:

```
El entrenamiento ha sido clasificado como resistencia aeróbica.

La carga obtenida mediante TRIMP ha sido moderada.

El historial reciente muestra una frecuencia de entrenamiento estable.

El estado fisiológico indica un equilibrio adecuado entre carga reciente y adaptación.

Por ello se recomienda continuar con la planificación prevista.
```

---

# Evolución prevista

Las siguientes versiones incorporarán:

- Interpretación completa de ATL, CTL y TSB.
- Utilización de Fatigue Score y Recovery Score.
- Predicción de fatiga.
- Predicción de rendimiento.
- Planificación semanal.
- Planificación mensual.
- Ajuste automático de carga.
- Objetivos personalizados.

---

# Relación con el motor fisiológico

El Coach no realiza cálculos fisiológicos.

Toda la información procede del módulo **Physiology**.

```
TrainingLoadResult

↓

TrainingStatus

↓

Coach
```

Esta separación permite mejorar el motor fisiológico sin modificar la lógica del Coach.

---

# Estado actual

Actualmente el Coach IA es capaz de:

- Clasificar el entrenamiento.
- Interpretar la carga obtenida mediante TRIMP.
- Utilizar el historial resumido del atleta.
- Trabajar sobre un `AthleteContext` completo.
- Acceder al estado fisiológico del atleta.
- Generar recomendaciones básicas.

El siguiente paso será utilizar ATL, CTL, TSB y las futuras métricas fisiológicas para generar recomendaciones adaptativas y completamente personalizadas.