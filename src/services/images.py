import logging
import os
import shutil

from src.services.base import BaseService
from src.tasks.task import resize_image
from src.config import settings

STATIC_DIR = "/home/eugen/Python_Projects/Hotels/src/static/images"

class ImageService(BaseService):
    def upload_image(self, image) -> None:
        image_path = os.path.join(settings.STATIC_DIR, image.filename)
        if os.path.exists(image_path):
            raise FileExistsError(f"Файл {image.filename} уже существует")
        logging.info(f"Обработка изображения: {image_path}")
        try:
            with open(image_path, "wb+") as f:
                shutil.copyfileobj(image.file, f)
        except FileNotFoundError as e:
            raise e

        resize_image.delay(image_path)
