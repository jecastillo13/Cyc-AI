# Motor Fisiológico de Cyc-AI

## Objetivo

El módulo **Physiology** es el responsable de calcular el estado fisiológico del atleta.

Su misión es transformar los datos del entrenamiento y el historial en información objetiva que pueda ser utilizada por el Coach y, en el futuro, por el motor de Inteligencia Artificial.

El Coach nunca realiza cálculos fisiológicos.

El motor fisiológico nunca genera recomendaciones.

Ambos módulos permanecen completamente desacoplados.

---

# Filosofía

Cada algoritmo debe ser independiente.

La arquitectura permite sustituir o incorporar nuevos métodos sin modificar el resto del sistema.

Ejemplo:

```
Workout

↓

TrainingLoadCalculator

↓

TrainingLoadResult
```

Hoy puede utilizar TRIMP.

Mañana podrá utilizar:

- TSS
- HRTSS
- Session RPE
- Cualquier otro algoritmo

sin modificar el resto de la aplicación.

---

# Arquitectura del módulo

Actualmente el módulo Physiology está compuesto por:

```
physiology/

│
├── atl.py
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

ATLCalculator

↓

TrainingStatusBuilder

↓

TrainingStatus

↓

AthleteContext

↓

Coach
```

Este flujo permite mantener desacoplados:

- el historial
- los algoritmos
- el Coach

---

# Modelos implementados

Actualmente existen los siguientes modelos.

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

Representa una serie temporal de cargas de entrenamiento.

Cada elemento contiene:

- Fecha.
- Valor de carga.

Su objetivo es alimentar los algoritmos fisiológicos.

---

## TrainingStatus

Representa el estado fisiológico del atleta.

Actualmente contiene:

- Training Load
- ATL
- CTL
- TSB
- Fatigue Score
- Recovery Score

Aunque algunos valores todavía se encuentran en desarrollo, el modelo ya está integrado en toda la arquitectura.

---

# Algoritmos implementados

## TRIMP (Bannister)

Estado:

✔ Implementado.

Se calcula utilizando:

- duración
- frecuencia cardíaca
- frecuencia cardíaca máxima
- frecuencia cardíaca en reposo

Devuelve un objeto:

```
TrainingLoadResult
```

---

## TSS

Estado:

Lectura desde TrainingPeaks.

Actualmente el sistema puede utilizar el TSS existente en el historial cuando está disponible.

El cálculo propio de TSS será implementado en futuras versiones.

---

## ATL (Acute Training Load)

Estado:

✔ Integrado.

Actualmente utiliza la serie temporal de carga generada por:

```
TrainingLoadSeriesBuilder
```

En próximas versiones se implementará el cálculo completo mediante media exponencial de 7 días.

---

# Algoritmos planificados

Las siguientes versiones incorporarán:

## CTL

Chronic Training Load.

Media exponencial de aproximadamente 42 días.

---

## TSB

Training Stress Balance.

Se calculará mediante:

```
TSB = CTL - ATL
```

Representará el equilibrio entre forma física y fatiga.

---

## Fatigue Score

Indicador simplificado de fatiga acumulada.

Se obtendrá combinando:

- ATL
- CTL
- TSB

---

## Recovery Score

Indicador del nivel de recuperación del atleta.

Permitirá al Coach ajustar la intensidad de los entrenamientos recomendados.

---

## Fitness Score

Indicador global del estado de forma.

Será calculado principalmente a partir del CTL.

---

## HRTSS

Heart Rate Training Stress Score.

Permitirá estimar la carga cuando no existan datos de potencia.

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

- tipo de entrenamiento
- carga del entrenamiento

En próximas versiones utilizará además:

- ATL
- CTL
- TSB
- Fatigue Score
- Recovery Score

para generar recomendaciones mucho más personalizadas.

---

# Principios de diseño

El módulo Physiology debe cumplir siempre las siguientes reglas:

- Una responsabilidad por clase.
- Cada algoritmo debe ser independiente.
- Ningún algoritmo accede directamente al historial CSV.
- Todos los algoritmos trabajan sobre modelos de dominio.
- El Coach nunca calcula fisiología.
- El DataEngine es el único encargado de integrar los resultados.

---

# Estado actual

Actualmente el motor fisiológico dispone de:

✔ TRIMP (Bannister)

✔ TrainingLoadResult

✔ TrainingLoadSeries

✔ TrainingLoadSeriesBuilder

✔ ATLCalculator

✔ TrainingStatus

✔ TrainingStatusBuilder

✔ Integración con DataEngine

✔ Integración con AthleteContext

✔ Integración con Coach

---

# Próximas fases

El siguiente sprint implementará:

- CTL
- TSB
- Fatigue Score
- Recovery Score
- Fitness Score
- Cálculo propio de TSS
- HRTSS

Con estos componentes el motor fisiológico estará preparado para alimentar al futuro Coach IA con información objetiva sobre el estado del atleta.