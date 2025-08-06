from celery import Celery

from src.config import settings

celery_instance = Celery("tasks", broker=settings.REDIS_URL, include=["src.tasks.task"])


celery_instance.conf.beat_schedule = {
    "send_email_to_users_with_today_checkin": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}
