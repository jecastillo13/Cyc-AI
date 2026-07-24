from dataclasses import dataclass


@dataclass
class Athlete:

    name: str
    weight: float | None
    height: float | None
    ftp: int | None
    birth_date: str | None