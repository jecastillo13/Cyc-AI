# API de Cyc-AI

## Introducción

La API de Cyc-AI permite analizar entrenamientos de ciclismo a partir de archivos **FIT** y **FIT.GZ**.

Actualmente la API expone un único endpoint para el análisis completo de un entrenamiento, aunque la arquitectura está preparada para incorporar nuevos servicios en futuras versiones.

---

# Base URL

Durante el desarrollo:

```
http://127.0.0.1:8000
```

Documentación interactiva:

```
http://127.0.0.1:8000/docs
```

OpenAPI:

```
http://127.0.0.1:8000/openapi.json
```

---

# Endpoint

## POST /fit/upload

Analiza un entrenamiento contenido en un archivo FIT o FIT.GZ.

---

## Parámetros

| Nombre | Tipo | Obligatorio | Descripción |
|----------|------|-------------|-------------|
| file | FIT / FIT.GZ | Sí | Archivo del entrenamiento |

---

# Flujo interno

El endpoint ejecuta el siguiente proceso:

```
Upload

↓

TrainingService

↓

FitImporter

↓

FitReader

↓

WorkoutAnalyzer

↓

TrainingLoadCalculator

↓

WorkoutHistory

↓

WorkoutHistoryAnalyzer

↓

HistorySummary

↓

DataEngine

↓

TrainingLoadSeriesBuilder

↓

TrainingLoadSeries

↓

ExponentialLoadCalculator

├────────────┐

↓            ↓

ATLCalculator
CTLCalculator

└──────┬─────┘

↓

TrainingStatusBuilder

↓

AthleteContext

↓

Coach

↓

Respuesta JSON
```

---

# Respuesta

Actualmente la API devuelve un objeto JSON con la siguiente estructura:

```json
{
    "archivo": "actividad.fit",

    "perfil": {
        "name": "Default User",
        "weight": 75,
        "height": 175,
        "ftp": 250,
        "birth_date": "1990-01-01",
        "max_hr": 190,
        "resting_hr": 55
    },

    "resumen": {
        "registros": 0,
        "distancia_km": 0,
        "duracion_segundos": 0,
        "potencia_media": null,
        "potencia_max": null,
        "fc_media": 0,
        "fc_max": 0,
        "cadencia_media": 0,
        "velocidad_media": 0
    },

    "coach": {
        "tipo_entrenamiento": "",
        "recomendacion": "",
        "training_load": {
            "method": "TRIMP",
            "value": 47.53,
            "confidence": 1.0,
            "notes": ""
        }
    },

    "history_summary": {
        "total_workouts": 0,
        "workouts_last_7_days": 0,
        "workouts_last_28_days": 0,
        "distance_last_7_days": 0,
        "distance_last_28_days": 0,
        "duration_last_7_days": 0,
        "duration_last_28_days": 0,
        "average_distance": 0,
        "average_duration": 0
    },

    "training_status": {
        "training_load": 47.53,
        "atl": 50.43,
        "ctl": 61.22,
        "tsb": 10.79,
        "fatigue_score": 0.0,
        "recovery_score": 0.0
    },

    "metricas": {
        "total_metricas": 0,
        "columnas": []
    }
}
```

---

# Descripción de la respuesta

## archivo

Nombre del archivo procesado.

---

## perfil

Información del atleta utilizada durante el análisis.

Incluye:

- Nombre.
- Peso.
- Altura.
- FTP.
- Fecha de nacimiento.
- Frecuencia cardíaca máxima.
- Frecuencia cardíaca en reposo.

---

## resumen

Resumen del entrenamiento obtenido tras analizar el archivo FIT.

Actualmente incluye:

- Número de registros.
- Distancia.
- Duración.
- Potencia media.
- Potencia máxima.
- Frecuencia cardíaca media.
- Frecuencia cardíaca máxima.
- Cadencia media.
- Velocidad media.

---

## coach

Resultado generado por el entrenador.

Actualmente contiene:

- Tipo de entrenamiento.
- Recomendación.
- Resultado del cálculo de carga (`TrainingLoadResult`).

Actualmente las recomendaciones utilizan:

- Tipo de entrenamiento.
- Carga del entrenamiento.
- Historial resumido.

En próximas versiones incorporarán el estado fisiológico completo.

---

## history_summary

Resumen estadístico del historial de entrenamientos.

Incluye:

- Número total de entrenamientos.
- Entrenamientos últimos 7 días.
- Entrenamientos últimos 28 días.
- Distancia acumulada.
- Duración acumulada.
- Promedios.

---

## training_status

Representa el estado fisiológico actual del atleta.

Actualmente contiene:

- Training Load.
- ATL (Acute Training Load).
- CTL (Chronic Training Load).
- TSB (Training Stress Balance).
- Fatigue Score.
- Recovery Score.

Este bloque es generado automáticamente por el motor fisiológico y forma parte del `AthleteContext`.

---

## metricas

Información adicional obtenida del histórico del atleta.

Actualmente se utiliza para futuras ampliaciones del sistema.

---

# Códigos de respuesta

## 200 OK

Entrenamiento procesado correctamente.

---

## 400 Bad Request

Archivo no válido.

Ejemplos:

- Formato incorrecto.
- Archivo vacío.
- Archivo corrupto.

---

## 404 Not Found

Perfil del atleta no encontrado.

---

## 422 Unprocessable Entity

Solicitud mal formada.

---

## 500 Internal Server Error

Error interno durante el procesamiento del entrenamiento.

---

# Tecnologías utilizadas

- FastAPI
- Uvicorn
- fitdecode
- Pandas

---

# Próximas ampliaciones de la API

En futuras versiones se añadirán nuevos endpoints:

```
GET /athlete

GET /history

GET /training-status

GET /dashboard

POST /coach/recommendation

POST /plan/generate
```

---

# Estado actual

Actualmente la API permite:

- Analizar archivos FIT y FIT.GZ.
- Calcular la carga mediante TRIMP.
- Procesar el historial del atleta.
- Generar un `HistorySummary`.
- Construir una serie temporal diaria continua.
- Calcular ATL.
- Calcular CTL.
- Calcular TSB.
- Construir un `TrainingStatus`.
- Exponer el estado fisiológico mediante la respuesta JSON.
- Generar recomendaciones mediante el Coach.

La siguiente evolución de la API incorporará recomendaciones adaptativas basadas en el estado fisiológico del atleta.