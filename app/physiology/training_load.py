from app.models.athlete import Athlete
from app.models.workout import Workout

from app.physiology.calculators.tss import TSSCalculator
from app.physiology.calculators.trimp import TRIMPCalculator
from app.physiology.models.training_load_result import TrainingLoadResult


class TrainingLoad:

    def __init__(self):

        self.tss = TSSCalculator()
        self.trimp = TRIMPCalculator()

    def calculate(
        self,
        athlete: Athlete,
        workout: Workout
    ) -> TrainingLoadResult:

        # Prioridad 1: utilizar TSS si el entrenamiento ya lo incluye
        if workout.tss is not None:
            return self.tss.calculate(
                athlete,
                workout
            )

        # Prioridad 2: calcular TRIMP si existe frecuencia cardíaca
        if workout.avg_hr is not None:
            return self.trimp.calculate(
                athlete,
                workout
            )

        # No es posible calcular la carga
        return TrainingLoadResult(
            method="UNKNOWN",
            value=0.0,
            confidence=0.0,
            notes="No hay suficientes datos para calcular la carga de entrenamiento."
        )