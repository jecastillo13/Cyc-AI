# 🚴 Cyc-AI

> Un entrenador inteligente para ciclistas basado en ciencia de datos, fisiología del ejercicio e inteligencia artificial.

---

## 📖 Descripción

Cyc-AI es una plataforma diseñada para analizar entrenamientos de ciclismo a partir de archivos **FIT**, interpretar la información fisiológica del atleta y generar recomendaciones inteligentes.

El objetivo del proyecto es ir más allá de mostrar métricas, proporcionando un entrenador virtual que ayude a mejorar el rendimiento y prevenir el sobreentrenamiento.

---

## ✨ Características

- 📂 Importación de archivos FIT y FIT.GZ.
- 📊 Análisis automático del entrenamiento.
- 👤 Gestión de perfiles de atleta.
- 📈 Historial de entrenamientos.
- ❤️ Análisis de frecuencia cardíaca.
- ⚡ Análisis de potencia.
- 🧠 Clasificación automática del entrenamiento.
- 💡 Recomendaciones personalizadas.
- 🏗 Arquitectura modular y escalable.

---

## 🏗 Arquitectura

```
FIT
 │
 ▼
API (FastAPI)
 │
 ▼
TrainingService
 │
 ▼
FitImporter
 │
 ▼
FitReader
 │
 ▼
WorkoutAnalyzer
 │
 ▼
DataEngine
 │
 ▼
Coach
 │
 ▼
Respuesta JSON
```

---

## 📁 Estructura del proyecto

```
Cyc-AI
│
├── app/
│   ├── analytics/
│   ├── api/
│   ├── coach/
│   ├── engine/
│   ├── fit/
│   ├── models/
│   ├── physiology/
│   ├── services/
│   └── users/
│
├── data/
├── docs/
├── users/
├── tests/
└── README.md
```

---

## 🧠 Filosofía

Cyc-AI está construido siguiendo principios de ingeniería de software:

- Una responsabilidad por clase.
- Arquitectura por capas.
- Código modular.
- Algoritmos documentados.
- Fácil mantenimiento.
- Fácil extensión.

---

## 🚀 Tecnologías

- Python
- FastAPI
- fitparse
- Pandas
- Pydantic
- Uvicorn

---

## 📚 Documentación

Toda la documentación oficial del proyecto se encuentra en la carpeta **docs/**.

- architecture.md
- roadmap.md
- changelog.md
- api.md
- physiology.md
- ai.md
- glossary.md

---

## 🗺 Roadmap

### ✅ Completado

- Lectura de archivos FIT.
- API REST.
- Data Engine.
- Domain Models.
- Coach.
- Arquitectura modular.

### 🚧 En desarrollo

- Motor fisiológico.
- TRIMP.
- HRTSS.
- Recovery.
- Fatigue.
- Dashboard.

### 🔮 Futuro

- Integración con Garmin Connect.
- Integración con Strava.
- Integración con TrainingPeaks.
- Coach basado en IA.
- Planificador de entrenamientos.
- Predicción de rendimiento.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas.

Si deseas colaborar:

1. Haz un Fork.
2. Crea una rama nueva.
3. Implementa tu mejora.
4. Envía un Pull Request.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT.

---

# 🚴 Cyc-AI

**Entrena con datos. Mejora con ciencia. Evoluciona con inteligencia artificial.**