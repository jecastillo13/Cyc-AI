# Motor Fisiológico

El objetivo del módulo Physiology es calcular la carga fisiológica del entrenamiento.

El Coach nunca realiza estos cálculos.

---

# Modelos

## Training Load

Representa la carga total del entrenamiento.

Actualmente soporta:

- TSS
- TRIMP (próximamente)
- HRTSS (próximamente)

---

# Próximos modelos

## CTL

Carga crónica.

## ATL

Fatiga aguda.

## TSB

Balance de entrenamiento.

## Recovery

Nivel de recuperación.

## Fatigue

Nivel de fatiga.

---

# Filosofía

Cada algoritmo será independiente.

Ejemplo

Workout

↓

TrainingLoad

↓

TSSCalculator

↓

TrainingLoadResult

Esto permitirá cambiar el algoritmo sin modificar el resto del sistema.