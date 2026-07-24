from fastapi import APIRouter, UploadFile, File

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

    return await service.process_upload(file)