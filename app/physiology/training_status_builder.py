from app.models.training_status import TrainingStatus

from app.physiology.atl import ATLCalculator
from app.physiology.ctl import CTLCalculator
from app.physiology.fatigue import FatigueCalculator
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

    def build(self, history, training_load):

        series = self.series_builder.build(history)

        atl = self.atl_calculator.calculate(series)

        ctl = self.ctl_calculator.calculate(series)

        tsb = ctl - atl
        fatigue_score = self.fatigue_calculator.calculate(atl, ctl, tsb)
        recovery_score = max(0.0, min(100.0, 100.0 - fatigue_score))

        return TrainingStatus(
            training_load=training_load.value,
            atl=atl,
            ctl=ctl,
            tsb=tsb,
            fatigue_score=round(fatigue_score, 2),
            recovery_score=round(recovery_score, 2),
        )
