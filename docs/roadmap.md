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

- [x] Lectura de archivos FIT
- [x] Lectura de archivos FIT.GZ
- [x] FitImporter
- [x] FitReader
- [x] WorkoutAnalyzer

---

# Sprint 3 — Historial

## Analytics

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
- [x] TrainingStatus

---

## Builders

Implementado:

- [x] TrainingLoadSeriesBuilder
- [x] TrainingStatusBuilder

---

## Algoritmos

Implementado:

- [x] ATLCalculator (estructura integrada)

Pendiente:

- [ ] Cálculo exponencial completo de ATL

---

## Integración

Implementado:

- [x] Integración con DataEngine
- [x] Integración con AthleteContext
- [x] Integración con Coach
- [x] Endpoint `/fit/upload` funcionando correctamente

---

# Sprint 6 — Estado fisiológico

Objetivo:

Convertir el historial del atleta en un estado fisiológico completo.

## Implementar

- [ ] ATL (media exponencial 7 días)
- [ ] CTL (media exponencial 42 días)
- [ ] TSB
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

TrainingStatus
```

---

# Sprint 7 — Coach avanzado

## Reglas fisiológicas

Pendiente:

- [ ] Utilizar ATL
- [ ] Utilizar CTL
- [ ] Utilizar TSB
- [ ] Detectar sobreentrenamiento
- [ ] Detectar falta de carga
- [ ] Recomendar recuperación
- [ ] Recomendar entrenamiento de calidad
- [ ] Ajustar intensidad semanal

---

# Sprint 8 — Inteligencia Artificial

## Coach IA

Pendiente:

- [ ] Explicaciones inteligentes
- [ ] Predicción de fatiga
- [ ] Predicción de rendimiento
- [ ] Ajuste automático de carga
- [ ] Planificador semanal
- [ ] Planificador mensual

---

# Sprint 9 — Dashboard

## Visualización

Pendiente:

- [ ] Estado fisiológico
- [ ] Historial
- [ ] Tendencias
- [ ] ATL
- [ ] CTL
- [ ] TSB
- [ ] Recovery
- [ ] Fatigue
- [ ] Fitness
- [ ] Gráficas

---

# Sprint 10 — Integraciones

Pendiente:

- [ ] Garmin Connect
- [ ] Strava
- [ ] TrainingPeaks
- [ ] Intervals.icu

---

# Testing

## Completado

- [x] Pytest
- [x] Pruebas manuales mediante Swagger
- [x] Flujo completo `/fit/upload`

Pendiente:

- [ ] Cobertura de Analytics
- [ ] Cobertura de Physiology
- [ ] Cobertura del Coach
- [ ] Cobertura de API
- [ ] Integración Continua (CI)

---

# Documentación

Completado:

- [x] README
- [x] Arquitectura
- [x] Roadmap
- [x] Changelog
- [x] API
- [x] Motor fisiológico
- [x] IA
- [x] Glosario
- [x] Desarrollo

---

# Estado actual del proyecto

Actualmente Cyc-AI es capaz de:

- Leer archivos FIT y FIT.GZ.
- Analizar entrenamientos automáticamente.
- Calcular TRIMP mediante el modelo de Bannister.
- Leer el historial de TrainingPeaks.
- Construir un HistorySummary.
- Construir un TrainingStatus.
- Integrar el contexto completo mediante DataEngine.
- Generar recomendaciones mediante el Coach.
- Exponer toda la información mediante FastAPI.

---

# Próximo objetivo

El siguiente sprint estará dedicado exclusivamente al motor fisiológico.

Objetivos:

1. Implementar ATL real.
2. Implementar CTL.
3. Implementar TSB.
4. Calcular Fatigue Score.
5. Calcular Recovery Score.
6. Integrar estas métricas en el Coach.

Este será el paso que convertirá a Cyc-AI de un analizador de entrenamientos a un entrenador inteligente capaz de interpretar el estado fisiológico del atleta.