# Roadmap de Cyc-AI

Este documento describe el estado del desarrollo del proyecto y la planificación de las siguientes fases.

---

# Visión del proyecto

Cyc-AI pretende convertirse en un entrenador inteligente capaz de interpretar los entrenamientos de un ciclista utilizando:

- Datos del entrenamiento.
- Historial deportivo.
- Estado fisiológico.
- Inteligencia Artificial.

La arquitectura está diseñada para crecer sin modificar el núcleo del sistema.

---

# Sprint 1 — Base del proyecto

## Arquitectura

Implementado:

- [x] FastAPI
- [x] API modular
- [x] Separación por capas
- [x] Domain Models
- [x] Services
- [x] Coach
- [x] DataEngine
- [x] AthleteContext

---

# Sprint 2 — Lectura de entrenamientos

## FIT

Implementado:

- [x] Lectura de archivos FIT
- [x] Lectura de archivos FIT.GZ
- [x] FitImporter
- [x] FitReader
- [x] WorkoutAnalyzer

---

# Sprint 3 — Historial

## Analytics

Implementado:

- [x] WorkoutHistory
- [x] WorkoutHistoryAnalyzer
- [x] HistorySummary
- [x] Integración con AthleteContext
- [x] Integración con DataEngine
- [x] Exposición mediante la API

Pendiente:

- [ ] Tendencias del historial
- [ ] Análisis de progresión
- [ ] Resumen mensual
- [ ] Resumen anual

---

# Sprint 4 — Carga de entrenamiento

## Training Load

Implementado:

- [x] Heart Rate Reserve
- [x] TrainingLoadCalculator
- [x] TrainingLoadResult
- [x] TRIMP (Bannister)
- [x] Lectura de TSS desde TrainingPeaks
- [x] Selección automática del método de carga
- [x] Integración con Coach

Pendiente:

- [ ] Cálculo propio de TSS
- [ ] HRTSS
- [ ] Session RPE

---

# Sprint 5 — Motor fisiológico

## Modelos

Implementado:

- [x] TrainingLoadSeries
- [x] TrainingLoadPoint
- [x] TrainingStatus

## Builders

Implementado:

- [x] TrainingLoadSeriesBuilder
- [x] TrainingStatusBuilder

## Algoritmos

Implementado:

- [x] ExponentialLoadCalculator
- [x] ATL (media exponencial de 7 días)
- [x] CTL (media exponencial de 42 días)
- [x] TSB (Training Stress Balance)

## Procesamiento del historial

Implementado:

- [x] Serie temporal diaria continua
- [x] Normalización de fechas
- [x] Agregación de múltiples entrenamientos por día
- [x] Inclusión automática de días de descanso

## Integración

Implementado:

- [x] Integración con DataEngine
- [x] Integración con AthleteContext
- [x] Exposición mediante la API
- [x] Endpoint `/fit/upload` funcionando correctamente

---

# Sprint 6 — Estado fisiológico avanzado

## Objetivo

Completar la evaluación fisiológica del atleta utilizando las métricas ya calculadas.

Implementar:

- [ ] Fatigue Score
- [ ] Recovery Score
- [ ] Fitness Score

Resultado esperado:

```
WorkoutHistory

↓

TrainingLoadSeries

↓

ATL

↓

CTL

↓

TSB

↓

Fatigue

↓

Recovery

↓

Fitness

↓

TrainingStatus
```

---

# Sprint 7 — Coach adaptativo

## Reglas fisiológicas

Pendiente:

- [ ] Utilizar ATL para interpretar la carga reciente.
- [ ] Utilizar CTL para interpretar la condición física.
- [ ] Utilizar TSB para evaluar recuperación.
- [ ] Detectar fatiga acumulada.
- [ ] Detectar falta de carga.
- [ ] Recomendar recuperación.
- [ ] Recomendar entrenamiento de calidad.
- [ ] Ajustar la intensidad semanal.
- [ ] Explicar el razonamiento fisiológico.

---

# Sprint 8 — Inteligencia Artificial

## Coach IA

Pendiente:

- [ ] Explicaciones inteligentes.
- [ ] Predicción de fatiga.
- [ ] Predicción de rendimiento.
- [ ] Ajuste automático de carga.
- [ ] Planificador semanal.
- [ ] Planificador mensual.
- [ ] Objetivos personalizados.

---

# Sprint 9 — Dashboard

## Visualización

Pendiente:

- [ ] Estado fisiológico.
- [ ] Historial.
- [ ] Tendencias.
- [ ] ATL.
- [ ] CTL.
- [ ] TSB.
- [ ] Fatigue Score.
- [ ] Recovery Score.
- [ ] Fitness Score.
- [ ] Gráficas.

---

# Sprint 10 — Integraciones

Pendiente:

- [ ] Garmin Connect.
- [ ] Strava.
- [ ] TrainingPeaks.
- [ ] Intervals.icu.

---

# Testing

## Completado

- [x] Pytest.
- [x] Pruebas manuales mediante Swagger.
- [x] Flujo completo `/fit/upload`.

Pendiente:

- [ ] Cobertura de Analytics.
- [ ] Cobertura de Physiology.
- [ ] Cobertura del Coach.
- [ ] Cobertura de la API.
- [ ] Integración Continua (CI).

---

# Documentación

Completado:

- [x] README.
- [x] Arquitectura.
- [x] Roadmap.
- [x] Changelog.
- [x] API.
- [x] Motor fisiológico.
- [x] IA.
- [x] Glosario.
- [x] Desarrollo.

---

# Estado actual del proyecto

Actualmente Cyc-AI es capaz de:

- Leer archivos FIT y FIT.GZ.
- Analizar entrenamientos automáticamente.
- Calcular TRIMP mediante el modelo de Bannister.
- Leer TSS desde el historial cuando está disponible.
- Procesar el historial de entrenamientos.
- Construir un `HistorySummary`.
- Generar una serie temporal diaria continua.
- Calcular ATL.
- Calcular CTL.
- Calcular TSB.
- Construir un `TrainingStatus`.
- Integrar el contexto completo mediante `DataEngine`.
- Exponer el estado fisiológico mediante la API.
- Generar recomendaciones mediante el Coach.

---

# Próximo objetivo

El siguiente sprint estará dedicado a transformar las métricas fisiológicas en decisiones útiles para el atleta.

Objetivos principales:

1. Implementar Fatigue Score.
2. Implementar Recovery Score.
3. Implementar Fitness Score.
4. Evolucionar el Coach para utilizar ATL, CTL y TSB.
5. Generar recomendaciones adaptativas basadas en el estado fisiológico.

Con este sprint, Cyc-AI dará el paso de calcular el estado fisiológico del atleta a interpretarlo de forma inteligente.