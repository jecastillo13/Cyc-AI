from datetime import date

from app.models.athlete import Athlete
from app.models.workout import Workout
from app.physiology.calculators.hrtss import HRTSSCalculator
from app.physiology.calculators.session_rpe import SessionRPECalculator
from app.physiology.calculators.tss import TSSCalculator


ATHLETE = Athlete("Test", 70, 175, 250, date(1990, 1, 1), 190, 50)


def test_calculates_power_tss():
    workout = Workout(40, 3600, None, None, 200, 500, 30, 80)
    result = TSSCalculator().calculate(ATHLETE, workout)
    assert result.method == "TSS"
    assert result.value == 64


def test_calculates_hrtss():
    workout = Workout(40, 3600, 120, 160, None, None, 30, 80)
    assert HRTSSCalculator().calculate(ATHLETE, workout).value == 25


def test_calculates_session_rpe():
    workout = Workout(40, 3600, None, None, None, None, 30, 80, rpe=6)
    assert SessionRPECalculator().calculate(ATHLETE, workout).value == 360
