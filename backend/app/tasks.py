import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template
from app.celery_app import celery_app
from app import flask_app
from config import Config


def send_email(to, subject, html_body):
    msg = MIMEMultipart()
    msg["From"] = Config.SMTP_EMAIL
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
        server.starttls()
        server.login(Config.SMTP_EMAIL, Config.SMTP_PASSWORD)
        server.send_message(msg)


def render_email_template(template_name, context):
    with flask_app.app_context():
        return render_template(template_name, **context)


@celery_app.task
def send_appointment_reminder_task(patient_email, patient_name, doctor_name, date, time_slot):
    time_label = "9 AM - 1 PM" if time_slot == "morning" else "3 PM - 7 PM"
    subject = "Appointment Reminder - Today"
    html_body = f"<p>Hi {patient_name},</p><p>You have an appointment today with {doctor_name} at {time_label}.</p>"
    send_email(patient_email, subject, html_body)
    return {"status": "sent", "to": patient_email}


@celery_app.task
def send_monthly_report_task(doctor_email, doctor_name, month, records):
    subject = f"Monthly Patient Report - {month}"
    html_body = render_email_template("monthly_report.html", {
        "doctor_name": doctor_name,
        "month": month,
        "records": records
    })
    send_email(doctor_email, subject, html_body)
    return {"status": "sent", "to": doctor_email}


@celery_app.task
def send_patient_export_email(patient_email, patient_name, user_id):
    subject = "Your Patient Report Export"
    download_link = f"http://localhost:5000/api/patient/export-csv?user_id={user_id}"
    html_body = render_email_template("patient_export.html", {
        "patient_name": patient_name or "Patient",
        "download_link": download_link
    })
    send_email(patient_email, subject, html_body)
    return {"status": "sent", "to": patient_email}
