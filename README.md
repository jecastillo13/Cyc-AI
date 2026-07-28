# 🚴 Cyc-AI

**Cyc-AI** es una plataforma de análisis de entrenamientos de ciclismo basada en FastAPI, diseñada para evolucionar hacia un entrenador inteligente capaz de interpretar el estado fisiológico del atleta y generar recomendaciones personalizadas mediante Inteligencia Artificial.

Actualmente el proyecto analiza archivos **FIT** y **FIT.GZ**, calcula la carga de entrenamiento, procesa el historial deportivo y construye un contexto completo del atleta para alimentar el motor de recomendaciones.

---

# Características

Actualmente Cyc-AI es capaz de:

- Leer archivos FIT.
- Leer archivos FIT.GZ.
- Analizar entrenamientos automáticamente.
- Construir un modelo de entrenamiento (`Workout`).
- Calcular la carga mediante TRIMP (Bannister).
- Leer el historial de entrenamientos.
- Generar un resumen estadístico (`HistorySummary`).
- Construir el estado fisiológico (`TrainingStatus`).
- Integrar toda la información mediante `AthleteContext`.
- Generar recomendaciones mediante el Coach.
- Exponer los resultados mediante una API REST desarrollada con FastAPI.

---

# Arquitectura

La arquitectura está diseñada siguiendo una separación estricta de responsabilidades.

```
FIT

↓

FitImporter

↓

FitReader

↓

WorkoutAnalyzer

↓

TrainingLoadCalculator

↓

WorkoutHistory

↓

WorkoutHistoryAnalyzer

↓

DataEngine

↓

TrainingLoadSeriesBuilder

↓

ATLCalculator

↓

TrainingStatusBuilder

↓

AthleteContext

↓

Coach

↓

API REST
```

Cada módulo tiene una única responsabilidad, lo que facilita el mantenimiento y la incorporación de nuevas funcionalidades.

---

# Estructura del proyecto

```
app/
│
├── api/
├── coach/
├── core/
├── data/
├── models/
├── physiology/
├── services/
└── utils/

docs/

tests/
```

---

# Modelos principales

El núcleo del proyecto se basa en los siguientes modelos de dominio:

- Athlete
- Workout
- AthleteContext
- HistorySummary
- TrainingLoadResult
- TrainingLoadSeries
- TrainingStatus

Estos modelos permiten desacoplar la lógica de negocio del resto de componentes.

---

# Motor fisiológico

El módulo `physiology` constituye la base para interpretar el estado del atleta.

Actualmente incluye:

- TrainingLoadSeries
- TrainingLoadSeriesBuilder
- TrainingStatus
- TrainingStatusBuilder
- ATLCalculator

La arquitectura está preparada para incorporar:

- CTLCalculator
- TSBCalculator
- FatigueCalculator
- RecoveryCalculator
- FitnessCalculator

---

# Coach

El Coach interpreta el `AthleteContext` para generar recomendaciones.

Actualmente utiliza:

- Tipo de entrenamiento.
- Carga del entrenamiento (`TrainingLoadResult`).
- Resumen del historial (`HistorySummary`).

En futuras versiones también empleará:

- ATL.
- CTL.
- TSB.
- Fatigue.
- Recovery.
- Fitness.

---

# API

Durante el desarrollo la aplicación queda disponible en:

```
http://127.0.0.1:8000
```

Documentación Swagger:

```
http://127.0.0.1:8000/docs
```

OpenAPI:

```
http://127.0.0.1:8000/openapi.json
```

Actualmente el endpoint principal es:

```
POST /fit/upload
```

Este endpoint procesa un entrenamiento completo y devuelve:

- Perfil del atleta.
- Resumen del entrenamiento.
- Carga de entrenamiento.
- Historial resumido.
- Estado del contexto.
- Recomendaciones del Coach.

---

# Tecnologías

- Python
- FastAPI
- Uvicorn
- Pandas
- fitdecode
- NumPy

---

# Instalación

Clonar el repositorio:

```bash
git clone <repositorio>
```

Entrar en el proyecto:

```bash
cd cyc-ai
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Iniciar la aplicación:

```bash
uvicorn app.main:app --reload
```

---

# Flujo de trabajo

El flujo principal de desarrollo es:

```
Implementación

↓

Pruebas

↓

Actualización de documentación

↓

git add .

↓

git commit

↓

git push
```

La documentación debe mantenerse sincronizada con el código en cada sprint.

---

# Roadmap

Próximas funcionalidades:

## Motor fisiológico

- ATL completo.
- CTL.
- TSB.
- Fatigue Score.
- Recovery Score.
- Fitness Score.

## Coach

- Reglas fisiológicas avanzadas.
- Detección de sobreentrenamiento.
- Ajuste automático de recomendaciones.

## Inteligencia Artificial

- Explicaciones inteligentes.
- Predicción de fatiga.
- Predicción de rendimiento.
- Planificación semanal.
- Planificación mensual.

## API

- GET /athlete
- GET /history
- GET /training-status
- GET /dashboard
- POST /plan/generate

---

# Estado actual

En este momento Cyc-AI dispone de un flujo completo capaz de:

1. Procesar un archivo FIT.
2. Analizar el entrenamiento.
3. Calcular la carga mediante TRIMP.
4. Procesar el historial del atleta.
5. Generar un `HistorySummary`.
6. Construir un `TrainingStatus`.
7. Crear un `AthleteContext`.
8. Generar recomendaciones mediante el Coach.
9. Exponer toda la información mediante FastAPI.

La siguiente fase del proyecto consistirá en completar el motor fisiológico (ATL, CTL y TSB) e incorporar un Coach basado en Inteligencia Artificial capaz de ofrecer recomendaciones personalizadas según el estado fisiológico del atleta.

---

# Documentación

La documentación del proyecto se encuentra en el directorio `docs/`:

- architecture.md
- physiology.md
- roadmap.md
- changelog.md
- api.md
- ai.md
- glossary.md
- development.md

Cada documento describe un aspecto específico de la arquitectura y debe mantenerse actualizado junto con el código.

---

# Licencia

Pendiente de definir.