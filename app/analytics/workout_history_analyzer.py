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

        current_month = today.to_period("M")
        current_year = today.year
        monthly = df[df["WorkoutDay"].dt.to_period("M") == current_month]
        yearly = df[df["WorkoutDay"].dt.year == current_year]
        load_7 = float(history_7.get("TSS", pd.Series(dtype=float)).fillna(0).sum())
        load_28 = float(history_28.get("TSS", pd.Series(dtype=float)).fillna(0).sum())
        previous_week_start = last_7_days - timedelta(days=7)
        previous_week = df[(df["WorkoutDay"] >= previous_week_start) & (df["WorkoutDay"] < last_7_days)]
        previous_load = float(previous_week.get("TSS", pd.Series(dtype=float)).fillna(0).sum())
        trend = 0.0 if previous_load == 0 else ((load_7 - previous_load) / previous_load) * 100
        progression = "increasing" if trend > 10 else "decreasing" if trend < -10 else "stable"

        return HistorySummary(

            total_workouts=len(df),

            workouts_last_7_days=len(history_7),
            workouts_last_28_days=len(history_28),

            distance_last_7_days=float(history_7["DistanceInMeters"].fillna(0).sum() / 1000),

            distance_last_28_days=float(history_28["DistanceInMeters"].fillna(0).sum() / 1000),

            duration_last_7_days=float(history_7["TimeTotalInHours"].fillna(0).sum()),

            duration_last_28_days=float(history_28["TimeTotalInHours"].fillna(0).sum()),

            average_distance=float(df["DistanceInMeters"].fillna(0).mean() / 1000),

            average_duration=float(df["TimeTotalInHours"].fillna(0).mean()),
            monthly_workouts=len(monthly),
            yearly_workouts=len(yearly),
            load_last_7_days=round(load_7, 2),
            load_last_28_days=round(load_28, 2),
            load_trend_percent=round(trend, 2),
            progression=progression,
        )
