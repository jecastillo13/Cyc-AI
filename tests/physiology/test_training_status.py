import pandas as pd

from app.physiology.models.training_load_result import TrainingLoadResult
from app.physiology.training_status_builder import TrainingStatusBuilder


def test_training_status_calculates_fatigue_and_recovery():
    history = pd.DataFrame({"WorkoutDay": ["2026-01-01"], "TSS": [100]})
    load = TrainingLoadResult("TSS", 100, 1.0, "test")
    status = TrainingStatusBuilder().build(history, load)
    assert status.atl == 100
    assert status.ctl == 100
    assert status.fatigue_score == 50
    assert status.recovery_score == 50
