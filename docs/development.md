# Guía de Desarrollo de Cyc-AI

## Introducción

Este documento describe las normas de desarrollo, la estructura del proyecto y el flujo de trabajo recomendado para contribuir a Cyc-AI.

Su objetivo es mantener una arquitectura limpia, modular y fácilmente extensible.

---

# Filosofía del proyecto

Cyc-AI se desarrolla siguiendo los siguientes principios:

- Arquitectura modular.
- Separación estricta de responsabilidades.
- Modelos de dominio independientes.
- Código fácilmente testeable.
- Componentes reutilizables.
- Bajo acoplamiento.
- Alta cohesión.
- Documentación sincronizada con el código.

Cada nueva funcionalidad debe integrarse sin romper el comportamiento existente.

---

# Flujo de desarrollo

Cada nueva característica debe seguir este proceso:

```
Análisis

↓

Diseño

↓

Implementación

↓

Pruebas

↓

Actualización de documentación

↓

Commit

↓

Push
```

No debe realizarse ningún commit sin haber actualizado previamente la documentación afectada.

---

# Organización del proyecto

La estructura general del proyecto es la siguiente:

```
app/
│
├── analytics/
├── api/
├── coach/
├── engine/
├── fit/
├── models/
├── physiology/
├── services/
└── users/

docs/

tests/
```

Cada módulo debe tener una responsabilidad claramente definida.

---

# Arquitectura

El flujo principal de procesamiento es:

```
Archivo FIT

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

HistorySummary

↓

DataEngine

↓

TrainingLoadSeriesBuilder

↓

TrainingLoadSeries

↓

ExponentialLoadCalculator

├────────────┐

↓            ↓

ATLCalculator
CTLCalculator

└──────┬─────┘

↓

TrainingStatusBuilder

↓

AthleteContext

↓

Coach

↓

Respuesta API
```

Cada componente únicamente conoce la información necesaria para cumplir su función.

---

# Modelos de dominio

Los modelos representan entidades del negocio y no contienen lógica de infraestructura.

Actualmente destacan:

- Athlete
- Workout
- AthleteContext
- TrainingLoadResult
- TrainingLoadSeries
- TrainingStatus
- HistorySummary

Las modificaciones sobre estos modelos deben evaluarse cuidadosamente, ya que son utilizados por varios módulos del sistema.

---

# DataEngine

El `DataEngine` es el punto central de construcción del contexto del atleta.

Entre sus responsabilidades se encuentran:

- Construir el modelo `Athlete`.
- Construir el modelo `Workout`.
- Calcular la carga del entrenamiento.
- Obtener el historial.
- Generar el `HistorySummary`.
- Construir el `TrainingStatus`.
- Crear el `AthleteContext`.

El resto del sistema consume el contexto generado sin necesidad de conocer los detalles de implementación.

---

# Motor fisiológico

El módulo `physiology` es responsable de calcular el estado fisiológico del atleta.

Actualmente incluye:

- TrainingLoadSeries
- TrainingLoadSeriesBuilder
- ExponentialLoadCalculator
- ATLCalculator
- CTLCalculator
- TrainingStatus
- TrainingStatusBuilder

El cálculo fisiológico se realiza sobre una serie temporal diaria continua.

Los algoritmos deben trabajar exclusivamente sobre modelos de dominio y nunca acceder directamente a archivos CSV.

---

# Coach

El Coach interpreta el `AthleteContext` y genera recomendaciones.

No debe:

- Leer archivos FIT.
- Leer archivos CSV.
- Acceder directamente a la base de datos.
- Realizar cálculos fisiológicos.

Toda la información necesaria debe llegar encapsulada en el contexto del atleta.

---

# Convenciones de código

## Nombres

- Clases en `PascalCase`.
- Funciones y variables en `snake_case`.
- Constantes en `UPPER_CASE`.

---

## Tipado

Todo el código nuevo debe utilizar anotaciones de tipo (`type hints`) siempre que sea posible.

Ejemplo:

```python
def build_status(
    history: pd.DataFrame,
    training_load: TrainingLoadResult
) -> TrainingStatus:
    ...
```

---

## Responsabilidad única

Cada clase debe tener un único propósito.

Si una clase empieza a asumir varias responsabilidades, deberá dividirse en componentes más pequeños.

---

# Gestión de dependencias

Las dependencias entre módulos deben seguir una dirección clara:

```
API

↓

Services

↓

Engine

↓

Analytics / Physiology

↓

Models

↓

Utilities
```

Los módulos de nivel inferior no deben depender de módulos superiores.

---

# Pruebas

Toda nueva funcionalidad debe incorporar pruebas cuando sea posible.

Se recomienda cubrir especialmente:

- Modelos.
- Builders.
- Calculadoras.
- Servicios.
- Endpoints.

Las pruebas deben ser independientes entre sí y reproducibles.

---

# Documentación

Toda modificación significativa debe actualizar, cuando corresponda:

- README.md
- architecture.md
- physiology.md
- roadmap.md
- changelog.md
- api.md
- ai.md
- glossary.md
- development.md

La documentación forma parte del proyecto y debe evolucionar al mismo ritmo que el código.

---

# Flujo de Git

El flujo recomendado es:

```
git status

git add .

git commit -m "Descripción del cambio"

git push
```

Los mensajes de commit deben ser claros y describir el objetivo principal del cambio.

---

# Buenas prácticas

Se recomienda:

- Mantener funciones pequeñas.
- Evitar duplicación de código.
- Reutilizar componentes existentes.
- Favorecer la composición frente a la herencia.
- Escribir código legible antes que código complejo.
- Mantener la documentación sincronizada con el código.
- Revisar el impacto arquitectónico antes de añadir nuevas dependencias.
- Añadir nuevas métricas fisiológicas reutilizando componentes existentes siempre que sea posible.

---

# Próximos objetivos de desarrollo

Las siguientes fases del proyecto incluyen:

- Implementación de Fatigue Score.
- Implementación de Recovery Score.
- Implementación de Fitness Score.
- Evolución del Coach mediante reglas fisiológicas.
- Incorporación de Inteligencia Artificial.
- Nuevos endpoints para consulta del estado del atleta.
- Dashboard de métricas fisiológicas.

---

# Estado actual

La arquitectura de Cyc-AI dispone actualmente de:

- Motor de análisis de entrenamientos.
- Procesamiento del historial.
- Cálculo de TRIMP.
- Serie temporal diaria continua.
- ExponentialLoadCalculator.
- ATL.
- CTL.
- TSB.
- TrainingStatus.
- AthleteContext.
- DataEngine como integrador del sistema.
- API REST con FastAPI.

El objetivo de los próximos sprints será convertir estas métricas fisiológicas en recomendaciones inteligentes y personalizadas mediante la evolución del Coach.