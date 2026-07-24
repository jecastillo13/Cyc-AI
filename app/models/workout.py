from dataclasses import dataclass


@dataclass
class Workout:

    distance_km: float
    duration_seconds: int

    avg_hr: int | None
    max_hr: int | None

    avg_power: float | None
    max_power: float | None

    avg_speed: float | None
    avg_cadence: float | None