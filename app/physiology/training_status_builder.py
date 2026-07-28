from app.models.training_status import TrainingStatus

from app.physiology.atl import ATLCalculator
from app.physiology.ctl import CTLCalculator
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

    def build(self, history, training_load):

        series = self.series_builder.build(history)

        atl = self.atl_calculator.calculate(series)

        ctl = self.ctl_calculator.calculate(series)

        tsb = ctl - atl

        return TrainingStatus(
            training_load=training_load.value,
            atl=atl,
            ctl=ctl,
            tsb=tsb,
            fatigue_score=0.0,
            recovery_score=0.0,
        )