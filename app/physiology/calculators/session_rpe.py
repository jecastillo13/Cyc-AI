from app.models.athlete import Athlete
from app.models.workout import Workout
from app.physiology.models.training_load_result import TrainingLoadResult


class SessionRPECalculator:
    def calculate(self, athlete: Athlete, workout: Workout) -> TrainingLoadResult:
        _ = athlete
        if workout.rpe is None or workout.duration_seconds <= 0:
            return TrainingLoadResult("SESSION_RPE", 0.0, 0.0, "Faltan RPE o duración.")
        value = (workout.duration_seconds / 60) * max(0.0, min(10.0, workout.rpe))
        return TrainingLoadResult("SESSION_RPE", round(value, 2), 0.75, "Carga session-RPE.")
