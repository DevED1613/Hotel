import asyncio
from time import sleep

from PIL import Image
import os

from src.utils.db_manger import DBManager
from src.tasks.celery_app import celery_instance
from src.database import async_session_maker_null_poll

@celery_instance.task
def test_task():
    sleep(5)
    print("Task done")


@celery_instance.task
def resize_image(input_path: str):
    sizes = [1000, 500, 200]
    output_dir = f"Hotels/src/static/images"
    """
    Преобразует изображение в заданные размеры и сохраняет результаты.
    
    """
    try:
        # Открываем изображение
        img = Image.open(input_path)
        # Получаем имя файла без расширения
        filename = os.path.splitext(os.path.basename(input_path))[0]
        # Перебираем все указанные размеры
        for size in sizes:
            # Создаем копию изображения
            resized_img = img.copy()
            # Изменяем размер, сохраняя пропорции
            resized_img.thumbnail((size, size), Image.Resampling.LANCZOS)
            # Создаем новое имя файла
            output_path = os.path.join(output_dir, f"{filename}_{size}x{size}.jpg")
            # Сохраняем изображение
            resized_img.save(output_path, "JPEG", quality=95)
            print(f"Изображение сохранено: {output_path}")
        # Закрываем исходное изображение
        img.close()

    except Exception as e:
        print(f"Ошибка при обработке изображения: {str(e)}")


async def get_booking_for_today_checkin_helper():
    async with DBManager(session=async_session_maker_null_poll) as db:
        bookings = await db.bookings.get_booking_for_today_checkin()
        print(f"{bookings=}")


@celery_instance.task(name="booking_today_checkin")
def send_email_to_users_with_today_checkin():
    asyncio.run(get_booking_for_today_checkin_helper())
