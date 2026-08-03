from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_and_core_read_endpoints():
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/athlete").status_code == 200
    assert client.get("/history").status_code == 200
    status = client.get("/training-status")
    assert status.status_code == 200
    assert "fitness_score" in status.json()


def test_dashboard_contains_chart_data():
    payload = client.get("/dashboard").json()
    assert payload["charts"]["daily_load"]
    assert client.get("/dashboard/ui").status_code == 200


def test_plan_generation_validates_range():
    assert client.post("/plan/generate?weeks=2&goal=base").status_code == 200
    assert client.post("/plan/generate?weeks=5").status_code == 422


def test_upload_rejects_wrong_extension():
    response = client.post("/fit/upload", files={"file": ("bad.txt", b"bad")})
    assert response.status_code == 400


def test_upload_rejects_invalid_gzip():
    response = client.post("/fit/upload", files={"file": ("bad.fit.gz", b"not-gzip")})
    assert response.status_code == 400
    assert "GZIP" in response.json()["detail"]


def test_integrations_do_not_expose_secrets():
    payload = client.get("/integrations").json()
    assert set(payload) == {"strava", "garmin", "trainingpeaks", "intervals_icu"}
    assert all("token" not in item for item in payload.values())
