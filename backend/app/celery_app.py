from celery import Celery
from celery.schedules import crontab
from config import Config

redis_url = Config.REDIS_URL + "?ssl_cert_reqs=CERT_NONE"

celery_app = Celery(
    'hms',
    broker=redis_url,
    backend=redis_url,
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True,
    task_routes={
        '*': {'queue': 'default'},
    },
    task_default_queue='default',
    include=['app.tasks', 'app.scheduler'],
    beat_schedule={
        'send-daily-reminders': {
            'task': 'app.scheduler.send_daily_appointment_reminders',
            'schedule': crontab(hour=5, minute=0),
        },
        'send-monthly-reports': {
            'task': 'app.scheduler.send_monthly_doctor_reports',
            'schedule': crontab(hour=5, minute=0, day_of_month=1),
        },
    },
)
