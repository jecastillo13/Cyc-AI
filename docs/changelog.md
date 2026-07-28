# Changelog

Todas las modificaciones importantes del proyecto se documentan en este archivo.

El proyecto sigue el versionado incremental basado en sprints de desarrollo.

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

- El flujo de construcción del contexto del atleta ahora incorpora el estado fisiológico.
- El procesamiento del historial queda desacoplado del Coach.
- La arquitectura queda preparada para CTL, TSB, Fatigue y Recovery.
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
- DataEngine.
- Athlete.
- Workout.
- AthleteContext.
- TrainingService.
- Coach.
- WorkoutClassifier.
- RecommendationEngine.
- Motor fisiológico inicial.

---

## Mejorado

- API simplificada.
- Separación de responsabilidades.
- Eliminación de lógica duplicada.
- Preparación para la evolución del proyecto.

---

# Próxima versión (v0.7.0)

## Objetivos

### Motor fisiológico

- Implementar ATL mediante media exponencial.
- Implementar CTL.
- Implementar TSB.
- Implementar Fatigue Score.
- Implementar Recovery Score.
- Implementar Fitness Score.

---

### Coach

- Incorporar reglas fisiológicas.
- Detectar sobreentrenamiento.
- Detectar falta de recuperación.
- Ajustar recomendaciones utilizando TrainingStatus.

---

### Inteligencia Artificial

- Primer razonamiento basado en contexto fisiológico.
- Explicaciones inteligentes.
- Recomendaciones personalizadas.
- Planificador de entrenamiento.

---

# Estado del proyecto

Actualmente Cyc-AI dispone de:

- Lectura de FIT y FIT.GZ.
- Procesamiento del historial de entrenamientos.
- HistorySummary.
- Cálculo de TRIMP.
- TrainingLoadResult.
- TrainingLoadSeries.
- TrainingStatus.
- Pipeline fisiológico integrado.
- DataEngine completamente desacoplado.
- Coach basado en contexto.
- API REST mediante FastAPI.

El siguiente hito del proyecto será transformar el estado fisiológico del atleta mediante el cálculo real de ATL, CTL y TSB.