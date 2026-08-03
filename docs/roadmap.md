# Roadmap de Cyc-AI

## Versión 1.0

El roadmap funcional local está completado:

- [x] Lectura y validación de FIT/FIT.GZ.
- [x] Historial, tendencias, resumen mensual y anual.
- [x] TRIMP, TSS por potencia, hrTSS y Session-RPE.
- [x] ATL, CTL, TSB, Fatigue, Recovery y Fitness Score.
- [x] Disponibilidad y riesgo estimado.
- [x] Coach adaptativo con explicación y predicciones basadas en reglas.
- [x] Planificador semanal y mensual orientado a objetivos.
- [x] API de atleta, historial, estado, dashboard y planes.
- [x] Dashboard visual de carga y estado fisiológico.
- [x] Pruebas unitarias, integración de API y flujo FIT real.
- [x] Integración continua mediante GitHub Actions.
- [x] Registro configurable para Garmin, Strava, TrainingPeaks e Intervals.icu.

## Integraciones externas

Los adaptadores reportan su configuración en `GET /integrations`. La sincronización
real requiere credenciales y aprobación de cada proveedor; no se incluyen secretos en
el repositorio.

Variables esperadas:

- `STRAVA_ACCESS_TOKEN`
- `GARMIN_CONNECT_TOKEN`
- `TRAININGPEAKS_TOKEN`
- `INTERVALS_ICU_API_KEY`

## Evolución posterior a 1.0

- Autenticación multiusuario y base de datos.
- OAuth real para proveedores compatibles.
- Modelos predictivos entrenados con suficiente historial individual.
- Planes recalculados automáticamente después de cada sesión.
- Alertas y notificaciones.
- Aplicación móvil o PWA.

Las predicciones actuales son heurísticas transparentes, no diagnósticos médicos ni
un modelo de aprendizaje automático entrenado.
