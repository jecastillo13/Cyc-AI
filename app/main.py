from fastapi import FastAPI
from app.api.fit import router

app = FastAPI(
    title="Cyc-AI Engine",
    version="0.1"
)

app.include_router(router)

@app.get("/")
def inicio():
    return {
        "mensaje": "🚴 Cyc-AI funcionando"
    }