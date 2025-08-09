from fastapi import APIRouter, HTTPException, UploadFile

from src.services.images import ImageService

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("")
async def upload_image(image: UploadFile):
    try:
        await ImageService().upload_image(image)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Произошла ошибка")
    except Exception:
        raise HTTPException(status_code=500, detail="Произошла ошибка")

    return {"status": "OK"}
