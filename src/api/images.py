import os
from fastapi import APIRouter, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse

from src.services.images import ImageService
from src.config import settings

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.get("/{filename}")
async def get_image(filename: str, size: int = Query(500)):
    """
    Отдаёт изображение нужного размера (200, 500, 1000).
    """
    allowed_sizes = [200, 500, 1000]
    if size not in allowed_sizes:
        raise HTTPException(status_code=400, detail="Недопустимый размер")

    name, _ = os.path.splitext(filename)
    file_path = os.path.join(settings.STATIC_DIR, f"{name}_{size}x{size}.jpg")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(file_path, media_type="image/jpeg")


@router.post("")
def upload_image(image: UploadFile):
    try:
        ImageService().upload_image(image)
    except FileExistsError:
        raise HTTPException(status_code=409, detail="Изображение уже существует")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Ошибка сохранения файла")
    except Exception:
        raise HTTPException(status_code=500, detail="Неизвестная ошибка")

    return {"status": "OK"}
