from app.physiology.models.training_load_series import TrainingLoadSeries


class ATLCalculator:
    """
    Calcula el Acute Training Load (ATL).

    El ATL representa la fatiga reciente del atleta y se calcula
    mediante una media móvil exponencial (EWMA) de la carga de
    entrenamiento.

    La carga utilizada puede ser:
        - TSS
        - TRIMP
        - HRTSS
        - cualquier otra métrica equivalente.

    El algoritmo únicamente trabaja con una TrainingLoadSeries,
    por lo que es independiente del origen de los datos.
    """

    TIME_CONSTANT = 7

    def calculate(self, series: TrainingLoadSeries) -> float:

        if not series.points:
            return 0.0

        alpha = 2 / (self.TIME_CONSTANT + 1)

        atl = series.points[0].load

        for point in series.points[1:]:
            atl = alpha * point.load + (1 - alpha) * atl

        return float(atl)