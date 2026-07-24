from fastapi import APIRouter, UploadFile, File
from app.fit.importer import FitImporter
from app.fit.reader import FitReader
from app.analytics.analyzer import WorkoutAnalyzer

import tempfile
import shutil
import os

router = APIRouter(prefix="/fit", tags=["FIT"])


@router.get("/test")
def test():
    return {"status": "FIT API OK"}


@router.post("/upload")
async def upload_fit(file: UploadFile = File(...)):

    # Guardar el archivo subido
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        shutil.copyfileobj(file.file, tmp)
        ruta_original = tmp.name

    ruta_fit = None

    try:

        # Si es .fit.gz lo descomprime; si es .fit lo deja igual
        ruta_fit = FitImporter.preparar(ruta_original)

        lector = FitReader(ruta_fit)
        registros = lector.read()

        analizador = WorkoutAnalyzer(registros)

        return {
            "archivo": file.filename,
            "resumen": analizador.summary()
        }

    finally:

        if os.path.exists(ruta_original):
            os.remove(ruta_original)

        if ruta_fit and ruta_fit != ruta_original and os.path.exists(ruta_fit):
            os.remove(ruta_fit)