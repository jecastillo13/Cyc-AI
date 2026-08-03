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


ROOT = Path(__file__).resolve().parents[2]


class TrainingService:

    ALLOWED_SUFFIXES = (".fit", ".fit.gz")
    MAX_UPLOAD_BYTES = 25 * 1024 * 1024

    async def process_upload(self, file):

        filename = Path(file.filename or "").name
        if not filename or not filename.lower().endswith(self.ALLOWED_SUFFIXES):
            raise ValueError("Solo se permiten archivos .fit o .fit.gz.")

        # Guardar temporalmente el archivo
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            ruta_original = tmp.name

        if Path(ruta_original).stat().st_size > self.MAX_UPLOAD_BYTES:
            Path(ruta_original).unlink(missing_ok=True)
            raise ValueError("El archivo supera el límite de 25 MB.")

        ruta_fit = None

        try:

            # Usuario
            usuario = UserManager("default")
            usuario.create_user()

            # Preparar FIT
            ruta_fit = FitImporter.preparar(ruta_original)

            # Leer FIT
            lector = FitReader(ruta_fit)
            registros = lector.read()

            # Archivar el original solo después de comprobar que es válido.
            destino = usuario.get_fits_path() / filename
            shutil.copy2(ruta_original, destino)

            # Resumen del entrenamiento
            analizador = WorkoutAnalyzer(registros)
            resumen = analizador.summary()

            # Historial
            historial = WorkoutHistory(ROOT / "data" / "workouts.csv")
            historial_info = historial.load()

            # Métricas
            metricas = MetricsHistory(ROOT / "data" / "metrics.csv")
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
                "archivo": filename,
                "perfil": perfil,
                "resumen": resumen,
                "coach": analisis,

                "training_status": {
                    "training_load": contexto.training_status.training_load,
                    "atl": contexto.training_status.atl,
                    "ctl": contexto.training_status.ctl,
                    "tsb": contexto.training_status.tsb,
                    "fatigue_score": contexto.training_status.fatigue_score,
                    "recovery_score": contexto.training_status.recovery_score,
                    "fitness_score": contexto.training_status.fitness_score,
                    "readiness": contexto.training_status.readiness,
                    "injury_risk": contexto.training_status.injury_risk,
                },

                "history_summary": {
                    "total_workouts": contexto.history_summary.total_workouts,
                    "workouts_last_7_days": contexto.history_summary.workouts_last_7_days,
                    "workouts_last_28_days": contexto.history_summary.workouts_last_28_days,
                    "distance_last_7_days": contexto.history_summary.distance_last_7_days,
                    "distance_last_28_days": contexto.history_summary.distance_last_28_days,
                    "duration_last_7_days": contexto.history_summary.duration_last_7_days,
                    "duration_last_28_days": contexto.history_summary.duration_last_28_days,
                    "average_distance": contexto.history_summary.average_distance,
                    "average_duration": contexto.history_summary.average_duration,
                    "monthly_workouts": contexto.history_summary.monthly_workouts,
                    "yearly_workouts": contexto.history_summary.yearly_workouts,
                    "load_last_7_days": contexto.history_summary.load_last_7_days,
                    "load_last_28_days": contexto.history_summary.load_last_28_days,
                    "load_trend_percent": contexto.history_summary.load_trend_percent,
                    "progression": contexto.history_summary.progression,
                },

                "metricas": metricas_info
            }

        finally:

            if os.path.exists(ruta_original):
                os.remove(ruta_original)

            if ruta_fit and ruta_fit != ruta_original and os.path.exists(ruta_fit):
                os.remove(ruta_fit)
