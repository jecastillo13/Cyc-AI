# API de Cyc-AI

---

## POST /fit/upload

Sube un archivo FIT o FIT.GZ para analizar un entrenamiento.

### Parámetros

| Nombre | Tipo | Obligatorio |
|---------|------|-------------|
| file | FIT/FIT.GZ | Sí |

---

## Respuesta

```json
{
    "archivo": "...",
    "perfil": {},
    "resumen": {},
    "coach": {},
    "historial": {},
    "metricas": {}
}
```

---

## Flujo interno

Upload

↓

TrainingService

↓

FitImporter

↓

WorkoutAnalyzer

↓

DataEngine

↓

Coach

↓

JSON

---

## Errores

400

Archivo inválido.

404

Usuario no encontrado.

500

Error interno.