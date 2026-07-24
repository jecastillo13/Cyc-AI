import math

from app.models.athlete import Athlete
from app.models.workout import Workout

from app.physiology.heart_rate import HeartRate
from app.physiology.models.training_load_result import TrainingLoadResult


class TRIMPCalculator:
    """
    Calcula la carga de entrenamiento utilizando
    el modelo TRIMP de Bannister.
    """

    def calculate(
        self,
        athlete: Athlete,
        workout: Workout
    ) -> TrainingLoadResult:

        if workout.avg_hr is None:

            return TrainingLoadResult(
                method="TRIMP",
                value=0,
                confidence=0.0,
                notes="No hay frecuencia cardíaca disponible."
            )

        duration_minutes = workout.duration_seconds / 60

        hrr = HeartRate.reserve(
            resting_hr=athlete.resting_hr,
            max_hr=athlete.max_hr,
            average_hr=workout.avg_hr
        )

        trimp = (
            duration_minutes *
            hrr *
            0.64 *
            math.exp(1.92 * hrr)
        )

        return TrainingLoadResult(
            method="TRIMP",
            value=round(trimp, 2),
            confidence=1.0,
            notes="TRIMP calculado mediante el modelo de Bannister."
        )