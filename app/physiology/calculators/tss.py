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

        if workout.tss is not None:
            return TrainingLoadResult(
                method="TSS",
                value=workout.tss,
                confidence=1.0,
                notes="TSS obtenido del entrenamiento."
            )

        if not workout.avg_power or not athlete.ftp or workout.duration_seconds <= 0:

            return TrainingLoadResult(
                method="TSS",
                value=0,
                confidence=0.0,
                notes="Faltan potencia, FTP o duración para calcular TSS."
            )

        return TrainingLoadResult(
            method="TSS",
            value=round((workout.duration_seconds / 3600) * (workout.avg_power / athlete.ftp) ** 2 * 100, 2),
            confidence=0.9,
            notes="TSS estimado a partir de potencia media y FTP."
        )
