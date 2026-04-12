from app.celery_app import celery_app
from app.tasks import send_appointment_reminder_task, send_monthly_report_task
from app import flask_app
from app.models.models import Appointment, User, PatientHistory
from datetime import datetime, date


@celery_app.task
def send_daily_appointment_reminders():
    with flask_app.app_context():
        today = date.today()
        appointments = Appointment.query.filter_by(date=today, status='booked').all()

        for apt in appointments:
            patient = User.query.get(apt.patient_id)
            if patient and patient.email:
                send_appointment_reminder_task.delay(
                    patient.email,
                    patient.name,
                    apt.doc_name,
                    today.strftime('%d %b %Y'),
                    apt.time_slot
                )

        return {"sent": len(appointments)}


@celery_app.task
def send_monthly_doctor_reports():
    with flask_app.app_context():
        doctors = User.query.filter_by(role='doctor').all()
        now = datetime.now()
        month_str = now.strftime('%B %Y')

        sent = 0
        for doctor in doctors:
            histories = PatientHistory.query.filter_by(
                doctor_id=doctor.id
            ).filter(
                PatientHistory.visit_date >= datetime(now.year, now.month, 1)
            ).all()

            records = [{
                'patient_name': User.query.get(h.patient_id).name if h.patient_id else 'Unknown',
                'diagnosis': h.diagnosis,
                'prescription': h.prescription,
                'tests_done': h.test_done,
                'visit_date': h.visit_date.strftime('%d %b %Y')
            } for h in histories]

            send_monthly_report_task.delay(doctor.email, doctor.name, month_str, records)
            sent += 1

        return {"sent": sent}
