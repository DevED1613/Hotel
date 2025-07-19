import shutil 
from fastapi import APIRouter, UploadFile

from src.tasks.task import resize_image

router = APIRouter(prefix="/images", tags=["Изображения"])

@router.post("")
async def upload_image(image: UploadFile):
    image_path = f'Hotels/src/static/images/{image.filename}'
    with open(image_path, 'wb+') as f:
        shutil.copyfileobj(image.file, f)

    resize_image.delay(image_path)

    
    return {"status": "OK"}