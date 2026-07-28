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
- La arquitectura debe permitir sustituir algoritmos sin modificar el resto del sistema.

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
        │                    ATLCalculator
        │                           │
        │                           ▼
        │                 TrainingStatusBuilder
        │                           │
        │                           ▼
        │                  TrainingStatus
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
HistorySummary
TrainingStatus
AthleteContext
```

Cada modelo representa una parte del dominio del entrenamiento y evita el uso de estructuras de datos genéricas.

---

# Motor fisiológico

El motor fisiológico está completamente desacoplado del Coach.

Su responsabilidad es transformar el historial del atleta en un estado fisiológico.

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
ATLCalculator
        │
        ▼
TrainingStatusBuilder
        │
        ▼
TrainingStatus
```

En futuras versiones este flujo incorporará:

```
CTLCalculator

↓

TSBCalculator

↓

FatigueCalculator

↓

RecoveryCalculator
```

sin modificar el resto del sistema.

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

WorkoutHistoryAnalyzer

↓

HistorySummary
```

El resultado se utiliza tanto por el Coach como por el motor fisiológico.

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

Esto garantiza que todos los motores trabajen sobre la misma información.

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

El objetivo es que cualquier componente del sistema pueda tomar decisiones únicamente utilizando este objeto.

---

# Coach

El Coach interpreta el contexto construido por el DataEngine.

Actualmente utiliza:

- Workout
- TrainingLoadResult
- HistorySummary

En próximas versiones utilizará además:

- TrainingStatus
- ATL
- CTL
- TSB
- Fatigue Score
- Recovery Score

para generar recomendaciones fisiológicas más precisas.

---

# Estado actual del proyecto

Actualmente Cyc-AI dispone de:

- Lectura de archivos FIT y FIT.GZ.
- Procesamiento automático del entrenamiento.
- Cálculo de TRIMP mediante el modelo de Bannister.
- Construcción del AthleteContext.
- Procesamiento del historial de entrenamientos.
- Generación de HistorySummary.
- Pipeline fisiológico inicial.
- TrainingLoadSeries.
- TrainingStatus.
- Integración completa con DataEngine.
- Recomendaciones del Coach.
- API REST mediante FastAPI.

---

# Próximas fases

Las siguientes versiones incorporarán:

- Chronic Training Load (CTL)
- Training Stress Balance (TSB)
- Fatigue Score
- Recovery Score
- Fitness Score
- Motor avanzado de IA
- Predicción de rendimiento
- Planificación inteligente del entrenamiento

La arquitectura actual ya está preparada para incorporar estos componentes sin modificar la estructura principal del sistema.