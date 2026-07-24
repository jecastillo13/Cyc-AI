# Arquitectura de Cyc-AI

## Objetivo

Cyc-AI está diseñado siguiendo una arquitectura modular basada en responsabilidades.

Cada módulo tiene una única función y evita dependencias innecesarias.

---

# Flujo principal

FIT
↓
API
↓
TrainingService
↓
FitImporter
↓
FitReader
↓
WorkoutAnalyzer
↓
DataEngine
↓
Coach
↓
Respuesta JSON

---

# Estructura del proyecto

app/

analytics/
Obtención de métricas y análisis de entrenamientos.

api/
Endpoints de FastAPI.

coach/
Clasificación del entrenamiento y recomendaciones.

engine/
Construcción del AthleteContext.

fit/
Importación y lectura de archivos FIT.

models/
Modelos de dominio.

physiology/
Modelos fisiológicos.

services/
Casos de uso del sistema.

users/
Gestión de perfiles de usuario.

---

# Principios

- Una responsabilidad por clase.
- La API nunca contiene lógica de negocio.
- Los servicios coordinan procesos.
- El Coach interpreta información.
- Physiology calcula métricas.
- Analytics obtiene datos.
- Los modelos representan el dominio.

---

# Flujo de datos

Workout
↓
TrainingLoad
↓
AthleteContext
↓
Coach
↓
Respuesta