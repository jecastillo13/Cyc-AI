import pytest

from app.physiology.heart_rate import HeartRate


def test_reserve_calculates_and_clamps_value():
    assert HeartRate.reserve(50, 190, 120) == pytest.approx(0.5)
    assert HeartRate.reserve(50, 190, 220) == 1.0


def test_reserve_rejects_invalid_heart_rates():
    with pytest.raises(ValueError):
        HeartRate.reserve(190, 190, 150)
