from app.analytics.workout_history_analyzer import WorkoutHistoryAnalyzer

from app.models.athlete import Athlete
from app.models.workout import Workout
from app.models.athlete_context import AthleteContext

from app.physiology.training_load import TrainingLoad
from app.physiology.training_status_builder import TrainingStatusBuilder


class DataEngine:
    """
    Construye el contexto completo del atleta a partir de los datos
    del entrenamiento, el perfil y el historial.
    """

    def __init__(self):

        self.training_load = TrainingLoad()
        self.history_analyzer = WorkoutHistoryAnalyzer()
        self.training_status_builder = TrainingStatusBuilder()

    def build(self, profile, summary, history, metrics):

        athlete = Athlete(
            name=profile["name"],
            weight=profile["weight"],
            height=profile["height"],
            ftp=profile["ftp"],
            birth_date=profile["birth_date"],
            max_hr=profile["max_hr"],
            resting_hr=profile["resting_hr"]
        )

        workout = Workout(
            distance_km=summary["distancia_km"],
            duration_seconds=summary["duracion_segundos"],
            avg_hr=summary["fc_media"],
            max_hr=summary["fc_max"],
            avg_power=summary["potencia_media"],
            max_power=summary["potencia_max"],
            avg_speed=summary["velocidad_media"],
            avg_cadence=summary["cadencia_media"]
        )

        training_load = self.training_load.calculate(
            athlete,
            workout
        )

        history_summary = self.history_analyzer.analyze(history)

        training_status = self.training_status_builder.build(
            history,
            training_load
        )

        context = AthleteContext(
            athlete=athlete,
            workout=workout,
            training_load=training_load,
            history_summary=history_summary,
            training_status=training_status,
            metrics=metrics
        )

        return context