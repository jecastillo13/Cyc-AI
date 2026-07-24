from app.models.athlete import Athlete
from app.models.workout import Workout
from app.models.athlete_context import AthleteContext


class DataEngine:

    def build(self, profile, summary, history, metrics):

        athlete = Athlete(
            name=profile["name"],
            weight=profile["weight"],
            height=profile["height"],
            ftp=profile["ftp"],
            birth_date=profile["birth_date"]
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

        context = AthleteContext(
            athlete=athlete,
            workout=workout,
            history=history,
            metrics=metrics
        )

        return context