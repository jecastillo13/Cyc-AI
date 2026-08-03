from dataclasses import dataclass


@dataclass
class TrainingStatus:
    """
    Representa el estado fisiológico actual del atleta.

    Este modelo agrupa las principales métricas de carga para que el
    AthleteContext y el Coach trabajen con un único objeto de dominio.

    A medida que el motor fisiológico evolucione, se incorporarán nuevos
    indicadores sin necesidad de modificar el resto de la arquitectura.
    """

    training_load: float
    atl: float
    ctl: float
    tsb: float
    fatigue_score: float
    recovery_score: float
    fitness_score: float
    readiness: str
    injury_risk: str
