from fastapi import FastAPI

from app.api.fit import router


app = FastAPI(
    title="Cyc-AI Engine",
    description="API para analizar entrenamientos de ciclismo en formato FIT.",
    version="0.2.0",
)

app.include_router(router)


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
