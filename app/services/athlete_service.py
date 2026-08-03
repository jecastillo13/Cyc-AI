from dataclasses import asdict
from pathlib import Path

from app.analytics.metrics import MetricsHistory
from app.analytics.workout_history import WorkoutHistory
from app.analytics.workout_history_analyzer import WorkoutHistoryAnalyzer
from app.coach.planner import TrainingPlanner
from app.physiology.models.training_load_result import TrainingLoadResult
from app.physiology.training_status_builder import TrainingStatusBuilder
from app.physiology.training_load_series_builder import TrainingLoadSeriesBuilder
from app.users.manager import UserManager


ROOT = Path(__file__).resolve().parents[2]


class AthleteService:
    def __init__(self):
        self.user = UserManager("default")
        self.user.create_user()

    def profile(self) -> dict:
        return self.user.get_profile()

    def history(self) -> dict:
        dataframe = WorkoutHistory(ROOT / "data" / "workouts.csv").load()
        return asdict(WorkoutHistoryAnalyzer().analyze(dataframe))

    def status(self):
        dataframe = WorkoutHistory(ROOT / "data" / "workouts.csv").load()
        latest_load = float(dataframe["TSS"].fillna(0).iloc[-1]) if not dataframe.empty and "TSS" in dataframe else 0.0
        return TrainingStatusBuilder().build(
            dataframe,
            TrainingLoadResult("TSS", latest_load, 1.0, "Última carga registrada."),
        )

    def dashboard(self) -> dict:
        dataframe = WorkoutHistory(ROOT / "data" / "workouts.csv").load()
        series = TrainingLoadSeriesBuilder().build(dataframe)
        return {
            "athlete": self.profile(),
            "history": self.history(),
            "training_status": asdict(self.status()),
            "metrics": MetricsHistory(ROOT / "data" / "metrics.csv").load(),
            "charts": {
                "daily_load": [
                    {"date": point.date.date().isoformat(), "load": point.load}
                    for point in series.points[-90:]
                ]
            },
        }

    def plan(self, weeks: int, goal: str) -> dict:
        return TrainingPlanner().generate(self.status(), weeks, goal)
