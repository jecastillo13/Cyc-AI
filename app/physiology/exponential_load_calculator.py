import math

from app.physiology.models.training_load_series import TrainingLoadSeries


class ExponentialLoadCalculator:
    """
    Calcula una media móvil exponencial utilizando una
    constante de tiempo fisiológica (tau).

    Esta clase implementa el algoritmo matemático común
    que utilizarán distintas métricas fisiológicas como:

    - ATL
    - CTL
    - futuras métricas basadas en decaimiento exponencial.

    Es completamente independiente del origen de la carga
    (TSS, TRIMP, HRTSS, etc.).
    """

    def calculate(
        self,
        series: TrainingLoadSeries,
        tau: float,
    ) -> float:

        if not series.points:
            return 0.0

        factor = 1 - math.exp(-1.0 / tau)

        value = series.points[0].load

        for point in series.points[1:]:
            value += (point.load - value) * factor

        return float(value)