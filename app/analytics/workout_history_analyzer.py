from datetime import datetime, timedelta

import pandas as pd

from app.models.history_summary import HistorySummary


class WorkoutHistoryAnalyzer:
    """
    Analiza el historial de entrenamientos y genera un resumen
    para el resto del sistema.
    """

    def analyze(self, history: pd.DataFrame) -> HistorySummary:

        if history.empty:

            return HistorySummary(
                total_workouts=0,
                workouts_last_7_days=0,
                workouts_last_28_days=0,
                distance_last_7_days=0.0,
                distance_last_28_days=0.0,
                duration_last_7_days=0.0,
                duration_last_28_days=0.0,
                average_distance=0.0,
                average_duration=0.0
            )

        df = history.copy()

        # Convertimos la fecha del entrenamiento
        df["WorkoutDay"] = pd.to_datetime(df["WorkoutDay"])

        today = df["WorkoutDay"].max()

        last_7_days = today - timedelta(days=7)
        last_28_days = today - timedelta(days=28)

        history_7 = df[df["WorkoutDay"] >= last_7_days]
        history_28 = df[df["WorkoutDay"] >= last_28_days]

        return HistorySummary(

            total_workouts=len(df),

            workouts_last_7_days=len(history_7),
            workouts_last_28_days=len(history_28),

            distance_last_7_days=history_7["DistanceInMeters"].fillna(0).sum() / 1000,

            distance_last_28_days=history_28["DistanceInMeters"].fillna(0).sum() / 1000,

            duration_last_7_days=history_7["TimeTotalInHours"].fillna(0).sum(),

            duration_last_28_days=history_28["TimeTotalInHours"].fillna(0).sum(),

            average_distance=df["DistanceInMeters"].fillna(0).mean() / 1000,

            average_duration=df["TimeTotalInHours"].fillna(0).mean()
        )