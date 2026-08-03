from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.fit import router
from app.api.athlete import router as athlete_router
from app.api.dashboard_ui import router as dashboard_ui_router


app = FastAPI(
    title="Cyc-AI Engine",
    description="API para analizar entrenamientos de ciclismo en formato FIT.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(athlete_router)
app.include_router(dashboard_ui_router)


@app.get("/", tags=["Sistema"])
def inicio():
    return {
        "mensaje": "Cyc-AI funcionando",
        "version": app.version,
        "documentacion": "/docs",
    }


@app.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok"}
