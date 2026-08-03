# Motor fisiológico

El motor transforma entrenamientos e historial en indicadores objetivos consumidos por
el Coach.

## Carga de sesión

- TSS recibido o estimado mediante potencia media y FTP.
- TRIMP de Bannister mediante duración y reserva cardíaca.
- hrTSS como alternativa cardíaca normalizada.
- Session-RPE mediante minutos por esfuerzo percibido.

La selección automática prioriza TSS por potencia, después TRIMP y finalmente
Session-RPE. Cada resultado informa método, valor, confianza y observaciones.

## Estado acumulado

- ATL: carga exponencial de 7 días.
- CTL: carga exponencial de 42 días.
- TSB: `CTL - ATL`.
- Fatigue Score: relación ATL/CTL ajustada por TSB.
- Recovery Score: inverso de fatiga ajustado por frescura.
- Fitness Score: CTL normalizado a 0-100.
- Readiness: disponibilidad alta, moderada o baja.
- Injury risk: señal conservadora baja, moderada o alta.

La serie es diaria y continua: agrupa sesiones del mismo día e inserta ceros en días de
descanso. Los scores son ayudas de planificación, no evaluaciones clínicas.
