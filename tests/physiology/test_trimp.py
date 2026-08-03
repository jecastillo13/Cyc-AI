from datetime import date

from app.models.athlete import Athlete
from app.models.workout import Workout
from app.physiology.calculators.trimp import TRIMPCalculator


def test_trimp_returns_positive_training_load():
    athlete = Athlete("Test", 70, 175, 250, date(1990, 1, 1), 190, 50)
    workout = Workout(40, 3600, 150, 180, None, None, None, None)
    result = TRIMPCalculator().calculate(athlete, workout)
    assert result.method == "TRIMP"
    assert result.value > 0
    assert result.confidence == 1.0
