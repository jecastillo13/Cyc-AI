# Coach IA

## Objetivo

El Coach IA es el componente encargado de transformar los datos del entrenamiento en recomendaciones comprensibles para el ciclista.

Su misión no es calcular métricas fisiológicas, sino interpretar la información generada por el resto del sistema y convertirla en decisiones útiles.

---

# Filosofía

La Inteligencia Artificial nunca inventa información.

Todas las recomendaciones deben estar basadas en datos objetivos obtenidos durante el análisis.

El Coach únicamente interpreta el contexto recibido.

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

En futuras versiones podrán añadirse nuevos modelos sin modificar el funcionamiento del Coach.

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

# Variables utilizadas

Actualmente el Coach utiliza:

- Tipo de entrenamiento.
- Carga del entrenamiento (TrainingLoadResult).
- Historial resumido (HistorySummary).

En próximas versiones utilizará además:

- ATL.
- CTL.
- TSB.
- Fatigue Score.
- Recovery Score.
- Fitness Score.

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

- ATL alto.
- CTL estable.
- TSB ligeramente negativo.

Entonces:

```
La carga reciente es elevada.

Se recomienda un entrenamiento regenerativo antes de realizar otra sesión intensa.
```

---

## Caso 3

Si:

- ATL muy bajo.
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
- Fatigue Score alto.

Entonces:

```
Se detectan signos de fatiga acumulada.

Se recomienda priorizar la recuperación.
```

---

# Explicaciones

Uno de los objetivos del Coach IA es justificar siempre sus recomendaciones.

Ejemplo:

```
Entrenamiento clasificado como resistencia aeróbica.

La carga obtenida mediante TRIMP ha sido moderada y el historial reciente muestra una frecuencia de entrenamiento estable.

Por ello se recomienda continuar con la planificación prevista.
```

---

# Evolución prevista

Las siguientes versiones incorporarán:

- Explicaciones fisiológicas.
- Predicción de fatiga.
- Predicción de rendimiento.
- Planificación semanal.
- Planificación mensual.
- Ajuste automático de carga.
- Objetivos personalizados.
- Adaptación al nivel del ciclista.

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

De esta forma ambos módulos permanecen completamente desacoplados.

---

# Estado actual

Actualmente el Coach IA es capaz de:

- Clasificar el entrenamiento.
- Interpretar la carga obtenida mediante TRIMP.
- Utilizar el historial resumido del atleta.
- Generar recomendaciones básicas.
- Trabajar sobre el AthleteContext construido por el DataEngine.

El siguiente paso será incorporar el estado fisiológico completo mediante ATL, CTL, TSB, Fatigue y Recovery para ofrecer recomendaciones mucho más precisas y personalizadas.