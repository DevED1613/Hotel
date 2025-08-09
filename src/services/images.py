import shutil

from src.services.base import BaseService
from src.tasks.task import resize_image


class ImageService(BaseService):
    def upload_image(self, image) -> None:
        image_path = f"Hotels/src/static/images/{image.filename}"
        try:
            with open(image_path, "wb+") as f:
                shutil.copyfileobj(image.file, f)
        except FileNotFoundError as e:
            raise e

        resize_image.delay(image_path)
