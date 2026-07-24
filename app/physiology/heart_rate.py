class HeartRate:
    """
    Utilidades para cálculos relacionados con la frecuencia cardíaca.
    """

    @staticmethod
    def reserve(
        resting_hr: int,
        max_hr: int,
        average_hr: float
    ) -> float:
        """
        Calcula la Reserva de Frecuencia Cardíaca (HRr).

        HRr = (FC media - FC reposo) / (FC máxima - FC reposo)

        Returns:
            Valor entre 0.0 y 1.0
        """

        if max_hr <= resting_hr:
            raise ValueError(
                "La frecuencia cardíaca máxima debe ser mayor que la frecuencia en reposo."
            )

        reserve = (
            average_hr - resting_hr
        ) / (
            max_hr - resting_hr
        )

        # Limitar el resultado al rango fisiológico válido
        return max(0.0, min(1.0, reserve))