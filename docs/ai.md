# Coach adaptativo

El Coach de Cyc-AI 1.0 es un sistema explicable basado en reglas. Consume únicamente
`AthleteContext` y no lee archivos ni calcula métricas fisiológicas.

Utiliza:

- tipo y carga de la última sesión;
- ATL, CTL y TSB;
- fatiga, recuperación, fitness, disponibilidad y riesgo;
- volumen y tendencia del historial.

Produce una recomendación, una explicación con los valores empleados y dos estimaciones
heurísticas: fatiga de la siguiente sesión y rendimiento actual. También alimenta el
planificador semanal/mensual.

Estas estimaciones no son diagnósticos médicos ni predicciones de aprendizaje automático.
Un modelo estadístico real requerirá más historial individual, variables de sueño,
variabilidad cardíaca, percepción subjetiva y validación con datos fuera de muestra.
