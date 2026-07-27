from pathlib import Path
import tempfile
import shutil
import os

from app.fit.importer import FitImporter
from app.fit.reader import FitReader

from app.analytics.analyzer import WorkoutAnalyzer
from app.analytics.workout_history import WorkoutHistory
from app.analytics.metrics import MetricsHistory

from app.users.manager import UserManager
from app.coach.coach import Coach
from app.engine.data_engine import DataEngine


class TrainingService:

    async def process_upload(self, file):

        # Guardar temporalmente el archivo
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            shutil.copyfileobj(file.file, tmp)
            ruta_original = tmp.name

        ruta_fit = None

        try:

            # Usuario
            usuario = UserManager("default")
            usuario.create_user()

            # Preparar FIT
            ruta_fit = FitImporter.preparar(ruta_original)

            # Guardar copia
            destino = usuario.get_fits_path() / Path(file.filename).name
            shutil.copy2(ruta_fit, destino)

            # Leer FIT
            lector = FitReader(ruta_fit)
            registros = lector.read()

            # Resumen del entrenamiento
            analizador = WorkoutAnalyzer(registros)
            resumen = analizador.summary()

            # Historial
            historial = WorkoutHistory("data/workouts.csv")
            historial_info = historial.load()

            # Métricas
            metricas = MetricsHistory("data/metrics.csv")
            metricas_info = metricas.load()

            # Perfil
            perfil = usuario.get_profile()

            # Construcción del contexto
            engine = DataEngine()

            contexto = engine.build(
                profile=perfil,
                summary=resumen,
                history=historial_info,
                metrics=metricas_info
            )

            # Coach
            coach = Coach(contexto)
            analisis = coach.analyze()

            return {
                "archivo": file.filename,
                "perfil": perfil,
                "resumen": resumen,
                "coach": analisis,
                "history_summary": {
                    "total_workouts": contexto.history_summary.total_workouts,
                    "workouts_last_7_days": contexto.history_summary.workouts_last_7_days,
                    "workouts_last_28_days": contexto.history_summary.workouts_last_28_days,
                    "distance_last_7_days": contexto.history_summary.distance_last_7_days,
                    "distance_last_28_days": contexto.history_summary.distance_last_28_days,
                    "duration_last_7_days": contexto.history_summary.duration_last_7_days,
                    "duration_last_28_days": contexto.history_summary.duration_last_28_days,
                    "average_distance": contexto.history_summary.average_distance,
                    "average_duration": contexto.history_summary.average_duration
                },
                "metricas": metricas_info
            }

        finally:

            if os.path.exists(ruta_original):
                os.remove(ruta_original)

            if ruta_fit and ruta_fit != ruta_original and os.path.exists(ruta_fit):
                os.remove(ruta_fit)