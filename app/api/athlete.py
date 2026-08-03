from dataclasses import asdict

from fastapi import APIRouter, Query

from app.services.athlete_service import AthleteService
from app.integrations.registry import IntegrationRegistry


router = APIRouter(tags=["Atleta"])


@router.get("/athlete")
def athlete():
    return AthleteService().profile()


@router.get("/history")
def history():
    return AthleteService().history()


@router.get("/training-status")
def training_status():
    return asdict(AthleteService().status())


@router.get("/dashboard")
def dashboard():
    return AthleteService().dashboard()


@router.post("/plan/generate")
def generate_plan(
    weeks: int = Query(1, ge=1, le=4),
    goal: str = Query("base", min_length=2, max_length=50),
):
    return AthleteService().plan(weeks, goal)


@router.get("/integrations")
def integrations():
    return IntegrationRegistry().status()
