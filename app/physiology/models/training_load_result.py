from dataclasses import dataclass


@dataclass
class TrainingLoadResult:

    method: str

    value: float

    confidence: float

    notes: str