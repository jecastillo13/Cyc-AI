from dataclasses import dataclass

from app.models.athlete import Athlete
from app.models.workout import Workout

from app.physiology.models.training_load_result import TrainingLoadResult


@dataclass
class AthleteContext:

    athlete: Athlete

    workout: Workout

    training_load: TrainingLoadResult

    history: dict

    metrics: dict