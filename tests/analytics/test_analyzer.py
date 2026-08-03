from datetime import datetime, timedelta

import pytest

from app.analytics.analyzer import WorkoutAnalyzer


def test_summary_uses_timestamp_span_for_duration():
    start = datetime(2026, 1, 1, 8, 0)
    records = [
        {"type": "record", "timestamp": start, "distance": 0},
        {"type": "record", "timestamp": start + timedelta(seconds=5), "distance": 100},
        {"type": "record", "timestamp": start + timedelta(seconds=10), "distance": 200},
    ]
    summary = WorkoutAnalyzer(records).summary()
    assert summary["duracion_segundos"] == 10
    assert summary["distancia_km"] == 0.2


def test_summary_rejects_fit_without_activity_records():
    with pytest.raises(ValueError, match="no contiene registros"):
        WorkoutAnalyzer([]).summary()
