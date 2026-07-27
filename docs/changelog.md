# Changelog

Todas las modificaciones importantes del proyecto se documentan aquí.

---

# v0.4.0

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

## Mejorado

- API simplificada.
- Separación de responsabilidades.
- Eliminación de lógica duplicada.

---

# Próxima versión

## Objetivos

- Integrar TrainingLoad en todo el sistema.
- Implementar TRIMP.
- Mejorar recomendaciones.

## v0.5.1

### Añadido

- HeartRate
- TRIMPCalculator
- Selección automática de TrainingLoad (TSS/TRIMP)
- Primer algoritmo fisiológico implementado

# Changelog

## Sprint 4 - History Summary

### Added

- Nuevo modelo `HistorySummary`.
- Nuevo analizador `WorkoutHistoryAnalyzer`.
- Integración del historial en `AthleteContext`.
- `WorkoutHistory` ahora devuelve un `DataFrame`.
- `DataEngine` genera automáticamente el resumen del historial.
- `TrainingService` expone `history_summary` en la respuesta de la API.

### Improved

- Eliminada la dependencia del diccionario de historial dentro del núcleo del sistema.
- Preparada la arquitectura para implementar ATL, CTL y TSB.