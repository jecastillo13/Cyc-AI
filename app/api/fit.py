from fastapi import APIRouter, UploadFile, File
from app.fit.importer import FitImporter
from app.fit.reader import FitReader
from app.analytics.analyzer import WorkoutAnalyzer
from app.analytics.workout_history import WorkoutHistory
from app.analytics.metrics import MetricsHistory
from app.users.manager import UserManager
from pathlib import Path

import tempfile
import shutil
import os

router = APIRouter(prefix="/fit", tags=["FIT"])


@router.get("/test")
def test():
    return {"status": "FIT API OK"}


@router.post("/upload")
async def upload_fit(file: UploadFile = File(...)):

    # Guardar temporalmente el archivo subido
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        shutil.copyfileobj(file.file, tmp)
        ruta_original = tmp.name

    ruta_fit = None

    try:

        # Crear el usuario por defecto si no existe
        usuario = UserManager("default")
        usuario.create_user()

        # Si es .fit.gz lo descomprime; si es .fit lo deja igual
        ruta_fit = FitImporter.preparar(ruta_original)

        # Guardar una copia del FIT en la carpeta del usuario
        destino = usuario.get_fits_path() / Path(file.filename).name
        shutil.copy2(ruta_fit, destino)

        # Leer el FIT
        lector = FitReader(ruta_fit)
        registros = lector.read()

        # Analizar entrenamiento
        analizador = WorkoutAnalyzer(registros)

        # Cargar historial
        historial = WorkoutHistory("data/workouts.csv")
        historial_info = historial.load()

        # Cargar métricas
        metricas = MetricsHistory("data/metrics.csv")
        metricas_info = metricas.load()

        # Obtener perfil del usuario
        perfil = usuario.get_profile()

        return {
            "archivo": file.filename,
            "perfil": perfil,
            "resumen": analizador.summary(),
            "historial": historial_info,
            "metricas": metricas_info
        }

    finally:

        if os.path.exists(ruta_original):
            os.remove(ruta_original)

        if ruta_fit and ruta_fit != ruta_original and os.path.exists(ruta_fit):
            os.remove(ruta_fit)