# Motor Fisiológico de Cyc-AI

## Objetivo

El módulo **Physiology** es el responsable de calcular el estado fisiológico del atleta.

Su misión es transformar los datos del entrenamiento y el historial en información objetiva que pueda ser utilizada por el Coach y, en el futuro, por el motor de Inteligencia Artificial.

El Coach nunca realiza cálculos fisiológicos.

El motor fisiológico nunca genera recomendaciones.

Ambos módulos permanecen completamente desacoplados.

---

# Filosofía

Cada algoritmo debe ser independiente y reutilizable.

La arquitectura permite sustituir o incorporar nuevos métodos sin modificar el resto del sistema.

Ejemplo:

```
Workout

↓

TrainingLoadCalculator

↓

TrainingLoadResult
```

Actualmente el sistema puede utilizar:

- TRIMP
- TSS (cuando está disponible en el historial)

En futuras versiones podrá incorporar nuevos métodos como:

- HRTSS
- Session RPE

sin modificar el resto de la aplicación.

---

# Arquitectura del módulo

Actualmente el módulo Physiology está compuesto por componentes especializados.

```
physiology/

│
├── exponential_load_calculator.py
├── atl.py
├── ctl.py
├── training_load.py
├── training_load_series_builder.py
├── training_status_builder.py
│
├── calculators/
│      trimp.py
│      tss.py
│
└── models/
       training_load_result.py
       training_load_series.py
```

Cada clase tiene una única responsabilidad.

---

# Flujo fisiológico

El estado fisiológico se construye mediante el siguiente flujo:

```
WorkoutHistory

↓

DataFrame

↓

TrainingLoadSeriesBuilder

↓

TrainingLoadSeries

↓

ExponentialLoadCalculator

├──────────────┐

↓              ↓

ATLCalculator  CTLCalculator

└──────┬───────┘

↓

TrainingStatusBuilder

↓

TrainingStatus

↓

AthleteContext

↓

Coach
```

El cálculo se realiza sobre una serie temporal diaria continua, lo que permite representar correctamente los periodos de entrenamiento y descanso.

---

# Serie temporal de entrenamiento

El historial del atleta se transforma en una serie diaria continua antes de realizar cualquier cálculo fisiológico.

Durante este proceso:

- Las fechas se normalizan.
- Los entrenamientos del mismo día se agregan.
- Los días sin entrenamiento se incorporan automáticamente con carga 0.
- La serie se ordena cronológicamente.

Esta representación reproduce el comportamiento esperado de los modelos fisiológicos basados en medias exponenciales.

---

# Modelos implementados

## TrainingLoadResult

Representa el resultado del cálculo de carga del entrenamiento.

Contiene:

- Método utilizado.
- Valor calculado.
- Nivel de confianza.
- Observaciones.

Ejemplo:

```
TrainingLoadResult

method = "TRIMP"

value = 47.53

confidence = 1.0

notes = "Modelo de Bannister."
```

---

## TrainingLoadSeries

Representa una serie temporal diaria de cargas de entrenamiento.

Cada elemento contiene:

- Fecha.
- Valor de carga.

Es la entrada utilizada por todos los algoritmos fisiológicos.

---

## TrainingStatus

Representa el estado fisiológico actual del atleta.

Actualmente contiene:

- Training Load
- ATL
- CTL
- TSB
- Fatigue Score
- Recovery Score

Este modelo forma parte del `AthleteContext` y es consumido por el resto de la aplicación.

---

# Algoritmos implementados

## TRIMP (Bannister)

**Estado:** ✔ Implementado.

Calcula la carga del entrenamiento utilizando:

- Duración.
- Frecuencia cardíaca.
- Frecuencia cardíaca máxima.
- Frecuencia cardíaca en reposo.

Devuelve un objeto `TrainingLoadResult`.

---

## ATL (Acute Training Load)

**Estado:** ✔ Implementado.

Calcula la carga aguda mediante una media exponencial con una constante temporal de **7 días**.

Representa la carga reciente soportada por el atleta.

---

## CTL (Chronic Training Load)

**Estado:** ✔ Implementado.

Calcula la carga crónica mediante una media exponencial con una constante temporal de **42 días**.

Representa la adaptación fisiológica acumulada del atleta.

---

## TSB (Training Stress Balance)

**Estado:** ✔ Implementado.

Se obtiene mediante:

```
TSB = CTL - ATL
```

Representa el equilibrio entre la forma física y la fatiga acumulada.

Valores positivos suelen indicar un atleta más recuperado.

Valores negativos suelen indicar una carga reciente elevada.

---

## ExponentialLoadCalculator

**Estado:** ✔ Implementado.

Es el componente reutilizable encargado de calcular medias exponenciales.

Actualmente es utilizado por:

- ATLCalculator
- CTLCalculator

Centralizar este algoritmo evita duplicación de código y garantiza consistencia entre ambos cálculos.

---

## TSS

**Estado:** Lectura desde TrainingPeaks.

Actualmente el sistema puede utilizar el TSS existente en el historial cuando está disponible.

El cálculo propio de TSS se implementará en futuras versiones.

---

# Integración con DataEngine

El DataEngine construye automáticamente el estado fisiológico del atleta.

Actualmente el flujo es:

```
TrainingLoadResult

↓

WorkoutHistory

↓

TrainingLoadSeriesBuilder

↓

TrainingLoadSeries

↓

ATLCalculator

↓

CTLCalculator

↓

TrainingStatusBuilder

↓

TrainingStatus

↓

AthleteContext
```

El resto del sistema únicamente consume el objeto `TrainingStatus`.

---

# Relación con el Coach

El Coach nunca calcula métricas fisiológicas.

Simplemente interpreta la información recibida.

Actualmente utiliza:

- Tipo de entrenamiento.
- Carga del entrenamiento.
- Historial resumido.

El siguiente sprint incorporará reglas basadas en:

- ATL.
- CTL.
- TSB.
- Fatigue Score.
- Recovery Score.

---

# Principios de diseño

El módulo Physiology debe cumplir siempre las siguientes reglas:

- Una responsabilidad por clase.
- Cada algoritmo debe ser independiente.
- Los algoritmos trabajan sobre modelos de dominio.
- Ningún algoritmo accede directamente al historial CSV.
- El Coach nunca calcula fisiología.
- El DataEngine es el único encargado de integrar los resultados.
- Los algoritmos reutilizables deben compartirse siempre que sea posible.

---

# Estado actual

Actualmente el motor fisiológico dispone de:

✔ TRIMP (Bannister)

✔ TrainingLoadResult

✔ TrainingLoadSeries

✔ Serie temporal diaria continua

✔ ExponentialLoadCalculator

✔ ATLCalculator

✔ CTLCalculator

✔ TSB

✔ TrainingStatus

✔ TrainingStatusBuilder

✔ Integración con DataEngine

✔ Integración con AthleteContext

✔ Exposición mediante la API

---

# Próximas fases

El siguiente sprint incorporará:

- Fatigue Score.
- Recovery Score.
- Fitness Score.
- Reglas fisiológicas para el Coach.
- Cálculo propio de TSS.
- HRTSS.

Con estos componentes el motor fisiológico proporcionará una descripción más completa del estado del atleta y permitirá generar recomendaciones cada vez más personalizadas.