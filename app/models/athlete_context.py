from dataclasses import dataclass

from app.models.athlete import Athlete
from app.models.workout import Workout
from app.models.history_summary import HistorySummary
from app.models.training_status import TrainingStatus

from app.physiology.models.training_load_result import TrainingLoadResult


@dataclass
class AthleteContext:
    """
    Contexto completo del atleta para el motor de IA.

    Reúne toda la información necesaria para que el Coach,
    el motor fisiológico y futuros modelos de IA puedan
    tomar decisiones sin acceder directamente a archivos
    o fuentes de datos.
    """

    athlete: Athlete

    workout: Workout

    training_load: TrainingLoadResult

    history_summary: HistorySummary

    training_status: TrainingStatus

    metrics: dict