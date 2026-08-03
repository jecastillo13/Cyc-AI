# API de Cyc-AI 1.0

Base local: `http://127.0.0.1:8000`. La especificación interactiva está en `/docs`.

## Endpoints

| Método | Ruta | Uso |
|---|---|---|
| GET | `/health` | Estado del servicio |
| POST | `/fit/upload` | Analiza y archiva un FIT/FIT.GZ válido |
| GET | `/athlete` | Perfil activo |
| GET | `/history` | Resumen, tendencias y periodos |
| GET | `/training-status` | ATL, CTL, TSB y scores derivados |
| GET | `/dashboard` | Datos agregados y serie para gráficas |
| GET | `/dashboard/ui` | Dashboard visual |
| POST | `/plan/generate` | Plan de 1 a 4 semanas |
| GET | `/integrations` | Estado de configuración de proveedores |

Ejemplo de plan:

```http
POST /plan/generate?weeks=4&goal=gran%20fondo
```

`POST /fit/upload` acepta únicamente `.fit` y `.fit.gz` hasta 25 MB. Un archivo
corrupto, vacío o con extensión incorrecta devuelve `400`; una petición con parámetros
inválidos devuelve `422`.

Las respuestas fisiológicas incluyen carga, ATL, CTL, TSB, fatiga, recuperación,
fitness, disponibilidad y riesgo estimado. El Coach devuelve recomendación, explicación
y predicciones heurísticas transparentes.
