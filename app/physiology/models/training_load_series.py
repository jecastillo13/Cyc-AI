from dataclasses import dataclass
from datetime import datetime


@dataclass
class TrainingLoadPoint:
    """
    Representa la carga de un entrenamiento concreto.
    """

    date: datetime
    load: float


@dataclass
class TrainingLoadSeries:
    """
    Serie temporal de cargas de entrenamiento.

    Cada elemento representa la carga (TSS, TRIMP, HRTSS, etc.)
    correspondiente a un entrenamiento.

    El motor fisiológico utilizará esta serie para calcular:
    - ATL
    - CTL
    - TSB
    """

    points: list[TrainingLoadPoint]