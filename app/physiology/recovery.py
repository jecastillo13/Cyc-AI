class RecoveryCalculator:
    """Estima recuperación en una escala de 0 a 100."""

    def calculate(self, fatigue: float, tsb: float) -> float:
        freshness_bonus = max(-15.0, min(15.0, tsb))
        score = 100.0 - fatigue + freshness_bonus
        return max(0.0, min(100.0, score))
