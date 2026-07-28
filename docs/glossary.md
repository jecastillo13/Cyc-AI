# Glosario de Cyc-AI

Este documento recopila los términos técnicos utilizados dentro del proyecto.

Su objetivo es unificar el vocabulario utilizado en el código, la documentación y el desarrollo.

---

# A

## Athlete

Modelo de dominio que representa al deportista.

Contiene la información necesaria para interpretar correctamente un entrenamiento, como peso, altura, FTP o frecuencia cardíaca.

---

## AthleteContext

Modelo principal del sistema.

Agrupa toda la información necesaria para que el Coach y futuros motores de Inteligencia Artificial puedan tomar decisiones sin acceder directamente a archivos o bases de datos.

Actualmente contiene:

- Athlete
- Workout
- TrainingLoadResult
- HistorySummary
- TrainingStatus
- Metrics

---

# C

## Cadencia

Número de pedaladas realizadas por minuto.

Unidad:

```
rpm
```

---

## Coach

Componente encargado de interpretar el contexto del atleta y generar recomendaciones.

No realiza cálculos fisiológicos.

---

## CTL

**Chronic Training Load**

Representa la carga crónica del atleta.

Se calcula mediante una media móvil exponencial de aproximadamente 42 días.

Un CTL elevado suele indicar una buena condición física.

Estado:

Pendiente de implementación.

---

# D

## DataEngine

Componente responsable de construir el `AthleteContext`.

Es el único punto donde se integran los distintos modelos del sistema.

---

# F

## Fatigue Score

Indicador simplificado del nivel de fatiga del atleta.

Se calculará a partir de:

- ATL
- CTL
- TSB

Estado:

Pendiente.

---

## FIT

Formato estándar utilizado por Garmin y otros dispositivos para almacenar entrenamientos.

---

## FIT.GZ

Archivo FIT comprimido mediante GZIP.

Cyc-AI puede procesarlo automáticamente.

---

## Fitness Score

Indicador global del estado de forma del atleta.

Estará basado principalmente en el CTL.

Estado:

Pendiente.

---

## FTP

**Functional Threshold Power**

Potencia máxima sostenible aproximadamente durante una hora.

Se utiliza como referencia para calcular zonas de entrenamiento.

---

# H

## Heart Rate

Frecuencia cardíaca.

Unidad:

```
ppm
```

---

## Heart Rate Reserve

Reserva de frecuencia cardíaca.

Se calcula mediante:

```
FC máxima - FC reposo
```

---

## HistorySummary

Resumen estadístico del historial de entrenamientos.

Es generado automáticamente por `WorkoutHistoryAnalyzer`.

El Coach utiliza este modelo en lugar de acceder directamente al historial CSV.

---

## HRTSS

**Heart Rate Training Stress Score**

Algoritmo para estimar la carga de entrenamiento utilizando únicamente la frecuencia cardíaca.

Estado:

Pendiente.

---

# I

## IF

**Intensity Factor**

Relación entre la potencia normalizada y el FTP.

Es una de las métricas utilizadas por TrainingPeaks.

---

# M

## Metrics

Información adicional del atleta obtenida desde los archivos CSV.

Actualmente se utiliza para futuras ampliaciones del sistema.

---

# P

## Potencia

Trabajo realizado por el ciclista.

Unidad:

```
vatios (W)
```

---

# R

## Recovery Score

Indicador del nivel de recuperación del atleta.

Permitirá al Coach ajustar las recomendaciones.

Estado:

Pendiente.

---

# T

## Training Load

Carga total producida por un entrenamiento.

Puede calcularse mediante distintos algoritmos.

Ejemplos:

- TRIMP
- TSS
- HRTSS

---

## TrainingLoadCalculator

Componente encargado de calcular la carga del entrenamiento.

Selecciona automáticamente el algoritmo más adecuado.

---

## TrainingLoadResult

Resultado del cálculo de carga.

Actualmente contiene:

- method
- value
- confidence
- notes

Este modelo desacopla el algoritmo utilizado del resto de la arquitectura.

---

## TrainingLoadSeries

Serie temporal de cargas de entrenamiento.

Se construye a partir del historial del atleta.

Su objetivo es alimentar los algoritmos fisiológicos.

---

## TrainingLoadPoint

Elemento individual de una `TrainingLoadSeries`.

Cada punto contiene:

- Fecha.
- Valor de carga.

---

## TrainingStatus

Modelo que representa el estado fisiológico del atleta.

Actualmente contiene:

- Training Load
- ATL
- CTL
- TSB
- Fatigue Score
- Recovery Score

Es el modelo que utilizarán el Coach y el futuro Coach IA.

---

## TRIMP

**Training Impulse**

Algoritmo desarrollado por Eric Bannister para estimar la carga de entrenamiento mediante la frecuencia cardíaca.

Es el algoritmo actualmente utilizado por Cyc-AI.

---

## TSB

**Training Stress Balance**

Representa el equilibrio entre la forma física y la fatiga.

Se calcula mediante:

```
TSB = CTL - ATL
```

Valores positivos suelen indicar buena recuperación.

Valores negativos suelen indicar fatiga acumulada.

Estado:

Pendiente.

---

## TSS

**Training Stress Score**

Métrica desarrollada por TrainingPeaks para cuantificar la carga del entrenamiento.

Actualmente Cyc-AI puede leer el TSS existente en el historial.

En futuras versiones podrá calcularlo de forma nativa.

---

# V

## Velocidad

Distancia recorrida por unidad de tiempo.

Habitualmente se expresa en:

```
km/h
```

---

# W

## Workout

Modelo de dominio que representa un entrenamiento individual.

Contiene la información obtenida tras analizar un archivo FIT.

---

## WorkoutAnalyzer

Componente encargado de transformar los datos leídos del archivo FIT en un modelo `Workout`.

---

## WorkoutHistory

Componente encargado de cargar el historial de entrenamientos desde el archivo CSV.

Actualmente devuelve un `DataFrame` de pandas.

---

## WorkoutHistoryAnalyzer

Procesa el historial y genera un objeto `HistorySummary`.

---

# Estado actual

El glosario se ampliará conforme se incorporen nuevos algoritmos fisiológicos y funcionalidades del Coach IA.

Todos los nuevos modelos de dominio deberán documentarse aquí antes de considerarse finalizado un sprint.