import pandas as pd

from app.analytics.workout_history_analyzer import WorkoutHistoryAnalyzer


def test_history_includes_trends_and_period_summaries():
    history = pd.DataFrame({
        "WorkoutDay": ["2026-01-01", "2026-01-08", "2026-01-09"],
        "DistanceInMeters": [10000, 20000, 30000],
        "TimeTotalInHours": [1, 2, 3],
        "TSS": [50, 100, 100],
    })
    result = WorkoutHistoryAnalyzer().analyze(history)
    assert result.monthly_workouts == 3
    assert result.yearly_workouts == 3
    assert result.load_last_7_days == 200
    assert result.progression == "increasing"
