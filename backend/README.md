running celery:

using python
```bash
.venv\Scripts\activate
celery -A app.celery_app.celery_app worker --loglevel=info --pool=solo
```

using uv

```bash
uv run celery -A app.celery_app.celery_app worker --loglevel=info --pool=solo

```

```bash
uv run python -c "from app import flask_app; from app.scheduler import send_daily_appointment_reminders, send_monthly_doctor_reports; flask_app.app_context().push(); send_daily_appointment_reminders.delay(); send_monthly_doctor_reports.delay(); print('triggered')"
```