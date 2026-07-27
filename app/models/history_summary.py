from dataclasses import dataclass


@dataclass
class HistorySummary:
    """
    Resumen del historial de entrenamientos del atleta.

    Contiene únicamente información agregada que será utilizada por
    el Coach y por los modelos fisiológicos.
    """

    total_workouts: int

    workouts_last_7_days: int
    workouts_last_28_days: int

    distance_last_7_days: float
    distance_last_28_days: float

    duration_last_7_days: float
    duration_last_28_days: float

    average_distance: float

    average_duration: float