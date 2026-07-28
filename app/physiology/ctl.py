from app.physiology.exponential_load_calculator import (
    ExponentialLoadCalculator,
)
from app.physiology.models.training_load_series import (
    TrainingLoadSeries,
)


class CTLCalculator:
    """
    Calcula el Chronic Training Load (CTL).

    El CTL representa el estado de forma del atleta y se calcula
    mediante una media móvil exponencial de la carga de entrenamiento.

    La carga utilizada puede ser:

        - TSS
        - TRIMP
        - HRTSS
        - cualquier otra métrica equivalente.

    El algoritmo únicamente trabaja con una TrainingLoadSeries,
    por lo que es independiente del origen de los datos.
    """

    TIME_CONSTANT = 42

    def __init__(self):

        self.calculator = ExponentialLoadCalculator()

    def calculate(self, series: TrainingLoadSeries) -> float:

        return self.calculator.calculate(
            series=series,
            tau=self.TIME_CONSTANT,
        )