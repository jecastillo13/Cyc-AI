from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.training_service import TrainingService

router = APIRouter(
    prefix="/fit",
    tags=["FIT"]
)


@router.get("/test")
def test():
    return {
        "status": "FIT API OK"
    }


@router.post("/upload")
async def upload_fit(file: UploadFile = File(...)):

    service = TrainingService()

    try:
        return await service.process_upload(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
