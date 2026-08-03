from dataclasses import asdict
from datetime import date, timedelta

from app.models.training_status import TrainingStatus


class TrainingPlanner:
    """Genera planes deterministas que respetan recuperación y carga actual."""

    def generate(self, status: TrainingStatus, weeks: int = 1, goal: str = "base") -> dict:
        weeks = max(1, min(4, weeks))
        plans = []
        start = date.today()
        for week in range(weeks):
            recovery_first = status.readiness == "low" or status.injury_risk == "high"
            sessions = self._week_sessions(recovery_first, goal, week)
            plans.append({
                "week": week + 1,
                "start_date": (start + timedelta(days=week * 7)).isoformat(),
                "sessions": sessions,
                "target_load": round(sum(item["target_load"] for item in sessions), 1),
            })
        return {
            "goal": goal,
            "weeks": plans,
            "based_on": asdict(status),
            "disclaimer": "Plan orientativo; ajusta según sensaciones y consejo profesional.",
        }

    def _week_sessions(self, recovery_first: bool, goal: str, week: int) -> list[dict]:
        factor = 1 + min(week * 0.05, 0.15)
        quality = "intervalos tempo" if goal == "base" else "intervalos específicos"
        template = [
            ("Lunes", "descanso", 0),
            ("Martes", "recuperación" if recovery_first else quality, 20 if recovery_first else 65),
            ("Miércoles", "resistencia suave", 35),
            ("Jueves", "descanso" if recovery_first else "intervalos", 0 if recovery_first else 55),
            ("Viernes", "recuperación", 20),
            ("Sábado", "fondo aeróbico", 75),
            ("Domingo", "resistencia suave", 35),
        ]
        return [
            {"day": day, "session": session, "target_load": round(load * factor, 1)}
            for day, session, load in template
        ]
