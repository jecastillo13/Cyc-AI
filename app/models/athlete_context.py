from dataclasses import dataclass

from app.models.athlete import Athlete
from app.models.workout import Workout


@dataclass
class AthleteContext:

    athlete: Athlete

    workout: Workout

    history: dict

    metrics: dict