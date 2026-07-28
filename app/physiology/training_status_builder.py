from app.models.training_status import TrainingStatus

from app.physiology.atl import ATLCalculator
from app.physiology.training_load_series_builder import (
    TrainingLoadSeriesBuilder,
)


class TrainingStatusBuilder:
    """
    Construye el estado fisiológico del atleta.

    Actualmente calcula:

    - Training Load
    - ATL

    En futuras versiones añadirá:

    - CTL
    - TSB
    - Fatigue
    - Recovery
    """

    def __init__(self):

        self.series_builder = TrainingLoadSeriesBuilder()
        self.atl_calculator = ATLCalculator()

    def build(self, history, training_load):

        series = self.series_builder.build(history)

        atl = self.atl_calculator.calculate(series)

        return TrainingStatus(
            training_load=training_load.value,
            atl=atl,
            ctl=0.0,
            tsb=0.0,
            fatigue_score=0.0,
            recovery_score=0.0,
        )