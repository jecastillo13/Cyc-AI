class FitnessCalculator:
    """Normaliza CTL como indicador práctico de forma (0-100)."""

    def calculate(self, ctl: float) -> float:
        return max(0.0, min(100.0, ctl))
