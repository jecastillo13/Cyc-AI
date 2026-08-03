from app.coach.planner import TrainingPlanner
from app.models.training_status import TrainingStatus


def status(readiness="high", risk="low"):
    return TrainingStatus(50, 40, 50, 10, 30, 80, 50, readiness, risk)


def test_weekly_plan_has_seven_sessions_and_target_load():
    plan = TrainingPlanner().generate(status(), 1, "base")
    assert len(plan["weeks"][0]["sessions"]) == 7
    assert plan["weeks"][0]["target_load"] > 0


def test_monthly_plan_is_capped_at_four_weeks():
    assert len(TrainingPlanner().generate(status(), 12, "evento")["weeks"]) == 4


def test_low_readiness_removes_hard_sessions():
    plan = TrainingPlanner().generate(status("low", "high"), 1, "base")
    sessions = [item["session"] for item in plan["weeks"][0]["sessions"]]
    assert "intervalos" not in sessions
