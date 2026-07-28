# Changelog

Todas las modificaciones importantes del proyecto se documentan en este archivo.

Cyc-AI sigue un versionado incremental basado en sprints de desarrollo.

---

# v0.7.0 — Motor fisiológico

## Fecha

Julio 2026

---

## Añadido

### Motor fisiológico

- Nuevo `ExponentialLoadCalculator`.
- Nuevo `CTLCalculator`.
- Cálculo de `TSB (Training Stress Balance)`.
- Serie temporal `TrainingLoadSeries` diaria y continua.
- Inclusión automática de días sin entrenamiento con carga 0.
- Normalización de fechas del historial.
- Agregación automática de múltiples entrenamientos realizados el mismo día.

### Integración

- `TrainingStatusBuilder` calcula ahora:
  - Training Load
  - ATL
  - CTL
  - TSB
- Integración completa del estado fisiológico dentro de `AthleteContext`.
- Exposición de `training_status` mediante la API REST.

---

## Mejorado

- Reutilización del algoritmo exponencial mediante `ExponentialLoadCalculator`.
- ATL implementado utilizando una constante temporal de 7 días.
- CTL implementado utilizando una constante temporal de 42 días.
- El cálculo fisiológico utiliza una serie diaria continua, reproduciendo el comportamiento esperado del modelo de Bannister.
- Mejor separación entre algoritmos fisiológicos y lógica de integración.

---

## Corregido

- Corrección del acceso a `TrainingLoadResult.value`.
- Corrección de la construcción del estado fisiológico.
- Corrección de imports del módulo `physiology`.
- Estabilización del cálculo de ATL, CTL y TSB.

---

# v0.6.0 — Integración del Motor Fisiológico

## Fecha

Julio 2026

---

## Añadido

- Nuevo modelo `TrainingStatus`.
- Nuevo modelo `TrainingLoadSeries`.
- Nuevo modelo `TrainingLoadPoint`.
- Nuevo `TrainingLoadSeriesBuilder`.
- Nuevo `TrainingStatusBuilder`.
- Nuevo `ATLCalculator`.
- Integración del estado fisiológico en `AthleteContext`.
- Integración completa del motor fisiológico dentro de `DataEngine`.

---

## Mejorado

- El flujo de construcción del contexto del atleta incorpora el estado fisiológico.
- El procesamiento del historial queda desacoplado del Coach.
- La arquitectura queda preparada para la evolución del motor fisiológico.
- El endpoint `/fit/upload` vuelve a funcionar correctamente tras la integración.

---

## Corregido

- Corrección de incompatibilidad entre `TrainingLoadResult` y `TrainingStatus`.
- Corrección de imports del módulo `physiology`.
- Corrección del flujo de construcción del contexto del atleta.
- Estabilización del motor fisiológico.

---

# v0.5.1 — Training Load

## Añadido

- Modelo `HeartRate`.
- `TRIMPCalculator`.
- Selección automática del método de carga.
- Primer algoritmo fisiológico implementado.
- Lectura del TSS existente en TrainingPeaks.

---

## Mejorado

- Cálculo automático del TRIMP mediante el modelo de Bannister.
- Integración del resultado de carga dentro del Coach.

---

# v0.5.0 — History Summary

## Añadido

- Nuevo modelo `HistorySummary`.
- Nuevo `WorkoutHistoryAnalyzer`.
- Integración del historial en `AthleteContext`.
- `WorkoutHistory` devuelve ahora un `DataFrame`.
- `DataEngine` genera automáticamente el resumen del historial.
- `TrainingService` expone `history_summary` mediante la API.

---

## Mejorado

- Eliminada la dependencia de diccionarios para representar el historial.
- Preparada la arquitectura para el motor fisiológico.

---

# v0.4.0 — Arquitectura Modular

## Añadido

- Arquitectura por capas.
- `DataEngine`.
- `Athlete`.
- `Workout`.
- `AthleteContext`.
- `TrainingService`.
- `Coach`.
- `WorkoutClassifier`.
- `RecommendationEngine`.
- Primer diseño del motor fisiológico.

---

## Mejorado

- API simplificada.
- Separación de responsabilidades.
- Eliminación de lógica duplicada.
- Preparación para la evolución del proyecto.

---

# Próxima versión (v0.8.0)

## Objetivos

### Coach fisiológico

- Utilizar ATL en las recomendaciones.
- Utilizar CTL en las recomendaciones.
- Utilizar TSB en las recomendaciones.
- Detectar fatiga acumulada.
- Detectar recuperación.
- Ajustar recomendaciones según el estado fisiológico.

---

### Nuevas métricas

- Fatigue Score.
- Recovery Score.
- Fitness Score.

---

### Inteligencia Artificial

- Primer razonamiento basado en el estado fisiológico.
- Explicaciones inteligentes.
- Recomendaciones personalizadas.
- Planificación adaptativa.

---

# Estado actual del proyecto

Actualmente Cyc-AI dispone de:

- Lectura de FIT y FIT.GZ.
- Procesamiento automático del entrenamiento.
- Procesamiento del historial.
- `HistorySummary`.
- Cálculo de TRIMP mediante el modelo de Bannister.
- `TrainingLoadSeries`.
- `ExponentialLoadCalculator`.
- ATL.
- CTL.
- TSB.
- `TrainingStatus`.
- `AthleteContext`.
- `DataEngine`.
- Recomendaciones mediante el Coach.
- API REST con FastAPI.