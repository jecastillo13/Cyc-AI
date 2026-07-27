# Arquitectura de Cyc-AI

## Objetivo

Cyc-AI está diseñado siguiendo una arquitectura modular basada en responsabilidades.

Cada módulo tiene una única función, evita dependencias innecesarias y trabaja con modelos de dominio bien definidos.

El objetivo es construir un motor de análisis de entrenamiento escalable, mantenible y preparado para incorporar algoritmos fisiológicos e inteligencia artificial.

---

# Flujo principal

```
FIT
        │
        ▼
API
        │
        ▼
TrainingService
        │
        ├──────────────► WorkoutHistory
        │                     │
        │                     ▼
        │            WorkoutHistoryAnalyzer
        │                     │
        │                     ▼
        │             HistorySummary
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
DataEngine
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

# Estructura del proyecto

```
app/

analytics/
    Obtención y análisis de datos de entrenamiento.
    Incluye el procesamiento del historial y métricas.

api/
    Endpoints de FastAPI.

coach/
    Clasificación del entrenamiento y generación de recomendaciones.

engine/
    Construcción del AthleteContext.

fit/
    Importación y lectura de archivos FIT.

models/
    Modelos de dominio utilizados por todo el sistema.

physiology/
    Modelos y algoritmos fisiológicos.

services/
    Casos de uso y orquestación del flujo principal.

users/
    Gestión de perfiles de usuario.
```

---

# Principios de diseño

- Una responsabilidad por clase.
- La API nunca contiene lógica de negocio.
- Los servicios coordinan procesos.
- El DataEngine construye el contexto completo del atleta.
- El Coach interpreta la información y genera recomendaciones.
- Physiology calcula métricas fisiológicas.
- Analytics obtiene y procesa datos.
- Los modelos representan el dominio del sistema.
- Los componentes intercambian modelos de dominio, no diccionarios.
- Ningún componente del núcleo debe acceder directamente a los archivos CSV.

---

# Modelos principales

Actualmente el núcleo del sistema está compuesto por los siguientes modelos:

```
Athlete
Workout
TrainingLoadResult
HistorySummary
AthleteContext
```

En futuras versiones se incorporarán:

```
MetricsSummary
TrainingStatus
```

---

# Flujo de datos

```
Athlete
        │
Workout
        │
TrainingLoad
        │
HistorySummary
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

---

# History Processing

El historial de entrenamientos ya no se utiliza directamente desde un diccionario.

El flujo actual es:

```
WorkoutHistory
        │
        ▼
WorkoutHistoryAnalyzer
        │
        ▼
HistorySummary
        │
        ▼
AthleteContext
        │
        ▼
Coach
```

Este diseño desacopla completamente el acceso al archivo CSV del resto del sistema.

El Coach y el motor fisiológico trabajan únicamente con el objeto `HistorySummary`, sin conocer cómo se almacenan los datos.

---

# Responsabilidad de cada componente

## WorkoutHistory

Carga el historial de entrenamientos desde el archivo CSV y devuelve un DataFrame.

---

## WorkoutHistoryAnalyzer

Procesa el historial de entrenamientos y genera un objeto `HistorySummary`.

---

## DataEngine

Construye el contexto completo del atleta.

Es el único componente encargado de crear:

- Athlete
- Workout
- TrainingLoadResult
- HistorySummary
- AthleteContext

---

## AthleteContext

Contiene toda la información necesaria para que el Coach y futuros motores de IA puedan tomar decisiones sin acceder directamente a archivos o fuentes externas.

---

## Coach

Interpreta el contexto del atleta y genera recomendaciones.

El Coach nunca accede directamente al historial, al archivo FIT o a los CSV.

Toda la información necesaria debe llegar mediante `AthleteContext`.

---

# Estado actual de la arquitectura

Actualmente Cyc-AI dispone de:

- Lectura de archivos FIT.
- Análisis del entrenamiento.
- Cálculo automático de TRIMP.
- Construcción del contexto del atleta.
- Procesamiento del historial de entrenamientos.
- Resumen inteligente del historial mediante `HistorySummary`.
- Motor de recomendaciones basado en contexto.

La siguiente fase del proyecto incorporará:

- Acute Training Load (ATL)
- Chronic Training Load (CTL)
- Training Stress Balance (TSB)
- Motor avanzado de IA para recomendaciones fisiológicas.