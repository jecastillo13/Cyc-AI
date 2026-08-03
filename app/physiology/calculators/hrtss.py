from app.models.athlete import Athlete
from app.models.workout import Workout
from app.physiology.heart_rate import HeartRate
from app.physiology.models.training_load_result import TrainingLoadResult


class HRTSSCalculator:
    """Calcula hrTSS a partir de duración e intensidad por reserva cardíaca."""

    def calculate(self, athlete: Athlete, workout: Workout) -> TrainingLoadResult:
        if workout.avg_hr is None or workout.duration_seconds <= 0:
            return TrainingLoadResult("HRTSS", 0.0, 0.0, "Faltan duración o frecuencia cardíaca.")
        intensity = HeartRate.reserve(athlete.resting_hr, athlete.max_hr, workout.avg_hr)
        value = (workout.duration_seconds / 3600) * intensity**2 * 100
        return TrainingLoadResult("HRTSS", round(value, 2), 0.85, "hrTSS estimado con reserva cardíaca.")
