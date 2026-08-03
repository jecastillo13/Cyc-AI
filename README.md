# Cyc-AI

Cyc-AI es una API para analizar entrenamientos de ciclismo exportados como archivos
`.fit` o `.fit.gz`. Extrae las métricas de la actividad, calcula carga fisiológica y
genera una recomendación basada en el entrenamiento y el estado reciente del atleta.

## Funcionalidades

- Lectura de archivos FIT y FIT.GZ.
- Resumen de distancia, duración, frecuencia cardíaca, potencia, velocidad y cadencia.
- Cálculo de carga mediante TSS cuando está disponible o TRIMP como alternativa.
- Cálculo de ATL, CTL, TSB, fatiga, recuperación y fitness.
- Resumen del historial exportado desde TrainingPeaks.
- Recomendaciones explicadas, predicciones heurísticas y planes de 1 a 4 semanas.
- Dashboard visual y series de carga para gráficas.
- API REST y documentación OpenAPI con FastAPI.

> El Coach actual utiliza reglas deterministas. La integración con un modelo de IA
> generativa todavía forma parte del roadmap.

## Instalación

Requiere Python 3.11 o superior.

```bash
python -m venv .venv
```

En Windows:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

En Linux o macOS:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecución

Desde la raíz del repositorio:

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Estado: http://127.0.0.1:8000/health
- Swagger: http://127.0.0.1:8000/docs
- Dashboard: http://127.0.0.1:8000/dashboard/ui

Frontend completo:

```bash
cd frontend
npm run dev
```

La interfaz usa `NEXT_PUBLIC_API_URL` cuando está definido y, en desarrollo,
se conecta por defecto a `http://127.0.0.1:8000`.

## Uso

```bash
curl -X POST http://127.0.0.1:8000/fit/upload \
  -F "file=@actividad.fit"
```

Solo se aceptan archivos `.fit` y `.fit.gz`. Los archivos inválidos o sin registros
de actividad reciben una respuesta `400` descriptiva.

## Pruebas

```bash
python -m pytest -q
```

## Estructura

```text
app/
  analytics/   Resumen e historial de entrenamientos
  api/         Endpoints FastAPI
  coach/       Clasificación y recomendaciones
  engine/      Construcción del contexto del atleta
  fit/         Importación y lectura de FIT
  models/      Modelos del dominio
  physiology/  Carga y estado fisiológico
  services/    Orquestación de casos de uso
  users/       Perfil y archivos del atleta
docs/          Documentación técnica
tests/         Pruebas automatizadas
```

## Estado

Versión actual: `1.0.0`. El proyecto es una primera versión funcional y no sustituye la
orientación de un entrenador ni de un profesional de salud.
