from dataclasses import dataclass
from datetime import date


@dataclass
class Athlete:

    name: str

    weight: float

    height: float

    ftp: int

    birth_date: date

    max_hr: int

    resting_hr: int