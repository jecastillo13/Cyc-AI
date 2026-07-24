from app.models.athlete import Athlete
from app.models.workout import Workout

from app.physiology.models.training_load_result import TrainingLoadResult


class TSSCalculator:

    def calculate(
        self,
        athlete: Athlete,
        workout: Workout
    ) -> TrainingLoadResult:

        # El atleta aún no es necesario para TSS,
        # pero mantenemos la misma interfaz que el resto
        # de calculadores.
        _ = athlete

        if workout.tss is None:

            return TrainingLoadResult(
                method="TSS",
                value=0,
                confidence=0.0,
                notes="No hay datos TSS disponibles."
            )

        return TrainingLoadResult(
            method="TSS",
            value=workout.tss,
            confidence=1.0,
            notes="TSS obtenido del entrenamiento."
        )