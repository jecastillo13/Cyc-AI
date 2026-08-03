from __future__ import annotations


class FatigueCalculator:
    """
    Calcula un índice simplificado de fatiga del atleta.

    El resultado está normalizado en el rango [0, 100].

    La implementación actual utiliza:

    - ATL
    - CTL
    - TSB

    La fórmula podrá evolucionar en futuras versiones sin afectar al
    resto de la arquitectura.
    """

    MIN_SCORE = 0.0
    MAX_SCORE = 100.0

    def calculate(
        self,
        atl: float,
        ctl: float,
        tsb: float,
    ) -> float:
        """
        Calcula el nivel de fatiga.

        Parameters
        ----------
        atl
            Acute Training Load.

        ctl
            Chronic Training Load.

        tsb
            Training Stress Balance.

        Returns
        -------
        float
            Valor entre 0 y 100.
        """

        if ctl <= 0:
            return 0.0

        score = (atl / ctl) * 50.0

        if tsb < 0:
            score += min(abs(tsb), 50.0)

        return max(self.MIN_SCORE, min(score, self.MAX_SCORE))