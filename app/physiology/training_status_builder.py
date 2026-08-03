from app.models.training_status import TrainingStatus

from app.physiology.atl import ATLCalculator
from app.physiology.ctl import CTLCalculator
from app.physiology.fatigue import FatigueCalculator
from app.physiology.power import FitnessCalculator
from app.physiology.recovery import RecoveryCalculator
from app.physiology.training_load_series_builder import (
    TrainingLoadSeriesBuilder,
)


class TrainingStatusBuilder:
    """
    Construye el estado fisiológico del atleta.

    Actualmente calcula:

    - Training Load
    - ATL
    - CTL
    - TSB

    En futuras versiones añadirá:

    - Fatigue
    - Recovery
    """

    def __init__(self):

        self.series_builder = TrainingLoadSeriesBuilder()

        self.atl_calculator = ATLCalculator()
        self.ctl_calculator = CTLCalculator()
        self.fatigue_calculator = FatigueCalculator()
        self.recovery_calculator = RecoveryCalculator()
        self.fitness_calculator = FitnessCalculator()

    def build(self, history, training_load):

        series = self.series_builder.build(history)

        atl = self.atl_calculator.calculate(series)

        ctl = self.ctl_calculator.calculate(series)

        tsb = ctl - atl
        fatigue_score = self.fatigue_calculator.calculate(atl, ctl, tsb)
        recovery_score = self.recovery_calculator.calculate(fatigue_score, tsb)
        fitness_score = self.fitness_calculator.calculate(ctl)
        readiness = "high" if recovery_score >= 70 else "moderate" if recovery_score >= 40 else "low"
        injury_risk = "high" if fatigue_score >= 80 or tsb <= -25 else "moderate" if fatigue_score >= 60 or tsb <= -10 else "low"

        return TrainingStatus(
            training_load=training_load.value,
            atl=atl,
            ctl=ctl,
            tsb=tsb,
            fatigue_score=round(fatigue_score, 2),
            recovery_score=round(recovery_score, 2),
            fitness_score=round(fitness_score, 2),
            readiness=readiness,
            injury_risk=injury_risk,
        )
