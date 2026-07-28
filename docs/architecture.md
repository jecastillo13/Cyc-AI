# Arquitectura de Cyc-AI

## Objetivo

Cyc-AI está diseñado siguiendo una arquitectura modular basada en responsabilidades.

Cada componente tiene una única responsabilidad y se comunica mediante modelos de dominio, evitando dependencias innecesarias entre módulos.

La arquitectura está preparada para crecer incorporando nuevos algoritmos fisiológicos, motores de inteligencia artificial e integraciones externas sin modificar el núcleo del sistema.

---

# Principios de diseño

- Una responsabilidad por clase.
- Separación estricta entre API, servicios y lógica de negocio.
- El DataEngine es el único encargado de construir el contexto del atleta.
- El Coach nunca accede directamente a archivos FIT o CSV.
- El motor fisiológico es independiente del Coach.
- Los componentes intercambian modelos de dominio, nunca diccionarios.
- El historial de entrenamiento se procesa una única vez.
- Los algoritmos fisiológicos son reutilizables e independientes.
- La arquitectura permite incorporar nuevos modelos sin modificar los existentes.

---

# Flujo principal del sistema

```
FIT / FIT.GZ
        │
        ▼
FastAPI
        │
        ▼
TrainingService
        │
        ├─────────────────────────────► WorkoutHistory
        │                                      │
        │                                      ▼
        │                           WorkoutHistoryAnalyzer
        │                                      │
        │                                      ▼
        │                              HistorySummary
        │
        ▼
FitImporter
        │
        ▼
FitReader
        │
        ▼
WorkoutAnalyzer
        │
        ▼
TrainingLoadCalculator
        │
        ▼
TrainingLoadResult
        │
        ▼
DataEngine
        │
        ├──────────────► TrainingLoadSeriesBuilder
        │                           │
        │                           ▼
        │                  TrainingLoadSeries
        │                           │
        │                           ▼
        │            ExponentialLoadCalculator
        │                  ├──────────┐
        │                  ▼          ▼
        │           ATLCalculator  CTLCalculator
        │                  │          │
        │                  └────┬─────┘
        │                       ▼
        │             TrainingStatusBuilder
        │                       │
        │                       ▼
        │               TrainingStatus
        │
        ▼
AthleteContext
        │
        ▼
Coach
        │
        ▼
Respuesta JSON
```

---

# Arquitectura del proyecto

```
app/

analytics/
    Procesamiento del historial y métricas.

api/
    Endpoints FastAPI.

coach/
    Clasificación del entrenamiento y generación
    de recomendaciones.

engine/
    Construcción del AthleteContext.

fit/
    Lectura e importación de archivos FIT/FIT.GZ.

models/
    Modelos de dominio.

physiology/
    Algoritmos fisiológicos.

services/
    Casos de uso.

users/
    Gestión del perfil del atleta.
```

---

# Modelos de dominio

Actualmente el sistema utiliza los siguientes modelos principales.

```
Athlete
Workout
TrainingLoadResult
TrainingLoadSeries
HistorySummary
TrainingStatus
AthleteContext
```

Cada modelo representa una parte del dominio del entrenamiento y evita el uso de estructuras de datos genéricas.

---

# Motor fisiológico

El motor fisiológico está completamente desacoplado del Coach.

Su responsabilidad es transformar el historial del atleta en un estado fisiológico objetivo.

Actualmente el flujo es:

```
WorkoutHistory
        │
        ▼
TrainingLoadSeriesBuilder
        │
        ▼
TrainingLoadSeries
        │
        ▼
ExponentialLoadCalculator
      ├────────────┐
      ▼            ▼
ATLCalculator   CTLCalculator
      │            │
      └──────┬─────┘
             ▼
TrainingStatusBuilder
             │
             ▼
TrainingStatus
```

El cálculo utiliza una serie temporal diaria continua, rellenando automáticamente los días sin entrenamiento con carga cero.

Esto permite obtener valores fisiológicamente consistentes para ATL y CTL mediante medias exponenciales.

---

# Flujo de datos

El flujo completo de construcción del contexto es:

```
Athlete
        │
Workout
        │
TrainingLoadResult
        │
HistorySummary
        │
TrainingStatus
        │
Metrics
        │
        ▼
AthleteContext
        │
        ▼
Coach
        │
        ▼
Respuesta JSON
```

El Coach únicamente interpreta el contexto.

Nunca realiza cálculos fisiológicos.

---

# Procesamiento del historial

El historial de entrenamientos se procesa en varias etapas.

```
WorkoutHistory

↓

DataFrame

↓

TrainingLoadSeriesBuilder

↓

Serie diaria continua

↓

WorkoutHistoryAnalyzer

↓

HistorySummary
```

La serie continua se utiliza para el cálculo fisiológico mientras que el resumen estadístico alimenta al Coach.

Ningún componente del sistema accede directamente al CSV.

---

# DataEngine

El DataEngine es el núcleo de integración del sistema.

Es el único componente responsable de construir el contexto completo del atleta.

Actualmente crea automáticamente:

- Athlete
- Workout
- TrainingLoadResult
- HistorySummary
- TrainingStatus
- AthleteContext

Esto garantiza que todos los módulos trabajen sobre la misma información.

---

# AthleteContext

AthleteContext representa el estado completo del atleta durante el análisis de un entrenamiento.

Actualmente contiene:

- Athlete
- Workout
- TrainingLoadResult
- HistorySummary
- TrainingStatus
- Metrics

El objetivo es que cualquier componente del sistema pueda tomar decisiones utilizando exclusivamente este objeto.

---

# Coach

El Coach interpreta el contexto construido por el DataEngine.

Actualmente utiliza:

- Workout
- TrainingLoadResult
- HistorySummary

El estado fisiológico (`TrainingStatus`) ya forma parte del contexto y será utilizado en el siguiente sprint para generar recomendaciones adaptativas basadas en:

- ATL
- CTL
- TSB
- Fatigue Score
- Recovery Score

---

# Estado actual del proyecto

Actualmente Cyc-AI dispone de:

- Lectura de archivos FIT y FIT.GZ.
- Procesamiento automático del entrenamiento.
- Cálculo de TRIMP mediante el modelo de Bannister.
- Construcción del AthleteContext.
- Procesamiento del historial de entrenamientos.
- Generación de HistorySummary.
- Construcción de una serie temporal diaria continua.
- Cálculo de ATL.
- Cálculo de CTL.
- Cálculo de TSB.
- Construcción de TrainingStatus.
- Integración completa con DataEngine.
- Recomendaciones del Coach.
- API REST mediante FastAPI.

---

# Próximas fases

Las siguientes versiones incorporarán:

- Fatigue Score.
- Recovery Score.
- Fitness Score.
- Coach adaptativo basado en TrainingStatus.
- Motor avanzado de IA.
- Predicción de rendimiento.
- Planificación inteligente del entrenamiento.

La arquitectura actual ya está preparada para incorporar estas capacidades sin modificar la estructura principal del sistema.